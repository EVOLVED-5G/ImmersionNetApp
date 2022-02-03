from evolved5g.sdk import LocationSubscriber
import datetime
from request.general.APIRequester import APIRequester


# Class dedicated to make requests to the 5G core about UE locations
# It relies on 1) the LocationSubscriber class from the SDK and 2) on the MonitoringEvent API
class LocationRequester(APIRequester):

    def __init__(self, endpoint_generator, access_token):
        super().__init__(endpoint_generator, access_token)
        self.location_subscriber = LocationSubscriber(self.host, self.token.access_token)

    # Create a subscription to be informed when the given UE moves to a new cell
    def track_ue_position(self, id_ue=10001, expire_delay=24):
        expire_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=expire_delay)).isoformat() + "Z"
        # To find external ids -> go to the online emulator map and click on a User icon
        external_id = str(id_ue) + "@domain.com"
        endpoint = self.endpoint_gen.create_ue_location_endpoint()

        subscription = self.location_subscriber.create_subscription(
            netapp_id=self.NETAPP_ID,
            external_id=external_id,
            notification_destination=endpoint,
            maximum_number_of_reports=1000,
            monitor_expire_time=expire_time
        )
        # From now on we should retrieve POST notifications to the endpoint
        print(subscription)

    def print_all_subscriptions(self):
        all_subscriptions = self.location_subscriber.get_all_subscriptions(self.NETAPP_ID, 0, 100)
        print(all_subscriptions)

    def print_subscription(self, subscription_id):
        subscription_info = self.location_subscriber.get_subscription(self.NETAPP_ID, subscription_id)
        print(subscription_info)