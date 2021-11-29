import http
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from os.path import abspath
from sys import stderr
from threading import Thread, current_thread


def start_http_server(directory="."):
    hostname = "localhost"
    port = 9999
    directory = abspath(directory)
    handler = partial(_SimpleRequestHandler, directory=directory)
    handler.protocol_version = 'HTTP/1.1'
    httpd = http.server.HTTPServer((hostname, port), handler, False)
    # Block only for 0.5 seconds max
    httpd.timeout = 0.5
    # Allow for reusing the address
    httpd.allow_reuse_address = True

    _xprint("server about to bind to port %d on hostname '%s'" % (port, hostname))
    httpd.server_bind()

    address = "http://%s:%d" % (httpd.server_name, httpd.server_port)

    _xprint("server about to listen on:", address)
    httpd.server_activate()

    def serve_forever(httpd):
        with httpd:  # to make sure httpd.server_close is called
            _xprint("server about to serve files from directory (infinite request loop):", directory)
            httpd.serve_forever()
            _xprint("server left infinite request loop")

    thread = Thread(target=serve_forever, args=(httpd, ))
    thread.setDaemon(True)
    thread.start()

    return httpd, address


def _xprint(*args, **kwargs):
    """Wrapper function around print() that prepends the current thread name"""
    print("[", current_thread().name, "]",
          " ".join(map(str, args)), **kwargs, file=stderr)


class _SimpleRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Same as SimpleHTTPRequestHandler with adjusted logging."""

    def _set_response(self):
        self.send_header('Content-type', 'application/json')
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        """Log an arbitrary message and prepend the given thread name."""
        stderr.write("[ " + current_thread().name + " ] ")
        http.server.SimpleHTTPRequestHandler.log_message(self, format, *args)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print("Received notif from emulator: " + str(body))
        self._set_response()
