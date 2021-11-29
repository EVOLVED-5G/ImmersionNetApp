import flask
import jsonpickle
from flask import request, Flask, jsonify

from connection.ServerThread import ServerThread
from msg.MsgDispatcher import MsgDispatcher
from qos.RequestManager import RequestManager


def print_readme():
    msg = "This is the IMM NetApp, version 1.0. This NetApp is built within the Evolved-5G european project."
    print(msg)


app = Flask(__name__)


@app.route("/monitoring", methods=['POST'])
def test():
    notif_json = request.json
    print('POST request received: ' + jsonpickle.dumps(notif_json))
    # return flask.Response(status=200)
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    print_readme()

    # Initialize all components in the correct order
    msgDispatcher = MsgDispatcher()
    serverThread = ServerThread(msgDispatcher)
    request_manager = RequestManager(serverThread)
    msgDispatcher.set_request_handler(request_manager)

    # Start the threads
    msgDispatcher.start()
    serverThread.start()

    request_manager.test_nef_emulator_calls()

    app.run(host="localhost", port=9999, debug=False)



