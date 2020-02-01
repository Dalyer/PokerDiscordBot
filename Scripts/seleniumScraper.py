from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import selenium

full_game_test_link = "https://www.pokernow.club/games/oDuvG8l90-TT1vi8cZOAIK7lh"  #  # "https://www.pokernow.club/games/oct_JAkdI3LIyZu-uBsuShMbm"

# setup firefox webdriver, call on bot start
def start_webdriver():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    return driver

def start_poker_game(driver):
    driver.get("https://www.pokernow.club")
    useless_name = driver.find_element_by_css_selector('#player-name')
    useless_name.clear()
    useless_name.send_keys("BotBoy")
    driver.find_element_by_css_selector(
        'div:nth-child(1) div:nth-child(4) div.intro-main-form-container '
        'form.main-form-1 > input.button-1:nth-child(4)').click()
    time.sleep(0.25)
    driver.find_element_by_class_name('modal-button-close').click()
    link = driver.find_element_by_css_selector('div:nth-child(1) div.main-container.two-color '
                                               'div.table div.table-warning-ctn.waiting-players-ctn '
                                               '> input:nth-child(2)').get_attribute('value')
    driver.find_element_by_css_selector('div:nth-child(1) div:nth-child(1) '
                                        'div.main-container.two-color div.top-buttons > '
                                        'button.top-buttons-button.quit:nth-child(2)').click()
    driver.find_element_by_css_selector('div.alert-1-container div.alert-1 '
                                        'div.alert-1-buttons span:nth-child(1) > '
                                        'button.button-1.gray:nth-child(1)').click()
    return link


def accept_seat_requests(driver):
    # driver.find_element_by_class_name('modal-button-close').click()
    driver.find_element_by_css_selector('div:nth-child(1) div:nth-child(1) div.main-container.two-color '
                                        'div.top-buttons > button.top-buttons-button.options').click()

    for i in range(1, 10):
        try:
            driver.find_element_by_css_selector(f'div:nth-child(1) div.main-container div.config-content '
                                                f'div.config-player-row.request-game-ingress:nth-child({i}) > '
                                                f'button.button-1.config-action-button').click()
            driver.find_element_by_css_selector('div.main-container div.config-content '
                                                'div.config-player-column.config-col-1:nth-child(2) '
                                                'form.form-1 > button.button-1').click()
            driver.find_element_by_css_selector('div:nth-child(1) div.alert-1-container div.alert-1 '
                                                'div.alert-1-buttons > span:nth-child(1)').click()
        except selenium.common.exceptions.NoSuchElementException:
            pass
    driver.find_element_by_css_selector('div:nth-child(1) div:nth-child(1) div.main-container '
                                        'div.config-top-tabs > button.config-top-tab-buttton.back:nth-child(1)').click()

    # check for $startgame in the chat log
    last_start_message = None
    for i in range(1, 5):
        try:
            message = driver.find_element_by_css_selector(f'div.main-container.two-color div.controls'
                                                          f' div.chat-and-log-ctn div.chat '
                                                          f'div.chat-container div.messages > p:nth-child({i})')
            message = message.text.split()
            if message[3] == '$startgame' and message[1] != last_start_message:
                driver.find_element_by_css_selector('div:nth-child(1) div.main-container.two-color div.controls '
                                                    'div.action-buttons.right-controls > button.button-1.green').click()
                last_start_message = message[1]
        except selenium.common.exceptions.NoSuchElementException:
            pass


