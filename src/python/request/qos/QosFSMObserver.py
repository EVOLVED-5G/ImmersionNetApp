from python.request.qos.GlobalQosUtils import GlobalQosVal
from python.request.qos.adaptations.ServiceAdaptations import ServiceAdaptation
from python.request.qos.adaptations.ServiceAdaptor import ServiceAdaptor


class QosFSMObserver(object):

    def __init__(self, fsm, req_manager):
        self.fsm = fsm
        self.req_manager = req_manager
        self.service_adaptor = ServiceAdaptor()
        self.last_adaptation = ServiceAdaptation()

    # Transitioning to a new QosState means that the global QoS of the system has changed
    # Thus, ask the RequestManager to notify the vApp
    def after_transition(self, event, source, target):
        # Get the appropriate adaptations for the new QoS
        match target.id:
            case "__initial__":
                print("Entering initial QoS state")

            case "not_started" | "normal":
                self.last_adaptation = self.service_adaptor.get_normal_qos_adaptations()

            case "local_not_guaranteed":
                self.last_adaptation = self.service_adaptor.get_local_user_degraded_adaptations()

            case "remote_not_guaranteed":
                self.last_adaptation = self.service_adaptor.get_remote_user_degraded_adaptations()

            case "degraded":
                self.last_adaptation = self.service_adaptor.get_degraded_qos_adaptations()

            case _:
                print("Cannot get QoS adaptations for state ", {target.id})

        # self.last_adaptation = ServiceAdaptation(mandatory=self.fsm.adaptation.mandatory,
        #                                          suggested=self.fsm.adaptation.suggested)

        global_qos_val = GlobalQosVal(self.fsm.current_state.value, self.last_adaptation)
        print("Notifying the vApp after transition. ", global_qos_val.to_display_string())
        self.req_manager.on_global_qos_changed(global_qos_val)

