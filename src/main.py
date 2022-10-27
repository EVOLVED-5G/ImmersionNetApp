import os

from python.MainController import MainController

import argparse


def welcome():
    msg = "This is the IMM NetApp, version 2.2. This NetApp is built within the Evolved-5G european project."
    print(msg)
    # Read command line arguments, including the selected configuration
    args = read_command_line_args()

    # Print the chosen config, then set env variables if we run the NetApp locally for dev/debug purposes
    print("Using the " + args.config + " config")
    if args.config == "default":
        add_local_env_var()


# Call me only when working locally for dev/debug
def add_local_env_var():
    os.environ['NETAPP_NAME'] = "IMM_Netapp"
    os.environ['NETAPP_ID'] = "imm_netapp"
    os.environ['NETAPP_IP'] = "http://0.0.0.0:"
    os.environ['NETAPP_SERVER_VAPP'] = "127.0.0.1"
    os.environ['NETAPP_PORT_5G'] = "9999"
    os.environ['NETAPP_PORT_WEB'] = "9998"
    os.environ['NETAPP_PORT_VAPP'] = "9877"
    os.environ['NEF_HOST'] = "http://localhost:8888"
    os.environ['NEF_EMULATOR_LOCALHOST'] = "http://host.docker.internal:"


def read_command_line_args():
    parser = argparse.ArgumentParser(description='Immersion\'s NetApp')
    parser.add_argument("--config", help="Use either the default config (default, NetApp running on host)"
                                         "or the containerized config (container)", default="default")
    parser.add_argument("--host", help="Specify host, default is 0.0.0.0", default="0.0.0.0")
    return parser.parse_args()


if __name__ == '__main__':
    welcome()
    # Let the MainController handle the rest
    mainController = MainController()
    mainController.start()
    mainController.join()
