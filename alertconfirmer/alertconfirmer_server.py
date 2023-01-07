import logging
from concurrent import futures

import alert_pb2
import alert_pb2_grpc
import grpc
from dotenv import load_dotenv


def make_status_message(okay: bool, msg: str = "") -> alert_pb2.Status:
    return alert_pb2.Status(okay=okay, message=msg)


class AlertConfirmerServicer(alert_pb2_grpc.AlertConfirmerServicer):
    """Provides methods that implement functionality of alert confirmer server."""

    def __init__(self, alertmanager_endpoint) -> None:
        self.alertmanager_endpoint = alertmanager_endpoint

    def confirmAlertReceipt(
        self, request: alert_pb2.ReceiptConfirmation, unused_context
    ):
        with grpc.insecure_channel(self.alertmanager_endpoint) as channel:
            stub = alert_pb2_grpc.AlertManagerStub(channel)
            response = stub.handleReceiptConfirmation(request.serviceId)
            return response


def serve(alertmanager_endpoint: str) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    alert_pb2_grpc.add_AlertConfirmerServicer_to_server(
        AlertConfirmerServicer(alertmanager_endpoint), server
    )

    server.add_insecure_port("[::]:50053")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    load_dotenv()
    alertmanager_endpoint = "[::]:50052"
    logging.basicConfig(level=logging.INFO)
    serve(alertmanager_endpoint)
