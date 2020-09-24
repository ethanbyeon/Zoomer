import capture
import time
import pandas as pd
import pyautogui as pug


class Zoomer:

    def __init__(self):
        self.name = 'Zoomer'
    

    def new_meeting(self):

        pug.click(capture.find_img_coordinates('new_meeting_btn.png', 'menu'))
        time.sleep(3.0)

        pug.moveTo(capture.find_img_coordinates('zoom_meeting_label.png', 'meeting'))
        pug.click(capture.find_img_coordinates('participants_btn.png', 'meeting'))


    def attendance(self, file_name, student_type):

        waiting_room_label = capture.find_img_coordinates('waiting_room_label.png', 'meeting')
        in_the_meeting_label = capture.find_img_coordinates('in_the_meeting_label.png', 'meeting')
        dot_btn = capture.find_img_coordinates('dot_btn.png', 'meeting')
        
        if waiting_room_label is not None:
            x1, y1 = waiting_room_label[0] - 35, waiting_room_label[1] + 10
            x2, y2 = dot_btn[0], in_the_meeting_label[1] - 5
            width = x2 - x1
            height = y2 - y1
            
            capture.part_screenshot(x1, y1, width, height, 'meeting')
            attendance_list = self.validate_students(x1, y1, file_name, student_type)
            self.roll_call(attendance_list)
        else:
            print("Attendance checked!")

    
    def validate_students(self, x, y, file_name, student_type):
        
        waiting_list = capture.get_text_coordinates('waiting_list.png', 'meeting')
        waiting_list_names = set(student['Text'] for student in waiting_list)
        attendance_list = {'Present': [], 'Absent': [], 'Unknown': []}

        student_data = pd.read_csv(file_name)
        all_students = set()
        
        if student_type == 'Leader':
            for c in student_data[student_type]:
                info = c.replace(',', '').split(' ')
                name = info[1] + ' ' + info[0]
                all_students.add(name)
        elif student_type == 'Student':
            for r in student_data.drop(['Group', 'Leader'], axis=1):
                print(r)
            
            # for r in student_data.iloc[:,2:]:
            #     print(r)
                
        present_students = waiting_list_names.intersection(all_students)
        absent_students = all_students.difference(waiting_list_names)
        unknown_students = waiting_list_names.difference(all_students)

        attendance_list['Present'].append(present_students)
        attendance_list['Absent'].append(absent_students)
        attendance_list['Unknown'].append(unknown_students)
        
        for student in waiting_list:
            if student['Text'] in present_students:
                pug.moveTo(x + student['Coordinates']['x'], y + student['Coordinates']['y'])
                pug.click(capture.find_img_coordinates('admit_btn.png', 'meeting'))

        return attendance_list


    def roll_call(self, attendance_list):

        print('Present Students: ' + str(attendance_list['Present']))
        print('Absent Students: ' + str(attendance_list['Absent']))
        print('Unknown Students: ' + str(attendance_list['Unknown']))
        print('Attendance checked!')