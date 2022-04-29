from emulator import Emulator_Utils
from utils import ConfigUtils


class APIRequester:

    def __init__(self, flask_th,  token):
        self.flask_thread = flask_th
        self.token = token
        self.host = Emulator_Utils.get_host_of_the_nef_emulator()
        config = ConfigUtils.read_config()
        self.netapp_id = config.netapp.id

