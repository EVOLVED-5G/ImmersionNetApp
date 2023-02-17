import os
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
        self.serv_addr = None
        self.serv_port = None

    def run(self):
        server_url = os.getenv('SERVER_FOR_VAPP').split(':')
        self.serv_addr = server_url[0]
        self.serv_port = int(server_url[1])
        # self.serv_addr = os.getenv('NETAPP_SERVER_VAPP')
        # self.serv_port = int(os.getenv('NETAPP_PORT_VAPP'))
        self.sock.bind(('0.0.0.0', self.serv_port))
        print("Server for vApp URL: " + self.serv_addr + "; port: " + str(self.serv_port))

        # Wait for incoming connections
        while self.must_run:
            self.sock.listen()
            print("vApp server waiting for incoming client...", flush=True)
            client_socket = self.sock.accept()[0]
            self.client_handle = HandleClientThread(client_socket, self.msg_dispatcher)
            self.client_handle.start()
            print("Client_" + str(self.numClient) + " accepted and handheld in a dedicated thread")
            print(client_socket)
            print(client_socket.getpeername())
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


