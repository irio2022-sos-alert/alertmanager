import logging
import os
from concurrent import futures

import alertsender_pb2
import alertsender_pb2_grpc
import grpc
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def make_status_message(okay: bool, msg: str = "") -> alertsender_pb2.Status:
    return alertsender_pb2.Status(okay=okay, message=msg)


class AlertSenderServicer(alertsender_pb2_grpc.AlertSenderServicer):
    """Provides methods that implement functionality of alert sender server."""

    def __init__(self, api_key: str, sender_email: str) -> None:
        self.sendgrid = SendGridAPIClient(api_key)
        self.sender_email = sender_email

    def compose_email(self, request: alertsender_pb2.NotificationRequest) -> Mail:
        return Mail(
            from_email=self.sender_email,
            to_emails=request.email_address,
            subject=request.subject,
            html_content=request.content,
        )

    def SendNotification(
        self, request: alertsender_pb2.NotificationRequest, context
    ) -> alertsender_pb2.Status:
        email = self.compose_email(request)
        sg_response = self.sendgrid.send(email)
        status = make_status_message(okay=True)

        if sg_response.status_code != 202:
            status = make_status_message(
                okay=False,
                msg=f"Sendgrid api call returned with code: {sg_response.status_code}",
            )

        return status


def serve(api_key: str, sender_email: str) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    alertsender_pb2_grpc.add_AlertSenderServicer_to_server(
        AlertSenderServicer(api_key, sender_email), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    load_dotenv()
    api_key = os.environ.get("SENDGRID_API_KEY")
    sender_email = os.environ.get("SENDER_EMAIL")

    logging.basicConfig(level=logging.INFO)
    serve(api_key, sender_email)
