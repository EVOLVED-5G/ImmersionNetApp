import os
import threading
from queue import Queue
import jsonpickle
from flask import Flask, request, jsonify

from python.network.msg import MsgUtils
from python.request.endpoint.EndPointGenerator import EndPointGenerator
from python.request.endpoint.EndpointUtils import EndpointType
from python.request.location.LocationUtils import LocationVal, LocationNotif
from python.request.qos.QosUtils import QosVal, QosNotif


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
        # Change the path to both the templates and the static folders
        self.app = Flask(__name__, template_folder="../../../web/templates", static_folder='../../../web/static')
        self.request_handler = request_handler
        self.port = None
        self.endpointGenerator = None

    def run(self):
        self.port = int(os.getenv('NETAPP_PORT_5G'))
        self.endpointGenerator = EndPointGenerator(self.port)

        # Start the Flask server in a dedicated thread to avoid being blocked here
        # Note: use "0.0.0.0" as host to make sure this Flask server will be reachable for the NEF emulator
        threading.Thread(target=lambda: self.app.run(host="0.0.0.0", port=self.port,
                                                     debug=False, use_reloader=False)).start()

        while not self.must_stop:
            # Blocking call, waiting until we are asked to create a route
            endpoint = self.queue.get(True)
            self.app.add_url_rule(endpoint.url_rule, methods=endpoint.methods, view_func=endpoint.func)

    # Call this to dynamically create an endpoint of the given type (+the corresponding rule for the flask server)
    # This method should return the complete endpoint url
    def add_5gcore_endpoint(self, type_ep):
        if type_ep == EndpointType.UE_LOCATION:
            func = self.on_post_location_notif
        elif type_ep == EndpointType.UE_GBR:
            func = self.on_post_qos_notif
        else:
            func = on_post_general_notif
        ep = self.endpointGenerator.create_5gcore_endpoint(func, type_ep)
        self.queue.put(ep)
        print("Will add rule for created 5GCore endpoint " + ep.complete_url)
        return ep.complete_url

    def on_post_location_notif(self):
        notif_json = request.json
        print('Location POST received: ' + jsonpickle.dumps(notif_json))
        # Extract data from the json msg
        loc_info = notif_json['locationInfo']
        loc_val = LocationVal(notif_json['ipv4Addr'], loc_info['cellId'], loc_info['enodeBId'])
        # Let the handler update our monitored UEs and notify the vApp
        self.request_handler.post_loc_received(loc_val)

        resp = jsonify(success=True)
        resp.status_code = 200
        return resp

    def on_post_qos_notif(self):
        notif_json = request.json
        print('QoS POST received: ' + jsonpickle.dumps(notif_json))
        # Extract data from the json msg and use it to send a notification to the vApp
        report_info = notif_json['eventReports']
        qos_val = QosVal(notif_json['ipv4Addr'], report_info[0]['event'])
        self.request_handler.notify_vapp(QosNotif(MsgUtils.MsgType.NOTIF, MsgUtils.ContentType.TYPE_LOCATION_NOTIF,
                                                  MsgUtils.AnswerStatus.OK, qos_val))
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp

    def polite_stop(self):
        self.must_stop = True
