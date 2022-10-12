import tkinter
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image


class Welcome:

    def __init__(self, root):
        root.title("Immersion NetApp")
        mainframe = ttk.Frame(root, padding="10 10 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        title = ttk.Label(mainframe, text='Welcome to Immersion\'s NetApp!')
        title.configure(font=("TkDefaultFont", 20, "bold"))
        title.grid(column=1, row=0, columnspan=3, sticky=N)

        s = ttk.Style()
        s.configure('Major1.TButton', bg='#ff6600', fg='#ffffff', borderwidth=5)
        start_button = tkinter.Button(mainframe, text='Start', command=None, bg='#ff6600', fg='#ffffff', width=30)
        start_button.grid(column=1, row=1, sticky=(N, W, E, S))

        self.img = PhotoImage(file="img/Logo1.png")
        logo_imm = ttk.Label(mainframe, image=self.img)
        # Important: save img into the widget to avoid the garbage collection
        # Forgetting to do so will prevent the img from appearing, giving you a headache (and a middle finger)
        logo_imm.image = self.img
        logo_imm.grid(column=1, row=2, sticky=(S, W))

        for child in mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)



