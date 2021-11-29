from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

import jsonpickle

from flask import request, jsonify


def on_post_location_notif():
    notif_json = request.json
    print('POST request received: ' + jsonpickle.dumps(notif_json))
    # return flask.Response(status=200)
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


class EndPointGenerator:
    def __init__(self, app):
        self.flask_app = app

    def start_ue_monitoring(self):
        self.flask_app.add_url_rule("/monitoring", methods=['POST'], view_func=on_post_location_notif)
        return 'http://host.docker.internal:9999/monitoring'





