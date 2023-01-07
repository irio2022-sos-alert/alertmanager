import logging
import os

import alertsender_pb2
import alertsender_pb2_grpc
import grpc
from dotenv import load_dotenv

load_dotenv()


def create_notification_order():
    return alertsender_pb2.NotificationRequest(
        email_address=os.environ.get("SENDER_EMAIL"),
        subject="test",
        content="RPCGreeterServerTest",
    )


def send_test_email(stub):
    order = create_notification_order()
    response = stub.SendNotification(order)

    if response.okay:
        print("email sent")
    else:
        print(response.message)


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = alertsender_pb2_grpc.AlertSenderStub(channel)
        send_test_email(stub)


if __name__ == "__main__":
    logging.basicConfig()
    run()
