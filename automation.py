import capture
import pandas as pd
import pyautogui as pug
import time

from tkinter import filedialog


def setup_df(input_file, output_file):
    """Prepares a default dataframe for an attendance sheet.

        This function reads an input file to create a dataframe for the output file
        that records the student's ID, name, status, and time of admittance. The student names
        are arranged alphabetically, and the "Status" and "Time" columns are set to "NA".

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

# FIGURE OUT HOW TO OMIT STUDENTS THAT WERE ADMITTED TO REDUCE SEARCH TIME
# MAYBE CONNECT APP TO A DATABASE
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
            search_x, search_y = search_bar[0] - 40, search_bar[1] + 20
            width = dot_btn[0] - search_x
            height = (dot_btn[1] - search_y) - 300

            if category == "Student":
                validate_students(search_x, search_y, width, height, search_bar, input_file, output_file)

            elif category == "Leader":
                validate_leaders(search_x, search_y, width, height, search_bar, input_file, output_file)

    else:
        return None

wait_x, wait_y, wait_w, wait_h = 0, 0, 0, 0

absent_students = set()

def validate_students(x, y, width, height, search_bar, input_file, output_file):
    """Verifies participant names through a dataframe before admission.

    This function types the name of each group leader, found in the student roster, into 
    the search bar and captures a precise region.
    Then, the name from the search result is extracted from the captured region and recorded in a set.
    The name in the set is then added to a "pool" that serves as a base for performing set operations.
    
    The present student is identified if the name extracted from the captured
    region can be found in the student roster.

    The absent student is identified if the name in the student roster
    cannot be extracted from the captured region.

    After this process, the present_students set and absent_students set are passed into
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

    out_df = pd.read_csv(output_file)
    
    # ADD CURRENT DATE
    # FILTER OUT PRESENT STUDENTS, ITERATE THROUGH ABSENT STUDENTS AFTER FIRST CLICK
    # if not out_df.isnull(df['C'].iloc[0]):
        
    out_df.fillna("NA", inplace=True)
    out_df.iat[0, 2] = pd.to_datetime('today').date().strftime('%m/%d/%Y')
    print(out_df.iat[0,2])

    for r in range(0, len(out_df.iloc[:, 1:2])):
        for c in out_df.iloc[r, 1:2]:
            if out_df.iat[r, 2] == "NA" or out_df.iat[r, 2] == "ABSENT":
                students.add(c.lower())

    for name in students:
        print(name)
        pug.click(search_bar)
        pug.typewrite(name)

        meeting_label = capture.find_img_coordinates("in_the_meeting_label.png", "meeting")
        
        if meeting_label is not None:
            capture.waiting_ss(x, y, width, height, "meeting")
            wait_x, wait_y, wait_w, wait_h = x, y, width, height

            wait_list = capture.get_text_coordinates("waiting_list.png", "meeting")
            wait_name = set(student['Text'].replace('‘','') for student in wait_list)
            
            present_students = wait_name.intersection(students)
            absent_students = students.difference(wait_name)
            
            record_student(x, y, present_students, absent_students, wait_list, output_file)
            search()

def validate_leaders(x, y, width, height, search_bar, input_file, output_file):
    """Verifies the names of group leaders through a dataframe before admission.

    This function types the name of each group leader found in the student roster into 
    the search bar and captures a precise region. 
    Then, the name from the search result is extracted from the captured region, and it is put through
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
            capture.waiting_ss(x, y, width, (meeting_label[1] - 5), "meeting")
            wait_x, wait_y, wait_w, wait_h = x, y, width, (meeting_label[1] - 5)
            wait_list = capture.get_text_coordinates("waiting_list.png", "meeting")
            wait_name = set(student['Text'].replace('‘','') for student in wait_list)   
            
            present_leader = wait_name.intersection(leaders)
            absent_leaders = leaders.difference(wait_name)
            
            record_student(x, y, present_leader, absent_leaders, wait_list, output_file)
            search()


def search():
    blue_close_btn = capture.find_img_coordinates("blue_close_search.png", "meeting")

    if blue_close_btn is not None:
        pug.click(blue_close_btn)


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
                if c.lower() in present_set:
                    admit_student(x, y, c.lower(), wait_list)
                    output_df.iat[r, 2] = "PRESENT"

                if c.lower() in absent_set:
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
            print("FOUND!!")
            match = person

    if match is not None:
        pug.moveTo(x + match['Coordinates']['x'], y + match['Coordinates']['y'])
        capture.waiting_ss(wait_x, wait_y, wait_w, wait_h, "meeting")
        pug.click(pug.locateOnScreen('images/meeting/admit_btn.png', grayscale=True))
              

#TEST
def test():
    setup_df("test/groups.csv", "test/out.csv")
    attendance_test()

def attendance_test():
    dot_btn = capture.find_img_coordinates("dot_btn.png", "meeting")

    if dot_btn is not None:
        waiting_room_label = capture.find_img_coordinates("waiting_room_label.png", "meeting")
        
        if waiting_room_label is not None:
            x, y = waiting_room_label[0] - 15, waiting_room_label[1] + 10
            x2, y2 = dot_btn[0], dot_btn[1] - 10
            width = x2 - x
            height = y2 - y

            width, height = check_nonverbal(x, y, width, height, dot_btn[0])
            wait_x, wait_y, wait_w, wait_h = x, y, width, height
            capture.waiting_ss(x, y, width, height, "meeting")
            val_students(x, y, "test/out.csv")

    else:
        return None

def check_nonverbal(x, y, w, h, dot_x):
    nonverbal_btns = capture.find_img_coordinates("nonverbal_btns.png", "meeting")
    
    if nonverbal_btns is not None:
        x2, y2 = dot_x, nonverbal_btns[1] - 20
        new_width = x2 - x
        new_height = y2 - y

        return new_width, new_height
    else:
        return w, h

def val_students(x, y, output_file="test/out.csv"):
    wait_list = capture.get_text_coordinates("waiting_list.png", "meeting")
    wait_names = set(student['Text'] for student in wait_list)
    df_pool = set()

    output_df = pd.read_csv(output_file)
    output_df.fillna("NA", inplace=True)
    for r in range(0, len(output_df.iloc[:, 1:])):
        for c in output_df.iloc[r, 1:]:
            if c != "NA":
                 df_pool.add(c)

    present_students = wait_names.intersection(df_pool)
    absent_students = df_pool.difference(wait_names)

    record_student(x, y, present_students, absent_students, wait_list, output_file="test/out.csv")