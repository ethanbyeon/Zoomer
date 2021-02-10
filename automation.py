import mss
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
        info = s.replace(',', '').split(' ')

        student['Student ID'].append(info[2])
        student['Name'].append(info[1] + ' ' + info[0])
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


wait_x, wait_y, wait_w, wait_h = 0, 0, 0, 0

leader_prep, student_prep = False, False
absent_students = set()
def validate_students(x, y, width, height, search_bar, input_file, output_file, leader=False):
    global absent_students
    students = set()

    out_df = pd.read_csv(output_file)
    out_df.fillna("NA", inplace=True)

    if leader:
        in_df = pd.read_csv(input_file)

        for r in range(len(in_df.iloc[:, 1])):
            info = (in_df.iloc[r, 1]).replace(',', '').split(' ')
            name = info[1] + ' ' + info[0]

            if leader_prep:
                pos = out_df.loc[out_df['Name'] == name].index[0]
                if out_df.iat[pos, 2] == "ABSENT":
                    students.add(name.lower())
                else:
                    continue
            else:
                students.add(name.lower())
    else:
        for r in range(0, len(out_df.iloc[:, 1:2])):
            for c in out_df.iloc[r, 1:2]:
                if student_prep:
                    if out_df.iat[r, 2] == "ABSENT":
                        students.add(c.lower())
                else:
                    if out_df.iat[r, 2] == "PRESENT":
                        continue
                    else:
                        students.add(c.lower())

    for name in students:
        print(name)
        pug.click(search_bar)
        pug.typewrite(name)

        meeting_label = capture.find_img_coordinates("in_the_meeting_label.png", "meeting")

        if meeting_label is not None:
            with mss.mss() as sct:
                wait_list = capture.get_text_coordinates(np.array(sct.grab({'top': int(y),
                                                                            'left': int(x),
                                                                            'width': int(width),
                                                                            'height': int(height)})))
            wait_name = set(student['Text'].replace('‘','') for student in wait_list)

            present_students = wait_name.intersection(students)
            absent_students = students.difference(wait_name)
            print("SIZE: " + str(len(absent_students)))

            record_student(x, y, present_students, absent_students, wait_list, output_file, leader)
            search()


def search():
    blue_close_btn = capture.find_img_coordinates("blue_close_search.png", "meeting")

    if blue_close_btn is not None:
        pug.click(blue_close_btn)


def record_student(x, y, present_set, absent_set, wait_list, output_file, leader):
    output_df = pd.read_csv(output_file)
    output_df.fillna("NA", inplace=True)

    for r in range(0, len(output_df.iloc[:, 1:2])):
        for c in output_df.iloc[r, 1:2]:
            if output_df.iat[r, 2] == "PRESENT":
                continue
            else:
                if c.lower() in present_set:
                    admit_student(x, y, c.lower(), wait_list)
                    output_df.iat[r, 2] = "PRESENT"

                if c.lower() in absent_set:
                    output_df.iat[r, 2] = "ABSENT"

            output_df.iat[r, 3] = time.strftime('%H:%M:%S', time.localtime())

    output_df.to_csv(output_file, index=False)

    global student_prep, leader_prep
    if leader:
        leader_prep = True
    else:
        student_prep = True


def admit_student(x, y, student, wait_list):
    match = None

    for person in wait_list:
        if person['Text'] == student:
            print("FOUND: " + student)
            match = person

    if match is not None:
        pug.moveTo(x + match['Coordinates']['x'], y + match['Coordinates']['y'])
        pug.click(pug.locateOnScreen('images/meeting/admit_btn.png', grayscale=True))
