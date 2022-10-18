from python.network.threads import HandleClientThread
from python.network.threads.PoliteThread import PoliteThread


# A basic thread watching the toBeSent msg queue and sending the corresponding msg 1 by 1
class MsgSenderThread(PoliteThread):

    def __init__(self, queue, socket):
        super().__init__()
        self.queue_out = queue
        self.sock = socket

    def run(self):
        # As long as we must run, take msg from the ToSend queue one by one (FIFO)
        while self.must_run:
            msg = self.queue_out.get()
            self.send_msg(msg)
            print("Sent msg: " + msg)
            self.queue_out.task_done()

    def send_msg(self, msg):
        total_send = 0
        msg_total_size = len(msg)
        # Send the msg size first: 4 bytes, little indian
        self.sock.send(msg_total_size.to_bytes(HandleClientThread.HandleClientThread.SIZE_INT, byteorder='little'))
        # Then, send the msg content
        while total_send < msg_total_size:
            # Encoding into UTF-8 should not be necessary with Python 3, but just to be sure
            sent = self.sock.send((msg[total_send:]).encode('utf-8'))
            if sent == 0:
                raise RuntimeError("Socket network broken, nothing could be sent.")
            total_send += sent


