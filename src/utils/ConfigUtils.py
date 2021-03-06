import jsonpickle


def read_config():
    with open("./ConfigChoice.txt") as f:
        chosen_config = f.read()

    if chosen_config == "container":
        config_file = "./ContainerConfig.json"
    else:
        config_file = "./DefaultConfig.json"

    with open(config_file) as f:
        jconfig = jsonpickle.decode(f.read())
        return BaseNetappConfig(jconfig)


class BaseNetappConfig(object):
    def __init__(self, data):
        self.serverForVApp = VAPPServerConfig(data['serverForVApp'])
        self.flask = FlaskParams(data['flask'])
        self.emulator = EmulatorParams(data['emulator'])
        self.netapp = NetappParams(data['netapp'])


class VAPPServerConfig(object):
    def __init__(self, values):
        self.ipv4_addr = values['ipv4']
        self.port = values['port']


class FlaskParams(object):
    def __init__(self, values):
        self.port = values['port']


class EmulatorParams(object):
    def __init__(self, values):
        self.localhost = values['localhost']
        self.nef_host = values['nef_host']


class NetappParams(object):
    def __init__(self, values):
        self.id = values['id']
