from emulator import Emulator_Utils
from request.general import SDK_5GRequester
from request.general.EndPointGenerator import EndPointGenerator
from request.location import LocationRequests
from request.location.LocationRequests import LocationRequester


class Core5GRequester:

    def __init__(self, vapp_manager, app):
        self.vAppManager = vapp_manager
        self.endpointGenerator = EndPointGenerator(app)
        self.token = None
        self.locationRequester = None

    def start_comm_with_emulator(self):
        self.token = Emulator_Utils.get_token()
        self.locationRequester = LocationRequester(self.endpointGenerator, self.token)

    def track_ue_location(self):
        self.locationRequester.track_ue_position()

    def showcase_sdk_loc1(self):
        # SDK5GRequestManager.showcase_login_to_the_emulator_and_test_token()
        SDK_5GRequester.showcase_create_subscription_and_retrieve_call_backs(self.endpointGenerator)
