import tkinter as tk
import pyautogui as pug
import cv2

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

        new_meeting_btn = tk.Button(self, text="New Meeting", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=BOT.new_meeting)
        attendance_btn = tk.Button(self, text="Attendance", height=BUTTON_HEIGHT, width=BUTTON_WIDTH, fg="black", command=BOT.attendance)

        new_meeting_btn.grid(row=0, column=0, padx=125, pady=10)
        attendance_btn.grid(row=1, column=0)


Display()