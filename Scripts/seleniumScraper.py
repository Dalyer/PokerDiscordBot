from selenium import webdriver
from selenium.webdriver.common.keys import Keys

full_game_test_link = "https://www.pokernow.club/games/oct_JAkdI3LIyZu-uBsuShMbm"


def start_poker_game():
    driver = webdriver.Firefox()
    driver.get("https://www.pokernow.club")
    useless_name = driver.find_element_by_css_selector('#player-name')
    useless_name.clear()
    useless_name.send_keys("BotBoy")
    driver.find_element_by_css_selector(
        'div:nth-child(1) div:nth-child(4) div.intro-main-form-container '
        'form.main-form-1 > input.button-1:nth-child(4)').click()
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


def get_log_lines(link):
    driver = webdriver.Firefox()
    driver.get(link)

    log_button = driver.find_element_by_css_selector('div:nth-child(1) div.main-container.two-color div.controls '
                                                     'div.chat-and-log-ctn > '
                                                     'button.button-1.show-log-button.small-button.dark-gray')
    popup_close = driver.find_element_by_class_name('modal-button-close')
    popup_close.click()
    log_button.click()

    game_log = driver.find_elements_by_css_selector("div:nth-child(1) div:nth-child(1) "
                                                    "div.main-container.two-color div.log-ctn > div.log-viewer")

    log = game_log[0].text.split('\n')

    log.reverse()       # reverse order so it is sequential
    game_data = {}
    seq_num = -1
    for line in log:
        seq_num += 1
        action = line.split()
        # find integer values
        value = 0
        action_type = ""
        for i in action:
            if i.isdigit():
                value = i
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
        if action_type != "":
            newdict = dict(time=action[0], player=action[1], stack_change=value, action_type=action_type, seq_num=seq_num)
        else:
            continue

        temp = "Line" + str(seq_num)
        game_data[temp] = newdict

    driver.close()
    return game_data


def parse_game_log_test(link):
    log_lines = get_log_lines(link)
    print(log_lines)


parse_game_log_test(full_game_test_link)




