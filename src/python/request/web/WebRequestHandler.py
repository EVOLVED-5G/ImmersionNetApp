from flask import render_template, request, jsonify


def home_page():
    return render_template('index.html')


def dashboard_page():
    return render_template('dashboard.html')


def debug_page():
    return render_template('debug.html')


def monitoring_session_page():
    return render_template('monitoringSession.html')


def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print('Ok')
    return jsonify(result=a + b)


def start_ue_monitoring():
    ue_num = request.args.get('ue_num', '1', type=int)
    ipv4 = request.args.get('ipv4', '10.0.0.1', type=str)
    monitor_loc = request.args.get('loc', 'true', type=bool)
    monitor_qos = request.args.get('qos', 'true', type=bool)
    print('Receiving a Web request to manually start monitoring UE', ue_num)
    return jsonify(result='Ok')


def stop_ue_monitoring():
    ue_num = request.args.get('ue_num', '1', type=int)
    print('Receiving a Web request to manually stop monitoring UE', ue_num)
    return jsonify(result='Done')


class WebRequestHandler:

    def __init__(self, flask_thread):
        self.flask = flask_thread

    def init_get_rules(self):
        # First, add the rules related to web pages
        self.flask.add_web_endpoint(url='/', func=home_page)
        self.flask.add_web_endpoint(url='/dashboard', func=dashboard_page)
        self.flask.add_web_endpoint(url='/debug', func=debug_page)
        self.flask.add_web_endpoint(url='/monitoringSession', func=monitoring_session_page)

        # Then, add rules related to function calls
        self.flask.add_web_endpoint(url='/_add_numbers', func=add_numbers)
        self.flask.add_web_endpoint(url='/_start_ue_monitoring', func=start_ue_monitoring)
        self.flask.add_web_endpoint(url='/_stop_ue_monitoring', func=stop_ue_monitoring)


