from evolved5g.sdk import TSNManager

from python.request.general.APIRequester import APIRequester


class TsnRequester(APIRequester):

    def __init__(self, flask_th, conf):
        super().__init__(flask_th, conf)
        # Initialization of the TNSManager
        self.tsn = TSNManager(
            folder_path_for_certificates_and_capif_api_key=self.myconfig.path_to_certs,
            capif_host=self.myconfig.capif_host,
            capif_https_port=self.myconfig.capif_https_port,
            https=False,
            tsn_host=self.myconfig.tsn_host,
            tsn_port=self.myconfig.tsn_port)
        self.current_tsn_identifier = None
        self.current_clearance_token = None

    def showcase_get_tsn_profiles(self):
        """
        Demonstrates how to retrieve information on all the available TSN profiles
        """
        profiles = self.tsn.get_tsn_profiles()
        print(f"Found {len(profiles)} profiles")
        for profile in profiles:
            profile_configuration = profile.get_configuration_for_tsn_profile()

            print(
                f"Profile {profile.name} with configuration parameters "
                f"{profile_configuration.get_profile_configuration_parameters()} "
            )

    def showcase_apply_tsn_profile_to_netapp(self):
        """
        Demonstrates how to apply a TSN profile configuration to a NetApp
        """
        profiles = self.tsn.get_tsn_profiles()
        # For demonstration purposes,  let's select the last profile to apply,
        profile_to_apply = profiles[-1]
        profile_configuration = profile_to_apply.get_configuration_for_tsn_profile()
        # Let's create an TSN identifier for this Net App.
        # This tsn_netapp_identifier can be used in two scenarios
        # a) When you want to apply a profile configuration for your net app
        # b) When you want to clear a profile configuration for your net app
        tsn_netapp_identifier = self.tsn.TSNNetappIdentifier(netapp_name=self.myconfig.netapp_id)

        print(
            f"Generated TSN traffic identifier for Netapp: {tsn_netapp_identifier.value}"
        )
        print(
            f"Apply {profile_to_apply.name} with configuration parameters"
            f"{profile_configuration.get_profile_configuration_parameters()} to NetApp {self.myconfig.netapp_id} "
        )
        clearance_token = self.tsn.apply_tsn_profile_to_netapp(
            profile=profile_to_apply, tsn_netapp_identifier=tsn_netapp_identifier
        )
        print(
            f"The profile configuration has been applied. The returned token {clearance_token} can be used "
            f"to reset the configuration"
        )
        self.current_tsn_identifier = tsn_netapp_identifier
        self.current_clearance_token = clearance_token
        return (tsn_netapp_identifier, clearance_token)

    def showcase_clear_profile_configuration_from_netapp(self, tsn_netapp_identifier: TSNManager.TSNNetappIdentifier,
                                                         clearance_token: str):
        """
        Demonstrates how to clear a previously applied TSN profile configuration from a NetApp
        """
        self.tsn.clear_profile_for_tsn_netapp_identifier(tsn_netapp_identifier, clearance_token)
        print(f"Cleared TSN configuration from {self.myconfig.netapp_id}")

    def showcase_apply_tsn_profile_with_overriden_parameters(self):
        """
        Demonstrates how to override the parameters of a TSN profile and apply it to a NetApp.
        """

        profiles = self.tsn.get_tsn_profiles()
        # For demonstration purposes,  let's select the first profile to apply,
        profile_to_apply = profiles[-1]
        profile_configuration = profile_to_apply.get_configuration_for_tsn_profile()
        profile_parameters = profile_configuration.get_profile_configuration_parameters()

        for parameter, value in profile_parameters.items():
            # For this example we retrieve the existing profile parameters
            # if this parameter is boolean, we just reverse it (so True parameters become False,
            # or False parameters become True)
            profile_parameters[parameter] = not value if isinstance(value, bool) else value

        tsn_netapp_identifier = self.tsn.TSNNetappIdentifier(netapp_name=self.myconfig.netapp_id)

        print(
            f"Generated TSN traffic identifier for Netapp: {tsn_netapp_identifier.value}"
        )
        print(
            f"Apply {profile_to_apply.name} with configuration parameters"
            f"{profile_configuration.get_profile_configuration_parameters()} to NetApp {self.myconfig.netapp_id} "
        )
        clearance_token = self.tsn.apply_tsn_profile_to_netapp(
            profile=profile_to_apply,
            tsn_netapp_identifier=tsn_netapp_identifier
        )
        print(
            f"The profile configuration has been applied. The returned token {clearance_token} can be used "
            f"to reset the configuration\n"
        )
        self.current_tsn_identifier = tsn_netapp_identifier
        self.current_clearance_token = clearance_token
        return (tsn_netapp_identifier, clearance_token)

    def display_profiles_and_adopt_last(self):
        self.showcase_get_tsn_profiles()
        self.showcase_apply_tsn_profile_to_netapp()

    def clear_current_profile(self):
        if self.current_tsn_identifier is not None and self.current_clearance_token is not None:
            self.showcase_clear_profile_configuration_from_netapp(
                self.current_tsn_identifier, self.current_clearance_token)

