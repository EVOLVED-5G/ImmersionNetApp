import jsonpickle
import requests
from emulator.Emulator_API import EmulatorAccessToken
from qos import SDK5GRequestManager
from qos.EndPointGenerator import EndPointGenerator
from datetime import datetime, timedelta


class Core5GRequestManager:

    def __init__(self, vapp_manager, app):
        self.vAppManager = vapp_manager
        self.accessToken = None
        self.endpointGenerator = EndPointGenerator(app)

    def request_qos(self, qos_params):
        # Create AsSessionWithQoS API call from the given QoS parameters
        print("5G Core API call not implemented yet")

    def ask_access_token(self):
        # Create the POST request to get an access token
        # Use the 'data' keyword of the requests module to provide id and password
        req_data = {'username': 'admin@my-email.com', 'password': 'pass'}
        response = requests.post('http://localhost:8888/api/v1/login/access-token', data=req_data)

        if response.status_code == 200:
            j_answer = response.json()
            self.accessToken = EmulatorAccessToken(j_answer['access_token'], j_answer['token_type'])
            print("Access token saved")
        else:
            print("Cannot obtain access token: " + response.text)

    def ask_cells(self):
        # We must be authenticated.
        # TODO: check if we could use a session instead
        #  (https://fr.python-requests.org/en/latest/user/advanced.html#objets-session)
        req_header = {'Authorization': "Bearer {}".format(self.accessToken.str)}
        req_params = {'skip': 0, 'limit': 5}
        req_data = {}
        response = requests.get('http://localhost:8888/api/v1/Cells/',
                                headers=req_header, params=req_params, data=req_data)
        print(response.text)

    def create_monitoring_subscription(self):
        # First, create the endpoint locally to be able to receive notifications from the emulator
        endpoint = self.endpointGenerator.start_ue_monitoring()

        req_header = {'Authorization': "Bearer {}".format(self.accessToken.str)}

        req_data = {'externalId': '10001@domain.com',
                    'notificationDestination': endpoint,
                    'monitoringType': 'LOCATION_REPORTING',
                    'maximumNumberOfReports': 100,
                    'monitorExpireTime': (datetime.today() + timedelta(hours=3)).isoformat()
                    }

        # Be careful, this now uses /nef in the path for Localization and QoS APIs
        # In case of "Subscription not found" msg, check this url on the online emulator to make sure it matches
        req_post_url = "http://localhost:8888/nef/api/v1/3gpp-monitoring-event/v1/myNetapp/subscriptions"
        response = requests.post(req_post_url,
                                 # Warning: the emulator expects a json object, so we must encapsulate the attributes
                                 # we could use json.dumps, but let's stick with jsonpickle for now
                                 headers=req_header, data=jsonpickle.encode(req_data, unpicklable=False))
        print(response.text)

    def delete_all_subscriptions(self):
        for i in range(60):
            self.delete_subscription(i)

    def delete_subscription(self, sub_id):
        req_header = {'Authorization': "Bearer {}".format(self.accessToken.str)}
        base_url = "http://localhost:8888/api/v1/3gpp-monitoring-event/v1/myNetapp/subscriptions/"

        response = requests.delete(base_url + str(sub_id), headers=req_header)
        print(response.text)

    def showcase_sdk_loc1(self):
        #SDK5GRequestManager.showcase_login_to_the_emulator_and_test_token()
        SDK5GRequestManager.showcase_create_subscription_and_retrieve_call_backs(self.endpointGenerator)
