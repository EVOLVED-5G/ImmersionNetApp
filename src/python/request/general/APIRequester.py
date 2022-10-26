import os

from python.emulator import Emulator_Utils


class APIRequester:

    def __init__(self, flask_th,  token):
        self.flask_thread = flask_th
        self.token = token
        self.host = Emulator_Utils.get_host_of_the_nef_emulator()
        self.netapp_id = os.getenv('NETAPP_ID')


