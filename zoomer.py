import pyautogui as pug

from datetime import datetime

class Zoomer():

    def __init__(self):
        self.name = 'Zoomer'

    def check_pos(self, position):
        if position:
            pug.moveTo(position)
        else:
            return False

    def new_meeting(self):

        meeting_pos = pug.locateCenterOnScreen('images/menu/new_meeting_btn.png')
        if self.check_pos(meeting_pos): pug.click()

    def attendance(self):

        participants_pos = pug.locateCenterOnScreen('images/meeting/participants_btn.png')
        waiting_room_label_pos = pug.locateCenterOnScreen('images/attendance/waiting_room_label.png')
        admit_remove_btn_pos = pug.locateCenterOnScreen('images/attendance/admit_remove_btn.png')

        if self.check_pos(participants_pos): pug.click()
        if waiting_room_label_pos:
            pug.moveTo(waiting_room_label_pos)
            pug.move(0, 33)
        
        if admit_remove_btn_pos:
            pug.moveTo(admit_remove_btn_pos)
            pug.click()

    def breakout(self):

        breakout_pos = pug.locateCenterOnScreen('images/breakout/breakout_room_btn.png')
        if self.check_pos(breakout_pos) == False:
            more_pos = pug.locateCenterOnScreen('images/breakout/more_btn.png')
            if self.check_pos(more_pos): pug.click()
            more_br_option = pug.locateCenterOnScreen('images/breakout/more_br_opt.png')
            if self.check_pos(more_br_option): pug.click()
        