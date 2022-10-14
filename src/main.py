import tkinter

from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image

from network.threads.ServerThread import ServerThread
from network.msg.MsgDispatcher import MsgDispatcher
from request.general.RequestManager import RequestManager
import argparse


from states.Welcome import Welcome


def welcome():
    msg = "This is the IMM NetApp, version 2.1. This NetApp is built within the Evolved-5G european project."
    print(msg)
    args = read_command_line_args()
    print("Using the " + args.config + " config")
    with open("./ConfigChoice.txt", "w") as f:
        f.write(args.config)


def read_command_line_args():
    parser = argparse.ArgumentParser(description='Immersion\'s NetApp')
    parser.add_argument("--config", help="Use either the default config (default, NetApp running on host)"
                                         "or the containerized config (container)", default="default")
    parser.add_argument("--host", help="Specify host, default is 0.0.0.0", default="0.0.0.0")
    return parser.parse_args()


if __name__ == '__main__':
    welcome()

    # Start the Tkinter GUI
    root = Tk()
    style = ttk.Style(root)
    root.tk.call('source', 'theme/breeze-dark/breeze-dark.tcl')
    style.theme_use('breeze-dark')
    Welcome(root)
    root.mainloop()

    # Initialize all components in the correct order
    # msgDispatcher = MsgDispatcher()
    # serverThread = ServerThread(msgDispatcher)
    # request_manager = RequestManager(serverThread)
    # msgDispatcher.prepare_handlers(request_manager)
    #
    # # Start the threads and test calls
    # msgDispatcher.start()
    # serverThread.start()

    # request_manager.start_communications()
    # request_manager.test_nef_emulator_calls()



