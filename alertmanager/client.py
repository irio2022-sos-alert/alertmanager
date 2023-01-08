import logging

import alert_pb2
import alert_pb2_grpc
import grpc
from dotenv import load_dotenv

load_dotenv()


def create_receipt_confirmation(service_id: int) -> alert_pb2.ReceiptConfirmation:
    return alert_pb2.ReceiptConfirmation(serviceId=service_id)


def send_confirmation_test(stub: alert_pb2_grpc.AlertManagerStub):
    confirmation = create_receipt_confirmation(20)
    response = stub.handleReceiptConfirmation(confirmation)

    if response.okay:
        print("Confirmed")
    else:
        print(response.message)


def run():
    with grpc.insecure_channel("localhost:50052") as channel:
        stub = alert_pb2_grpc.AlertManagerStub(channel)
        send_confirmation_test(stub)


if __name__ == "__main__":
    logging.basicConfig()
    run()
