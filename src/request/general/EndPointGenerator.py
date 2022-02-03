
import jsonpickle
from flask import request, jsonify


def on_post_general_notif():
    notif_json = request.json
    print('POST request received: ' + jsonpickle.dumps(notif_json))
    # Make sure we return a json acknowledgment
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


class EndPointGenerator:
    def __init__(self, app):
        self.flask_app = app

    def create_ue_location_endpoint(self):
        self.flask_app.add_url_rule("/monitoring/location", methods=['POST'], view_func=on_post_general_notif)
        return 'http://host.docker.internal:9999/monitoring/location'

    def create_gbr_monitoring_endpoint(self):
        self.flask_app.add_url_rule("/monitoring/gbr", methods=['POST'], view_func=on_post_general_notif)
        return 'http://host.docker.internal:9999/monitoring/gbr'



