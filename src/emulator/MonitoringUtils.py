from network.msg.MsgUtils import AnswerForVApp


# Classes to be translated into Json messages about monitoring
class MonitoringRequest(object):

    def __init__(self, params):
        self.monitoring_params = params


class MonitoringParams(object):

    def __init__(self, num, must_start, frequency):
        self.num = num
        self.start = must_start
        self.frequency = frequency


class MonitoringTriggerAnswer(AnswerForVApp):

    def __init__(self, type_msg, num, status):
        super().__init__(type_msg, num, status)


