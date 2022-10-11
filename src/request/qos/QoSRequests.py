from evolved5g.sdk import QosAwareness
from evolved5g.swagger_client import UsageThreshold
from evolved5g.swagger_client.rest import ApiException

from request.endpoint.EndpointUtils import EndpointType
from request.general.APIRequester import APIRequester


# Class dedicated to make requests to the 5G core about QoS monitoring
# It relies on 1) the QosAwareness class from the SDK and 2) on the AsSessionWithQos API
class QoSRequester(APIRequester):

    def __init__(self, flask_th, access_token):
        super().__init__(flask_th, access_token)
        self.qos_awareness = QosAwareness(self.host, self.token.access_token)

    def sessionqos_subscription(self, ue_ipv4="10.0.0.1"):
        network_identifier = QosAwareness.NetworkIdentifier.IP_V4_ADDRESS
        # In this scenario we monitor UPLINK
        uplink = QosAwareness.QosMonitoringParameter.UPLINK
        # Minimum delay of data package during uplink, in milliseconds
        uplink_threshold = 20
        gigabyte = 1024 * 1024 * 1024
        # Up to 10 gigabytes 5 GB downlink, 5gb uplink
        usage_threshold = UsageThreshold(duration=None,  # not supported
                                         total_volume=10 * gigabyte,  # 10 Gigabytes of total volume
                                         downlink_volume=5 * gigabyte,  # 5 Gigabytes for downlink
                                         uplink_volume=5 * gigabyte  # 5 Gigabytes for uplink
                                         )

        notification_destination = self.flask_thread.add_endpoint(EndpointType.UE_GBR)

        subscription = self.qos_awareness.create_guaranteed_bit_rate_subscription(
            netapp_id=self.netapp_id,
            equipment_network_identifier=ue_ipv4,
            network_identifier=network_identifier,
            notification_destination=notification_destination,
            gbr_qos_reference=QosAwareness.GBRQosReference.CONVERSATIONAL_VIDEO,
            usage_threshold=usage_threshold,
            qos_monitoring_parameter=uplink,
            threshold=uplink_threshold,
            # reporting_mode=QosAwareness.EventTriggeredReportingConfiguration(wait_time_in_seconds=10)
            reporting_mode= QosAwareness.PeriodicReportConfiguration(repetition_period_in_seconds=10)
        )
        # From now on we should retrieve POST notifications when:
        # a) two users connect to the same cell at the same time (which is how NEF simulates loss of GBT), or
        # b) when Usage threshold is exceeded(notice this is not supported by the NEF,
        #    so you will never retrieve this notification while testing with the NEF)
        # print(subscription)

    def read_and_delete_all_existing_subscriptions(self):
        try:
            all_subscriptions = self.qos_awareness.get_all_subscriptions(self.netapp_id)
            print(all_subscriptions)

            for subscription in all_subscriptions:
                id_sub = subscription.link.split("/")[-1]
                print("Deleting subscription with id: " + id_sub)
                self.qos_awareness.delete_subscription(self.netapp_id, id_sub)
        except ApiException as ex:
            if ex.status == 404:
                print("No active qos subscription found")
            else: # something else happened, re-throw the exception
                raise

    def delete_all_existing_subscriptions(self):
        try:
            all_subscriptions = self.qos_awareness.get_all_subscriptions(self.netapp_id)

            for subscription in all_subscriptions:
                id_sub = subscription.link.split("/")[-1]
                self.qos_awareness.delete_subscription(self.netapp_id, id_sub)

        except ApiException as ex:
            if ex.status == 404:
                print("No active transcriptions found")
            else:  # something else happened, re-throw the exception
                raise

