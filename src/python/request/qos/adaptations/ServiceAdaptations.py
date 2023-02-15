import enum


class ServiceAdaptation(object):
    def __init__(self, mandatory=None, suggested=None):
        self.mandatory = mandatory
        self.suggested = suggested


class AdaptationCode(enum.Enum):
    RESET_TO_NORMAL = 0

    # +-[10, 19]: audio
    STOP_SENDING_AUDIO = -10, START_SENDING_AUDIO = 10
    STOP_RECEIVING_AUDIO = -11, START_RECEIVING_AUDIO = 11,

    # +-[20, 29]: video
    STOP_SENDING_VIDEO = -20, START_SENDING_VIDEO = 20,
    STOP_RECEIVING_VIDEO = -21, START_RECEIVING_VIDEO = 21,
    REDUCE_QUALITY_SENT_VIDEO = -22, INCREASE_QUALITY_SENT_VIDEO = 22,

    # +-[30, 39]: AR features
    STOP_ALL_AR = -30, START_ALL_AR = 30,
    STOP_OBJECT_SYNCHRO = -31, START_OBJECT_SYNCHRO = 31

