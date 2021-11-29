from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

from connection.ServerThread import NotificationServerThread
from monitoring.TestHttpServer import start_http_server
from flask import Flask, request


def add_endpoint():
    print('start')
    header = 'http://'
    ip = 'localhost'
    ip_for_emulator = 'host.docker.internal'
    port = 9999
    endpoint_addr = '/monitoring'
    server_url = header + ip + ':' + str(port) + endpoint_addr
    emulator_endpoint = header + ip + ':' + str(port) + endpoint_addr


class EndPointGenerator:
    def __init__(self):
        self.endpointList = []
        self.notif_server = NotificationServerThread()

    def add_server(self):
        start_http_server('monitoring')
        return 'http://host.docker.internal:9999/monitoring'

    def start_notif_server(self):
        self.notif_server.start()
        return 'http://host.docker.internal:9999/monitoring'

    def start_flask(self):
        return 'http://host.docker.internal:9999/monitoring'




