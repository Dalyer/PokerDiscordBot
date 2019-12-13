from selenium import webdriver
from selenium.webdriver.common.keys import Keys

GAME_LINK = "https://www.pokernow.club/games/3tcFstG17zZqVTqIPdt9w1J36"
USABLE_SYMBOLS = ['~', '1', '2']    # fix
driver = webdriver.Firefox()
driver.get(GAME_LINK)

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
    # check for stack increases
    if 'wins' in action:
        newdict = dict(time=action[0], player=action[1], stack_change=value, action_type=action_type, seq_num=seq_num)
    elif 'gained' in action:
        pass
    # check for big and little blinds
    elif 'posts' in action:
        print("big/little blinds found")
    # check for calls
    elif 'calls' in action:
        print("call found")
    # check for raises
    elif 'raises' in action:
        print("raise found")
    else:
        continue


