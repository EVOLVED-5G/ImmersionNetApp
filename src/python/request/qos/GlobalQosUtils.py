from python.network.msg.MsgUtils import AnswerForVApp


# Classes about QoS changes for 1 single UE
class GlobalQosNotif(AnswerForVApp):

    def __init__(self, type_msg, type_content, status, qos_data):
        super().__init__(type_msg, type_content, status)
        self.content = GlobalQosContent(qos_data)
        self.display_str = "QoS notif: " + self.content.to_display_string()


class GlobalQosContent(object):

    def __init__(self, global_data):
        self.content_type = 2
        self.global_qos_data = global_data

    def to_display_string(self):
        return self.global_qos_data.to_display_string()


class GlobalQosVal(object):

    def __init__(self, status, adaptation):
        self.new_qos_status = status
        self.service_adaptation = adaptation

    def to_display_string(self):
        return "New QoS: " + str(self.new_qos_status) + self.service_adaptation.to_display_string()


