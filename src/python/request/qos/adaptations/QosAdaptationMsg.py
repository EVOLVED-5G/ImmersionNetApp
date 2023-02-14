from python.network.msg.MsgUtils import AnswerForVApp, AnswerStatus


class QosAdaptationMsg(AnswerForVApp):

    def __init__(self, type_msg, type_content, status, content):
        super().__init__(type_msg, type_content, status)
        self.content = QosAdaptationContent(content)
        self.display_str = self.to_display_string()

    def to_display_string(self):
        return "QoS changed!"


class QosAdaptationContent(object):

    def __init__(self, data):
        self.data = data


class AdaptationData(object):

    def __init__(self, new_qos_id, adaptation_list):
        self.new_qos_id = new_qos_id
        self.list = adaptation_list

