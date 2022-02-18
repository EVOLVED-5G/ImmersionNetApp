import enum

from request.endpoint.EndpointUtils import EndpointType
from request.general import FlaskThread


class EndPointGenerator:

    def __init__(self):
        self.endpoints = []
        self.num_location_ep = 0
        self.num_gbr_ep = 0

    def create_dynamic_endpoint(self, func, type_endpoint):
        if type_endpoint == EndpointType.UE_LOCATION:
            endpoint = CustomEndpoint(type_endpoint, "/monitoring/loc" + str(self.num_location_ep), func)
            self.num_location_ep += 1

        elif type_endpoint == EndpointType.UE_GBR:
            endpoint = CustomEndpoint(type_endpoint, "/monitoring/gbr" + str(self.num_gbr_ep), func)
            self.num_gbr_ep += 1

        else:
            endpoint = None
            raise NameError('Unknown endpoint type id ' + str(type_endpoint))

        self.endpoints.append(endpoint)
        return endpoint

    def get_loc_endpoint(self):
        return self.endpoints[0]

    def get_gbr_endpoint(self):
        return self.endpoints[1]


class CustomEndpoint:

    LOCALHOST_FOR_DOCKER = "http://host.docker.internal:"

    def __init__(self, type_ep, url_rule, func):
        self.type_ep = type_ep
        self.url_rule = url_rule
        self.complete_url = self.LOCALHOST_FOR_DOCKER + str(FlaskThread.FLASK_SERVER_PORT) + self.url_rule
        self.func = func

