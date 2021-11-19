import jsonpickle
import requests
from emulator.Emulator_API import EmulatorAccessToken


class Core5GRequestManager:

    def __init__(self, vapp_manager):
        self.vAppManager = vapp_manager
        self.accessToken = None

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
        req_header = {'Authorization': "Bearer {}".format(self.accessToken.str)}

        req_data = {'externalId': '10002@domain.com',
                    'notificationDestination': 'http://host.docker.internal:9999/api/v1/utils/monitoring/callback',
                    'monitoringType': 'LOCATION_REPORTING',
                    'maximumNumberOfReports': 1,
                    'monitorExpireTime': '2021-11-19T16:43:48.483Z'
                    }

        response = requests.post("http://localhost:8888/api/v1/3gpp-monitoring-event/v1/myNetapp/subscriptions",
                                 # Warning: the emulator expects a json object, so we must encapsulate the attributes
                                 # we could use json.dumps, but let's stick with jsonpickle for now
                                 headers=req_header, data=jsonpickle.encode(req_data, unpicklable=False))
        print(response.text)
