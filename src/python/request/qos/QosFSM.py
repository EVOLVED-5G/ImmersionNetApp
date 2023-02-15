from statemachine import StateMachine, State
from python.request.qos.adaptations.ServiceAdaptor import ServiceAdaptor


class QosFSM(StateMachine):

    STATE_NOT_STARTED = "Not_started"
    STATE_NORMAL = "Normal"
    STATE_LOCAL_NG = "Local_QoS_not_guaranteed"
    STATE_REMOTE_NG = "Remote_QoS_not_guaranteed"
    STATE_DEGRADED = "Degraded"
    STATE_ENDED = "Call_Ended"

    def __init__(self, req_manager):
        super().__init__()
        self.request_manager = req_manager
        self.service_adaptor = ServiceAdaptor()

    # All possible states
    not_started = State(STATE_NOT_STARTED, value=-1, initial=True)
    normal = State(STATE_NORMAL, value=0)
    local_not_guaranteed = State(STATE_LOCAL_NG, value=1)
    remote_not_guaranteed = State(STATE_REMOTE_NG, value=2)
    degraded = State(STATE_DEGRADED, value=3)
    call_ended = State(STATE_ENDED, value=4, final=True)

    # All valid transitions between states
    start_call = not_started.to(normal)
    local_qos_degradation = normal.to(local_not_guaranteed) | degraded.to(local_not_guaranteed)
    remote_qos_degradation = normal.to(remote_not_guaranteed) | degraded.to(remote_not_guaranteed)
    both_sides_degradation = local_not_guaranteed.to(degraded) | remote_not_guaranteed.to(degraded)
    back_to_normal = local_not_guaranteed.to(normal) | remote_not_guaranteed.to(normal) | degraded.to(normal)
    # The call can be ended from any state other than NotStarted
    end_call = normal.to(call_ended) | local_not_guaranteed.to(call_ended) | remote_not_guaranteed.to(call_ended) \
               | degraded.to(call_ended)

    def on_enter_state(self, event, state):
        print("Entering into state ", {state}, " after event ", {event})
        adaptation = None

        # Get the appropriate adaptations for the new QoS
        match state.id:
            case self.STATE_NOT_STARTED | self.STATE_NORMAL:
                adaptation = self.service_adaptor.get_normal_qos_adaptations()

            case self.STATE_LOCAL_NG:
                adaptation = self.service_adaptor.get_local_user_degraded_adaptations()

            case self.STATE_REMOTE_NG:
                adaptation = self.service_adaptor.get_remote_user_degraded_adaptations()

            case self.STATE_DEGRADED:
                adaptation = self.service_adaptor.get_degraded_qos_adaptations()

            case _:
                print("Cannot get QoS adaptations for state ", {state.id})

        # Ask the request manager to notify the vApp
        self.request_manager.on_global_qos_changed(adaptation)

    # When receiving a qos update for a monitored UE, call me to trigger global Qos state change
    # and notify the vApp
    def on_ue_qos_update(self, monitored_ues):
        degraded_ue_nb = 0
        nb_local_users = 0
        nb_remote_users = 0

        # Count the number of ues with degraded QoS
        for ue in monitored_ues:
            if not ue.qos_guaranteed:
                degraded_ue_nb += 1
                if ue.is_local_user:
                    nb_local_users += 1
                else:
                    nb_remote_users += 1

        # No UE found? => Normal QoS
        if degraded_ue_nb == 0 and "Normal" not in self.current_state.id:
            self.back_to_normal()

        # At least one local or remote UE has degraded oS
        elif degraded_ue_nb == 1:
            if nb_local_users > 0 and "Local" not in self.current_state.id:
                self.local_qos_degradation()
            elif "Remote" not in self.current_state.id:
                self.remote_qos_degradation()

        # Both local and remote UEs have degraded QoS => enter Degraded state
        elif "Degraded" not in self.current_state.id:
            self.both_sides_degradation()

