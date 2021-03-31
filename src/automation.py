import capture
import numpy as np
import pandas as pd
import pyautogui as pug
import time

from tkinter import filedialog
from collections import OrderedDict

setup = False
def setup_df(input_file):
    global df
    
    student_df = pd.read_csv(input_file)
    student_df.fillna('NA', inplace=True)
    d = OrderedDict({'ID': [], 'Name': [], 'Status': [], 'Time': []})
    
    students = []
    for r in range(0, len(student_df.iloc[:, 1:])):
        for c in student_df.iloc[r, 1:]:
            if c != "NA":
                students.append(c)

    for s in sorted(students):
        info = (s.replace(',','').replace('(','').replace(')','')).split(' ')
        if len(info) == 4:
            d['Name'].append(f'{info[0]}, {info[1]} {info[2]}')
            d['ID'].append(info[3])
        elif len(info) == 3:
            d['Name'].append(f'{info[0]}, {info[1]}')
            d['ID'].append(info[2])
        else:
            print(f"Format error in cell containing: {info}")

        d['Status'].append("NA")
        d['Time'].append("NA")
    df = pd.DataFrame(d)
    # print(df)


def export(output_file):
    df.to_csv(output_file, index=False)


x, y, width = 0, 0, 0
def attendance(input_file, category):
    global setup, x, y, width, df
    try:
        if not setup:
            setup_df(input_file)
            setup = True
    except:
        print("Error in roster!")
    else:
        dot_btn = capture.find_img_coordinates("dot_btn.png", "meeting")

        if dot_btn:
            search_bar = capture.find_img_coordinates("participants_search.png", "meeting")
            if search_bar:
                x, y = search_bar[0] - 100, search_bar[1] + 20
                width = dot_btn[0] - x

                if category == "student":
                    validate(search_bar, input_file)
                elif category == "leader":
                    validate(search_bar, input_file, leader=True)
            else:
                print("Please clear the search bar.")


leader_prep, student_prep = False, False
present_students, absent_students, students = set(), set(), set()

def validate(search_bar, input_file, leader=False):
    global present_students, absent_students, students, width

    if leader:
        in_df = pd.read_csv(input_file)
        print("Admitting LEADERS . . .")
        for r in range(len(in_df.iloc[:, 1])):
            info = ((in_df.iloc[r, 1]).replace(',', '').replace('(', '').replace(')', '')).split(' ')
            
            if len(info) == 4:
                df_name = f'{info[0]}, {info[1]} {info[2]}'
            elif len(info) == 3:
                df_name = f'{info[0]}, {info[1]}'
            name = f'{info[1]} {info[0]}'

            name_pos = df.loc[(df_name == df['Name'])].index[0]
            if df.iat[name_pos, 2] == "PRESENT":
                continue
            else:
                students.add(name)
                absent_students.add(name)
    else:
        print("Admitting STUDENTS . . .")
        for r in range(0, len(df.iloc[:, 1:2])):
            for c in df.iloc[r, 1:2]:
                info = c.replace(',', '').split(' ')
                name = f'{info[1]} {info[0]}'

                if df.iat[r, 2] == "PRESENT":
                    continue
                else:
                    students.add(name)
                    absent_students.add(name)

    for name in absent_students:
        print(f"[?] Searching  : {name}")
        pug.click(search_bar)
        pug.typewrite(name)

        wait_label = capture.find_img_coordinates("waiting_room_label.png", "meeting")
        in_meeting_label = capture.find_img_coordinates("in_the_meeting_label.png", "meeting")
        
        if wait_label and in_meeting_label:
            x, y = wait_label[0] - 20, wait_label[1] + 10
            height = in_meeting_label[1] - (wait_label[1] + 25)
            
            wait_list = capture.get_text_coordinates(x, y, width, height)
            wait_name = set(student['Text'] for student in wait_list)
            
            if len(wait_name) > 1:
                print(f"IMPOSTER DETECTED: {name}")
                continue

            present_students = wait_name.intersection(students)
            absent_students = students.difference(wait_name)

            record_student(present_students, absent_students, wait_list, leader)
            close_search()
        else:
            close_search()
            print("Could not locate labels.")
            break
    
    print(f"\nABSENT  ({len(absent_students)}): {absent_students}")
    print(f"PRESENT ({len(present_students)}): {present_students}")
    print("-------")


def record_student(present_set, absent_set, wait_list, leader):
    global student_prep, leader_prep

    for r in range(0, len(df.iloc[:, 1:2])):
        for c in df.iloc[r, 1:2]:
            info = (c.replace(',','')).split(' ')
            name = f'{info[1]} {info[0]}'

            if df.iat[r, 2] == "PRESENT":
                continue
            else:
                if name in present_set:
                    admit_student(name, wait_list)
                    df.iat[r, 2] = "PRESENT"
                if name in absent_set:
                    df.iat[r, 2] = "ABSENT"
            df.iat[r, 3] = time.strftime('%H:%M:%S', time.localtime())
    # print(df)


def admit_student(student, wait_list):
    global x, y
    for person in wait_list:
        if person['Text'] == student:
            print(f'[!] IDENTIFIED : {student}')
            match = person

    if match:
        pug.moveTo(x + match['Coordinates']['x'], y + match['Coordinates']['y'])
        pug.click(pug.locateOnScreen('res/meeting/admit_btn.png', grayscale=True))
        print(f"[!] ADMITTED   : {match['Text']}")


def close_search():
    blue_close_btn = capture.find_img_coordinates("blue_close_search.png", "meeting")
    if blue_close_btn:
        pug.click(blue_close_btn[0]-5, blue_close_btn[1])
    else:
        close_btn = capture.find_img_coordinates("close_search.png", "meeting")
        if close_btn:
            pug.click(close_btn[0]-5, close_btn[1])
