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
    automation.export(FILES["Output"])
    return file


@eel.expose
def admit(category):
    if FILES.get('Input'):
        try:
            automation.attendance(FILES["Input"], category)
        except RuntimeError:
            raise
        else:
            eel.exportCSV()
    else:
        print("Please select a Roster.")


eel.start('index.html')