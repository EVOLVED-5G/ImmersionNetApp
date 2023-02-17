from enum import Enum
from queue import Queue

from python.network.msg.MsgDispatcher import MsgDispatcher
from python.network.threads.PoliteThread import PoliteThread
from python.network.threads.ServerThread import ServerThread
from python.request.general.RequestManager import RequestManager


class ControllerCMD(Enum):
    START_COMM = 0


class MainController(PoliteThread):

    def __init__(self):
        super().__init__()
        self.queue = Queue()

        # Initialize all components in the correct order
        self.msgDispatcher = MsgDispatcher()
        self.serverThread = ServerThread(self.msgDispatcher)
        self.request_manager = RequestManager(self.serverThread, self.queue)
        self.msgDispatcher.prepare_handlers(self.request_manager)

    def run(self):
        # Wait for incoming connections
        while self.must_run:
            # Blocking call, waiting for a command from a child object or sub-thread
            msg = self.queue.get(True)
            if msg == ControllerCMD.START_COMM:
                self.start_session()

        # At the end, stop gracefully all our threads
        self.msgDispatcher.polite_stop()
        self.serverThread.polite_stop()
        self.request_manager.polite_stop_children()

    def start_session(self):
        print("Starting session...")
        self.msgDispatcher.start()
        self.serverThread.start()
        self.request_manager.start_communications()

