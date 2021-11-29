import queue

from connection.MsgSenderThread import MsgSenderThread
from connection.PoliteThread import PoliteThread


# A thread managing in&out messages with an accepted client
class HandleClientThread(PoliteThread):

    must_run = True
    SIZE_INT = 4
    MSG_QUEUE_LIMIT = 256

    def __init__(self, client_socket, msg_dispatcher):
        super().__init__()
        self.msg_dispatcher = msg_dispatcher
        self.clientSocket = client_socket
        # Create two synchronized queues: one for incoming msg and the other one for msg to be sent
        self.queue_in = queue.Queue(self.MSG_QUEUE_LIMIT)
        self.queue_out = queue.Queue(self.MSG_QUEUE_LIMIT)
        self.sender = None

    def run(self):
        # Dedicate the process of sending msg to another thread
        self.sender = MsgSenderThread(self.queue_out, self.clientSocket)
        self.sender.start()
        # self.add_msg_to_send("Hello from the NetApp")
        while self.must_run:
            # In this loop, only wait for incoming messages
            self.read_incoming_msg()
        self.sender.polite_stop()
        self.clientSocket.close()

    def read_incoming_msg(self):
        # Read the msg content size first
        msg_content_size = int.from_bytes(self.clientSocket.recv(self.SIZE_INT), "little")
        total_read = 0
        chunks = []
        msg = ""
        # Read until we get the whole msg content, progressively assembling chunks
        while total_read < msg_content_size:
            chunk = self.clientSocket.recv(msg_content_size - total_read)
            chunks.append(chunk)
            total_read = total_read + len(chunk)
            msg = msg + chunk.decode('utf-8')
        print("Received message: " + msg)
        # Give the msg to the dispatcher
        self.msg_dispatcher.add_msg(msg)

    def add_msg_to_send(self, msg):
        self.queue_out.put(msg)

    def polite_stop(self):
        super().polite_stop()
        self.sender.polite_stop()
        self.clientSocket.close()

