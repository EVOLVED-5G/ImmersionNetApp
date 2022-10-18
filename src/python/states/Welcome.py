import tkinter
from tkinter import *
from tkinter import ttk, font

from python.states.Dashboard import Dashboard


class Welcome:

    def __init__(self, root):
        self.root = root
        self.root.title("Immersion NetApp")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.mainframe = ttk.Frame(root, padding="10 10 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        title = ttk.Label(self.mainframe, text='Welcome to Immersion\'s NetApp!')
        title.configure(font=("TkDefaultFont", 20, "bold"))
        title.grid(column=1, row=0, columnspan=1)

        # s = ttk.Style()
        # s.configure('Major1.TButton', bg='#ff6600', fg='#ffffff', borderwidth=5)
        start_button = tkinter.Button(self.mainframe, text='Start', command=self.on_start_clicked,
                                      bg='#ff6600', fg='#ffffff', width=10, borderwidth=0)
        start_button['font'] = font.Font(size=16)
        start_button.grid(column=1, row=1)

        raw_img1 = PhotoImage(file="img/Immersion_Logo2022.png")
        self.img1 = raw_img1.subsample(7, 7)
        logo_imm = ttk.Label(self.mainframe, image=self.img1)
        # Important: save img into the widget to avoid the garbage collection
        # Forgetting to do so will prevent the img from appearing, giving you a headache (and a middle finger)
        logo_imm.image = self.img1
        logo_imm.grid(column=0, row=2)

        raw_img2 = PhotoImage(file="img/Ev5G_Logo.png")
        self.img2 = raw_img2.subsample(2, 2)
        logo_ev5g = ttk.Label(self.mainframe, image=self.img2)
        logo_ev5g.image = self.img2
        logo_ev5g.grid(column=2, row=2)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def on_start_clicked(self):
        Dashboard(self.root)
        self.mainframe.destroy()

