from python.MainController import MainController
from python.network.threads.ServerThread import ServerThread
from python.network.msg.MsgDispatcher import MsgDispatcher
from python.request.general.RequestManager import RequestManager
import argparse


def welcome():
    msg = "This is the IMM NetApp, version 2.1. This NetApp is built within the Evolved-5G european project."
    print(msg)
    # Read command line arguments, including the selected configuration
    args = read_command_line_args()
    # Write the chosen config into a text file to keep track of it
    print("Using the " + args.config + " config")
    with open("config/ConfigChoice.txt", "w") as f:
        f.write(args.config)


def read_command_line_args():
    parser = argparse.ArgumentParser(description='Immersion\'s NetApp')
    parser.add_argument("--config", help="Use either the default config (default, NetApp running on host)"
                                         "or the containerized config (container)", default="default")
    parser.add_argument("--host", help="Specify host, default is 0.0.0.0", default="0.0.0.0")
    return parser.parse_args()


if __name__ == '__main__':
    welcome()
    mainController = MainController()
    mainController.start()
    mainController.join()

    # Start the threads and test calls
    # msgDispatcher.start()
    # serverThread.start()

    # request_manager.start_communications()
    # request_manager.test_nef_emulator_calls()



