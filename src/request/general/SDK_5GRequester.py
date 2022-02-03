from evolved5g.swagger_client.rest import ApiException
from evolved5g.sdk import LocationSubscriber
import emulator.Emulator_Utils as emulator_utils
import datetime
from evolved5g.swagger_client import LoginApi, User


def showcase_login_to_the_emulator_and_test_token():
    """
    Demonstrate how to interact with the Emulator, to a token and the current logged in User
    """

    token = emulator_utils.get_token()
    print("-----")
    print("Got token")
    print(token)
    api_client = emulator_utils.get_api_client(token)
    api = LoginApi(api_client)
    print("-----")
    print("Getting login info")
    response = api.test_token_api_v1_login_test_token_post_with_http_info()
    assert isinstance(response[0], User)
    print(response[0])


def showcase_create_subscription_and_retrieve_call_backs(endpointGenerator):
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

    endpoint = endpointGenerator.start_ue_monitoring()

    subscription = location_subscriber.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination=endpoint,
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time
    )

    # From now on we should retrieve POST notifications to the endpoint
    print(subscription)

    # How to get all subscriptions
    all_subscriptions = location_subscriber.get_all_subscriptions(netapp_id, 0, 100)
    print(all_subscriptions)

    # Request information about a subscription
    id = subscription.link.split("/")[-1]
    subscription_info = location_subscriber.get_subscription(netapp_id, id)
    print(subscription_info)