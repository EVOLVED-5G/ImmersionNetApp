from emulator import Emulator_Utils


class APIRequester:
    NETAPP_ID = "myNetapp"

    def __init__(self, endpoint_generator,  token):
        self.endpoint_gen = endpoint_generator
        self.token = token
        self.host = Emulator_Utils.get_host_of_the_nef_emulator()

