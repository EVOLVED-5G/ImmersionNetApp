import os

from python.request.endpoint.EndpointUtils import EndpointType
from python.utils import ConfigUtils

DEF_LOC_URL_PART = "/monitoring/loc"
DEF_QOS_URL_PART = "/monitoring/gbr"


# Class handling the creation of Endpoint objects
# In particular, it manages the corresponding urls depending on each endpoint type
class EndPointGenerator:

    def __init__(self, flask_port):
        self.endpoints = []
        self.num_location_ep = 0
        self.num_gbr_ep = 0
        self.flask_port = flask_port

    # Call me to create an endpoint dedicated to communication with 5G components (ex: the NEF emulator)
    def create_5gcore_endpoint(self, func, type_endpoint):
        if type_endpoint == EndpointType.UE_LOCATION:
            endpoint = CustomEndpoint(type_endpoint, DEF_LOC_URL_PART + str(self.num_location_ep),
                                      ['POST'], func, True)
            self.num_location_ep += 1

        elif type_endpoint == EndpointType.UE_GBR:
            endpoint = CustomEndpoint(type_endpoint, DEF_QOS_URL_PART + str(self.num_gbr_ep),
                                      ['POST'], func, True)
            self.num_gbr_ep += 1

        else:
            raise NameError('Unknown endpoint type id ' + str(type_endpoint))

        self.endpoints.append(endpoint)
        return endpoint

    def create_web_endpoint(self, url, func):
        endpoint = CustomEndpoint(EndpointType.WEB, url, ['GET'], func, False)
        self.endpoints.append(endpoint)
        return endpoint


class CustomEndpoint:

    # def __init__(self, type_ep, url_rule, methods, func, flask_port):
    #     self.type_ep = type_ep
    #     self.url_rule = url_rule
    #     self.methods = methods
    #     self.func = func
    #     # self.complete_url = str(os.getenv('CALLBACK_IP')) + ':' + str(flask_port) + self.url_rule
    #     self.complete_url = str(os.getenv('CALLBACK_IP')) + ':' + str(flask_port) + self.url_rule
    #     print("Endpoint addr:", self.complete_url)

    def __init__(self, type_ep, url_rule, methods, func, use_5g_port):
        self.type_ep = type_ep
        self.url_rule = url_rule
        self.methods = methods
        self.func = func

        # self.complete_url = str(os.getenv('CALLBACK_IP')) + ':' + str(flask_port) + self.url_rule
        if use_5g_port:
            self.complete_url = str(os.getenv('CALLBACK_ADDRESS')) + self.url_rule
            # self.complete_url = "http://imm-netapp:9999" + self.url_rule
        else:
            self.complete_url = str(os.getenv('FRONTEND_CALLBACK_ADDRESS')) + self.url_rule
            # self.complete_url = "http://imm-netapp:9988" + self.url_rule

        print("Endpoint addr:", self.complete_url)


