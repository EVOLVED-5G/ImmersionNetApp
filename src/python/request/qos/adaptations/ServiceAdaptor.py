from python.request.qos.adaptations.ServiceAdaptations import ServiceAdaptation, AdaptationCode


class ServiceAdaptor:

    def __init__(self):
        self.last_adaptation = None

    def get_normal_qos_adaptations(self):
        mandatory = {AdaptationCode.RESET_TO_NORMAL}
        suggested = {}
        self.last_adaptation = ServiceAdaptation(mandatory, suggested)


