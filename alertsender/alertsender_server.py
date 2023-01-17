import logging
import os
from concurrent import futures

import alert_pb2
import alert_pb2_grpc
import grpc
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def make_status_message(okay: bool, msg: str = "") -> alert_pb2.Status:
    return alert_pb2.Status(okay=okay, message=msg)


class AlertSenderServicer(alert_pb2_grpc.AlertSenderServicer):
    """Provides methods that implement functionality of alert sender server."""

    def __init__(self, api_key: str, sender_email: str) -> None:
        self.sendgrid = SendGridAPIClient(api_key)
        self.sender_email = sender_email

    def compose_email(self, request: alert_pb2.NotificationRequest) -> Mail:
        return Mail(
            from_email=self.sender_email,
            to_emails=request.email_address,
            subject=request.subject,
            html_content=request.content,
        )

    def SendNotification(
        self, request: alert_pb2.NotificationRequest, context
    ) -> alert_pb2.Status:
        email = self.compose_email(request)
        sg_response = self.sendgrid.send(email)
        status = make_status_message(okay=True)

        if sg_response.status_code != 202:
            status = make_status_message(
                okay=False,
                msg=f"Sendgrid api call returned with code: {sg_response.status_code}",
            )

        return status


def serve(port: str, api_key: str, sender_email: str) -> None:
    bind_address = f"[::]:{port}"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    alert_pb2_grpc.add_AlertSenderServicer_to_server(
        AlertSenderServicer(api_key, sender_email), server
    )
    server.add_insecure_port(bind_address)
    server.start()
    logging.info("Listening on %s.", bind_address)
    server.wait_for_termination()


if __name__ == "__main__":
    port = os.environ.get("PORT", "50051")
    api_key = os.environ.get("SENDGRID_API_KEY")
    sender_email = os.environ.get("SENDER_EMAIL")

    logging.basicConfig(level=logging.INFO)
    serve(port, api_key, sender_email)
