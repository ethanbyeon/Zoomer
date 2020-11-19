import capture
import pandas as pd
import pyautogui as pug
import time

from tkinter import filedialog


def setup_df(input_file, output_file):
    """Prepares a default dataframe for an attendance sheet.

        This function reads an input file to create a dataframe for the output file
        that records the student's ID, name, status, and time. The student names
        are arranged alphabetically and the "Status" and "Time" columns are set to "NA".

        Args:
            input_file: The student roster.
            output_file: The attendance sheet.

        Returns:
            None
    """
    
    student_df = pd.read_csv(input_file)
    student_df.fillna('NA', inplace=True)
    student = {'Student ID': [], 'Name': [], 'Status': [], 'Time': []}
    
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

    output_df = pd.DataFrame(student)
    output_df.to_csv(output_file, index=False)


def attendance(input_file, output_file, category):
    """Checks if the student or leader attendance button is pressed.

    This function checks if the dot/more button can be found on the "Participants" tab
    to ensure that the user has host or co-host permissions.
    Then, it passes necessary arguments to the function that was called by 
    the appropriate button.

    If the "Take Attendance" button is pressed, the check_queue() function is called.
    If the "Admit Group Leaders" button is pressed, the search_leader() function is called.

    Args:
        input_file: The student roster.
        output_file: The attendance sheet.
        category: The type of student (Student, Leader, etc.).

    Returns:
        None: If the dot/more button cannot be found on the bottom right of the "Participants" tab.
    """

    dot_btn = capture.find_img_coordinates("dot_btn.png", "meeting")
    
    if dot_btn is not None:
        
        search_bar = capture.find_img_coordinates("participants_search.png", "meeting")

        if search_bar is not None:
            x, y = search_bar[0] - 145, search_bar[1] + 30
            x2 = dot_btn[0]
            width = x2 - x
            height = y

            if category == "Student":
                validate_students(x, y, width, height, search_bar, input_file, output_file)

            elif category == "Leader":
                validate_leaders(x, y, width, height, search_bar, input_file, output_file)

    else:
        return None


def validate_students(x, y, width, height, search_bar, input_file, output_file):
    """Verifies participant names through a dataframe before admission.

    This function types the name of each group leader found in the student roster into 
    the search bar and captures a precise region (provided by the x-y and width-height args).
    Then, the name from the search result is extracted from the captured region and recorded in a set.
    The name in the set is then added to a "pool" that serves as a base for performing
    set operations.
    
    The present student is identified if the name extracted from the captured
    region can be found in the student roster.

    The absent student is identified if the name in the student roster
    cannot be extracted from the captured region.

    After this process, the present_student set and absent_students set are passed into
    the record_student() function to be recorded into the dataframe (attendance sheet).
    
    Args:
        x: The x-coordinate of the waiting-room label.
        y: The y-coordinate of the waiting-room label.
        width: The width of the captured region.
        height: The height of the captured region.
        search_bar: The coordinates of the search bar.
        input_file: The student roster.
        output_file: The attendance sheet.

    Return:
        None
    """
    
    students = set()

    output_df = pd.read_csv(output_file)
    output_df.fillna("NA", inplace=True)

    for r in range(0, len(output_df.iloc[:, 1:2])):
        for c in output_df.iloc[r, 1:2]:
            if output_df.iat[r, 2] == "NA" or output_df.iat[r, 2] == "ABSENT":
                students.add(c)

    for name in students:
        print(name)
        pug.click(search_bar)
        pug.typewrite(name)

        meeting_label = capture.find_img_coordinates("in_the_meeting_label.png", "meeting")
        
        if meeting_label is not None:
            capture.part_screenshot(x, y, width, (meeting_label[1] - 5) - height, "meeting")
            wait_list = capture.get_text_coordinates("waiting_list.png", "meeting")
            wait_name = set(student['Text'].replace('‘','') for student in wait_list)
            
            present_student = wait_name.intersection(students)
            absent_students = students.difference(wait_name)
            
            record_student(x, y, present_student, absent_students, wait_list, output_file)
            search()

