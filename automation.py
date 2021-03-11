import time
import capture
import numpy as np
import pandas as pd
import pyautogui as pug

from tkinter import filedialog

def setup_df(input_file, output_file):
    student_df = pd.read_csv(input_file)

    student_df.fillna('NA', inplace=True)
    student = {'Student ID': [], 'Name': [], 'Status': [], 'Time': [], 'Date': []}
    
    students = []
    for r in range(0, len(student_df.iloc[:, 1:])):
        for c in student_df.iloc[r, 1:]:
            if c != "NA":
                students.append(c)

    for s in sorted(students):
        info = (s.replace(',', '').replace('(', '').replace(')', '')).split(' ')

        if len(info) == 4:
            student['Name'].append(f'{info[0]}, {info[1]} {info[2]}')
            student['Student ID'].append(info[3])
        elif len(info) == 3:
            student['Name'].append(f'{info[0]}, {info[1]}')
            student['Student ID'].append(info[2])

        student['Status'].append("NA")
        student['Time'].append("NA")
        student['Date'].append(pd.to_datetime('today').date().strftime('%m/%d/%Y'))

    output_df = pd.DataFrame(student)
    output_df.to_csv(output_file, index=False)


def attendance(input_file, output_file, category):
    dot_btn = capture.find_img_coordinates("dot_btn.png", "meeting")

    if dot_btn is not None:
        search_bar = capture.find_img_coordinates("participants_search.png", "meeting")
        if search_bar is not None:
            search_x, search_y = search_bar[0] - 40, search_bar[1] + 20
            width = dot_btn[0] - search_x
            height = (dot_btn[1] - search_y) - 300

            if category == "Student":
                validate_students(search_x, search_y, width, height, search_bar, input_file, output_file)
            elif category == "Leader":
                validate_students(search_x, search_y, width, height, search_bar, input_file, output_file, leader=True)
    else:
        return None


leader_prep, student_prep = False, False
present_students, absent_students = set(), set()

def validate_students(x, y, width, height, search_bar, input_file, output_file, leader=False):
    global present_students, absent_students
    students = set()

    out_df = pd.read_csv(output_file)
    out_df.fillna("NA", inplace=True)

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

            if leader_prep:
                name_pos = out_df.loc[(df_name == out_df['Name'])].index[0]
                if out_df.iat[name_pos, 2] == "ABSENT":
                    students.add(name)
                else:
                    continue
            else:
                students.add(name)
    else:
        print("Admitting STUDENTS . . .")
        for r in range(0, len(out_df.iloc[:, 1:2])):
            for c in out_df.iloc[r, 1:2]:
                info = c.replace(',', '').split(' ')
                name = f'{info[1]} {info[0]}'

                if student_prep:
                    if out_df.iat[r, 2] == "ABSENT":
                        students.add(name)
                else:
                    if out_df.iat[r, 2] == "PRESENT":
                        continue
                    else:
                        students.add(name)

    for name in students:
        print(f"[?] Searching  : {name}")
        pug.click(search_bar)
        pug.typewrite(name)

        meeting_label = capture.find_img_coordinates("in_the_meeting_label.png", "meeting")

        if meeting_label is not None:
            wait_list = capture.get_text_coordinates(x, y, width, height)
            wait_name = set(student['Text'] for student in wait_list)

            present_students = wait_name.intersection(students)
            absent_students = students.difference(wait_name)

            record_student(x, y, present_students, absent_students, wait_list, output_file, leader)
            search()
        
    print(f"[#] ABSENT  ({len(absent_students)}): {absent_students}")
    print(f"[#] PRESENT ({len(present_students)}): {present_students}")


def search():
    blue_close_btn = capture.find_img_coordinates("blue_close_search.png", "meeting")
    if blue_close_btn is not None:
        pug.click(blue_close_btn)


def record_student(x, y, present_set, absent_set, wait_list, output_file, leader):
    global student_prep, leader_prep

    output_df = pd.read_csv(output_file)
    output_df.fillna("NA", inplace=True)

    for r in range(0, len(output_df.iloc[:, 1:2])):
        for c in output_df.iloc[r, 1:2]:
            info = (c.replace(',','')).split(' ')
            name = f'{info[1]} {info[0]}'

            if output_df.iat[r, 2] == "PRESENT":
                continue
            else:
                if name in present_set:
                    admit_student(x, y, name, wait_list)
                    output_df.iat[r, 2] = "PRESENT"
                if name in absent_set:
                    output_df.iat[r, 2] = "ABSENT"

            output_df.iat[r, 3] = time.strftime('%H:%M:%S', time.localtime())

    output_df.to_csv(output_file, index=False)

    if leader:
        leader_prep = True
    else:
        student_prep = True


def admit_student(x, y, student, wait_list):
    for person in wait_list:
        if person['Text'] == student:
            print(f'[!] IDENTIFIED : {student}')
            match = person

    if match is not None:
        pug.moveTo(x + match['Coordinates']['x'], y + match['Coordinates']['y'])
        pug.click(pug.locateOnScreen('images/meeting/admit_btn.png', grayscale=True))
