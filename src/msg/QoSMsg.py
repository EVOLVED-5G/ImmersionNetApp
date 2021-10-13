from enum import Enum


class QoSRequest(object):

    def __init__(self, params):
        self.qos_params = params


class QoSParams(object):

    def __init__(self, num, l_max, l_desired, bandwidth):
        self.num = num
        self.max_latency = l_max
        self.desired_latency = l_desired
        self.bandwidth = bandwidth


class QoSAnswer(object):

    def __init__(self, type_msg, num, status, proposed_qos):
        self.type = type_msg
        self.content = JsonAnswerContent(num, status, proposed_qos)


class JsonAnswerContent(object):
    ERROR = -1
    OK = 0
    MODIF = 1

    def __init__(self, num, status, proposed_qos):
        self.numAnswer = num
        self.status = status
        self.proposedQos = proposed_qos

