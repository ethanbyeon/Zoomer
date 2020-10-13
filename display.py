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
        self.master.geometry('330x300')

        self.create_widgets()
        self.mainloop()
        

    def create_widgets(self):

        f_in_label = tk.Label(self, text="Roster: EMPTY")
        f_out_label = tk.Label(self, text="Results: EMPTY")

        f_in_btn = tk.Button(self, text="Student Roster", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=lambda: self.addFile("Input", f_in_label))
        f_out_btn = tk.Button(self, text="Attendance Results", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=lambda: self.addFile("Output", f_out_label))

        student_btn = tk.Button(self, text="Take Attendance", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", 
            command=lambda: self.attendance("Student", f_in_label, f_out_label, output_label))
        leaders_btn = tk.Button(self, text="Admit Group Leaders", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", 
            command=lambda: self.attendance("Leader", f_in_label, f_out_label, output_label))

        output_label = tk.Label(self, text="")
        
        f_in_label.grid(row=1, column=0, padx=10, pady=(15,10))
        f_out_label.grid(row=1, column=1, pady=(15,10))

        f_in_btn.grid(row=2, column=0, padx=10, pady=5)
        f_out_btn.grid(row=2, column=1, pady=5)
        
        student_btn.grid(row=3, column=0, pady=5)
        leaders_btn.grid(row=3, column=1, pady=5)

        output_label.grid(row=4, column=0, pady=10, columnspan=2)

    
    def addFile(self, file, label):
        file_name = filedialog.askopenfilename(initialdir='/', title="Select A File", filetypes=(("csv files", '*.csv'),))
        
        if os.path.isfile(file_name):
            FILES[file] = file_name
            f = file_name.split('/')
            
            if file == "Input":
                label.config(text="Roster: " + f[-1])
            else:
                label.config(text="Results: " + f[-1])

        if FILES['Input'] != '' and FILES['Output'] != '':
            zoomer.setup_df(FILES['Input'], FILES['Output'])


    def attendance(self, student_type, f_in_label, f_out_label, output_label):
        if FILES['Input'] == '' or FILES['Output'] == '':
            if FILES['Input'] == '':
                output_label.config(text="Please select an input file.")
            if FILES['Output'] == '':
                output_label.config(text="Please select an output file.")
        else:
            output_label.config(text="")
            run = zoomer.attendance(FILES['Input'], FILES['Output'], student_type)
            if run is None:
                output_label.config(text="Please make sure to: \nminimize all unused windows \nkeep the Zoom app visible on the desktop.")
            
Display()