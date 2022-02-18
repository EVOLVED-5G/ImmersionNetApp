from emulator import Emulator_Utils


class APIRequester:
    NETAPP_ID = "myNetapp"

    def __init__(self, flask_th,  token):
        self.flask_thread = flask_th
        self.token = token
        self.host = Emulator_Utils.get_host_of_the_nef_emulator()

