import os
import mss
import time
import pyautogui as pug
import pandas as pd

from PIL import Image

images = {

    # USER SCREEN
    'desktop_window' : 'desktop_window.png',

    # BREAKOUT ROOM
    'br_btn' : 'breakout_room_btn.png',
    'more_br_opt' : 'more_br_opt.png',
    'more_btn' : 'more_btn.png',

    # MEETING
    'admit_btn' : 'admit_btn.png',
    'dot_btn' : 'dot_btn.png',
    'in_the_meeting_label' : 'in_the_meeting_label',
    'participants_btn' : 'participants_btn.png',
    'participants_label' : 'participants_label.png',
    'remove_btn' : 'remove_btn.png',
    'waiting_list' : 'waiting_list.png',
    'waiting_room_label' : 'waiting_room_label.png',
    'zoom_meeting_label' : 'zoom_meeting_label.png',

    # MENU
    'join_btn' : 'join_btn.png',
    'new_meeting_btn' : 'new_meeting_btn.png',
    'schedule_btn' : 'schedule_btn.png',
}

class Zoomer():

    def __init__(self):
        self.name = 'Zoomer'


    def full_screenshot(self):
        with mss.mss() as sct:
            sct.shot(output="images/user/" + images['desktop_window'])

    
    def part_screenshot(self, xpos, ypos, width, height, img_folder):
        with mss.mss() as sct:
            area = {"top": int(ypos), 'left': int(xpos), 'width': int(width), 'height': int(height)}
            
            area_img = sct.grab(area)
            mss.tools.to_png(area_img.rgb, area_img.size, output='images/' + img_folder + '/waiting_list.png')


    def find_img_coordinates(self, img_name, img_folder, scale=''):
        self.full_screenshot()

        needle = os.path.abspath('images/' + img_folder + '/' + img_name)
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
        time.sleep(3.0)

        zoom_meeting_label = self.find_img_coordinates(images['zoom_meeting_label'], 'meeting')
        pug.moveTo(zoom_meeting_label)

        participants_btn = self.find_img_coordinates(images['participants_btn'], 'meeting')
        pug.click(participants_btn)


    def attendance(self):
        waiting_room_label = self.find_img_coordinates(images['waiting_room_label'], 'meeting')
        dot_btn = self.find_img_coordinates(images['dot_btn'], 'meeting')
        
        x1, y1 = waiting_room_label[0] - 40, waiting_room_label[1]
        x2, y2 = dot_btn[0], dot_btn[1]
        width = x2 - x1
        height = y2 - y1
        
        self.part_screenshot(x1, y1, width, height, 'meeting')
        