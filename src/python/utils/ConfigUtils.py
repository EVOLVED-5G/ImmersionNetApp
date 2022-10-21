import jsonpickle


def read_config():
    with open("./config/ConfigChoice.txt") as f:
        chosen_config = f.read()

    if chosen_config == "container":
        config_file = "./config/IMM_Dockerized.json"
    elif chosen_config == "malaga":
        config_file = "./config/Magala.json"
    else:
        config_file = "./config/IMM_local.json"

    with open(config_file) as f:
        jconfig = jsonpickle.decode(f.read())
        return BaseNetappConfig(jconfig)


class ConfigReader:

    def __init__(self):
        self.baseConfig = read_config()
        self.existing_configs = ["IMM_local", "IMM_Dockerized", "Malaga"]

    def get_config_text(self, filename):
        if filename not in self.existing_configs:
            raise NameError("Unknown config file ", filename)
        else:
            configfilepath = "./config/" + filename + ".json"
            with open(configfilepath) as f:
                return f.read()


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
        self.port_5G = values['5G_port']
        self.port_web = values['web_port']


class EmulatorParams(object):
    def __init__(self, values):
        self.localhost = values['localhost']
        self.nef_host = values['nef_host']


class NetappParams(object):
    def __init__(self, values):
        self.id = values['id']
