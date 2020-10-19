import os
import tkinter as tk
import zoomer

from tkinter import filedialog
from tkinter import tix


WIN_W = 370
WIN_H = 235

BTN_W = 20
BTN_H = 2

COLOR = {
    'danger': '#F04D43',
    'grey': '#CED4DA',
    'light-grey': '#E9ECEF',
    'mango': '#FB9927',
    'mint': '#5BBD93',
    'success': '#A3DE83',
    'white': '#F8F9FA',
}

FONT = ('arial', 10, 'bold')

FILES = {'Input': '', 'Output': ''}

# MESSAGES
f_in_msg = ("Select an Excel file (.csv) that contains"
                "\na student roster for the desired class/period.")
f_out_msg = ("Select an empty Excel file (.csv) that"
                "\nwould store the attendance results"
                "\nfor the desired class/period.")
student_msg = ("Admit students from the waiting room."
                "\nIf the waiting room is not empty,"
                "\npress this button again.")
leaders_msg = ("Admit group leaders from the waiting room."
                "\nIf the waiting room is not empty,"
                "\npress this button again.")
output_msg = ("Please make sure to: "
                "\nMinimize all unused windows "
                "\nKeep the Zoom app visible on the desktop"
                "\n(Hover over a button for more information)")

class Display(tk.Frame):

    @classmethod
    def main(cls):
        root = tix.Tk()
        root.title("Zoomer")
        root.iconbitmap('images/app/check.ico')
        root.resizable(width=False, height=False)
        root.configure(bg=COLOR['grey'])
        root.geometry(f'{WIN_W}x{WIN_H}')

        frame = cls(root, bg=COLOR['grey'])
        frame.grid()
        root.mainloop()


    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        # FILES LABEL
        self.f_in_label = tk.Label(self, text="Roster: EMPTY", font=FONT)
        self.f_out_label = tk.Label(self, text="Results: EMPTY", font=FONT)

        # FILE BUTTONS
        self.f_in_btn = tk.Button(self, text="Student Roster", font=FONT, 
            height=BTN_H, width=BTN_W, borderwidth=0, 
            fg="white", bg=COLOR['danger'], activebackground=COLOR['mango'], activeforeground='white', 
            command=lambda: addFile("Input", self.f_in_label, self.f_in_btn, self.f_out_btn))
        self.f_out_btn = tk.Button(self, text="Attendance Results", font=FONT, 
            height=BTN_H, width=BTN_W, borderwidth=0, 
            fg="white", bg=COLOR['danger'], activebackground=COLOR['mango'], activeforeground='white',
            command=lambda: addFile("Output", self.f_out_label, self.f_in_btn, self.f_out_btn))

        # AUTOMATION BUTTONS
        self.student_btn = tk.Button(self, text="Take Attendance", font=FONT, 
            height=BTN_H, width=BTN_W, borderwidth=0, 
            fg="white", bg=COLOR['mint'], activebackground=COLOR['mango'], activeforeground='white', 
            command=lambda: attendance("Student", self.f_in_label, self.f_out_label, self.output_label))
        self.leaders_btn = tk.Button(self, text="Admit Group Leaders", font=FONT, 
            height=BTN_H, width=BTN_W, borderwidth=0, 
            fg="white", bg=COLOR['mint'], activebackground=COLOR['mango'], activeforeground='white', 
            command=lambda: attendance("Leader", self.f_in_label, self.f_out_label, self.output_label))

        # HELP LABEL
        self.output_label = tk.Label(self, text=output_msg, font=FONT, bg=COLOR['grey'])

        # BALLOON MESSAGES
        self.f_in_tip = tix.Balloon(self)
        self.f_in_tip.config(bg=COLOR['light-grey'])
        self.f_in_tip.bind_widget(self.f_in_btn, balloonmsg=f_in_msg)

        self.f_out_tip = tix.Balloon(self)
        self.f_out_tip.config(bg=COLOR['light-grey'])
        self.f_out_tip.bind_widget(self.f_out_btn, balloonmsg=f_out_msg)

        self.student_tip = tix.Balloon(self)
        self.student_tip.config(bg=COLOR['light-grey'])
        self.student_tip.bind_widget(self.student_btn, balloonmsg=student_msg)

        self.leaders_tip = tix.Balloon(self)
        self.leaders_tip.config(bg=COLOR['light-grey'])
        self.leaders_tip.bind_widget(self.leaders_btn, balloonmsg=leaders_msg)

        balloons = [self.f_in_tip, self.f_out_tip, self.student_tip, self.leaders_tip]
        for msg in balloons:
            for sub in msg.subwidgets_all():
                sub.config(bg=COLOR['light-grey'])
        
        # GRID
        self.f_in_label.grid(row=1, column=0, padx=10, pady=(20,0), sticky='WENS')
        self.f_out_label.grid(row=1, column=1, padx=10, pady=(20,0), sticky='WENS')

        self.f_in_btn.grid(row=2, column=0, padx=10, pady=(0,10))
        self.f_out_btn.grid(row=2, column=1, padx=10, pady=(0,10))
        
        self.student_btn.grid(row=3, column=0, pady=(0,5))
        self.leaders_btn.grid(row=3, column=1, pady=(0,5))

        self.output_label.grid(row=4, column=0, pady=15, columnspan=2)
        
        # BINDS
        self.student_btn.bind('<Enter>', self.student_hover)
        self.leaders_btn.bind('<Enter>', self.leaders_hover)

        self.student_btn.bind('<Leave>', self.student_leave)
        self.leaders_btn.bind('<Leave>', self.leaders_leave)
    
    # HOVER METHODS
    def student_hover(self, e):
        self.student_btn['bg'] = COLOR['mango']
    def leaders_hover(self, e):
        self.leaders_btn['bg'] = COLOR['mango']

    def student_leave(self, e):
        self.student_btn['bg'] = COLOR['mint']
    def leaders_leave(self, e):
        self.leaders_btn['bg'] = COLOR['mint']


def addFile(file, label, in_btn, out_btn):
    file_name = filedialog.askopenfilename(initialdir='/', title="Select A File", filetypes=(("csv files", '*.csv'),))
    
    if os.path.isfile(file_name):
        FILES[file] = file_name
        f = file_name.split('/')
        
        if file == "Input":
            label.config(text="Roster: " + f[-1])
            in_btn['bg'] = COLOR['success']
        else:
            label.config(text="Results: " + f[-1])
            out_btn['bg'] = COLOR['success']

    if FILES['Input'] != '' and FILES['Output'] != '':
        zoomer.setup_df(FILES['Input'], FILES['Output'])


def attendance(student_type, f_in_label, f_out_label, output_label):
    if FILES['Input'] != '' and FILES['Output'] != '':
        zoomer.attendance(FILES['Input'], FILES['Output'], student_type)

           
if __name__ == '__main__':
    Display.main()