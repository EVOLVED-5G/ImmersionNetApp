import enum


class AnswerForVApp(object):

    def __init__(self, type_msg, type_content, status):
        self.type_msg = type_msg
        self.type_content = type_content
        self.status = status
        self.display_str = None


class MsgType(enum.Enum):
    INFO = 0
    ANSWER = 1
    NOTIF = 2


class ContentType(enum.Enum):
    TYPE_INIT_REQUEST = 0
    TYPE_START_MONITORING = 1
    TYPE_LOCATION_NOTIF = 2
    TYPE_QOS_NOTIF = 3


class AnswerStatus(enum.Enum):
    ERROR = -1
    OK = 0
    MODIF = 1