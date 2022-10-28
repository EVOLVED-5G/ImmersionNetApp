import jsonpickle
from python.emulator.MonitoringUtils import MonitoringTriggerAnswer
from python.network.msg import MsgUtils
from python.request.general.UEsController import UEsController
from python.request.qos.QoSMsg import QosMsg
from python.request.general.Core5GRequester import Core5GRequester
from python.request.general.FlaskThread import FlaskThread


# RequestManager
# A class handling requests from the VApp and messages from/to the 5G Core.
# It triggers the corresponding actions, like creating the corresponding 5G API calls
from python.request.web.FlashWebServer import FlaskWebServer


class RequestManager:

    def __init__(self, server, controller_queue):
        self.server = server
        self.controller_queue = controller_queue
        self.flask_thread = FlaskThread(self)
        self.core5GManager = Core5GRequester(self, self.flask_thread)
        self.ue_controller = UEsController(self)

        # Create and start immediately the web server to have access to the web GUI
        self.web_flask = FlaskWebServer(self)
        self.web_flask.start()

    def start_communications_request(self):
        from python.MainController import ControllerCMD
        self.controller_queue.put(ControllerCMD.START_COMM)

    def start_communications(self):
        self.flask_thread.start()
        # Mandatory call to get access token and create APIRequester instances
        self.core5GManager.start_comm_with_emulator()
        self.core5GManager.clean_subscriptions()
        # If needed for debug purposes, trigger a few loc and Qos subscriptions
        # self.test_nef_emulator_calls()

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
            self.core5GManager.track_ue_location(id_ue=10002)
            self.core5GManager.track_ue_location(id_ue=10004)
            self.core5GManager.start_gbr_monitoring(ue_ipv4="10.0.0.2")
            self.core5GManager.start_gbr_monitoring(ue_ipv4="10.0.0.4")
            # Inform the vApp that we accepted the monitoring request
            answer = MonitoringTriggerAnswer(MsgUtils.MsgType.ANSWER, content_type, MsgUtils.AnswerStatus.OK)
            self.server.add_msg_to_send(jsonpickle.encode(answer, unpicklable=False, make_refs=False))

    def test_nef_emulator_calls(self):
        # Optional calls to showcase the different APIs
        self.core5GManager.track_ue_location(id_ue=10002)
        self.core5GManager.start_gbr_monitoring(ue_ipv4="10.0.0.2")
        self.core5GManager.track_ue_location(id_ue=10004)
        self.core5GManager.start_gbr_monitoring(ue_ipv4="10.0.0.4")
        # Record the fact that we now monitor both UEs
        self.ue_controller.add_monitored_ue("10.0.0.2", True, True)
        self.ue_controller.add_monitored_ue("10.0.0.4", True, True)
        return self.ue_controller.get_monitored_ues()

    def notify_vapp(self, notif):
        self.server.add_msg_to_send(jsonpickle.encode(notif, unpicklable=False))

    def get_monitored_ues(self):
        return self.ue_controller.get_monitored_ues()

    def polite_stop_children(self):
        self.flask_thread.polite_stop()








