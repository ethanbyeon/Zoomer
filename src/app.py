import eel
import tkinter as tk
import automation

from tkinter import filedialog

eel.init('web')

FILES = {'Input': '', 'Output': ''}

@eel.expose
def input_file():
    root = tk.Tk()
    root.withdraw()
    root.title("NZA")
    root.iconbitmap('res/check.ico')
    root.wm_attributes('-topmost',1)
    file = tk.filedialog.askopenfilename(initialdir='/Desktop', title="Select A File", filetypes=(("CSV FILE", "*.csv"),))
    FILES["Input"] = file
    return file


@eel.expose
def output_file():
    root = tk.Tk()
    root.withdraw()
    root.title("NZA")
    root.iconbitmap('res/check.ico')
    root.wm_attributes('-topmost',1)
    file = filedialog.asksaveasfilename(defaultextension='.csv')
    FILES["Output"] = file
    return file


@eel.expose
def admit(category):
    if FILES.get('Input') and FILES.get('Output'):
        automation.setup_df(FILES["Input"], FILES["Output"])
        automation.attendance(FILES["Input"], FILES["Output"], category)
    elif not FILES.get('Input') and FILES.get('Output'):
        print("Please select a Roster.")
    elif not FILES.get('Output') and FILES.get('Input'):
        print("Please select an Attendance Sheet.")
    else:
        print("Please select a Roster AND an Attendance Sheet.")

eel.start('index.html')