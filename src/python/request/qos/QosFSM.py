from statemachine import StateMachine, State

from python.request.qos.adaptations.ServiceAdaptations import ServiceAdaptation
from python.request.qos.adaptations.ServiceAdaptor import ServiceAdaptor


class QosFSM(StateMachine):

    STATE_NOT_STARTED = "Not_started"
    STATE_NORMAL = "Normal"
    STATE_LOCAL_NG = "Local_QoS_not_guaranteed"
    STATE_REMOTE_NG = "Remote_QoS_not_guaranteed"
    STATE_DEGRADED = "Degraded"
    STATE_ENDED = "Call_Ended"

    # All possible states
    not_started = State(STATE_NOT_STARTED, value=-1, initial=True)
    normal = State(STATE_NORMAL, value=0)
    local_not_guaranteed = State(STATE_LOCAL_NG, value=1)
    remote_not_guaranteed = State(STATE_REMOTE_NG, value=2)
    degraded = State(STATE_DEGRADED, value=3)
    call_ended = State(STATE_ENDED, value=4, final=True)

    # All valid transitions between states
    start_call = not_started.to(normal)
    local_qos_degradation = normal.to(local_not_guaranteed) | degraded.to(local_not_guaranteed) | \
                            remote_not_guaranteed.to(local_not_guaranteed)
    remote_qos_degradation = normal.to(remote_not_guaranteed) | degraded.to(remote_not_guaranteed) | \
                            local_not_guaranteed.to(remote_not_guaranteed)
    both_sides_degradation = local_not_guaranteed.to(degraded) | remote_not_guaranteed.to(degraded) | \
                             normal.to(degraded)
    back_to_normal = local_not_guaranteed.to(normal) | remote_not_guaranteed.to(normal) | degraded.to(normal)
    # The call can be ended from any state other than NotStarted
    end_call = normal.to(call_ended) | local_not_guaranteed.to(call_ended) | remote_not_guaranteed.to(call_ended) \
               | degraded.to(call_ended)

    # Other self attributes required for adaptations. The state-machine lib is a bit weird on that,
    # so use a trick with an Observer instead of classical constructor attributes
    service_adaptor = ServiceAdaptor()
    adaptation = ServiceAdaptation()

    def __init__(self):
        super().__init__()

    def on_enter_state(self, event, state):
        print("Entering into state ", {state}, " after event ", {event})

    # When receiving a qos update for a monitored UE, call me to trigger global Qos state change
    # and notify the vApp
    def on_ue_qos_update(self, monitored_ues):
        degraded_ue_nb = 0
        nb_local_users = 0
        nb_remote_users = 0

        # print(monitored_ues, flush=True)

        # Count the number of ues with degraded QoS
        for ue in monitored_ues.values():
            if not ue.qos_guaranteed:
                degraded_ue_nb += 1
                if ue.is_local_user:
                    nb_local_users += 1
                else:
                    nb_remote_users += 1

        # No UE found? => Normal QoS
        if degraded_ue_nb == 0:
            # Safeguard: cannot enter into normal state if we were already in it
            if "normal" not in self.current_state.id:
                self.back_to_normal()

        # At least one local or remote UE has degraded oS
        elif degraded_ue_nb == 1:
            if nb_local_users > 0:
                if "local" not in self.current_state.id:
                    self.local_qos_degradation()
            elif "remote" not in self.current_state.id:
                self.remote_qos_degradation()

        # Both local and remote UEs have degraded QoS => enter Degraded state
        elif "degraded" not in self.current_state.id:
            self.both_sides_degradation()

