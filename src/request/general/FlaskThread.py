import threading
from queue import Queue
import jsonpickle
from flask import Flask, request, jsonify

from network.msg import MsgUtils
from request.endpoint.EndPointGenerator import EndPointGenerator
from request.endpoint.EndpointUtils import EndpointType
from request.location.LocationUtils import LocationVal, LocationNotif
from request.qos.QosUtils import QosVal, QosNotif
from utils import ConfigUtils
from utils.ConfigUtils import BaseNetappConfig


def on_post_general_notif():
    notif_json = request.json
    print('POST request received: ' + jsonpickle.dumps(notif_json))
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


# A dedicated class to 1) run the flask server in a dedicated thread and 2) create rules/endpoints at runtime
class FlaskThread(threading.Thread):

    def __init__(self, request_handler):
        super().__init__()
        self.queue = Queue()
        self.must_stop = False
        self.app = Flask(__name__)
        self.request_handler = request_handler
        config = ConfigUtils.read_config()
        self.port = config.flask.port
        self.endpointGenerator = EndPointGenerator(self.port)

    def run(self):
        # Start the Flask server in a dedicated thread to avoid being blocked here
        threading.Thread(target=lambda: self.app.run(host="localhost", port=self.port,
                                                     debug=False, use_reloader=False)).start()
        while not self.must_stop:
            # Blocking call, waiting until we are asked to create a route
            endpoint = self.queue.get(True)
            self.app.add_url_rule(endpoint.url_rule, methods=['POST'], view_func=endpoint.func)
            print("Adding rule for endpoint " + endpoint.complete_url)

    # Call this to dynamically create an endpoint of the given type (+the corresponding rule for the flask server)
    # This method should return the complete endpoint url
    def add_endpoint(self, type_ep):
        if type_ep == EndpointType.UE_LOCATION:
            func = self.on_post_location_notif
        elif type_ep == EndpointType.UE_GBR:
            func = self.on_post_qos_notif
        else:
            func = on_post_general_notif
        ep = self.endpointGenerator.create_dynamic_endpoint(func, type_ep)
        self.queue.put(ep)
        return ep.complete_url

    def on_post_location_notif(self):
        notif_json = request.json
        print('POST request received: ' + jsonpickle.dumps(notif_json))
        # Extract data from the json msg and use it to send a notification to the vApp
        loc_info = notif_json['locationInfo']
        loc_val = LocationVal(notif_json['ipv4Addr'], loc_info['cellId'], loc_info['enodeBId'])
        self.request_handler.notify_vapp(LocationNotif(MsgUtils.MsgType.NOTIF, MsgUtils.ContentType.TYPE_LOCATION_NOTIF,
                                                       MsgUtils.AnswerStatus.OK, loc_val))
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp

    def on_post_qos_notif(self):
        notif_json = request.json
        print('POST request received: ' + jsonpickle.dumps(notif_json))
        # Extract data from the json msg and use it to send a notification to the vApp
        report_info = notif_json['eventReports']
        loc_val = QosVal(notif_json['ipv4Addr'], report_info[0]['event'])
        self.request_handler.notify_vapp(QosNotif(MsgUtils.MsgType.NOTIF, MsgUtils.ContentType.TYPE_LOCATION_NOTIF,
                                                  MsgUtils.AnswerStatus.OK, loc_val))
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp

    def polite_stop(self):
        self.must_stop = True
