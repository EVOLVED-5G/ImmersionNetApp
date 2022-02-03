import queue
import re

import jsonpickle

from network.threads.PoliteThread import PoliteThread
from emulator.MonitoringUtils import MonitoringRequest
from network.msg.QoSMsg import QoSRequest
from request.general.RequestManager import RequestManager


# MsgDispatcher
# Thread receiving the incoming msg from the network. It decodes and passes them to the corresponding handler
class MsgDispatcher(PoliteThread):

    MSG_QUEUE_LIMIT = 256
    INIT_QOS_REQ = "initialQoSRequest"
    TOGGLE_MONITORING = "toggleMonitoring"

    def __init__(self):
        super().__init__()
        self.queue_in = queue.Queue(self.MSG_QUEUE_LIMIT)
        self.qos_handler = None

    def run(self):
        while self.must_run:
            raw_msg = self.queue_in.get(True)
            decoded_msg = jsonpickle.decode(raw_msg)
            # Find the first json key, which should be the first word between "" symbols
            pattern = "\"(.*?)\""
            first_key = re.search(pattern, raw_msg).group(1)

            # According to the first msg key, create the corresponding msg instance and dispatch it
            if first_key is not None:
                if first_key == self.INIT_QOS_REQ:
                    qos_msg = QoSRequest(decoded_msg)
                    self.qos_handler.handle_vapp_qos_request(qos_msg, RequestManager.TYPE_INIT_REQUEST)

                if first_key == self.TOGGLE_MONITORING:
                    monitor_msg = MonitoringRequest(decoded_msg)
                    self.qos_handler.handle_vapp_monitoring_request(monitor_msg, RequestManager.TYPE_START_MONITORING)

    def add_msg(self, msg):
        self.queue_in.put(msg)

    def set_request_handler(self, qh):
        self.qos_handler = qh

