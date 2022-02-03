from emulator import Emulator_Utils
from request.general.EndPointGenerator import EndPointGenerator
from request.location.LocationRequests import LocationRequester
from request.qos.QoSRequests import QoSRequester


class Core5GRequester:

    def __init__(self, vapp_manager, app):
        self.vAppManager = vapp_manager
        self.endpointGenerator = EndPointGenerator(app)
        self.token = None
        self.locationRequester = None
        self.qosRequester = None

    def start_comm_with_emulator(self):
        self.token = Emulator_Utils.get_token()
        self.locationRequester = LocationRequester(self.endpointGenerator, self.token)
        self.qosRequester = QoSRequester(self.endpointGenerator, self.token)

    def track_ue_location(self):
        self.locationRequester.track_ue_position()

    def start_gbr_monitoring(self, ue_ipv4):
        self.qosRequester.read_and_delete_all_existing_subscriptions()
        self.qosRequester.create_gbr_subscription(ue_ipv4)

