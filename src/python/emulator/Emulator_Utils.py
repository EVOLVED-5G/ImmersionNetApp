import os

from evolved5g import swagger_client
from evolved5g.swagger_client import LoginApi, Configuration, ApiClient
from evolved5g.swagger_client.models import Token

from python.utils import ConfigUtils


class EmulatorAccessToken:

    def __init__(self, token_str, token_type):
        self.str = token_str
        self.token_type = token_type


class MyConfig:
    def __int__(self):
        self.token = get_token_with_capif()
        self.netapp_id = os.getenv('NETAPP_ID')
        self.nef_host = os.getenv('NEF_HOST')
        self.nef_url = "http://{}:{}".format(self.nef_host, os.getenv('NEF_PORT'))
        self.nef_user = os.getenv('NEF_USER')
        self.nef_pass = os.getenv('NEF_PASS')
        self.capif_host = os.getenv('CAPIF_HOST')
        self.capif_https_port = os.getenv('CAPIF_HTTPS_PORT')
        self.path_to_certs = os.getenv('PATH_TO_CERTS')


def get_token() -> Token:
    # Username and pass matches are set in the .env of the docker of NEF_EMULATOR. See
    # https://github.com/EVOLVED-5G/NEF_emulator
    username = os.getenv('NEF_USER')
    password = os.getenv('NEF_PASS')
    configuration = swagger_client.Configuration()
    # The host of the 5G API (emulator)
    configuration.host = get_host_of_the_nef_emulator()
    api_client = swagger_client.ApiClient(configuration=configuration)
    api_client.select_header_content_type(["application/x-www-form-urlencoded"])
    api = LoginApi(api_client)
    token = api.login_access_token_api_v1_login_access_token_post("", username, password, "", "", "")
    return token


def get_api_client(token) -> swagger_client.ApiClient:
    configuration = swagger_client.Configuration()
    configuration.host = get_host_of_the_nef_emulator()
    configuration.access_token = token.access_token
    api_client = swagger_client.ApiClient(configuration=configuration)
    return api_client


def get_token_with_capif() -> Token:
    nef_url = "http://{}:{}".format(os.getenv('NEF_HOST'), os.getenv('NEF_PORT'))
    nef_user = os.getenv('NEF_USER')
    nef_pass = os.getenv('NEF_PASS')

    configuration = Configuration()
    configuration.host = nef_url
    api_client = ApiClient(configuration=configuration)
    api_client.select_header_content_type(["application/x-www-form-urlencoded"])
    api = LoginApi(api_client)
    token = api.login_access_token_api_v1_login_access_token_post("", nef_user, nef_pass, "", "", "")
    return token


def get_host_of_the_nef_emulator() -> str:
    return os.getenv('NEF_HOST')

