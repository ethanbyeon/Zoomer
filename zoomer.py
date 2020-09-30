import capture
import pandas as pd
import pyautogui as pug
import time
from tkinter import filedialog

class Zoomer:

    def __init__(self):
        self.name = 'Zoomer'

    
    def setup_df(self, input_file, output_file):
        
        student_df = pd.read_csv(input_file)
        student_df.fillna('NA', inplace=True)
        student = {'Student ID': [], 'Name': [], 'Status': []}
        
        students = []
        for r in range(0, len(student_df.iloc[:, 1:])):
            for c in student_df.iloc[r, 1:]:
                if c != 'NA':
                    students.append(c)
        
        for s in sorted(students):
            info = s.replace(',', '').split(' ')

            student['Student ID'].append(info[2])
            student['Name'].append(info[1] + ' ' + info[0])
            student['Status'].append('NA')

        output_df = pd.DataFrame(student)
        output_df.to_csv(output_file, index=False)
    

    def attendance(self, output_file, student_type):

        waiting_room_label = capture.find_img_coordinates('waiting_room_label.png', 'meeting')
        dot_btn = capture.find_img_coordinates('dot_btn.png', 'meeting')
        
        nonverbal_btns = capture.find_img_coordinates('nonverbal_btns.png', 'meeting')
        if nonverbal_btns is not None:
            x1, y1 = waiting_room_label[0] - 35, waiting_room_label[1] + 10
            x2, y2 = dot_btn[0], nonverbal_btns[1] - 20
            width = x2 - x1
            height = y2 - y1
        elif waiting_room_label is not None:
                x1, y1 = waiting_room_label[0] - 35, waiting_room_label[1] + 10
                x2, y2 = dot_btn[0], dot_btn[1] - 10
                width = x2 - x1
                height = y2 - y1
        else:
            return
    
        capture.part_screenshot(x1, y1, width, height, 'meeting')
        attendance_list = self.validate_students(x1, y1, output_file, student_type)
        self.roll_call(attendance_list)


    # CHECKS IF THE STUDENT'S NAME IN WAITING ROOM IS WRITTEN IN THE STUDENT ROSTER
    def validate_students(self, x, y, output_file, student_type):
       
        waiting_list = capture.get_text_coordinates('waiting_list.png', 'meeting')
        waiting_list_names = set(student['Text'] for student in waiting_list)
        df_pool = set()

        attendance_list = {'Present': [], 'Absent': [], 'Unknown': []}
        
        output_df = pd.read_csv(output_file)
        output_df.fillna('NA', inplace=True)
        for r in range(0, len(output_df.iloc[:, 1:])):
            for c in output_df.iloc[r, 1:]:
                if c != 'NA':
                    df_pool.add(c)

        present_students = waiting_list_names.intersection(df_pool)
        absent_students = df_pool.difference(waiting_list_names)
        unknown_students = waiting_list_names.difference(df_pool)
    
        for r in range(0, len(output_df.iloc[:, 1:])):
            for c in output_df.iloc[r, 1:]:
                if c in present_students:
                    output_df.iat[r, 2] = 'PRESENT'
                if c in absent_students:
                    output_df.iat[r, 2] = 'ABSENT'
        
        output_df.to_csv(output_file, index=False)

        attendance_list['Present'].append(present_students)
        attendance_list['Absent'].append(absent_students)
        attendance_list['Unknown'].append(unknown_students)

        # self.admit_students(x, y, present_students, waiting_list)
        
        return attendance_list


    def admit_students(self, x, y, present_students, waiting_list):
        for student in waiting_list:
            if student['Text'] in present_students:
                pug.moveTo(x + student['Coordinates']['x'], y + student['Coordinates']['y'])
                pug.click(capture.find_img_coordinates('admit_btn.png', 'meeting'))


    def roll_call(self, attendance_list):

        print('Present Students: ' + str(attendance_list['Present']))
        print('Absent Students: ' + str(attendance_list['Absent']))
        print('Unknown Students: ' + str(attendance_list['Unknown']))
        print('Attendance checked!')