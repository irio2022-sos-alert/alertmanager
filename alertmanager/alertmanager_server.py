import logging
import os
from concurrent import futures
from datetime import datetime

import alertmanager_pb2
import alertmanager_pb2_grpc
import grpc
from db import create_db_and_tables, engine
from dotenv import load_dotenv
from models import Admins, Alerts, Ownership, Services
from sqlmodel import Session

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


class AlertManagerServicer(alertmanager_pb2_grpc.AlertManagerServicer):
    """Provides methods that implement functionality of alert manager server."""

    def __init__(self, alertsender_endpoint) -> None:
        self.alertsender_endpoint = alertsender_endpoint
        create_db_and_tables()

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
        service = get_service(request.serviceId)

        if service is None:
            return make_status_message(okay=False, msg="No such service!")
        if alert_exists(request.serviceId):
            return make_status_message(okay=True, msg="Alert is already being handled")

        register_alert(service.id)
        emails = get_first_contact_emails(service.id)

        alerting_routine_status = make_status_message(okay=True)

        with grpc.insecure_channel(self.alertsender_endpoint) as channel:
            stub = alertsender_pb2_grpc.AlertSenderStub(channel)
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
        self, request: alertmanager_pb2.ReceiptConfirmation, unused_context
    ):
        with Session(engine) as session:
            status = make_status_message(okay="True")
            service = session.query(Services).get(request.serviceId)
            if service is None:
                status = make_status_message(okay=False, msg="No such service!")
            else:
                alert = session.query(Alerts).get(service.id)

                if alert is None:
                    status = make_status_message(
                        okay=False, msg="No ongoing alerting routine for this service!"
                    )
                else:
                    alert.delete()
                    session.commit()

            return status


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    alertmanager_pb2_grpc.add_AlertManagerServicer_to_server(
        AlertManagerServicer(), server
    )

    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    load_dotenv()
    logging.basicConfig(level=logging.INFO)
    serve()
