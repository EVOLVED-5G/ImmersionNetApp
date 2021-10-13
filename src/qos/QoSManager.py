import jsonpickle

from msg.QoSMsg import QoSAnswer, JsonAnswerContent


# QoSManager
# A class handling QoS messages and triggering the corresponding actions
class QoSManager:
    TYPE_INIT_REQUEST = 0

    def __init__(self, server):
        self.server = server

    def handle_qos_msg(self, msg, type_id):
        if type_id == self.TYPE_INIT_REQUEST:
            # For now, skip the 5G API calls
            # Simply create a dummy answer and send it back to the vApp
            asked_qos = msg.qos_params['initialQoSRequest']
            # Dummy answer saying OK, includes either None or the asked QoS
            answer = QoSAnswer(type_id, asked_qos['numRequest'], JsonAnswerContent.OK, asked_qos)
            # Translate it into json with the unpickable flag set to false to remove jsonpickle artifacts
            self.server.add_msg_to_send(jsonpickle.encode(answer, unpicklable=False))
