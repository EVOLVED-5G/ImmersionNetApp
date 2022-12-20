import os
from python.MainController import MainController
import argparse


def welcome():
    msg = "This is the IMM NetApp, version 3.0. This NetApp is built within the Evolved-5G european project."
    print(msg)
    # Read command line arguments, including the selected configuration
    args = read_command_line_args()

    # Print the chosen config, then set env variables if we run the NetApp locally for dev/debug purposes
    print("Using the " + args.config + " config")
    if args.config == "default":
        add_local_env_var()

    debug_env_vars()


def debug_env_vars():
    print("NetApp id: ", str(os.environ['NETAPP_ID']))
    print("Callback address: ", str(os.environ['CALLBACK_ADDRESS']))
    print("Frontend callback address: ", str(os.environ['FRONTEND_CALLBACK_ADDRESS']))
    print("Nef address: ", str(os.environ['NEF_ADDRESS']))
    print("Path to capif certificates: ", str(os.environ['PATH_TO_CERTS']))


# Call me only when working locally for dev/debug
def add_local_env_var():
    # Env variables related to NetApp and vApp
    os.environ['NETAPP_NAME'] = "IMM_Netapp"
    os.environ['NETAPP_ID'] = "imm_netapp"
    os.environ['NETAPP_IP'] = "http://0.0.0.0:"
    os.environ['NETAPP_SERVER_VAPP'] = "127.0.0.1"
    os.environ['NETAPP_PORT_5G'] = "9999"
    os.environ['NETAPP_PORT_WEB'] = "9998"
    os.environ['NETAPP_PORT_VAPP'] = "9877"
    os.environ['NEF_CALLBACK_URL'] = "http://host.docker.internal:"

    # Env variables related to NEF
    # os.environ['NEF_HOST'] = "http://localhost:8888"
    os.environ['NEF_IP'] = "http://localhost"
    os.environ['NEF_PORT'] = "8888"
    os.environ['NEF_USER'] = "admin@my-email.com"
    os.environ['NEF_PASS'] = "pass"

    # Env variables related to Capif
    os.environ['CAPIF_HOST'] = "172.18.0.1"
    os.environ['CAPIF_HTTP_PORT'] = "8080"
    os.environ['CAPIF_HTTPS_PORT'] = "443"

    # Note: now that Capif is integrated, you should probably not test locally anyway.
    # Use the container instead!
    os.environ['PATH_TO_CERTS'] = "D:\\Charles\\Code\\Evolved5G\\ImmersionNetApp\\src\\capif_onboarding"


def read_command_line_args():
    parser = argparse.ArgumentParser(description='Immersion\'s NetApp')
    parser.add_argument("--config", help="Use either the default config (default, NetApp running on host)"
                                         "or the containerized config (container)", default="container")
    parser.add_argument("--host", help="Specify host, default is 0.0.0.0", default="0.0.0.0")
    return parser.parse_args()


if __name__ == '__main__':
    welcome()
    # Let the MainController handle the rest
    mainController = MainController()
    mainController.start()
    mainController.join()
