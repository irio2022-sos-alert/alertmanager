import logging
import os
from concurrent import futures
from datetime import datetime

import alert_pb2
import alert_pb2_grpc
import grpc
from db import init_connection_pool, migrate_db
from models import Admins, Alerts, Ownership, Services
from sqlmodel import Session


def make_status_message(okay: bool, msg: str = "") -> alert_pb2.Status:
    return alert_pb2.Status(okay=okay, message=msg)


def make_alert_notification(email, service_name, confirmation_link):
    return alert_pb2.NotificationRequest(
        email_address=email,
        subject=f"Your {service_name} service is down!",
        content=f"""As of {datetime.utcnow()} (UTC) your {service_name} service
        was unresponsive for longer than set allowed time.

        Please confirm receipt of this notification:
        {confirmation_link}""",
    )


def make_confirmation_link(alertconfirmer_endpoint: str, service: Services):
    return f"{alertconfirmer_endpoint}/{service.id}"


def get_contact_emails(service_id: int, first_contact: bool) -> list[str]:
    with Session(engine) as session:
        if first_contact:
            contacts = (
                session.query(Ownership)
                .where(
                    Ownership.service_id == service_id,
                    Ownership.first_contact == first_contact,
                )
                .all()
            )

        contacts_ids = [contact.admin_id for contact in contacts]
        admins = session.query(Admins).where(Admins.id.in_(contacts_ids)).all()

        return [admin.email for admin in admins]


def alert_exists(service_id: int) -> bool:
    with Session(engine) as session:
        return session.query(Alerts).get(service_id) is not None


def register_alert(service_id: int):
    with Session(engine) as session:
        session.add(Alerts(service_id=service_id))
        session.commit()


def get_service(service_id: int) -> Services:
    with Session(engine) as session:
        return session.query(Services).get(service_id)


class AlertManagerServicer(alert_pb2_grpc.AlertManagerServicer):
    """Provides methods that implement functionality of alert manager server."""

    def __init__(self, alertsender_endpoint: str, alertconfirmer_endpoint: str) -> None:
        self.alertsender_endpoint = alertsender_endpoint
        self.alertconfirmer_endpoint = alertconfirmer_endpoint

    def Alert(
        self, request: alert_pb2.AlertRequest, unused_context
    ) -> alert_pb2.Status:
        service = get_service(request.serviceId)

        if service is None:
            logging.info("No such service!")
            return make_status_message(okay=False, msg="No such service!")

        if alert_exists(request.serviceId):
            logging.info(f"Routine already exists for id: {request.serviceId}")
            return make_status_message(okay=True, msg="Alert is already being handled")
        else:
            register_alert(service.id)

        emails = get_contact_emails(service.id, True)
        logging.info(f"Received valid alert request for service_id: {service.id}")
        if len(emails) == 0:
            logging.info("No emails are assigned to this service!")

        alerting_routine_status = make_status_message(okay=True)
        confirmation_link = make_confirmation_link(
            self.alertconfirmer_endpoint, service
        )

        with grpc.secure_channel(
            self.alertsender_endpoint, grpc.ssl_channel_credentials()
        ) as channel:
            stub = alert_pb2_grpc.AlertSenderStub(channel)
            for email in emails:
                notification = make_alert_notification(
                    email, service, confirmation_link
                )
                call_status = stub.SendNotification(notification)
                if call_status.okay is False:
                    logging.info(
                        f"Failed to notify {email} about issues with service_id: {service.id}"
                    )
                    alerting_routine_status = make_status_message(
                        okay=False,
                        msg="Not all calls to alertsender service were successful",
                    )
                else:
                    logging.info(
                        f"Sent out notification to {email} about issues with service_id: {service.id}"
                    )

        return alerting_routine_status

    def HandleResponseDeadline(self, request, context):

        with Session(engine) as session:
            service = session.query(Services).get(request.serviceId)
            alert = session.query(Alerts).get(service.id)

            if service is None:
                logging.info(
                    f"Invalid response deadline request for {request.serviceId}, No such service!"
                )
                return make_status_message(okay=False, msg="No such service!")

            if alert is None:
                logging.info(
                    f"Invalid confirmation request for {service.id}, No ongoing alerting routine for this service!"
                )
                return make_status_message(
                    okay=False, msg="No ongoing alerting routine for this service!"
                )

            alerting_routine_status = make_status_message(okay=True)
            emails = get_contact_emails(service.id, first_contact=False)
            confirmation_link = make_confirmation_link(
                self.alertconfirmer_endpoint, service
            )

            with grpc.secure_channel(
                self.alertsender_endpoint, grpc.ssl_channel_credentials()
            ) as channel:
                stub = alert_pb2_grpc.AlertSenderStub(channel)
                for email in emails:
                    notification = make_alert_notification(
                        email, service, confirmation_link
                    )
                    call_status = stub.SendNotification(notification)
                    if call_status.okay is False:
                        logging.info(
                            f"Failed to notify {email} about issues with service_id: {service.id}"
                        )
                        alerting_routine_status = make_status_message(
                            okay=False,
                            msg="Not all calls to alertsender service were successful",
                        )
                    else:
                        logging.info(
                            f"Sent out notification to {email} about issues with service_id: {service.id}"
                        )

            # call off alerting routine
            session.delete(alert)
            return alerting_routine_status

    def handleReceiptConfirmation(
        self, request: alert_pb2.ReceiptConfirmation, unused_context
    ):
        with Session(engine) as session:
            status = make_status_message(okay=True)
            service = session.query(Services).get(request.serviceId)
            if service is None:
                status = make_status_message(okay=False, msg="No such service!")
                logging.info(
                    f"Invalid confirmation request for {request.serviceId}, {status.message}"
                )
            else:
                alert = session.query(Alerts).get(service.id)

                if alert is None:
                    status = make_status_message(
                        okay=False,
                        msg="No ongoing alerting routine for this service!",
                    )
                    logging.info(
                        f"Invalid confirmation request for {service.id}, {status.message}"
                    )
                else:
                    session.delete(alert)
                    session.commit()
                    logging.info(
                        f"Alert routine successfully called off for service_id: {service.id}"
                    )

            return status


def init_db():
    global engine
    engine = init_connection_pool()
    migrate_db(engine)


def serve() -> None:
    # get port and endpoints of other services
    port = os.environ.get("PORT", "50052")
    alertsender_endpoint = os.environ.get("ALERTSENDER_ENDPOINT", "[::]:50051")
    alertconfirmer_endpoint = os.environ.get("ALERTCONFIRMER_ENDPOINT", "[::]:50053")
    bind_address = f"[::]:{port}"

    # initialize database connection
    init_db()

    # initialize servicer
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    alert_pb2_grpc.add_AlertManagerServicer_to_server(
        AlertManagerServicer(alertsender_endpoint, alertconfirmer_endpoint), server
    )
    server.add_insecure_port(bind_address)
    server.start()
    logging.info("Listening on %s.", bind_address)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
