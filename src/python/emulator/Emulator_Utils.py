import os

from evolved5g import swagger_client
from evolved5g.swagger_client import LoginApi, Configuration, ApiClient
from evolved5g.swagger_client.models import Token

from python.utils import ConfigUtils


class EmulatorAccessToken:

    def __init__(self, token_str, token_type):
        self.str = token_str
        self.token_type = token_type


# MyConfig: class regrouping all nef/capif variables that we may need in several places
class MyConfig:
    def __init__(self):
        self.netapp_id = str(os.getenv('NETAPP_ID'))
        self.nef_url = "{}:{}".format(os.getenv('NEF_IP'), os.getenv('NEF_PORT'))
        self.nef_user = str(os.getenv('NEF_USER'))
        self.nef_pass = str(os.getenv('NEF_PASS'))
        self.callback_url = "{}:{}".format(os.getenv('CALLBACK_IP'), os.getenv('NETAPP_PORT_5G'))
        self.token = get_token_with_capif(self.nef_url, self.nef_user, self.nef_pass)
        self.capif_host = str(os.getenv('CAPIF_HOST'))
        self.capif_https_port = int(os.getenv('CAPIF_HTTPS_PORT'))
        self.path_to_certs = str(os.getenv('PATH_TO_CERTS'))


def get_token_with_capif(nef_url, nef_user, nef_pass):
    configuration = Configuration()
    configuration.host = nef_url
    api_client = ApiClient(configuration=configuration)
    api_client.select_header_content_type(["application/x-www-form-urlencoded"])
    api = LoginApi(api_client)
    token = api.login_access_token_api_v1_login_access_token_post("", nef_user, nef_pass, "", "", "")
    return token



