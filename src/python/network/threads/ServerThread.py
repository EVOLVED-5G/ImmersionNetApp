import socket

from python.network.threads.HandleClientThread import HandleClientThread
from python.network.threads.PoliteThread import PoliteThread
from python.utils import ConfigUtils


# ServerThread class: accept connections from clients and handle each of them in a dedicated thread
# For now, run the NetApp locally. The HMD will be on the same local network and will be able to access to this machine.
class ServerThread(PoliteThread):

    def __init__(self, msg_dispatcher):
        super().__init__()
        self.msg_dispatcher = msg_dispatcher
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.numClient = 0
        self.client_handle = None
        # Read the config to know which ip and port to use for the server
        config = ConfigUtils.read_config()
        self.serv_addr = config.serverForVApp.ipv4_addr
        self.serv_port = config.serverForVApp.port
        self.sock.bind((self.serv_addr, self.serv_port))

    def run(self):
        while self.must_run:
            self.sock.listen()
            print("Server waiting for incoming client...")
            client_socket = self.sock.accept()[0]
            self.client_handle = HandleClientThread(client_socket, self.msg_dispatcher)
            self.client_handle.start()
            print("Client_" + str(self.numClient) + " accepted and handheld in a dedicated thread")
            self.numClient += 1

        # At the end, properly close my client handler
        if self.client_handle is not None:
            self.client_handle.polite_stop()

    def add_msg_to_send(self, msg):
        if self.client_handle is not None:
            self.client_handle.add_msg_to_send(msg)

    def polite_stop(self):
        super().polite_stop()
        self.client_handle.polite_stop()


