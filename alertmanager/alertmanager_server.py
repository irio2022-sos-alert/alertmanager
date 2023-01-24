import logging
import os
from concurrent import futures
from datetime import datetime

import alert_pb2
import alert_pb2_grpc
import grpc
from db import create_db_and_tables, engine
from models import Admins, Alerts, Ownership, Services
from sqlmodel import Session


def make_status_message(okay: bool, msg: str = "") -> alert_pb2.Status:
    return alert_pb2.Status(okay=okay, message=msg)


def make_alert_notification(email, service_name):
    return alert_pb2.NotificationRequest(
        email_address=email,
        subject=f"Your {service_name} service is down!",
        content=f"""As of {datetime.utcnow()} (UTC) your {service_name} service
        was unresponsive for longer than set allowed time.""",
    )


def get_first_contact_emails(service_id: int) -> list[str]:
    with Session(engine) as session:
        first_contacts = (
            session.query(Ownership)
            .where(Ownership.service_id == service_id, Ownership.first_contact is True)
            .all()
        )

        first_contacts_ids = [contact.admin_id for contact in first_contacts]
        admins = session.query(Admins).where(Admins.id in first_contacts_ids)

        return [admin.email for admin in admins]


def alert_exists(service_id: int) -> bool:
    with Session(engine) as session:
        return session.query(Alerts).get(service_id) is not None


def register_alert(service_id: int):
    with Session(engine) as session:
        session.add(Alerts(service_id=service_id))


def get_service(service_id: int) -> Services:
    with Session(engine) as session:
        return session.query(Services).get(service_id)


class AlertManagerServicer(alert_pb2_grpc.AlertManagerServicer):
    """Provides methods that implement functionality of alert manager server."""

    def __init__(self, alertsender_endpoint) -> None:
        self.alertsender_endpoint = alertsender_endpoint
        create_db_and_tables()

    def Alert(
        self, request: alert_pb2.AlertRequest, unused_context
    ) -> alert_pb2.Status:
        service = get_service(request.serviceId)

        if service is None:
            return make_status_message(okay=False, msg="No such service!")
        if alert_exists(request.serviceId):
            return make_status_message(okay=True, msg="Alert is already being handled")

        register_alert(service.id)
        emails = get_first_contact_emails(service.id)

        alerting_routine_status = make_status_message(okay=True)

        with grpc.insecure_channel(self.alertsender_endpoint) as channel:
            stub = alert_pb2_grpc.AlertSenderStub(channel)
            for email in emails:
                notification = make_alert_notification(email, service.name)
                call_status = stub.SendNotification(notification)
                if call_status.okay is False:
                    alerting_routine_status = make_status_message(
                        okay=False,
                        msg="Not all calls to alertsender service were successful",
                    )

        return alerting_routine_status

    def handleReceiptConfirmation(
        self, request: alert_pb2.ReceiptConfirmation, unused_context
    ):
        with Session(engine) as session:
            status = make_status_message(okay=True)
            service = session.query(Services).get(request.serviceId)
            if service is None:
                status = make_status_message(okay=False, msg="No such service!")
            else:
                alert = session.query(Alerts).get(service.id)

                if alert is None:
                    status = make_status_message(
                        okay=False,
                        msg="No ongoing alerting routine for this service!",
                    )
                else:
                    alert.delete()
                    session.commit()

            print(status)
            return status


def serve(port: str, alertsender_endpoint: str) -> None:
    bind_address = f"[::]:{port}"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    alert_pb2_grpc.add_AlertManagerServicer_to_server(
        AlertManagerServicer(alertsender_endpoint), server
    )

    server.add_insecure_port(bind_address)
    server.start()
    logging.info("Listening on %s.", bind_address)
    server.wait_for_termination()


if __name__ == "__main__":
    port = os.environ.get("PORT", "50052")
    alertsender_endpoint = os.environ.get("ALERTSENDER_ENDPOINT", "[::]:50051")
    logging.basicConfig(level=logging.INFO)
    serve(port, alertsender_endpoint)
