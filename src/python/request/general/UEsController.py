from enum import Enum


class UEsController:

    def __init__(self, request_manager):
        self.monitored_ues = {}
        self.request_manager = request_manager

    def add_monitored_ue(self, ipv4, use_loc, use_qos):
        # Update the dictionary of UEs (maj existing or add a new one)
        ue = MonitoredUE(ipv4, use_loc, use_qos, NetworkStatus.AS_REQUESTED)
        self.monitored_ues.update({ipv4: ue})

    def update_ue_loc(self, ipv4, use_loc):
        # Id it does not exist, add the UE
        if ipv4 not in self.monitored_ues:
            self.monitored_ues[ipv4] = MonitoredUE(ipv4, use_loc, False, NetworkStatus.AS_REQUESTED)
        # Else, update the corresponding params
        else:
            current = self.monitored_ues[ipv4]
            self.monitored_ues[ipv4] = MonitoredUE(ipv4, use_loc, current.use_qos, current.status)

    def update_ue_qos(self, ipv4, use_qos):
        # Id it does not exist, add the UE
        if ipv4 not in self.monitored_ues:
            self.monitored_ues[ipv4] =  MonitoredUE(ipv4, False, use_qos, NetworkStatus.AS_REQUESTED)
        # Else, update the corresponding params
        else:
            current = self.monitored_ues[ipv4]
            self.monitored_ues[ipv4] = MonitoredUE(ipv4, current.use_loc, use_qos, current.status)

    def update_ue_status(self, ipv4, status):
        # Id it does not exist, add the UE
        if ipv4 not in self.monitored_ues:
            self.monitored_ues[ipv4] = MonitoredUE(ipv4, False, False, NetworkStatus.AS_REQUESTED)
        # Else, update the corresponding params
        else:
            current = self.monitored_ues[ipv4]
            self.monitored_ues[ipv4] = MonitoredUE(ipv4, current.use_loc, current.use_qos, status)

    def get_monitored_ues(self):
        result = ""
        if not self.monitored_ues:
            return "No monitored UE for now."

        else:
            for ue in self.monitored_ues.values():
                result += ue.str_summary() + "\n"

        return result


class MonitoredUE:

    def __init__(self, ipv4, loc, qos, status):
        self.ipv4 = ipv4
        self.use_loc = loc
        self.use_qos = qos
        self.status = status

    def str_summary(self):
        res = "UE: " + self.ipv4 + "   "
        res += "Monitor_loc: " + str(self.use_loc) + "   "
        res += "Monitor_qos: " + str(self.use_qos) + "   "
        res += "Network status: " + str(self.status)
        return res


class NetworkStatus(Enum):
    AS_REQUESTED = 0
    CORRECT = 1
    DEGRADED = 2
    MINIMAL = 3
    FAILURE = 4

