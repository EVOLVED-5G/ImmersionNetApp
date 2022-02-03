from evolved5g.sdk import LocationSubscriber
import emulator.Emulator_Utils as emulator_utils
import datetime
from evolved5g.swagger_client import LoginApi, User

from request.general.APIRequester import APIRequester


def showcase_create_subscription_and_retrieve_call_backs(endpoint_generator):
    """
    This example showcases how you can create a subscription to the 5G-API in order to monitor device location.
    In order to run this example you need to follow the instructions in  readme.md in order to a) run the NEF emulator
    and b) run a local webserver that will print the location notifications it retrieves from the emulator.
    A testing local webserver (Flask webserver) can be initiated by running the examples/api.py
    """

    # Create a subscription, that will notify us 1000 times, for the next 1 day starting from now
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + "Z"
    netapp_id = "myNetapp"
    host = emulator_utils.get_host_of_the_nef_emulator()
    token = emulator_utils.get_token()
    location_subscriber = LocationSubscriber(host, token.access_token)
    # The following external identifier was copy pasted by the NEF emulator. Go to the Map and click on a User icon.
    # There you can retrieve the id
    external_id = "10001@domain.com"

    # In this example we are running flask at http://localhost:5000 with a POST route to (/monitoring/callback)
    # in order to retrieve notifications.
    # If you are running on the NEF emulator, you need to provide a notification_destination with an IP that the
    # NEF emulator docker can understand
    # For latest versions of docker this should be: http://host.docker.internal:5000/monitoring/callback"
    # Alternative you can find the ip of the HOST by running
    # 'ip addr show | grep "\binet\b.*\bdocker0\b" | awk '{print $2}' | cut -d '/' -f 1'
    # See article for details:
    # https://stackoverflow.com/questions/48546124/what-is-linux-equivalent-of-host-docker-internal/61001152

    endpoint = endpoint_generator.start_ue_monitoring()

    subscription = location_subscriber.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination=endpoint,
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time
    )

    # From now on we should retrieve POST notifications to the endpoint
    print(subscription)


class LocationRequester(APIRequester):

    def __init__(self, endpoint_generator, access_token):
        super().__init__(endpoint_generator, access_token)

    def track_ue_position(self, id_ue=10001, expire_delay=24):
        expire_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=expire_delay)).isoformat() + "Z"
        host = emulator_utils.get_host_of_the_nef_emulator()
        # To find external ids -> go to the online emulator map and click on a User icon
        external_id = str(id_ue) + "@domain.com"
        endpoint = self.endpoint_gen.start_ue_monitoring()
        location_subscriber = LocationSubscriber(host, self.token.access_token)

        subscription = location_subscriber.create_subscription(
            netapp_id=self.NETAPP_ID,
            external_id=external_id,
            notification_destination=endpoint,
            maximum_number_of_reports=1000,
            monitor_expire_time=expire_time
        )

        # From now on we should retrieve POST notifications to the endpoint
        print(subscription)

