import queue
import jsonpickle

from connection.PoliteThread import PoliteThread
from msg.QoSMsg import QoSRequest
from qos import QoSManager


# MsgDispatcher
# Thread receiving the incoming msg from the network. It decodes and passes them to the corresponding handler
class MsgDispatcher(PoliteThread):

    MSG_QUEUE_LIMIT = 256

    def __init__(self):
        super().__init__()
        self.queue_in = queue.Queue(self.MSG_QUEUE_LIMIT)
        self.qos_handler = None

    def run(self):
        while self.must_run:
            raw_msg = self.queue_in.get(True)
            decoded_msg = jsonpickle.decode(raw_msg)

            if "initialQoSRequest" in decoded_msg:
                qos_msg = QoSRequest(decoded_msg)
                self.qos_handler.handle_qos_msg(qos_msg, QoSManager.QoSManager.TYPE_INIT_REQUEST)

    def add_msg(self, msg):
        self.queue_in.put(msg)

    def set_qos_handler(self, qh):
        self.qos_handler = qh
