import os
import tkinter as tk
import automation

from tkinter import filedialog

WIN_W = 240
WIN_H = 335

BTN_W = 20

FONT = ('arial', 12, 'bold')
FILES = {'Input': '', 'Output': ''}

COLOR = {
    'kombu': '#3C493F',
    'xanadu': '#7E8D85',
    'ash': '#B3BFB8',
    'mint': '#A2E3C4',
    'white': '#F0F7F4',
    'danger': '#F04D43',
    'mango': '#FB9927',
    'success': '#A3DE83',
}

class Display(tk.Frame):

    @classmethod
    def main(cls):
        root = tk.Tk()
        root.title("NZA")
        root.iconbitmap('res/check.ico')
        root.configure(bg=COLOR['ash'])
        root.geometry(f'{WIN_W}x{WIN_H}')

        frame = cls(root, bg=COLOR['ash'])
        frame.grid()
        root.mainloop()


    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        # FILE BORDERS
        self.fin_border = tk.Button(self, 
            text="BORDER 1", 
            font=FONT, 
            height=4, 
            width=BTN_W, 
            borderwidth=0, 
            bg=COLOR['xanadu'],
            fg=COLOR['kombu'],
            activebackground=COLOR['xanadu'], 
            activeforeground=COLOR['kombu'])
        self.fout_border = tk.Button(self, 
            text="BORDER 2", 
            font=FONT, 
            height=4, 
            width=BTN_W, 
            borderwidth=0, 
            bg=COLOR['xanadu'],
            fg=COLOR['kombu'],
            activebackground=COLOR['xanadu'], 
            activeforeground=COLOR['kombu'])

        # FILE BUTTONS
        self.fin_btn = tk.Button(self, 
            text="CLASS ROSTER", 
            font=FONT, 
            height=3, 
            width=BTN_W-1, 
            borderwidth=0, 
            fg=COLOR['kombu'], 
            bg=COLOR['ash'], 
            activebackground=COLOR['mint'], 
            activeforeground=COLOR['white'], 
            command=lambda: addFile(self.fin_btn, self.fin_border))
        self.fout_btn = tk.Button(self, 
            text="ATTENDANCE SHEET", 
            font=FONT, 
            height=3, 
            width=BTN_W-1, 
            borderwidth=0, 
            fg=COLOR['kombu'], 
            bg=COLOR['ash'],
            activebackground=COLOR['mint'], 
            activeforeground=COLOR['white'],
            command=lambda: saveFile(self.fout_btn, self.fout_border))

        # AUTOMATION BUTTONS
        self.student_btn = tk.Button(self, 
            text="ADMIT STUDENTS", 
            font=FONT, 
            height=2, 
            width=BTN_W, 
            borderwidth=0, 
            fg="white", 
            bg=COLOR['danger'], 
            activebackground=COLOR['mango'], 
            activeforeground='white', 
            command=lambda: attendance("student"))
        self.leaders_btn = tk.Button(self, 
            text="ADMIT LEADERS", 
            font=FONT, 
            height=2, 
            width=BTN_W, 
            borderwidth=0, 
            fg="white", 
            bg=COLOR['danger'], 
            activebackground=COLOR['mango'], 
            activeforeground='white', 
            command=lambda: attendance("leader"))
        
        # GRID
        self.fin_border.grid(row=1, column=0, padx=17, pady=(20,10))
        self.fout_border.grid(row=2, column=0, pady=(0,10))
        
        self.fin_btn.grid(row=1, column=0, padx=17, pady=(20,10))
        self.fout_btn.grid(row=2, column=0, pady=(0,10))
        
        self.student_btn.grid(row=3, column=0, pady=(0,10))
        self.leaders_btn.grid(row=4, column=0)
        
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
        self.student_btn['bg'] = COLOR['danger']
    def leaders_leave(self, e):
        self.leaders_btn['bg'] = COLOR['danger']

def saveFile(out_btn, border):
    export_path = filedialog.asksaveasfilename(defaultextension='.csv')
    
    FILES["Output"] = export_path
    f = export_path.split('/')

    out_btn.config(text="ATTENDANCE SHEET:\n" + f[-1])
    out_btn['fg'] = COLOR['white']
    out_btn['bg'], border['bg'] = COLOR['success'], COLOR['success']

    if FILES["Input"] and FILES["Output"]:
        if FILES["Input"] != FILES["Output"]:
            automation.setup_df(FILES["Input"], FILES["Output"])


def addFile(in_btn, border):
    file_name = filedialog.askopenfilename(initialdir='/Desktop', title="Select A File", filetypes=(("CSV FILE", "*.csv"),))
    
    if os.path.isfile(file_name):
        FILES["Input"] = file_name
        f = file_name.split('/')
        
        in_btn.config(text="CLASS ROSTER:\n" + f[-1])
        in_btn['fg'] = COLOR['white']
        in_btn['bg'], border['bg'] = COLOR['success'], COLOR['success']


def attendance(student_type):
    if FILES:
        automation.attendance(FILES['Input'], FILES['Output'], student_type)

           
if __name__ == '__main__':
    Display.main()