import os
import time
import mss
import cv2
import pyautogui as pug
import pytesseract as tess
import pandas as pd

from PIL import Image
from pytesseract import Output

images = {

    # USER
    'desktop_window' : 'desktop_window.png',
    'student_list' : 'students.csv',

    # BREAKOUT ROOM
    'br_btn' : 'breakout_room_btn.png',
    'more_br_opt' : 'more_br_opt.png',
    'more_btn' : 'more_btn.png',

    # MEETING
    'admit_btn' : 'admit_btn.png',
    'dot_btn' : 'dot_btn.png',
    'in_the_meeting_label' : 'in_the_meeting_label',
    'participants_btn' : 'participants_btn.png',
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

    
    def get_text_coordinates(self, img_name, img_folder):
        img = cv2.imread('images/' + img_folder + '/' + img_name)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        names = tess.image_to_data(gray, output_type=Output.DICT)
        
        # waiting_names = [line.strip() for line in tess.image_to_string(gray).splitlines() if len(line.strip()) != 0]
        for i in range(0, len(names["text"])):
      
            x = names["left"][i]
            y = names["top"][i]
            w = names["width"][i]
            h = names["height"][i]
            
            text = names["text"][i]
            conf = int(names["conf"][i])
                
            print("Confidence: {}".format(conf))
            print("Text: {}".format(text))
            print("")
            
            text = "".join(text).strip()
            cv2.rectangle(gray,
                        (x, y),
                        (x + w, y + h),
                        (0, 0, 255), 2)
            
        cv2.imshow('Output', gray)

    
    def validate_students(self, list):
        df = pd.read_csv('images/user/' + images['student_list'])
        # print(df[['Groups', 'Leader']])
        for index, row in df.iterrows():
            print(index, row)
        


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
        
        x1, y1 = waiting_room_label[0] - 30, waiting_room_label[1] + 10
        x2, y2 = dot_btn[0], dot_btn[1] - 15
        width = x2 - x1
        height = y2 - y1
        
        self.part_screenshot(x1, y1, width, height, 'meeting')
        print(self.get_text_coordinates(images['waiting_list'], 'meeting'))