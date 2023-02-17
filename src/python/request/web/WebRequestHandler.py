from flask import render_template, request, jsonify
from python.utils.ConfigUtils import ConfigReader
import time
import flask

from python.utils.WebUtils import ActionResult


def home_page():
    return render_template('index.html')


def dashboard_page():
    return render_template('dashboard.html')


def debug_page():
    return render_template('debug.html')


def config_choice_page():
    return render_template('configChoice.html')


def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print('Ok')
    return jsonify(result=a + b)


def get_message():
    time.sleep(1.0)
    s = time.ctime(time.time())
    return s


class WebRequestHandler:

    def __init__(self, flask_thread):
        self.flask = flask_thread
        self.config_reader = ConfigReader()

    def init_get_rules(self):
        # First, add the rules related to web pages
        self.flask.add_web_endpoint(url='/', func=home_page)
        self.flask.add_web_endpoint(url='/dashboard', func=dashboard_page)
        self.flask.add_web_endpoint(url='/debug', func=debug_page)
        self.flask.add_web_endpoint(url='/monitoringSession', func=self.monitoring_session_page)
        self.flask.add_web_endpoint(url='/configChoice', func=config_choice_page)

        # Then, add rules related to function calls
        self.flask.add_web_endpoint(url='/_add_numbers', func=add_numbers)
        self.flask.add_web_endpoint(url='/_start_ue_monitoring', func=self.start_ue_monitoring)
        self.flask.add_web_endpoint(url='/_stop_ue_monitoring', func=self.stop_ue_monitoring)
        self.flask.add_web_endpoint(url='/_selected_config_changed', func=self.on_selected_config_changed)
        self.flask.add_web_endpoint(url="/_get_monitored_ues", func=self.on_get_monitored_ues)
        self.flask.add_web_endpoint(url="/_add_test_ues", func=self.on_adding_test_ues)
        self.flask.add_web_endpoint(url="/stream", func=self.stream)
        self.flask.add_web_endpoint(url="/_clean_subs", func=self.delete_all_subscriptions)

    def monitoring_session_page(self):
        self.flask.start_session_requested()
        return render_template('monitoringSession.html')

    def on_selected_config_changed(self):
        # Get which item has been selected
        config_name = request.args.get('config_name', 'IMM local', type=str)
        filename = ""
        if config_name == "IMM_Dockerized":
            filename = "IMM_Dockerized.json"
        elif config_name == "Malaga":
            filename = "MalagaConfig.json"
        else:
            filename = "IMM_local.json"
        # Return the content of the corresponding config file
        return jsonify(result=self.config_reader.get_config_text(config_name))

    def on_get_monitored_ues(self):
        return jsonify(result=self.flask.get_monitored_ues_str())

    # Same than before, but return the raw string instead of building json from it
    def on_get_raw_monitored_ues(self):
        time.sleep(3.0)
        return self.flask.get_monitored_ues_str()

    def on_adding_test_ues(self):
        print("Adding test ues...")
        res = self.flask.add_test_ues()
        return jsonify(result_type=res["res_type"], ues=res["ues"])

    def start_ue_monitoring(self):
        ipv4 = request.args.get('ipv4', type=str)
        monitor_loc = request.args.get('loc', type=bool)
        monitor_qos = request.args.get('qos', type=bool)
        print('Receiving a Web request to manually start monitoring UE ', ipv4, " Monitoring_loc: ", monitor_loc)
        res = self.flask.add_or_update_ue_monitoring(ipv4, monitor_loc, monitor_qos)
        return jsonify(result_type=res["res_type"], ues=res["ues"])

    def stop_ue_monitoring(self):
        ue_num = request.args.get('ue_num', '1', type=int)
        print('Receiving a Web request to manually stop monitoring UE', ue_num)
        return jsonify(result='Done')

    def stream(self):
        def eventStream():
            while True:
                # wait for source data to be available, then push it
                report = 'data: {}\n\n'.format(self.on_get_raw_monitored_ues())
                yield report

        return flask.Response(eventStream(), mimetype="text/event-stream")

    def delete_all_subscriptions(self):
        self.flask.delete_all_subscriptions()
        res_type = ActionResult.SUCCESS
        return jsonify(result_type=res_type)

