import tkinter
from tkinter import *
from tkinter import ttk, font


class Dashboard:

    def __init__(self, root):
        root.title("Immersion NetApp")
        self.mainframe = ttk.Frame(root, padding="10 10 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        title = ttk.Label(self.mainframe, text='Main dashboard')
        title.configure(font=("TkDefaultFont", 20, "bold"))
        title.grid(column=1, row=0, sticky=(N, S, E, W))

        width_major_button = 20
        width_minor_button = 16
        monitor_button = tkinter.Button(self.mainframe, text='\n\n\n\nMonitor the QoS of \na remote assistance',
                                        command=None, borderwidth=1, width=width_major_button, height=10)
        monitor_button['font'] = font.Font(size=16)
        monitor_button.grid(column=0, row=1, rowspan=4)
        monitor_button.lift()

        raw_img1 = PhotoImage(file="img/Icon_RemoteAssist.png")
        self.img1 = raw_img1.subsample(2, 2)
        icon_remote_assist = ttk.Label(self.mainframe, image=self.img1)
        icon_remote_assist.image = self.img1
        icon_remote_assist.grid(column=0, row=1, rowspan=3)

        quicktest_button = tkinter.Button(self.mainframe, text='Quick test', command=None,
                                          borderwidth=1, width=width_major_button)
        quicktest_button['font'] = font.Font(size=16)
        quicktest_button.grid(column=0, row=5)

        raw_img2 = PhotoImage(file="img/Icon_Questionmark.png")
        self.img2 = raw_img2.subsample(4, 4)
        icon_about = ttk.Label(self.mainframe, image=self.img2)
        icon_about.image = self.img2
        icon_about.grid(column=2, row=1, sticky=S)

        about1_button = tkinter.Button(self.mainframe, text='About 5G', command=None,
                                       borderwidth=1, width=width_minor_button)
        about1_button['font'] = font.Font(size=16)
        about1_button.grid(column=2, row=2)

        about2_button = tkinter.Button(self.mainframe, text='About this NetApp', command=None,
                                       borderwidth=1, width=width_minor_button)
        about2_button['font'] = font.Font(size=16)
        about2_button.grid(column=2, row=3)

        about3_button = tkinter.Button(self.mainframe, text='About Immersion', command=None,
                                       borderwidth=1, width=width_minor_button)
        about3_button['font'] = font.Font(size=16)
        about3_button.grid(column=2, row=4)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=20, pady=10)

    def on_monitoring_clicked(self):
        print('todo')

    def on_quick_test_clicked(self):
        print('todo')

    def on_about_5g_clicked(self):
        print('todo')

    def on_about_netapp_clicked(self):
        print('todo')

    def on_about_imm_clicked(self):
        print('todo')

