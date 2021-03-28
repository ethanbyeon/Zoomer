import re
import os
import cv2
import numpy as np
import pytesseract
import mss, mss.tools
import pyautogui as pug

from PIL import Image
from pytesseract import Output

# pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR\\tesseract.exe'

def find_img_coordinates(img_name, img_folder):
    with mss.mss() as sct:
        needle = os.path.abspath("res/" + img_folder + '/' + img_name)
        haystack = np.array(sct.grab(sct.monitors[1]).pixels, dtype=np.uint8)
        img_coordinates = pug.locate(needle, haystack, grayscale=True, confidence=0.8)

    if img_coordinates is not None:
        img_x, img_y = pug.center(img_coordinates)
        return img_x, img_y
    else:
        print('Image "' + img_name + '" not found')
        return None


def get_text_coordinates(x, y, width, height):
    with mss.mss() as sct:
        gray = cv2.cvtColor(np.array(sct.grab({'top': int(y),
                                               'left': int(x),
                                               'width': int(width),
                                               'height': int(height)})), cv2.COLOR_BGR2GRAY)
    
    scale = 220
    width = int(gray.shape[1] * scale / 100)
    height = int(gray.shape[0] * scale / 100)
    dim = (width, height)

    resized = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)
    d = pytesseract.image_to_data(resized, output_type=Output.DICT)

    text_coords = []
    for i in range(0, len(d['text'])):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if i < len(d['text']) - 1:
            (x2, y2, w2, h2) = (d['left'][i + 1], d['top'][i + 1], d['width'][i + 1], d['height'][i + 1])
            
            if d['text'][i]:
                if d['text'][i + 1]:
                    text = d['text'][i] + ' ' + d['text'][i + 1]
                    coordinates = {'x': x, 'y': y}
                    
                    text_coords.append({'Text': text, 'Coordinates': coordinates})
                    print(f"[.] Recognized : {text}")

                    # cv2.rectangle(resized,
                    #     (x - 10, y - 10),
                    #     ((x + w + w2) + 20, (y + h) + 10),
                    #     (0, 0, 255), 2)
                    # cv2.imshow("OCR Image", resized)

    return text_coords