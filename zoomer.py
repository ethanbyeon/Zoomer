import pyautogui as pug

from datetime import datetime

class Zoomer():

    def __init__(self):
        self.name = 'Zoomer'

    def check_pos(self, position):
        if position:
            pug.moveTo(position)
            pug.click()
        else:
            return False

    def new_meeting(self):

        meeting_pos = pug.locateCenterOnScreen('images/menu/new_meeting_btn.png')
        self.check_pos(meeting_pos)

    def attendance(self):

        participants_pos = pug.locateCenterOnScreen('images/meeting/participants_btn.png')
        self.check_pos(participants_pos)

    def breakout(self):

        breakout_pos = pug.locateCenterOnScreen('images/breakout/breakout_room_btn.png')
        if self.check_pos(breakout_pos) == False:
            more_pos = pug.locateCenterOnScreen('images/breakout/more_btn.png')
            self.check_pos(more_pos)
            more_br_option = pug.locateCenterOnScreen('images/breakout/more_br_opt.png')
            self.check_pos(more_br_option)
        