import os
from datetime import datetime

import alertmanager_pb2
import alertmanager_pb2_grpc
import grpc

import alertsender.alertsender_pb2 as alertsender_pb2
import alertsender.alertsender_pb2_grpc as alertsender_pb2_grpc


def make_status_message(okay: bool, msg: str = "") -> alertmanager_pb2.Status:
    return alertmanager_pb2.Status(okay=okay, message=msg)


def make_alert_notification(email, service_name):
    return alertsender_pb2.NotificationRequest(
        email_address=email,
        subject=f"Your {service_name} service is down!",
        content=f"""As of {datetime.utcnow()} (UTC) your {service_name} service
        was unresponsive for longer than set allowed time.""",
    )


class AlertMangerServicer(alertmanager_pb2_grpc.AlertManagerServicer):
    """Provides methods that implement functionality of alert manager server."""

    def __init__(self, alertsender_endpoint) -> None:
        self.alertsender_endpoint = alertsender_endpoint

    def get_first_contact_email(self, service_id):
        # should call db to get it
        return os.environ.get("SENDER_EMAIL")

    def get_service_name(self, service_id):
        # should call db to get it
        return "usos.uw.edu.pl"

    def alert_routine_exists(self, service_id):
        return True

    def stop_alert_routine(self, service_id):
        return

    def Alert(
        self, request: alertmanager_pb2.AlertRequest, unused_context
    ) -> alertmanager_pb2.Status:

        # verify that alert isn't handled already

        # if not get email of first contact
        first_contact_email = self.get_first_contact_email(request.serviceId)
        service_name = self.get_service_name(request.serviceId)
        alert_notification = make_alert_notification(first_contact_email, service_name)
        status = make_status_message(okay=True)

        # send notification request to alertsender
        with grpc.insecure_channel(self.alertsender_endpoint) as channel:
            stub = alertsender_pb2_grpc.AlertSenderStub(channel)
            call_status = stub.SendNotification(alert_notification)

            if call_status.okay is False:
                status = make_status_message(
                    okay=False, msg="Unsuccessful call to alertsender service."
                )

        return status

    def handleReceiptConfirmation(self, request, unused_context):
        # check if there is any alert routing going on for given serviceID
        # if there is call it off

        if self.alert_routine_exists(request.serviceId):
            self.stop_alert_routine(request.serviceId)
        else:
            service_name = self.get_service_name(request.serviceId)
            status = make_status_message(
                okay=False,
                msg=f"There is no running alert routine for service {service_name}",
            )

        return status
