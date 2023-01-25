import logging
import os

import alert_pb2
import alert_pb2_grpc
import grpc


def create_receipt_confirmation(service_id: int) -> alert_pb2.ReceiptConfirmation:
    return alert_pb2.ReceiptConfirmation(serviceId=service_id)


def create_alert_request(service_id: int) -> alert_pb2.AlertRequest:
    return alert_pb2.AlertRequest(serviceId=service_id)


def test_send_confirmation(stub: alert_pb2_grpc.AlertManagerStub):
    confirmation = create_receipt_confirmation(20)
    response = stub.handleReceiptConfirmation(confirmation)

    if response.okay:
        print("Confirmed!")
    else:
        print(response.message)


def test_send_alert_request(stub: alert_pb2_grpc.AlertManagerStub) -> None:
    request = create_alert_request(1)
    response = stub.Alert(request)

    if response.okay:
        print("Request handled!")
    else:
        print(response.message)


def run():
    endpoint = os.getenv("MANAGER_ENDPOINT", "localhost:50052")
    logging.info(f"endpoint : {endpoint}")
    with grpc.secure_channel(endpoint, grpc.ssl_channel_credentials()) as channel:
        stub = alert_pb2_grpc.AlertManagerStub(channel)
        test_send_confirmation(stub)
        test_send_alert_request(stub)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
