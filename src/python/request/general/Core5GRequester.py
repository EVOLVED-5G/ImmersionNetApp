from python.emulator.Emulator_Utils import MyConfig
from python.request.location.LocationRequests import LocationRequester
from python.request.qos.QoSRequests import QoSRequester
from python.request.tsn.TsnRequester import TsnRequester


class Core5GRequester:

    def __init__(self, vapp_manager, flask_th):
        self.vAppManager = vapp_manager
        self.flask_thread = flask_th
        self.myconfig = None
        self.locationRequester = None
        self.qosRequester = None
        self.tsnRequester = None

    def start_comm_with_emulator(self):
        self.myconfig = MyConfig()
        self.locationRequester = LocationRequester(self.flask_thread, self.myconfig)
        self.qosRequester = QoSRequester(self.flask_thread, self.myconfig)
        self.tsnRequester = TsnRequester(self.flask_thread, self.myconfig)
        print("Loc Requester: ", self.locationRequester)
        print("QoS Requester: ", self.qosRequester)
        print("TSN Requester: ", self.tsnRequester)

    def track_ue_location(self, id_ue):
        if self.locationRequester is not None:
            self.locationRequester.monitor_subscription_capif(times=10, id_ue=id_ue)
        else:
            print("Cannot create loc subscription: LocationRequester is null. Please check Capif registration.")

    def start_gbr_monitoring(self, ue_ipv4):
        if self.qosRequester is not None:
            self.qosRequester.sessionqos_subscription_capif(ue_ipv4=ue_ipv4)
        else:
            print("Cannot create qos subscription: QoSRequester is null. Please check Capif registration.")

    def select_tsn_profile(self):
        # print('Commented for now')
        if self.tsnRequester is not None:
            # print("Commented")
            self.tsnRequester.display_profiles_and_adopt_last()
        else:
            print("Cannot select TSN profile: TsnRequester is null. Please check Capif registration.")

    def clean_subscriptions(self):
        self.locationRequester.delete_all_existing_subscriptions()
        self.qosRequester.delete_all_existing_subscriptions()
        self.tsnRequester.clear_current_profile()
        print("Cleaned all location, qos and tsn subscriptions/profiles")

