import os

from python.emulator import Emulator_Utils


class APIRequester:

    def __init__(self, flask_th, conf):
        self.flask_thread = flask_th
        self.myconfig = conf


