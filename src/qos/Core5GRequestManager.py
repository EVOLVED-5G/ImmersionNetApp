import requests


class Core5GRequestManager:

    def __init__(self, vapp_manager):
        self.vAppManager = vapp_manager

    def request_qos(self, qos_params):
        # Create AsSessionWithQoS API call from the given QoS parameters
        print("5G Core API call not implemented yet")

    def test_emulator_call(self):
        query = {'username': 'admin@my-email.com', 'password': 'pass'}
        response = requests.get('http://localhost:8888/api/v1/login/access-token', params=query)
        print(response)


