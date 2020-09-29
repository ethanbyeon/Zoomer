import tkinter as tk

from tkinter import filedialog
from zoomer import Zoomer


BUTTON_HEIGHT = 2
BUTTON_WIDTH = 20

BOT = Zoomer()

class Display(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)

        self.grid()
        self.master.title("Zoomer")
        self.master.resizable(width=False, height=False)
        self.master.geometry('400x400')

        self.create_widgets()
        self.mainloop()
        

    def create_widgets(self):

        student_btn = tk.Button(self, text="Student Attendance", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=self.student_file_input)
        leaders_btn = tk.Button(self, text="Group Leaders", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=self.leader_file_input)

        student_btn.grid(row=1, column=0, padx=125, pady=10)
        leaders_btn.grid(row=2, column=0)


    def student_file_input(self):
        student_roster = filedialog.askopenfilename(title='Select A File', filetypes=(('csv files', '*.csv'),))
        attendance_list = filedialog.askopenfilename(title='Select A File', filetypes=(('csv files', '*.csv'),))
        BOT.attendance(student_roster, attendance_list, 'Student')
    
    
    def leader_file_input(self):
        student_roster = filedialog.askopenfilename(title='Select A File', filetypes=(('csv files', '*.csv'),))
        attendance_list = filedialog.askopenfilename(title='Select A File', filetypes=(('csv files', '*.csv'),))
        BOT.attendance(student_roster, attendance_list, 'Leader')
        

Display()