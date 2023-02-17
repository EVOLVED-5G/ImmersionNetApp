

class QosFSMObserver(object):

    def __init__(self, fsm, req_manager):
        self.fsm = fsm
        self.req_manager = req_manager

    # Transitioning to a new QosState means that the global QoS of the system has changed
    # Thus, ask the RequestManager to notify the vApp
    def after_transition(self, event, source, target):
        print("Notifying the vApp after transition. Adaptations: ", self.fsm.adaptation.to_display_string())
        self.req_manager.on_global_qos_changed(self.fsm.adaptation)

