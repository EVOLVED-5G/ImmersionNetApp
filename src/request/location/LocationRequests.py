from evolved5g.sdk import LocationSubscriber
import datetime
from evolved5g.swagger_client.rest import ApiException

from request.endpoint.EndpointUtils import EndpointType
from request.general.APIRequester import APIRequester


# Class dedicated to make requests to the 5G core about UE locations
# It relies on 1) the LocationSubscriber class from the SDK and 2) on the MonitoringEvent API
class LocationRequester(APIRequester):

    def __init__(self, flask_th, access_token):
        super().__init__(flask_th, access_token)
        self.location_subscriber = LocationSubscriber(self.host, self.token.access_token)

    # Create a subscription to be informed when the given UE moves to a new cell
    def track_ue_position(self, id_ue=10001, expire_delay=24):
        expire_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=expire_delay)).isoformat() + "Z"
        # To find external ids -> go to the online emulator map and click on a User icon
        external_id = str(id_ue) + "@domain.com"
        # endpoint = self.endpoint_gen.create_ue_location_endpoint()
        subscription = self.location_subscriber.create_subscription(
            netapp_id=self.NETAPP_ID,
            external_id=external_id,
            # notification_destination=self.endpoint_gen.get_loc_endpoint().complete_url,
            notification_destination=self.flask_thread.add_endpoint(EndpointType.UE_LOCATION),
            maximum_number_of_reports=1000,
            monitor_expire_time=expire_time
        )
        # From now on we should retrieve POST notifications to the endpoint
        # print(subscription)

    def print_all_subscriptions(self):
        all_subscriptions = self.location_subscriber.get_all_subscriptions(self.NETAPP_ID, 0, 100)
        print(all_subscriptions)

    def print_subscription(self, subscription_id):
        subscription_info = self.location_subscriber.get_subscription(self.NETAPP_ID, subscription_id)
        print(subscription_info)

    def read_and_delete_all_existing_subscriptions(self):
        try:
            all_subscriptions = self.location_subscriber.get_all_subscriptions(self.NETAPP_ID)
            print(all_subscriptions)

            for subscription in all_subscriptions:
                id_sub = subscription.link.split("/")[-1]
                print("Deleting subscription with id: " + id_sub)
                self.location_subscriber.delete_subscription(self.NETAPP_ID, id_sub)
        except ApiException as ex:
            if ex.status == 404:
                print("No active transcriptions found")
            else: # something else happened, re-throw the exception
                raise

    def delete_all_existing_subscriptions(self):
        try:
            all_subscriptions = self.location_subscriber.get_all_subscriptions(self.NETAPP_ID)
            for subscription in all_subscriptions:
                id_sub = subscription.link.split("/")[-1]
                self.location_subscriber.delete_subscription(self.NETAPP_ID, id_sub)

        except ApiException as ex:
            if ex.status == 404:
                print("No active transcriptions found")
            else: # something else happened, re-throw the exception
                raise
