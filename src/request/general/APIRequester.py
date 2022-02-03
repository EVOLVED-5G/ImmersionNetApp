

class APIRequester:
    NETAPP_ID = "myNetapp"

    def __init__(self, endpoint_generator,  token):
        self.endpoint_gen = endpoint_generator
        self.token = token