def validate_leaders(x, y, width, height, search_bar, input_file, output_file):
    """Verifies the names of group leaders through a dataframe before admission.

    This function types the name of each group leader found in the student roster into 
    the search bar and captures a precise region (provided by the x-y and width-height args). 
    Then, the name from the search result is extracted from the captured region and is put through
    a set operation similar to the validate_students() function. After the status of the group leader
    is determined, the present_leader set and absent_leaders set are passed into the write_to_csv()
    function to be recorded into the dataframe (attendance sheet).
    
    Args:
        x: The x-coordinate of the waiting-room label.
        y: The y-coordinate of the waiting-room label.
        width: The width of the captured region.
        height: The height of the captured region.
        search_bar: The coordinates of the search bar.
        input_file: The student roster.
        output_file: The attendance sheet.

    Return:
        None
    """

    leaders = set()

    input_df = pd.read_csv(input_file)
    for r in input_df.iloc[:, 1]:
        info = r.replace(',', '').split(' ')
        name = info[1] + ' ' + info[0]
        leaders.add(name)

    for name in leaders:
        print(name)
        pug.click(search_bar)
        pug.typewrite(name)

        meeting_label = capture.find_img_coordinates("in_the_meeting_label.png", "meeting")
        
        if meeting_label is not None:
            capture.part_screenshot(x, y, width, (meeting_label[1] - 5) - height, "meeting")
            wait_list = capture.get_text_coordinates("waiting_list.png", "meeting")
            wait_name = set(student['Text'].replace('‘','') for student in wait_list)   
            
            present_leader = wait_name.intersection(leaders)
            absent_leaders = leaders.difference(wait_name)
            
            record_student(x, y, present_leader, absent_leaders, wait_list, output_file)
            search()


def search():
    blue_close_btn = capture.find_img_coordinates("blue_close_search.png", "meeting")
    if blue_close_btn is not None:
        pug.moveTo(blue_close_btn[0] - 5, blue_close_btn[1])


def record_student(x, y, present_set, absent_set, wait_list, output_file):
    """Records the status of the student and calls for student admission if necessary.

    This function iterates over each row in the dataframe (attendance sheet) and marks
    the student either "PRESENT" or "ABSENT" based on the sets passed in as arguments.

    If the student is in the present set, the student is marked "PRESENT" and the
    x-y coordinates, student's name, and the coordinates of the extracted text(s) from
    the captured region are passed into the admit_student() function.

    If the student is already marked "PRESENT", this function will skip the student as
    they were already accounted for.
    
    Args:
        x: The x-coordinate of the waiting-room label.
        y: The y-coordinate of the waiting-room label.
        present_set: The set of present students.
        absent_set: The set of absent students.
        wait_list: The list of coordinates of each student's name that are found the waiting room.
        output_file: The attendance sheet.
        
    Return:
        None
    """

    output_df = pd.read_csv(output_file)
    output_df.fillna("NA", inplace=True)

    for r in range(0, len(output_df.iloc[:, 1:2])):
        for c in output_df.iloc[r, 1:2]:
            if output_df.iat[r, 2] == "PRESENT":
                continue
            else:
                if c in present_set:
                    admit_student(x, y, c, wait_list)
                    output_df.iat[r, 2] = "PRESENT"

                if c in absent_set:
                    output_df.iat[r, 2] = "ABSENT"

            output_df.iat[r, 3] = time.strftime('%H:%M:%S', time.localtime())
    
    output_df.to_csv(output_file, index=False)


def admit_student(x, y, student, wait_list):
    """Admits student after validating with the dataframe.
    
    This function iterates over each name in the wait_list list to find the
    coordinates that correspond to the student's name.

    Args:
        x: The x-coordinate of the waiting-room label.
        y: The y-coordinate of the waiting-room label.
        student: The student's name.
        wait_list: 
            The list of coordinates of each student's name that 
            are extracted from the captured region.

    Return:
        None
    """

    match = None
    for person in wait_list:
        if person['Text'] == student:
            match = person

    if match is not None:
        pug.moveTo(x + match['Coordinates']['x'], y + match['Coordinates']['y'])
        pug.click(capture.find_img_coordinates("admit_btn.png", "meeting"))