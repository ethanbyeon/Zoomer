import pyautogui as pug
import pandas as pd
import time

from datetime import datetime

def start():
    app_pos = pug.locateCenterOnScreen('images/zoomApp.png')
    print(app_pos)
    pug.moveTo(app_pos)

def attendance():
    participants_loc = pug.locateCenterOnScreen('images/participants_btn.png')
    pug.moveTo(participants_loc)
    pug.click()

attendance()