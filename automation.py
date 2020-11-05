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

        if category == "Student":
            check_queue(dot_btn, output_file)

        elif category == "Leader":
            search_leader(dot_btn, input_file, output_file)

    else:
        return None


def check_queue(dot_btn, output_file):
    """Checks if there are participants in the waiting room.

    This function records the coordinates of the waiting room label if it is present.
    The coordinates of the waiting room label are used in conjunction with the 
    coordinates of the dot/more button and the nonverbal buttons (if it is present) 
    to create a precise region for the computer to analyze. After capturing the 
    specified region, each participant's name in the waiting room is validated 
    through the validate_students() function.

    Args:
        dot_btn: The dot/more button coordinates.
        output_file: The attendance sheet.

    Returns: 
        None
    """

    waiting_room_label = capture.find_img_coordinates("waiting_room_label.png", "meeting")

    if waiting_room_label is not None:
        x, y = waiting_room_label[0] - 15, waiting_room_label[1] + 10
        x2, y2 = dot_btn[0], dot_btn[1] - 10
        width = x2 - x
        height = y2 - y

        width, height = check_nonverbal(x, y, width, height, dot_btn[0])
        
        capture.part_screenshot(x, y, width, height, "meeting")
        validate_students(x, y, output_file)


def search_leader(dot_btn, input_file, output_file):
    """Searches for group leaders using the participants search bar.

    This function records the coordinates of the participants search bar if it is present.
    The coordinates of the participants search bar are used in conjunction with 
    the coordinates of the dot/more button and the nonverbal buttons (if it is present)
    to create a precise region for the computer to analyze. After capturing the
    specified region, each participant's name that appears in the region from the search
    result is validated through the validate_leaders() function.

    Args:
        dot_btn: The dot/more button coordinates.
        input_file: The student roster.
        output_file: The attendance sheet.

    Return:
        None
    """

    search_bar = capture.find_img_coordinates("participants_search.png", "meeting")

    if search_bar is not None:
        x, y = search_bar[0] - 145, search_bar[1] + 30
        x2, y2 = dot_btn[0], dot_btn[1] - 10
        width = x2 - x
        height = y2 - y

        width, height = check_nonverbal(x, y, width, height, dot_btn[0])
        validate_leaders(x, y, width, height, search_bar, input_file, output_file)


def check_nonverbal(x, y, width, height, dot_xpos):
    """Returns the width and height of the captured region that accounts for the nonverbal buttons.
    
    This function adjusts the width and height of the captured region 
    according to the coordinates of the nonverbal buttons.

    Args:
        x: The x-coordinate of the waiting-room label.
        y: The y-coordinate of the waiting-room label.
        width: The width of the captured region.
        height: The height of the captured region.
        dot_xpos: The x-coordinate of the dot/more button.

    Return:
        new_width, new_height: int, int
            The new adjusted width and height that accounts for the nonverbal buttons.
        width, heigth: int, int
            The original width and height that does not account for the nonverbal buttons.
    """
    
    nonverbal_btns = capture.find_img_coordinates("nonverbal_btns.png", "meeting")
    
    if nonverbal_btns is not None:
        x2, y2 = dot_xpos, nonverbal_btns[1] - 20
        new_width = x2 - x
        new_height = y2 - y
        
        return new_width, new_height
    else:
        return width, height


def validate_students(x, y, output_file):
    """Verifies participant names through a dataframe before admission.

    This function extracts text from the captured region and records them in a set.
    Each name in the set is then added to a "pool" that serves as a base for performing
    set operations.
    
    The present students are found in the list of names extracted from the captured
    region and are recorded in the student roster.

    The absent students are not found in the list of names extracted from the captured
    region but are recorded in the student roster.

    The unknown students are found in both the list of names extracted from the
    captured region but are not recorded in the student roster.

    After this process, the present_students set and absent_students set are passed into
    the write_to_csv() function to be recorded into the dataframe (attendance sheet).
    
    Args:
        x: The x-coordinate of the waiting-room label.
        y: The y-coordinate of the waiting-room label.
        student: The student name.
        wait_list: The list of coordinates of each student's name that are found the waiting room.

    Return:
        attendance_list: dict
            Returns
    """
    
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
    unknown_students = wait_names.difference(df_pool)

    write_to_csv(x, y, present_students, absent_students, wait_list, output_file)


def validate_leaders(x, y, width, height, search_bar, input_file, output_file):
    """Verifies the names of group leaders through a dataframe before admission.

    This function types the name of each group leader found in the student roster into 
    the search bar and captures a precise region (provided by the x-y and width-height args). 
    Then, the name from the search result is extracted from the captured region and is put through
    a set operation similar to the validate_students() function. After the status of the group leader
    is determined, the present_leaders set and absent_leaders set are passed into the write_to_csv()
    function to be recorded into the dataframe (attendance sheet).
    
    Args:
        x: The x-coordinate of the waiting-room label.
        y: The y-coordinate of the waiting-room label.
        width: The width of the captured region.
        height: The height of the captured region.
        input_file: The student roster.
        output_file: The attendance sheet.

    Return:
        set: The set of the names of group leaders.
    """

    leaders = set()

    input_df = pd.read_csv(input_file)
    for r in input_df.iloc[:, 1]:
        info = r.replace(',', '').split(' ')
        name = info[1] + ' ' + info[0]
        leaders.add(name)

    for name in leaders:
        pug.click(search_bar)
        pug.typewrite(name)

        capture.part_screenshot(x, y, width, height, "meeting")
        wait_list = capture.get_text_coordinates("waiting_list.png", "meeting")
        wait_names = set(student['Text'].replace('‘','') for student in wait_list)   
        
        present_leaders = wait_names.intersection(leaders)
        absent_leaders = leaders.difference(wait_names)
        
        write_to_csv(x, y, present_leaders, absent_leaders, wait_list, output_file)
        
        blue_close_btn = capture.find_img_coordinates("blue_close_search.png", "meeting")

        if blue_close_btn is not None:
            pug.click(blue_close_btn[0] - 10, blue_close_btn[1])
        else:
            close_btn = capture.find_img_coordinates("close_search.png", "meeting")
            if close_btn is not None:
                pug.click(close_btn[0] - 7, close_btn[1])


def write_to_csv(x, y, present, absent, wait_list, output_file):
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
        present: The list of present students.
        absent: The list of absent students.
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
            if c in present or c in absent:
                if c in present:
                    output_df.iat[r, 2] = "PRESENT"
                    admit_student(x, y, c, wait_list)
                if c in absent:
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
    
    pug.moveTo(x + match['Coordinates']['x'], y + match['Coordinates']['y'])
    pug.click(capture.find_img_coordinates("admit_btn.png", "meeting"))