import os
import threading
from queue import Queue
import jsonpickle
from flask import Flask, request, jsonify, render_template

from python.network.msg import MsgUtils
from python.request.endpoint.EndPointGenerator import EndPointGenerator
from python.request.endpoint.EndpointUtils import EndpointType
from python.request.location.LocationUtils import LocationVal, LocationNotif
from python.request.qos.QosUtils import QosVal, QosNotif
from python.request.web.WebRequestHandler import WebRequestHandler
from python.utils import ConfigUtils


def on_post_general_notif():
    notif_json = request.json
    print('POST request received: ' + jsonpickle.dumps(notif_json))
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


# A class to run the flask web server in a dedicated thread
# It delegates the details of url_rules to a WebRequestHandler
class FlaskWebServer(threading.Thread):

    def __init__(self, request_handler):
        super().__init__()
        self.queue = Queue()
        self.must_stop = False
        # Change the path to both the templates and the static folders
        self.app = Flask(__name__, template_folder="../../../web/templates", static_folder='../../../web/static')
        self.request_handler = request_handler
        self.web_port = None
        self.endpointGenerator = None
        self.webHandler = None

    def run(self):
        self.web_port = int(os.getenv('NETAPP_PORT_WEB'))
        self.endpointGenerator = EndPointGenerator(self.web_port)
        self.webHandler = WebRequestHandler(self)

        # Start the Flask server in a dedicated thread to avoid being blocked here
        # Note: use "0.0.0.0" as host to make sure this Flask server will be reachable for the NEF emulator
        threading.Thread(target=lambda: self.app.run(host="0.0.0.0", port=self.web_port,
                                                     debug=False, use_reloader=False)).start()
        # Add basic rules for GET methods
        self.webHandler.init_get_rules()

        while not self.must_stop:
            # Blocking call, waiting until we are asked to create a route
            endpoint = self.queue.get(True)
            self.app.add_url_rule(endpoint.url_rule, methods=endpoint.methods, view_func=endpoint.func)

    def add_web_endpoint(self, url, func):
        ep = self.endpointGenerator.create_web_endpoint(url, func)
        self.queue.put(ep)

    def start_session_requested(self):
        self.request_handler.start_communications_request()

    def polite_stop(self):
        self.must_stop = True
