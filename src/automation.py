import capture
import numpy as np
import pandas as pd
import pyautogui as pug
import time

from tkinter import filedialog
from collections import OrderedDict


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
            return False
        d['Status'].append("NA")
        d['Time'].append("NA")
    
    df = pd.DataFrame(d)
    # print(df)
    return True


def attendance(input_file, category):
    global df

    if check_screen():
        if category == "student":
            queue = validate_students()
        elif category == "leader":
            queue = validate_leaders(input_file)
        
        search(queue['DF'], queue['ABSENT'], category)


search_bar = None
x, y, width = 0, 0, 0
def check_screen():
    global search_bar, x, y, width
    
    dot_btn = capture.find_img_coordinates("dot_btn.png", "meeting")
    if dot_btn:
        search_bar = capture.find_img_coordinates("participants_search.png", "meeting")
        if search_bar:
            x, y = search_bar[0] - 100, search_bar[1] + 20
            width = dot_btn[0] - x
            return True
        else:
            print("Please clear the search bar.")
            return False


students, present_students, absent_students = set(), set(), set()
def validate_students():
    global df, students, absent_students

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
    
    search = {'DF': students, 'ABSENT': absent_students}
    return search


leaders, present_leaders, absent_leaders = set(), set(), set()
def validate_leaders(input_file):
    global df, leaders, absent_leaders
    print(df)
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
            leaders.add(name)
            absent_leaders.add(name)

    search = {'DF': leaders, 'ABSENT': absent_leaders}
    return search


def search(df_member, absent_set, category):
    global search_bar, width, students, absent_students, present_students, leaders, absent_leaders, present_leaders

    for name in absent_set:
        print(f"[?] Searching  : {name}")
        pug.click(search_bar)
        pug.typewrite(name)

        wait_label = capture.find_img_coordinates("waiting_room_label.png", "meeting")
        in_meeting_label = capture.find_img_coordinates("in_the_meeting_label.png", "meeting")
        
        if wait_label and in_meeting_label:
            x, y = wait_label[0] - 20, wait_label[1] + 10
            height = in_meeting_label[1] - (wait_label[1] + 25)

            wait_list = capture.get_text_coordinates(x, y, width, height)

            # wait_name = set(student['Text'] for student in wait_list)
            # if len(wait_name) > 1:
            #     print(f"IMPOSTER DETECTED: {name}")
            #     continue
            # present = wait_name.intersection(df_member)
            # absent = leaders.difference(wait_name)

            if len(wait_list) > 1:
                print(f"IMPOSTER DETECTED: {name}")
                continue
            wait_name = wait_list[0]['Text']
            
            if len(wait_name) == len(name):
                if spell_check({name : wait_name}) <= 2:
                    present = set([name]).intersection(df_member)
                    if category == "student":
                        absent = students.difference(set([name]))
                    elif category == "leader":
                        absent = leaders.difference(set([name]))
            else:
                present = set([wait_name]).intersection(df_member)
                absent = df_member.difference(set([wait_name]))
            
            if category == "student":
                present_students = present
                absent_students = absent
            elif category == "leader":
                present_leaders = present
                absent_leaders = absent

            record_student(present, absent, wait_list)
            close_search()
        else:
            close_search()
            print("Could not locate labels.")
            break
    
    print(f"\nABSENT  ({len(absent)}): {absent}")
    print(f"PRESENT ({len(present)}): {present}")
    print("-------")
    return len(absent), len(present)


def record_student(present_set, absent_set, wait_list):

    for r in range(0, len(df.iloc[:, 1:2])):
        for c in df.iloc[r, 1:2]:
            info = (c.replace(',','')).split(' ')
            name = f'{info[1]} {info[0]}'

            if df.iat[r, 2] == "PRESENT":
                continue
            else:
                wait_name = wait_list[0]['Text']
                if name in present_set:
                    admit_student(wait_list)
                    df.iat[r, 2] = "PRESENT"
                elif len(name) == len(wait_name):
                    if spell_check({name : wait_name}) <= 2:
                        print("SPELL CHECKED!")
                        admit_student(wait_list)
                        df.iat[r, 2] = "PRESENT"
                elif name in absent_set:
                    df.iat[r, 2] = "ABSENT"
            df.iat[r, 3] = time.strftime('%H:%M:%S', time.localtime())
    print(df)


def admit_student(student):
    global x, y

    pug.moveTo(x + student[0]['Coordinates']['x'], y + student[0]['Coordinates']['y'])
    pug.click(pug.locateOnScreen('res/meeting/admit_btn.png', grayscale=True))
    print(f"[!] ADMITTED   : {student[0]['Text']}")


def spell_check(name_dict):
    count = 0
    for key, value in name_dict.items():
        for i in range(len(value)):
            if(value[i] != key[i]):
                count+=1
    return count


def close_search():
    blue_close_btn = capture.find_img_coordinates("blue_close_search.png", "meeting")
    if blue_close_btn:
        pug.click(blue_close_btn[0]-5, blue_close_btn[1])
    else:
        close_btn = capture.find_img_coordinates("close_search.png", "meeting")
        if close_btn:
            pug.click(close_btn[0]-5, close_btn[1])


def export(output_file):
    df.to_csv(output_file, index=False)