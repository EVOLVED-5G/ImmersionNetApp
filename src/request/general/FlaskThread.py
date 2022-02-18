import threading
from queue import Queue
import jsonpickle
from flask import Flask, request, jsonify
from request.endpoint.EndPointGenerator import EndPointGenerator

FLASK_SERVER_PORT = 9999


def on_post_general_notif():
    notif_json = request.json
    print('POST request received: ' + jsonpickle.dumps(notif_json))
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


class FlaskThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self.queue = Queue()
        self.must_stop = False
        self.app = Flask(__name__)
        self.endpointGenerator = EndPointGenerator()

    def run(self):
        # Start the Flask server in a dedicated thread to avoid being blocked here
        threading.Thread(target=lambda: self.app.run(host="localhost", port=FLASK_SERVER_PORT,
                                                     debug=False, use_reloader=False)).start()
        while not self.must_stop:
            # Blocking call, waiting until we are asked to create a route
            endpoint = self.queue.get(True)
            self.app.add_url_rule(endpoint.url_rule, methods=['POST'], view_func=endpoint.func)
            print("Adding rule for endpoint " + endpoint.complete_url)

    def add_endpoint(self, type_ep):
        ep = self.endpointGenerator.create_dynamic_endpoint(on_post_general_notif, type_ep)
        self.queue.put(ep)
        return ep.complete_url

    def polite_stop(self):
        self.must_stop = True
