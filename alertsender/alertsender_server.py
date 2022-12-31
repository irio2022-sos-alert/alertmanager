import asyncio
import logging

import grpc
import alertsender_pb2
import alertsender_pb2_grpc
from google.protobuf import empty_pb2
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os


class AlertSenderServicer(alertsender_pb2_grpc.AlertSenderServicer):
    """Provides methods that implement functionality of alert sender server."""

    def __init__(self) -> None:
        self.sendgrid = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        self.email_address = SendGridAPIClient(
            os.environ.get("ALERTSENDER_EMAIL_ADDRESS")
        )

    def compose_email(
        self, request: alertsender_pb2.NotificationRequest
    ) -> Mail:
        return Mail(
            from_email=self.email_address,
            to_emails=request.email_address,
            subject=request.subject,
            html_content=request.content,
        )

    async def SendNotification(
        self, request: alertsender_pb2.NotificationRequest, context
    ) -> empty_pb2:
        email = self.compose_email(request)
        response = self.sendgrid.send(email)

        if response.status_code != 200:
            context.set_code(response.status_code)
            context.details("Email not delivered")

        return empty_pb2


async def serve() -> None:
    server = grpc.aio.server()
    alertsender_pb2_grpc.add_AlertSenderServicer_to_server(
        AlertSenderServicer(), server
    )

    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(serve())
