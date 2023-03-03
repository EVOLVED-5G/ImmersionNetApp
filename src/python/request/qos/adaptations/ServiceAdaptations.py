import enum
import copy


class ServiceAdaptation(object):

    NO_ADAPTATION = "None"

    def __init__(self, mandatory_l=None, suggested_l=None):
        self.mandatory_list = mandatory_l
        # Construct the str from the list
        if mandatory_l is None:
            self.mandatory_str = self.NO_ADAPTATION
        elif len(mandatory_l) <= 0:
            self.mandatory_str = self.NO_ADAPTATION
        else:
            self.mandatory_str = ""
            for code in self.mandatory_list:
                self.mandatory_str += str(code) + ";"

        # Same for suggested adaptations
        self.suggested_list = suggested_l
        if suggested_l is None:
            self.suggested_str = self.NO_ADAPTATION
        elif len(suggested_l) <= 0:
            self.suggested_str = self.NO_ADAPTATION
        else:
            self.suggested_str = ""
            for code in self.suggested_list:
                self.suggested_str += str(code) + ";"

        print("Created new service adaptation: " + self.mandatory_str + " " + self.suggested_str)

    def to_display_string(self):
        res = ". Mandatory adaptations: "
        if len(self.mandatory_list) == 0:
            res += "None"
        else:
            for adapt in self.mandatory_list:
                res += str(adapt) + " "

        res += ". Suggested service adaptations: "
        if len(self.suggested_list) == 0:
            res += "None."
        else:
            for adapt in self.suggested_list:
                res += str(adapt) + " "

        return res

    # Exclude adaptation lists from json serialization
    def __getstate__(self):
        state = self.__dict__.copy()
        del state['mandatory_list']
        del state['suggested_list']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


class AdaptationCode(object):
    RESET_TO_NORMAL = 0

    # +-[10, 19]: audio
    STOP_SENDING_AUDIO = -10
    START_SENDING_AUDIO = 10
    STOP_RECEIVING_AUDIO = -11
    START_RECEIVING_AUDIO = 11

    # +-[20, 29]: video
    STOP_SENDING_VIDEO = -20
    START_SENDING_VIDEO = 20
    STOP_RECEIVING_VIDEO = -21
    START_RECEIVING_VIDEO = 21
    REDUCE_QUALITY_SENT_VIDEO = -22
    INCREASE_QUALITY_SENT_VIDEO = 22

    # +-[30, 39]: AR features
    STOP_ALL_AR = -30
    START_ALL_AR = 30
    STOP_OBJECT_SYNCHRO = -31
    START_OBJECT_SYNCHRO = 31

