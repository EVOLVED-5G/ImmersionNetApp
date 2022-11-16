from python.emulator import Emulator_Utils
from python.emulator.Emulator_Utils import MyConfig
from python.request.location.LocationRequests import LocationRequester
from python.request.qos.QoSRequests import QoSRequester


class Core5GRequester:

    def __init__(self, vapp_manager, flask_th):
        self.vAppManager = vapp_manager
        self.flask_thread = flask_th
        self.myconfig = None
        self.locationRequester = None
        self.qosRequester = None

    def start_comm_with_emulator(self):
        self.myconfig = MyConfig()
        self.locationRequester = LocationRequester(self.flask_thread, self.myconfig)
        self.qosRequester = QoSRequester(self.flask_thread, self.myconfig)

    def track_ue_location(self, id_ue):
        self.locationRequester.monitor_subscription_capif(id_ue)

    def start_gbr_monitoring(self, ue_ipv4):
        self.qosRequester.sessionqos_subscription_capif(ue_ipv4)

    def clean_subscriptions(self):
        self.locationRequester.delete_all_existing_subscriptions()
        self.qosRequester.delete_all_existing_subscriptions()
        print("Cleaned all location and qos subscriptions")

