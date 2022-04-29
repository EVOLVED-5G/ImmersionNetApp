from network.msg.MsgUtils import AnswerForVApp, AnswerStatus


# Classes to be translated into Json messages about monitoring
class MonitoringRequest(object):

    def __init__(self, params):
        self.monitoring_params = params

    def to_string(self):
        return self.monitoring_params.to_string()


class MonitoringParams(object):

    def __init__(self, num, must_start, frequency):
        self.num = num
        self.start = must_start
        self.frequency = frequency

    def to_string(self):
        return "Starting? " + str(self.start) + ", Report frequency: " + self.frequency + "ms"


class MonitoringTriggerAnswer(AnswerForVApp):

    def __init__(self, type_msg, type_content, status):
        super().__init__(type_msg, type_content, status)
        self.display_str = self.to_display_string()

    def to_display_string(self):
        if self.status == AnswerStatus.OK:
            return "The NetApp accepted the monitoring request"
        elif self.status == AnswerStatus.MODIF:
            return "The NetApp adapted the monitoring request"
        return "The NetApp could not accept the monitoring request"




