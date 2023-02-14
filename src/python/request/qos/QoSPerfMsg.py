
from python.network.msg.MsgUtils import AnswerForVApp, AnswerStatus


class QosPerfMsg(AnswerForVApp):

    def __init__(self, type_msg, type_content, status, proposed_qos):
        super().__init__(type_msg, type_content, status)
        self.content = JsonAnswerContent(proposed_qos)
        self.display_str = self.to_display_string()

    def to_display_string(self):
        if self.status == AnswerStatus.OK:
            return "The NetApp accepted the QoS request"
        elif self.status == AnswerStatus.MODIF:
            return "The NetApp had to adapt the QoS request"
        return "The NetApp could not accept the QoS request"


class JsonAnswerContent(object):

    def __init__(self, proposed_qos):
        self.proposedQos = proposed_qos

    def to_string(self):
        return self.proposedQos.to_string()


class QoSRequest(object):

    def __init__(self, params):
        self.qos_params = params

    def to_string(self):
        return self.qos_params.to_string()


class QoSPerfParams(object):

    def __init__(self, l_max, l_desired, bandwidth):
        self.max_latency = l_max
        self.desired_latency = l_desired
        self.bandwidth = bandwidth

    def to_string(self):
        return "Max_latency: " + str(self.max_latency) + "ms, " + "Desired_latency: " + str(self.desired_latency) + \
               "ms, " + "Bandwidth: " + str(self.bandwidth) + "Mb/s"

