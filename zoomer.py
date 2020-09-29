import capture
import pandas as pd
import pyautogui as pug
import time
from tkinter import filedialog

class Zoomer:

    def __init__(self):
        self.name = 'Zoomer'
    

    def attendance(self, file_name, file2_name, student_type):

        waiting_room_label = capture.find_img_coordinates('waiting_room_label.png', 'meeting')
        dot_btn = capture.find_img_coordinates('dot_btn.png', 'meeting')
        
        in_the_meeting_label = capture.find_img_coordinates('in_the_meeting_label.png', 'meeting')
        if in_the_meeting_label is not None:
            time.sleep(1.0)
            pug.click(in_the_meeting_label[0] + 85, in_the_meeting_label[1])
            pug.moveTo(in_the_meeting_label[0], in_the_meeting_label[1] + 20)
        
        nonverbal_btns = capture.find_img_coordinates('nonverbal_btns.png', 'meeting')
        if nonverbal_btns is not None:
            x1, y1 = waiting_room_label[0] - 35, waiting_room_label[1] + 10
            x2, y2 = dot_btn[0], nonverbal_btns[1] - 20
            width = x2 - x1
            height = y2 - y1
        else:
            if waiting_room_label is not None:
                x1, y1 = waiting_room_label[0] - 35, waiting_room_label[1] + 10
                x2, y2 = dot_btn[0], dot_btn[1] - 10
                width = x2 - x1
                height = y2 - y1
            else:
                print("Attendance checked!")
        
        capture.part_screenshot(x1, y1, width, height, 'meeting')
        attendance_list = self.validate_students(x1, y1, file_name, file2_name, student_type)
        self.roll_call(attendance_list)

    # CHECKS IF THE STUDENT'S NAME IN WAITING ROOM IS WRITTEN IN THE STUDENT ROSTER
    def validate_students(self, x, y, file_name, file2_name, student_type):
        
        waiting_list = capture.get_text_coordinates('waiting_list.png', 'meeting')
        waiting_list_names = set(student['Text'] for student in waiting_list)

        student_pool = set()
        attendance_list = {'Present': [], 'Absent': [], 'Unknown': []}

        # USER STUDENT ROSTER
        student_df = pd.read_csv(file_name)

        # OUTPUT ATTENDANCE LIST
        students = {'Student ID': [], 'First Name': [], 'Last Name': [], 'Status': []}
        
        if student_type == 'Leader':
        
            for c in student_df[student_type]:
                info = c.replace(',', '').split(' ')
                name = info[1] + ' ' + info[0]
                student_pool.add(name)

                students['Student ID'].append(info[2])
                students['First Name'].append(info[1])
                students['Last Name'].append(info[0])
                students['Status'].append('')
            
            output_df = pd.DataFrame(students)
            output_file = output_df.to_csv(file2_name, index=False)

        elif student_type == 'Student':
                        
            for r in range(0, len(student_df.iloc[:, 2:])):
                for c in student_df.iloc[r, 2:]:
                    if type(c) is float:
                        continue
                    else:
                        info = c.replace(',', '').split(' ')
                        name = info[1] + ' ' + info[0]
                        student_pool.add(name)
                
        present_students = waiting_list_names.intersection(student_pool)
        absent_students = student_pool.difference(waiting_list_names)
        unknown_students = waiting_list_names.difference(student_pool)

        attendance_list['Present'].append(present_students)
        attendance_list['Absent'].append(absent_students)
        attendance_list['Unknown'].append(unknown_students)
        
        # for student in waiting_list:
        #     if student['Text'] in present_students:
        #         pug.moveTo(x + student['Coordinates']['x'], y + student['Coordinates']['y'])
        #         pug.click(capture.find_img_coordinates('admit_btn.png', 'meeting'))

        return attendance_list


    def roll_call(self, attendance_list):

        print('Present Students: ' + str(attendance_list['Present']))
        print('Absent Students: ' + str(attendance_list['Absent']))
        print('Unknown Students: ' + str(attendance_list['Unknown']))
        print('Attendance checked!')