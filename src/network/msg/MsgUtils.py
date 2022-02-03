

class AnswerForVApp(object):

    ERROR = -1
    OK = 0
    MODIF = 1

    def __init__(self, type_msg, num, status):
        self.type = type_msg
        self.num = num
        self.status = status

