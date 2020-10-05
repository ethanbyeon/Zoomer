import os
import tkinter as tk
import zoomer

from tkinter import filedialog


BUTTON_HEIGHT = 2
BUTTON_WIDTH = 20

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

        input_label = tk.Label(self, text="Student Roster: Empty")
        output_label = tk.Label(self, text="Attendance Results: Empty")

        file_in_btn = tk.Button(self, text="Student Roster", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=lambda: self.addFile("Input", input_label))
        file_out_btn = tk.Button(self, text="Attendance Results", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=lambda: self.addFile("Output", output_label))

        student_btn = tk.Button(self, text="Take Attendance", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=lambda: self.attendance("Student", input_label, output_label))
        leaders_btn = tk.Button(self, text="Admit Group Leaders", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=lambda: self.attendance("Leader", input_label, output_label))
        
        input_label.grid(row=3, column=0, columnspan=2)
        output_label.grid(row=4, column=0, pady=5, columnspan=2)

        file_in_btn.grid(row=1, column=0, padx=10, pady=5)
        file_out_btn.grid(row=1, column=1, pady=5)
        student_btn.grid(row=2, column=0, pady=5)
        leaders_btn.grid(row=2, column=1, pady=5)

    
    def addFile(self, file, label):
        file_name = filedialog.askopenfilename(initialdir='/', title="Select A File", filetypes=(("csv files", '*.csv'),))
        
        if os.path.isfile(file_name):
            FILES[file] = file_name
            
            if file == "Input":
                label.config(text="Student Roster: " + file_name)
            else:
                label.config(text="Attendance Results: " + file_name)

        if FILES['Input'] != '' and FILES['Output'] != '':
            zoomer.setup_df(FILES['Input'], FILES['Output'])


    def attendance(self, student_type, input_label, output_label):
        if FILES['Input'] == '' or FILES['Output'] == '':
            if FILES['Input'] == '':
                input_label.config(text="Student Roster: Please select an input file.")
            if FILES['Output'] == '':
                output_label.config(text="Attendance Results: Please select an output file.")
        else:
            zoomer.attendance(FILES['Input'], FILES['Output'], student_type)
            
Display()