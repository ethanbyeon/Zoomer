import tkinter as tk
import pyautogui as pug

from zoomer import Zoomer

HEIGHT = 500
WIDTH = 500

BOT = Zoomer()

class Display(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)

        self.grid()
        self.master.title("Zoomer")

        self.main_grid = tk.Frame(
            self, bg="gray", bd=3, width=WIDTH, height=HEIGHT
        )
        self.main_grid.grid()

        self.create_widgets()
        self.mainloop()

    def create_widgets(self):
        new_meeting_btn = tk.Button(self, text="New Meeting", fg="black", command=BOT.new_meeting)
        attendance_btn = tk.Button(self, text="Attendance", fg="black", command=BOT.attendance)

        new_meeting_btn.grid(row=0, column=0)
        attendance_btn.grid(row=1, column=0)

Display()