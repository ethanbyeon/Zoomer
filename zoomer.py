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
    'student_list' : 'attendance.csv',

    # BREAKOUT ROOM
    'br_btn' : 'breakout_room_btn.png',
    'more_br_opt' : 'more_br_opt.png',
    'more_btn' : 'more_btn.png',

    # MEETING
    'admit_btn' : 'admit_btn.png',
    'dot_btn' : 'dot_btn.png',
    'in_the_meeting_label' : 'in_the_meeting_label.png',
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
        d = tess.image_to_data(gray, output_type=Output.DICT)
        
        text_coords = []
        for i in range(0, len(d['text'])):
      
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])

            if d['text'][i] != 0 and len(d['text'][i]) != 0:
                text = d['text'][i]
                coordinates = {'x': x, 'y': y}
                text_coords.append({'Text': text, 'Coordinates': coordinates})
                
        #         cv2.rectangle(gray,
        #                 (x, y),
        #                 (x + w, y + h),
        #                 (0, 0, 255), 2)
            
        # cv2.imshow('Output', gray)
        return text_coords

    
    def validate_students(self, x, y):
        
        waiting_list = self.get_text_coordinates(images['waiting_list'], 'meeting')
        waiting_list_names = set(student['Text'] for student in waiting_list)
        
        attendance_list = {'Present': [], 'Absent': []}
    
        df = pd.read_csv('images/user/' + images['student_list'])
        all_students = set()
        for index, row in df.iterrows():
            students = row['Leader'].replace(',',' ').split(',')
            for student in students:
                info = student.split(' ')
                f_name, l_name = info[2], info[0]
                all_students.add(f_name)
                all_students.add(l_name)

        present_students = waiting_list_names.intersection(all_students)
        absent_students = all_students.difference(waiting_list_names)
        attendance_list['Present'].append(present_students)
        attendance_list['Absent'].append(absent_students)
        
        for student in waiting_list:
            if student['Text'] in present_students:
                pug.moveTo(x + student['Coordinates']['x'], y + student['Coordinates']['y'])
                pug.click(self.find_img_coordinates(images['admit_btn'], 'meeting'))

        return attendance_list
        

    def new_meeting(self):
        pug.click(self.find_img_coordinates(images['new_meeting_btn'], 'menu'))
        time.sleep(3.0)

        pug.moveTo(self.find_img_coordinates(images['zoom_meeting_label'], 'meeting'))
        pug.click(self.find_img_coordinates(images['participants_btn'], 'meeting'))


    def attendance(self):
        waiting_room_label = self.find_img_coordinates(images['waiting_room_label'], 'meeting')
        in_the_meeting_label = self.find_img_coordinates(images['in_the_meeting_label'], 'meeting')
        dot_btn = self.find_img_coordinates(images['dot_btn'], 'meeting')
        
        if waiting_room_label is not None:
            x1, y1 = waiting_room_label[0] - 35, waiting_room_label[1] + 10
            x2, y2 = dot_btn[0], in_the_meeting_label[1] - 5
            width = x2 - x1
            height = y2 - y1
            
            self.part_screenshot(x1, y1, width, height, 'meeting')
            attendance_list = self.validate_students(x1, y1)
            print(attendance_list['Present'])
            print(attendance_list['Absent'])
        else:
            print("Attendance checked!")