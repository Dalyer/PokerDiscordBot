from selenium import webdriver
from selenium.webdriver.common.keys import Keys

game_link = "https://www.pokernow.club/games/3tcFstG17zZqVTqIPdt9w1J36"


def get_log_lines(link):
    driver = webdriver.Firefox()
    driver.get(link)

    log_button = driver.find_element_by_css_selector('div:nth-child(1) div.main-container.two-color div.controls div.chat-and-log-ctn > button.button-1.show-log-button.small-button.dark-gray')
    popup_close = driver.find_element_by_class_name('modal-button-close')
    popup_close.click()
    log_button.click()

    game_log = driver.find_elements_by_css_selector("div:nth-child(1) div:nth-child(1) div.main-container.two-color div.log-ctn > div.log-viewer")

    log = game_log[0].text.split('\n')

    log.reverse()       # reverse order so it is sequential
    game_data = {}
    seq_num = -1
    for line in log:
        seq_num += seq_num
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

    return game_data


print(get_log_lines(game_link))




