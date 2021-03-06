
from network.threads.ServerThread import ServerThread
from network.msg.MsgDispatcher import MsgDispatcher
from request.general.RequestManager import RequestManager
import argparse


def welcome():
    msg = "This is the IMM NetApp, version 2.0. This NetApp is built within the Evolved-5G european project."
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

    # Initialize all components in the correct order
    msgDispatcher = MsgDispatcher()
    serverThread = ServerThread(msgDispatcher)
    request_manager = RequestManager(serverThread)
    msgDispatcher.prepare_handlers(request_manager)

    # Start the threads and test calls
    msgDispatcher.start()
    serverThread.start()

    request_manager.start_communications()
    # request_manager.test_nef_emulator_calls()



