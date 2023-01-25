import os

import alert_pb2
import alert_pb2_grpc
import grpc
from flask import Flask

app = Flask(__name__)


def create_receipt_confirmation(service_id: int) -> alert_pb2.ReceiptConfirmation:
    return alert_pb2.ReceiptConfirmation(serviceId=service_id)


@app.before_first_request
def init():
    global alertmanager_endpoint
    alertmanager_endpoint = os.getenv("ALERTMANAGER_ENDPOINT", "[::]:50052")


@app.route("/<service_id>")
def confirm_receipt(service_id: int):
    try:
        confirmation = create_receipt_confirmation(int(service_id))

        with grpc.secure_channel(
            alertmanager_endpoint, grpc.ssl_channel_credentials()
        ) as channel:
            stub = alert_pb2_grpc.AlertManagerStub(channel)
            response = stub.handleReceiptConfirmation(confirmation)

            if response.okay is True:
                return "Notification receipt confirmed!"
            else:
                return f"Error! {response.message}"

    except ValueError:
        return "Invalid argument!"


if __name__ == "__main__":
    app.run()
