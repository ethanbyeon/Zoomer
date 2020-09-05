import pyautogui as pug
import pandas as pd
import time

from datetime import datetime

def check_pos(position):
    if position:
        pug.moveTo(position)
        pug.click()
    else:
        return False

def new_meeting():

    meeting_pos = pug.locateCenterOnScreen('images/new_meeting_btn.png')
    check_pos(meeting_pos)

def attendance():

    participants_pos = pug.locateCenterOnScreen('images/participants_btn.png')
    check_pos(participants_pos)

def breakout():

    breakout_pos = pug.locateCenterOnScreen('images/breakout_room_btn.png')
    if check_pos(breakout_pos) == False:
        more_pos = pug.locateCenterOnScreen('images/more_btn.png')
        check_pos(more_pos)
        more_br_option = pug.locateCenterOnScreen('images/more_br_opt.png')
        check_pos(more_br_option)
        