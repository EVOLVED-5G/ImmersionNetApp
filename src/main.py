
from flask import Flask

from connection.ServerThread import ServerThread
from msg.MsgDispatcher import MsgDispatcher
from qos.RequestManager import RequestManager


def print_readme():
    msg = "This is the IMM NetApp, version 1.0. This NetApp is built within the Evolved-5G european project."
    print(msg)


FLASK_SERVER_PORT = 9999
app = Flask(__name__)


if __name__ == '__main__':
    print_readme()

    # Initialize all components in the correct order
    msgDispatcher = MsgDispatcher()
    serverThread = ServerThread(msgDispatcher)
    request_manager = RequestManager(serverThread, app)
    msgDispatcher.set_request_handler(request_manager)

    # Start the threads and the flask server
    msgDispatcher.start()
    serverThread.start()

    request_manager.test_nef_emulator_calls()
    # Start the flask server last
    app.run(host="localhost", port=FLASK_SERVER_PORT, debug=False)




