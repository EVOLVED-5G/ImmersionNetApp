
from network.msg.MsgUtils import AnswerForVApp


class QoSAnswer(AnswerForVApp):

    def __init__(self, type_msg, num, status, proposed_qos):
        super().__init__(type_msg, num, status)
        self.content = JsonAnswerContent(proposed_qos)


class JsonAnswerContent(object):

    def __init__(self, proposed_qos):
        self.proposedQos = proposed_qos


class QoSRequest(object):

    def __init__(self, params):
        self.qos_params = params


class QoSParams(object):

    def __init__(self, num, l_max, l_desired, bandwidth):
        self.num = num
        self.max_latency = l_max
        self.desired_latency = l_desired
        self.bandwidth = bandwidth

