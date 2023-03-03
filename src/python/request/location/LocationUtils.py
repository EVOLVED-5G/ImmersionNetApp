from python.network.msg.MsgUtils import AnswerForVApp


class LocationNotif(AnswerForVApp):

    def __init__(self, type_msg, type_content, status, location_data):
        super().__init__(type_msg, type_content, status)
        self.content = LocationContent(location_data)
        self.display_str = "Location notif: " + self.content.to_display_string()


class LocationContent:

    def __init__(self, loc_val):
        self.content_type = 1
        self.loc_data = loc_val

    def to_display_string(self):
        return self.loc_data.to_display_string()


class LocationVal:

    def __init__(self, ue_id, cell_id, enodeb_id):
        self.ue_id = ue_id
        self.cell_id = cell_id
        self.enodeb_id = enodeb_id

    def to_display_string(self):
        return "UE " + str(self.ue_id) + " moved to cell " + str(self.cell_id) + " in enodeB " + str(self.enodeb_id)

