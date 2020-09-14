import pyautogui as pug
import os

from datetime import datetime

images = {

    # USER SCREEN
    'desktop_window' : 'desktop_window.png',

    # BREAKOUT ROOM
    'br_btn' : 'breakout_room_btn.png',
    'more_br_opt' : 'more_br_opt.png',
    'more_btn' : 'more_btn.png',

    # MEETING
    'admit_remove_btn' : 'admit_remove_btn.png',
    'in_the_meeting_label' : 'in_the_meeting_label',
    'participants_btn' : 'participants_btn.png',
    'participants_label' : 'participants_label.png',
    'waiting_room_label' : 'waiting_room_label.png',

    # MENU
    'join_btn' : 'join_btn.png',
    'new_meeting_btn' : 'new_meeting_btn.png',
    'schedule_btn' : 'schedule_btn.png',
}

class Zoomer():

    def __init__(self):
        self.name = 'Zoomer'

    def find_img_coordinates(self, img_name, img_folder, scale=''):
        needle = os.path.abspath('images/' + 'img_folder/' + img_name)
        haystack = os.path.abspath('images/user/' + images['desktop_window'])
        
        img_coordinates = pug.locate(needle, haystack, grayscale=False)
        if img_coordinates is not None:
            img_getX, img_getY = pug.center(img_coordinates)
            return img_getX, img_getY
        else:
            print('Image "' + img_name + '" not found.')
            return None

    def new_meeting(self):
        new_meeting_btn = self.find_img_coordinates(images['new_meeting_btn'], 'menu')
        pug.click(new_meeting_btn)

    def attendance(self):
        participants_btn = self.find_img_coordinates(images['participants_btn'], 'meeting')
        pug.click(participants_btn)
        
        waiting_room_label = self.find_img_coordinates(images['waiting_room_label'], 'meeting')
        pug.click(waiting_room_label)
        pug.move(0,33)
        
        admit_remove_btn = self.find_img_coordinates(images['admit_remove_btn'], 'meeting')
        pug.click(admit_remove_btn)