
from connection.ServerThread import ServerThread
from msg.MsgDispatcher import MsgDispatcher
from qos.RequestManager import RequestManager


def print_readme():
    msg = "This is the IMM NetApp, version 1.0. This NetApp is built within the Evolved-5G european project."
    print(msg)


if __name__ == '__main__':
    print_readme()

    # Initialize all components in the correct order
    msgDispatcher = MsgDispatcher()
    serverThread = ServerThread(msgDispatcher)
    request_manager = RequestManager(serverThread)
    msgDispatcher.set_request_handler(request_manager)

    # Start the threads
    msgDispatcher.start()
    serverThread.start()

    request_manager.test_nef_emulator_calls()