#div.main-container.two-color div.controls div.chat-and-log-ctn div.chat div.chat-container div.messages p:nth-child(2) > span.highlight
def get_log_lines(link, driver):
    driver.get(link)
    time.sleep(0.25)
    log_button = driver.find_element_by_css_selector('div:nth-child(1) div.main-container.two-color div.controls '
                                                     'div.chat-and-log-ctn > '
                                                     'button.button-1.show-log-button.small-button.dark-gray')
    popup_close = driver.find_element_by_class_name('modal-button-close')
    time.sleep(0.25)
    popup_close.click()
    log_button.click()

    game_log = driver.find_elements_by_css_selector("div:nth-child(1) div:nth-child(1) "
                                                    "div.main-container.two-color div.log-ctn > div.log-viewer")

    log = game_log[0].text.split('\n')

    log.reverse()       # reverse order so it is sequential
    game_data = []
    seq_num = -1
    betting_cycle = 0
    for line in log:
        seq_num += 1
        action = line.split()
        # find integer values
        value = 0
        action_type = ""
        for i in action:
            if i.isdigit():
                value = i
                break
        # get action type
        for i in action:
            if i == 'calls':
                action_type = 'calls'
            elif i == 'raises':
                action_type = 'raises'
            elif i == 'posts':
                action_type = 'blind'
            elif i == 'wins' or i == 'gained':
                action_type = "win"
            elif i in ['turn:', 'flop:', 'river:', 'starting']:
                betting_cycle += 1

        if action_type != "":
            newdict = dict(time=action[0], player=action[1][0], stack_change=int(value), action_type=action_type, seq_num=seq_num, betting_cycle=betting_cycle)
        else:
            continue
        game_data.append(newdict)

    return game_data


def parse_game_log_test(link):
    log_lines = get_log_lines(link)
    print(log_lines)
    # trackable_players = get_players() here, add tests
    player1 = dict(id='david', identifier='~', score=0, last_action=dict(action_type=None, betting_cycle=1), games_won=0)
    player2 = dict(id='TEST', identifier='#', score=0, last_action=dict(action_type=None, betting_cycle=1), games_won=0)
    player3 = dict(id='DALYER', identifier='^', score=0, last_action=dict(action_type=None, betting_cycle=1), games_won=0)
    players_test = [player1, player2, player3]

    for i in log_lines:
        for player in players_test:
            if i['player'] == player['identifier']:
                score_change = 0
                # determine valid player stack changes
                if i['action_type'] == "win":      # positive stack changes
                    score_change = i['stack_change']
                    player['games_won'] += 1

                elif i['action_type'] == 'calls':  # negative stack changes
                    if player['last_action']['action_type'] == 'blind':
                        if i['betting_cycle'] != player['last_action']['betting_cycle']:
                            score_change = i['stack_change'] * -1
                        else:
                            score_change = (i['stack_change'] - int(player['last_action']['stack_change'])) * -1
                    elif player['last_action']['action_type'] == 'calls':    # case 3
                        # check if new betting round has began or its looped
                        if i['betting_cycle'] == player['last_action']['betting_cycle']:
                            score_change = (i['stack_change'] - int(player['last_action']['stack_change'])) * -1
                        else:
                            score_change = i['stack_change'] * -1
                    elif player['last_action']['action_type'] == 'raises':
                        if i['betting_cycle'] == player['last_action']['betting_cycle']:
                            score_change = (i['stack_change'] - int(player['last_action']['stack_change'])) * -1
                        else:
                            score_change = i['stack_change'] * -1
                    else:
                        score_change = i['stack_change'] * -1

                elif i['action_type'] == 'raises':
                    if player['last_action']['action_type'] == 'blind':
                        if i['betting_cycle'] != player['last_action']['betting_cycle']:
                            score_change = i['stack_change'] * -1
                        else:
                            score_change = (i['stack_change'] - int(player['last_action']['stack_change'])) * -1
                    elif player['last_action']['action_type'] == 'calls':    # case 3
                        # check if new betting round has began or its looped
                        if i['betting_cycle'] == player['last_action']['betting_cycle']:
                            score_change = (i['stack_change'] - int(player['last_action']['stack_change'])) * -1
                        else:
                            score_change = i['stack_change'] * -1
                    elif player['last_action']['action_type'] == 'raises':
                        if i['betting_cycle'] == player['last_action']['betting_cycle']:
                            score_change = (i['stack_change'] - int(player['last_action']['stack_change'])) * -1
                        else:
                            score_change = i['stack_change'] * -1
                    else:
                        score_change = i['stack_change'] * -1
                elif i['action_type'] == 'blind':       # case 1
                    score_change = i['stack_change'] * -1
                player['score'] = player['score'] + score_change
                print(player['score'], player['id'], i['action_type'], (player['last_action']['action_type']), i['betting_cycle'], player['last_action']['betting_cycle'])
                player['last_action'] = i

    print(players_test[0]['score'], players_test[1]['score'], players_test[2]['score'])






