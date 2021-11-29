import socket

from connection.HandleClientThread import HandleClientThread
from connection.PoliteThread import PoliteThread


# ServerThread class: accept connections from clients and handle each of them in a dedicated thread
class ServerThread(PoliteThread):

    mustRun = True
    # Run the NetApp locally. The HMD will be on the same local network and will be able to access to this machine.
    IPV4_ADDR = "127.0.0.1"
    VAPP_PORT = 9877

    def __init__(self, msg_dispatcher):
        super().__init__()
        self.msg_dispatcher = msg_dispatcher
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.numClient = 0
        self.client_handle = None
        # Accept any connection (but the client will target localhost for now)
        self.sock.bind(('', self.VAPP_PORT))

    def run(self):
        while self.mustRun:
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


