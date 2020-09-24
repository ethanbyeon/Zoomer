import cv2
import os
import mss
import pyautogui as pug
import pytesseract as tess
import re

from PIL import Image
from pytesseract import Output


def full_screenshot():

    with mss.mss() as sct:
        sct.shot(output='images/user/desktop_window.png')


def part_screenshot(xpos, ypos, width, height, img_folder):

    with mss.mss() as sct:
        area = {"top": int(ypos), 'left': int(xpos), 'width': int(width), 'height': int(height)}
        
        area_img = sct.grab(area)
        mss.tools.to_png(area_img.rgb, area_img.size, output='images/' + img_folder + '/waiting_list.png')


def find_img_coordinates(img_name, img_folder):

    full_screenshot()

    needle = os.path.abspath('images/' + img_folder + '/' + img_name)
    haystack = os.path.abspath('images/user/desktop_window.png')
    
    img_coordinates = pug.locate(needle, haystack, grayscale=False)
    if img_coordinates is not None:
        img_getX, img_getY = pug.center(img_coordinates)
        return img_getX, img_getY
    else:
        print('Image "' + img_name + '" not found.')
        return None


def get_text_coordinates(img_name, img_folder):

    img = cv2.imread('images/' + img_folder + '/' + img_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    d = tess.image_to_data(gray, output_type=Output.DICT)
    
    text_coords = []
    for i in range(0, len(d['text'])):
        
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])

        if i < len(d['text']) - 1:
            (x2, y2, w2, h2) = (d['left'][i + 1], d['top'][i + 1], d['width'][i + 1], d['height'][i + 1])

            if d['text'][i] != 0 and len(d['text'][i]) != 0:
                if d['text'][i + 1] != 0 and len(d['text'][i + 1]) != 0:
                    text = d['text'][i] + ' ' + d['text'][i + 1]
                    
                    if re.match(r'Meeting ([0-5])', text) or re.match(r'[0-50] the', text) or re.match(r'([1-50]) >', text):
                        cv2.rectangle(gray,
                            (x - 10, y),
                            (x + w + w2 + 50, y + h + 5),
                            (255, 255, 255), -1)
                    else:
                        coordinates = {'x': x, 'y': y}
                        text_coords.append({'Text': text, 'Coordinates': coordinates})
                    
                    # DEBUG DETECTION
                    cv2.rectangle(gray,
                            (x, y),
                            (x + w + w2 + 10, y + h),
                            (0, 0, 255), 2)
        
    cv2.imshow('Output', gray)
    return text_coords