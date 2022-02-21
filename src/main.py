import threading

from flask import Flask

from network.threads.ServerThread import ServerThread
from network.msg.MsgDispatcher import MsgDispatcher
from request.general.RequestManager import RequestManager


def print_readme():
    msg = "This is the IMM NetApp, version 2.0. This NetApp is built within the Evolved-5G european project."
    print(msg)


if __name__ == '__main__':
    print_readme()

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



