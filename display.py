import os
import tkinter as tk

from tkinter import filedialog
from zoomer import Zoomer


BUTTON_HEIGHT = 2
BUTTON_WIDTH = 20

BOT = Zoomer()
FILES = {'Input': '', 'Output': ''}

class Display(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)

        self.grid()
        self.master.title("Zoomer")
        self.master.resizable(width=False, height=False)
        self.master.geometry('330x400')

        self.create_widgets()
        self.mainloop()
        

    def create_widgets(self):

        file_in_btn = tk.Button(self, text="Student Roster", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=lambda: self.addFile("Input"))
        file_out_btn = tk.Button(self, text="Attendance Results", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=lambda: self.addFile("Output"))

        student_btn = tk.Button(self, text="Take Attendance", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=lambda: self.attendance("Student"))
        leaders_btn = tk.Button(self, text="Admit Group Leaders", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=lambda: self.attendance("Leader"))
        
        file_in_btn.grid(row=1, column=0, padx=10, pady=5)
        file_out_btn.grid(row=1, column=1, pady=5)
        student_btn.grid(row=2, column=0, pady=5)
        leaders_btn.grid(row=2, column=1, pady=5)

    
    def addFile(self, file):
        file_name = filedialog.askopenfilename(initialdir='/', title="Select A File", filetypes=(("csv files", '*.csv'),))
        
        if os.path.isfile(file_name):
            FILES[file] = file_name

        if FILES['Input'] != '' and FILES['Output'] != '':
            BOT.setup_df(FILES["Input"], FILES["Output"])


    def attendance(self, student_type):
        if FILES['Input'] == '' or FILES['Output'] == '':
            if FILES['Input'] == '':
                print("Please select an input file for the student roster.")
            if FILES['Output'] == '':
                print("Please select an output file for the attendance results.")
        else:
            BOT.attendance(FILES["Output"], student_type)
        

Display()