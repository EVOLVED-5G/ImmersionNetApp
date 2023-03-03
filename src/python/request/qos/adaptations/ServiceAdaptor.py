from python.request.qos.adaptations.ServiceAdaptations import ServiceAdaptation, AdaptationCode


class ServiceAdaptor:

    def __init__(self):
        self.last_adaptation = ServiceAdaptation()

    def get_normal_qos_adaptations(self):
        mandatory = {AdaptationCode.RESET_TO_NORMAL}
        suggested = {}
        self.last_adaptation = ServiceAdaptation(mandatory, suggested)
        return self.last_adaptation

    def get_local_user_degraded_adaptations(self):
        mandatory = {}
        suggested = {AdaptationCode.STOP_OBJECT_SYNCHRO}
        self.last_adaptation = ServiceAdaptation(mandatory, suggested)
        return self.last_adaptation

    def get_remote_user_degraded_adaptations(self):
        mandatory = {}
        suggested = {AdaptationCode.REDUCE_QUALITY_SENT_VIDEO}
        self.last_adaptation = ServiceAdaptation(mandatory, suggested)
        return self.last_adaptation

    def get_degraded_qos_adaptations(self):
        mandatory = {AdaptationCode.STOP_OBJECT_SYNCHRO, AdaptationCode.STOP_ALL_AR}
        suggested = {AdaptationCode.STOP_SENDING_VIDEO}
        self.last_adaptation = ServiceAdaptation(mandatory, suggested)
        return self.last_adaptation


