from evolved5g.sdk import LocationSubscriber
import datetime
from evolved5g.swagger_client.rest import ApiException
from python.request.endpoint.EndpointUtils import EndpointType
from python.request.general.APIRequester import APIRequester


# Class dedicated to make requests to the 5G core about UE locations
# It relies on 1) the LocationSubscriber class from the SDK and 2) on the MonitoringEvent API
class LocationRequester(APIRequester):

    def __init__(self, flask_th, conf):
        super().__init__(flask_th, conf)
        self.location_subscriber = LocationSubscriber(self.myconfig.nef_url, self.myconfig.token.access_token,
                                                      self.myconfig.path_to_certs,
                                                      self.myconfig.capif_host, self.myconfig.capif_https_port)

    # Create a subscription to be informed when the given UE moves to a new cell
    def monitor_subscription(self, id_ue=10001, expire_delay=24):
        expire_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=expire_delay)).isoformat() + "Z"
        # To find external ids -> go to the online emulator map and click on a User icon
        external_id = str(id_ue) + "@domain.com"
        subscription = self.location_subscriber.create_subscription(
            netapp_id=self.myconfig.netapp_id,
            external_id=external_id,
            # notification_destination=self.endpoint_gen.get_loc_endpoint().complete_url,
            notification_destination=self.flask_thread.add_5gcore_endpoint(EndpointType.UE_LOCATION),
            maximum_number_of_reports=1000,
            monitor_expire_time=expire_time
        )
        # From now on we should retrieve POST notifications to the endpoint
        # print(subscription)

    def monitor_subscription_capif(self, times, host, access_token, certificate_folder,
                                   capifhost, capifport, callback_server, id_ue=10001):
        expire_time = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        netapp_id = self.myconfig.netapp_id
        location_subscriber = LocationSubscriber(host, access_token, certificate_folder, capifhost, capifport)
        external_id = str(id_ue) + "@domain.com"

        subscription = location_subscriber.create_subscription(
            netapp_id=netapp_id,
            external_id=external_id,
            notification_destination=callback_server,
            maximum_number_of_reports=times,
            monitor_expire_time=expire_time
        )
        monitoring_response = subscription.to_dict()
        return monitoring_response

    def print_all_subscriptions(self):
        all_subscriptions = self.location_subscriber.get_all_subscriptions(self.myconfig.netapp_id, 0, 100)
        print(all_subscriptions)

    def print_subscription(self, subscription_id):
        subscription_info = self.location_subscriber.get_subscription(self.myconfig.netapp_id, subscription_id)
        print(subscription_info)

    def read_and_delete_all_existing_subscriptions(self):
        try:
            all_subscriptions = self.location_subscriber.get_all_subscriptions(self.myconfig.netapp_id)
            print(all_subscriptions)

            for subscription in all_subscriptions:
                id_sub = subscription.link.split("/")[-1]
                print("Deleting subscription with id: " + id_sub)
                self.location_subscriber.delete_subscription(self.myconfig.netapp_id, id_sub)
        except ApiException as ex:
            if ex.status == 404:
                print("No active location subscription found")
            else:  # something else happened, re-throw the exception
                raise

    def delete_all_existing_subscriptions(self):
        try:
            all_subscriptions = self.location_subscriber.get_all_subscriptions(self.myconfig.netapp_id)
            for subscription in all_subscriptions:
                id_sub = subscription.link.split("/")[-1]
                self.location_subscriber.delete_subscription(self.myconfig.netapp_id, id_sub)

        except ApiException as ex:
            if ex.status == 404:
                print("No active transcriptions found")
            else:  # something else happened, re-throw the exception
                raise
