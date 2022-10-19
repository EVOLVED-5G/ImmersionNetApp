from flask import render_template, request, jsonify


def home_page():
    return render_template('index.html')


def dashboard_page():
    return render_template('Dashboard.html')


def debug_page():
    return render_template('debug.html')


def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print('Ok')
    return jsonify(result=a + b)


class WebRequestHandler:

    def __init__(self, flask_thread):
        self.flask = flask_thread

    def init_get_rules(self):
        self.flask.add_web_endpoint(url='/', func=home_page)
        self.flask.add_web_endpoint(url='/dashboard', func=dashboard_page)
        self.flask.add_web_endpoint(url='/debug', func=debug_page)
        self.flask.add_web_endpoint(url='/_add_numbers', func=add_numbers)


