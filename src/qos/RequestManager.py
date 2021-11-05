import jsonpickle

from monitoring.MonitoringUtils import MonitoringTriggerAnswer
from msg.MsgUtils import AnswerForVApp
from msg.QoSMsg import QoSAnswer


# RequestManager
# A class handling requests from the VApp and messages from/to the 5G Core.
# It triggers the corresponding actions, like answering with dummy data or creating the corresponding 5G API calls
from qos.Core5GRequestManager import Core5GRequestManager


class RequestManager:
    TYPE_INIT_REQUEST = 0
    TYPE_START_MONITORING = 1

    def __init__(self, server):
        self.server = server
        self.core5GManager = Core5GRequestManager(self)

    # Handle a QoS request from the vApp
    def handle_qos_request(self, msg, type_id):
        if type_id == self.TYPE_INIT_REQUEST:
            asked_qos = msg.qos_params['initialQoSRequest']
            # For now, no 5G API call is triggered
            # Simply create a dummy answer and send it back to the vApp
            self.core5GManager.request_qos(asked_qos)
            # Dummy answer saying OK, includes either None or the asked QoS
            answer = QoSAnswer(type_id, asked_qos['numRequest'], AnswerForVApp.OK, asked_qos)
            # Translate it into json with the unpickable flag set to false to remove jsonpickle artifacts
            self.server.add_msg_to_send(jsonpickle.encode(answer, unpicklable=False))

    # Handle a monitoring request from the vApp
    def handle_monitoring_request(self, msg, type_id):
        if type_id == self.TYPE_START_MONITORING:
            content = msg.monitoring_params['toggleMonitoring']
            answer = MonitoringTriggerAnswer(type_id, content['numRequest'],  AnswerForVApp.OK)
            # Translate it into json with the unpickable flag set to false to remove jsonpickle artifacts
            self.server.add_msg_to_send(jsonpickle.encode(answer, unpicklable=False))

    def test_nef_emulator_calls(self):
        self.core5GManager.test_emulator_call()


