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
    root.iconbitmap('images/check.ico')
    root.wm_attributes('-topmost',1)
    file = tk.filedialog.askopenfilename(initialdir='/Desktop', title="Select A File", filetypes=(("CSV FILE", "*.csv"),))
    FILES["Input"] = file
    return file


@eel.expose
def output_file():
    root = tk.Tk()
    root.withdraw()
    root.title("NZA")
    root.iconbitmap('images/check.ico')
    root.wm_attributes('-topmost',1)
    file = filedialog.asksaveasfilename(defaultextension='.csv')
    FILES["Output"] = file
    return file


@eel.expose
def start(category):
    automation.setup_df(FILES["Input"], FILES["Output"])
    automation.attendance(FILES["Input"], FILES["Output"], category)

eel.start('index.html')