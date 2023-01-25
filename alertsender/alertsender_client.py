import logging
import os

import alert_pb2
import alert_pb2_grpc
import grpc


def create_notification_order() -> alert_pb2.NotificationRequest:
    return alert_pb2.NotificationRequest(
        email_address=os.environ["SENDER_EMAIL"],
        subject="test",
        content="RPCGreeterServerTest",
    )


def send_test_email(stub: alert_pb2_grpc.AlertSenderStub):
    order = create_notification_order()
    response = stub.SendNotification(order)

    if response.okay:
        print("email sent")
    else:
        print(response.message)


def run():
    endpoint = os.getenv("SENDER_ENDPOINT", "localhost:50051")
    logging.info(f"endpoint : {endpoint}")
    with grpc.secure_channel(endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = alert_pb2_grpc.AlertSenderStub(channel)
        send_test_email(stub)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
