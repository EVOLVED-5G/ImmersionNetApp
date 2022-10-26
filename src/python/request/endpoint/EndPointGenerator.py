import os

from python.request.endpoint.EndpointUtils import EndpointType
from python.utils import ConfigUtils


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
            endpoint = CustomEndpoint(type_endpoint, "/monitoring/loc" + str(self.num_location_ep),
                                      ['POST'], func, self.flask_port)
            self.num_location_ep += 1

        elif type_endpoint == EndpointType.UE_GBR:
            endpoint = CustomEndpoint(type_endpoint, "/monitoring/gbr" + str(self.num_gbr_ep),
                                      ['POST'], func, self.flask_port)
            self.num_gbr_ep += 1

        else:
            raise NameError('Unknown endpoint type id ' + str(type_endpoint))

        self.endpoints.append(endpoint)
        return endpoint

    def create_web_endpoint(self, url, func):
        endpoint = CustomEndpoint(EndpointType.WEB, url, ['GET'], func, self.flask_port)
        self.endpoints.append(endpoint)
        return endpoint


class CustomEndpoint:

    def __init__(self, type_ep, url_rule, methods, func, flask_port):
        self.type_ep = type_ep
        self.url_rule = url_rule
        self.methods = methods
        self.func = func
        # Read the config file to get the first part of the endpoint url
        self.complete_url = os.getenv('NEF_EMULATOR_LOCALHOST') + str(flask_port) + self.url_rule


