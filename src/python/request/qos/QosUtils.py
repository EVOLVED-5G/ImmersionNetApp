from python.network.msg.MsgUtils import AnswerForVApp


class QosNotif(AnswerForVApp):

    def __init__(self, type_msg, type_content, status, qos_data):
        super().__init__(type_msg, type_content, status)
        self.content = QosContent(qos_data)
        self.display_str = "QoS notif: " + self.content.to_display_string()


class QosContent:

    def __init__(self, qos_val):
        self.qos_data = qos_val

    def to_display_string(self):
        return self.qos_data.to_display_string()


class QosVal:

    def __init__(self, ue_id, is_qos_guaranteed):
        self.ue_id = ue_id
        if "NOT" in is_qos_guaranteed:
            self.is_qos_guaranteed = False
        else:
            self.is_qos_guaranteed = True

    def to_display_string(self):
        if self.is_qos_guaranteed:
            return "QOS guaranteed for UE " + str(self.ue_id)
        return "QOS can NOT be guaranteed for UE for now" + str(self.ue_id)


