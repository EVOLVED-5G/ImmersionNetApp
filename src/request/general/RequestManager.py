import jsonpickle

from emulator.MonitoringUtils import MonitoringTriggerAnswer
from network.msg import MsgUtils
from network.msg.QoSMsg import QosMsg
from request.general.Core5GRequester import Core5GRequester


# RequestManager
# A class handling requests from the VApp and messages from/to the 5G Core.
# It triggers the corresponding actions, like answering with dummy data or creating the corresponding 5G API calls
from request.general.FlaskThread import FlaskThread


class RequestManager:

    def __init__(self, server):
        self.server = server
        self.flask_thread = FlaskThread(self)
        self.core5GManager = Core5GRequester(self, self.flask_thread)

    # Handle a QoS request from the vApp
    def handle_vapp_qos_request(self, msg, content_type):
        if content_type == MsgUtils.ContentType.TYPE_INIT_REQUEST:
            asked_qos = msg.qos_params['initialQoSRequest']
            # Simply create a dummy answer and send it back to the vApp
            answer = QosMsg(MsgUtils.MsgType.ANSWER, content_type, MsgUtils.AnswerStatus.OK, asked_qos)
            # Translate it into json with the unpickable flag set to false to remove jsonpickle artifacts
            self.server.add_msg_to_send(jsonpickle.encode(answer, unpicklable=False, make_refs=False))

    # Handle a monitoring request from the vApp
    def handle_vapp_monitoring_request(self, msg, content_type):
        if content_type == MsgUtils.ContentType.TYPE_START_MONITORING:
            # Extract monitoring parameters if required
            content = msg.monitoring_params['toggleMonitoring']
            # Start both UE location and QoS monitoring
            self.core5GManager.track_ue_location(id_ue=10001)
            self.core5GManager.track_ue_location(id_ue=10003)
            self.core5GManager.start_gbr_monitoring(ue_ipv4="10.0.0.1")
            # Inform the vApp that we accepted the monitoring request
            answer = MonitoringTriggerAnswer(MsgUtils.MsgType.ANSWER, content_type, MsgUtils.AnswerStatus.OK)
            self.server.add_msg_to_send(jsonpickle.encode(answer, unpicklable=False, make_refs=False))

    def start_communications(self):
        self.flask_thread.start()
        # Mandatory call to get access token and create APIRequester instances
        self.core5GManager.start_comm_with_emulator()
        self.core5GManager.clean_subscriptions()

    def test_nef_emulator_calls(self):
        # Optional calls to showcase the different APIs
        self.core5GManager.track_ue_location(id_ue=10001)
        self.core5GManager.start_gbr_monitoring(ue_ipv4="10.0.0.1")

    def notify_vapp(self, notif):
        self.server.add_msg_to_send(jsonpickle.encode(notif, unpicklable=False))








