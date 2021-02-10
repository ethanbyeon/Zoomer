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
        needle = os.path.abspath("images/" + img_folder + '/' + img_name)
        haystack = np.array(sct.grab(sct.monitors[1]).pixels, dtype=np.uint8)
        img_coordinates = pug.locate(needle, haystack, grayscale=True, confidence=0.8)

    if img_coordinates is not None:
        img_getX, img_getY = pug.center(img_coordinates)
        return img_getX, img_getY
    else:
        print('Image "' + img_name + '" not found.')
        return None


def get_text_coordinates(img_as_np: np.ndarray):
    if not isinstance(img_as_np, np.ndarray):
        raise TypeError(f"get_text_coordinates() argument must be a numpy.ndarray, not {type(img_as_np).__name__!r}")
    gray = cv2.cvtColor(img_as_np, cv2.COLOR_BGR2GRAY)
    d = pytesseract.image_to_data(gray, output_type=Output.DICT)

    text_coords = []
    for i in range(0, len(d['text'])):

        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])

        if i < len(d['text']) - 1:
            (x2, y2, w2, h2) = (d['left'][i + 1], d['top'][i + 1], d['width'][i + 1], d['height'][i + 1])

            if d['text'][i] != 0 and len(d['text'][i]) != 0:
                if d['text'][i + 1] != 0 and len(d['text'][i + 1]) != 0:
                    text = d['text'][i] + ' ' + d['text'][i + 1]

                    if re.match(r'Meeting \([0-5]\)', text) or re.match(r'[0-50] the', text) or re.match(r'\([1-50]\) >', text) or text == "the Meeting":
                        cv2.rectangle(gray,
                            (x - 10, y),
                            (x + w + w2 + 100, y + h + 5),
                            (255, 255, 255), -1)
                        continue
                    else:
                        coordinates = {'x': x, 'y': y}
                        text_coords.append({'Text': text.lower(), 'Coordinates': coordinates})

                    # CV2
                    # cv2.rectangle(gray,
                    #     (x, y),
                    #     (x + w + w2 + 10, y + h),
                    #     (0, 0, 255), 2)
                    # cv2.imshow('Output', gray)

    return text_coords
