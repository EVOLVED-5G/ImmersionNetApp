
from connection.ServerThread import ServerThread
from msg.MsgDispatcher import MsgDispatcher
from qos.QoSManager import QoSManager


def print_readme():
    msg = "This is the IMM NetApp, version 1.0. This NetApp is built within the Evolved-5G european project."
    print(msg)


if __name__ == '__main__':
    print_readme()

    # Initialize all components in the correct order
    msgDispatcher = MsgDispatcher()
    serverThread = ServerThread(msgDispatcher)
    qoS_manager = QoSManager(serverThread)
    msgDispatcher.set_qos_handler(qoS_manager)

    # Start the threads
    msgDispatcher.start()
    serverThread.start()

