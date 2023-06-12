import jsonpickle
from python.emulator.MonitoringUtils import MonitoringTriggerAnswer
from python.network.msg import MsgUtils
from python.request.general.UEsController import UEsController
from python.request.location.LocationUtils import LocationNotif
from python.request.qos.GlobalQosUtils import GlobalQosNotif, GlobalQosContent
from python.request.qos.QoSPerfMsg import QosPerfMsg
from python.request.general.Core5GRequester import Core5GRequester
from python.request.general.FlaskThread import FlaskThread
import threading
import time

from python.request.qos.QosFSM import QosFSM
from python.request.qos.QosFSMObserver import QosFSMObserver
from python.request.qos.UEQosUtils import UEQosNotif
# RequestManager
# A class handling requests from the VApp and messages from/to the 5G Core.
# It triggers the corresponding actions, like creating the corresponding 5G API calls
from python.request.web.FlaskWebServer import FlaskWebServer
from python.utils.WebUtils import ActionResult


class RequestManager(object):

    def __init__(self, server, controller_queue):
        self.server = server
        self.controller_queue = controller_queue
        self.flask_thread = FlaskThread(self)
        self.core5GManager = Core5GRequester(self, self.flask_thread)
        self.ue_controller = UEsController(self)
        self.qos_fsm = QosFSM()
        self.fsm_observer = QosFSMObserver(self.qos_fsm, self)
        self.qos_fsm.add_observer(self.fsm_observer)

        # Create and start immediately the web server to have access to the web GUI
        self.web_flask = FlaskWebServer(self)
        self.web_flask.start()

    def start_communications_request(self):
        from python.MainController import ControllerCMD
        print("Receiving start communication request")
        self.controller_queue.put(ControllerCMD.START_COMM)

    def start_communications(self):
        # Consider that the call has started
        self.qos_fsm.start_call()
        print("Starting comms with emulator...")
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
            answer = QosPerfMsg(MsgUtils.MsgType.ANSWER, content_type, MsgUtils.AnswerStatus.OK, asked_qos)
            # Translate it into json with the unpickable flag as False to remove jsonpickle artifacts
            self.server.add_msg_to_send(jsonpickle.encode(answer, unpicklable=False, make_refs=False))

    # Handle a monitoring request from the vApp
    def handle_vapp_monitoring_request(self, msg, content_type):
        if content_type == MsgUtils.ContentType.TYPE_START_MONITORING:
            # Extract monitoring parameters if required
            content = msg.monitoring_params['toggleMonitoring']
            # Start both UE location and QoS monitoring
            res = self.test_nef_emulator_calls()
            # Inform the vApp that we accepted the monitoring request
            answer = MonitoringTriggerAnswer(MsgUtils.MsgType.ANSWER, content_type, MsgUtils.AnswerStatus.OK)
            self.server.add_msg_to_send(jsonpickle.encode(answer, unpicklable=False, make_refs=False))

    def test_nef_emulator_calls(self):
        # Optional calls to showcase the different APIs. Try to monitor two UEs.
        # Each time, check if the monitored UE already exists or not
        already_exist_1 = self.ue_controller.add_monitored_ue("10.0.0.2", True, True)
        if not already_exist_1:
            self.core5GManager.track_ue_location(id_ue=10002)
            self.core5GManager.start_gbr_monitoring(ue_ipv4="10.0.0.2")

        already_exist_2 = self.ue_controller.add_monitored_ue("10.0.0.4", True, True)
        if not already_exist_2:
            self.core5GManager.track_ue_location(id_ue=10004)
            self.core5GManager.start_gbr_monitoring(ue_ipv4="10.0.0.4")

        res_type = ActionResult.SUCCESS
        if already_exist_1 and already_exist_2:
            res_type = ActionResult.WARNING
        # UE were added, update the QoS fsm
        self.qos_fsm.on_ue_qos_update(self.ue_controller.monitored_ues)

        # Also ask for a TSN profile
        self.core5GManager.select_tsn_profile()

        # In the end, return the description of currently monitored UEs
        res = {"res_type": res_type, "ues": self.ue_controller.monitored_ues_to_string()}
        return res

    def add_or_update_ue_monitoring(self, ipv4, use_loc, use_qos):
        already_exist = self.ue_controller.add_monitored_ue(ipv4, use_loc, use_qos)
        res_type = ActionResult.SUCCESS

        if already_exist:
            res_type = ActionResult.WARNING
        else:
            if use_loc:
                self.core5GManager.track_ue_location(id_ue=ipv4.replace(".", ""))
            if use_qos:
                self.core5GManager.start_gbr_monitoring(ue_ipv4=ipv4)
        # At least one ue was added or updated, we must notify the QosFSM
        self.qos_fsm.on_ue_qos_update(self.ue_controller.monitored_ues)

        res = {"res_type": res_type, "ues": self.ue_controller.monitored_ues_to_string()}
        return res

    def post_loc_received(self, loc_info):
        # Update our monitored UEs list
        self.ue_controller.update_ue_loc(ipv4=loc_info.ue_id, use_loc=True, loc_info=loc_info)

        # Send a notification to the vApp
        self.notify_vapp(LocationNotif(MsgUtils.MsgType.INFO, MsgUtils.ContentType.TYPE_UE_LOCATION_NOTIF,
                                       MsgUtils.AnswerStatus.MODIF, loc_info))

    def post_qos_received(self, qos_info):
        self.ue_controller.update_ue_qos(ipv4=qos_info.ue_id, use_qos=True, qos_info=qos_info)
        # At least one ue was added or updated, we must notify the QosFSM
        self.qos_fsm.on_ue_qos_update(self.ue_controller.monitored_ues)
        # Then, notify the vApp
        self.notify_vapp(UEQosNotif(MsgUtils.MsgType.INFO, MsgUtils.ContentType.TYPE_UE_QOS_NOTIF,
                                    MsgUtils.AnswerStatus.MODIF, qos_info))

    def on_global_qos_changed(self, global_qos_data):
        self.notify_vapp(GlobalQosNotif(MsgUtils.MsgType.NOTIF, MsgUtils.ContentType.TYPE_GLOBAL_QOS_NOTIF,
                                    MsgUtils.AnswerStatus.MODIF, global_qos_data))

    def notify_vapp(self, notif):
        json_content = jsonpickle.encode(notif, unpicklable=False)
        print("Sending: " + json_content)
        self.server.add_msg_to_send(json_content)

    def get_monitored_ues_str(self):
        return self.ue_controller.monitored_ues_to_string()

    def get_monitored_ues(self):
        return self.ue_controller.monitored_ues

    def delete_all_subscriptions(self):
        self.core5GManager.clean_subscriptions()
        self.ue_controller.clean_all_ues()

    def polite_stop_children(self):
        self.flask_thread.polite_stop()








