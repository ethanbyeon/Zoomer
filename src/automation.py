import capture
import datetime
import numpy as np
import pandas as pd
import pyautogui as pug

from tables import (Base, 
                    engine,
                    Attendance,
                    Leader, 
                    Student,
                    Session)

from sqlalchemy import select, insert, update


def setup_df(input_file):
    df = pd.read_csv(input_file, header=None)
    f_row = df.iloc[0].str.match(r"([A-Z][-a-zA-Z]*'?[-a-zA-Z]+), ([A-Z][a-z]*'?[-a-zA-Z]+)( [A-Z]'?[-a-zA-Z]*)? (\((\d{6})?\))?")
    
    if not f_row.any(axis=None):
        df = df.iloc[1:]

    f_col = df.iloc[:,0].str.match(r"([A-Z][-a-zA-Z]*'?[-a-zA-Z]+), ([A-Z][a-z]*'?[-a-zA-Z]+)( [A-Z]'?[-a-zA-Z]*)? (\((\d{6})?\))?")
    if not f_col.any(axis=None):
        df = df.iloc[:,1:]

    dfs = []
    for index, series in df.iterrows():
        c = series.str.extract(r"([A-Z][-a-zA-Z]*'?[-a-zA-Z]+), ([A-Z][a-z]*'?[-a-zA-Z]+)( [A-Z]'?[-a-zA-Z]*)? (\((\d{6})?\))?")
        c.drop(columns=3, inplace=True)
        c.dropna(how='all', inplace=True)
        c['Leader_ID'] = c.iloc[0, 3]
        c.rename(columns={0:'Last', 1:'First', 2:'Middle', 4:'ID'}, inplace=True)
        c['ID'] = c['ID'].astype(int)
        c['Leader_ID'] = c['Leader_ID'].astype(int)
        dfs.append(c)

    with engine.begin() as conn:
        Base.metadata.create_all(conn)

        for r in dfs:
            r.iloc[:1, :4].to_sql("leader", con=conn, if_exists='append', index=False)
            r.iloc[:1, :4].to_sql("student", con=conn, if_exists='append', index=False)
            r.iloc[1:].to_sql("student", con=conn, if_exists='append', index=False)

            for student_id in r.iloc[:, 3]:
                dt = datetime.datetime.now()
                dt_format = dt.strftime('%m/%d/%Y %H:%M:%S')
                t = datetime.datetime.strptime(dt_format, '%m/%d/%Y %H:%M:%S')
        
                attn_table = insert(Attendance).values(id=int(student_id), date=t, status="ABSENT")
                conn.execute(attn_table)


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
            return "Please clear<br/>search bar"
    else:
        return """Check:
                <br/>• Hosting Privileges
                <br/>• Open Participant's tab
                <br/>• No overlapping tabs
                """

def attendance(category):
    screen = check_screen()
    if screen == True:
        if category == "STUDENTS":
            validate_students()
        if category == "LEADERS":
            validate_leaders()
    else:
        return screen


def validate_students():
    with Session(engine) as session, session.begin():
        students = session.execute(
            select(Student, Attendance).\
            where(Student.id == Attendance.id).\
            where(Attendance.status == "ABSENT")
        ).scalars().all()

        for student in students:
            name = f'{student.first} {student.last}'
            print(name)

        search(students)


def validate_leaders():
    with Session(engine) as session, session.begin():
        leaders = session.execute(
            select(Leader, Attendance).\
            where(Leader.id == Attendance.id).\
            where(Attendance.status == "ABSENT")
        ).scalars().all()

        for leader in leaders:
            name = f'{leader.first} {leader.last}'
            print(name)

        search(leaders)


def search(absent_list):
    global search_bar, width

    for user in absent_list:
        name = f'{user.first} {user.last}'
        
        print(f"[?] Searching  : {name}")
        pug.click(search_bar)
        pug.typewrite(name)

        wait_label = capture.find_img_coordinates("waiting_room_label.png", "meeting")
        in_meeting_label = capture.find_img_coordinates("in_the_meeting_label.png", "meeting")
        
        if wait_label and in_meeting_label:
            x, y = wait_label[0] - 20, wait_label[1] + 10
            height = in_meeting_label[1] - (wait_label[1] + 25)

            wait_list = capture.get_text_coordinates(x, y, width, height)
            
            # MOVE TO NEXT STUDENT IF MORE THAN ONE NAME IS DETECTED
            if len(wait_list) > 1:
                return f"IMPOSTER DETECTED:<br/>{name}"
            
            print("WAIT LIST:", wait_list)
            for person in wait_list:
                cv_name = person['Text']
                if (cv_name != name) and len(cv_name) == len(name):
                    if spell_check({name : cv_name}) <= 2:
                        record(user)
                        admit(name, wait_list)
                elif cv_name == name:
                    print("NO SPELL:", name)
                    record(user)
                    admit(name, wait_list) 
            close_search()
        else:
            close_search()
            print("Could not locate labels.")
            return f'Could not<br/>locate labels.'


def record(user):
    with Session(engine) as session, session.begin():
        print(user)

        dt = datetime.datetime.now()
        dt_format = dt.strftime('%m/%d/%Y %H:%M:%S')
        t = datetime.datetime.strptime(dt_format, '%m/%d/%Y %H:%M:%S')

        session.execute(
            update(Attendance).\
            where(user.id == Attendance.id).\
            where(Attendance.status == "ABSENT").\
            values(status="PRESENT").\
            values(date=t).\
            execution_options(synchronize_session="fetch")
        )
        print(session.execute(select(Attendance).where(Attendance.status=="PRESENT")).scalars().all())

def admit(name, wait_list):
    global x, y

    match = next((cv_name for cv_name in wait_list if cv_name['Text'] == name), None)
    if match:
        pug.moveTo(x + match['Coordinates']['x'], y + match['Coordinates']['y'])
        pug.click(pug.locateOnScreen('res/meeting/admit_btn.png', grayscale=True))
        print(f"[!] ADMITTED   : {match['Text']}")


def spell_check(name_dict):
    count = 0
    for key, value in name_dict.items():
        for i in range(len(value)):
            if(value[i] != key[i]):
                count+=1
    print(f"SPELL CHECK: {name_dict} {count}")
    return count


def close_search():
    blue_close_btn = capture.find_img_coordinates("blue_close_search.png", "meeting")
    if blue_close_btn:
        pug.click(blue_close_btn[0]-5, blue_close_btn[1])
    else:
        close_btn = capture.find_img_coordinates("close_search.png", "meeting")
        if close_btn:
            pug.click(close_btn[0]-5, close_btn[1])