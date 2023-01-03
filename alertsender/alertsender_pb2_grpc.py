# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import alertsender_pb2 as alertsender__pb2


class AlertSenderStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendNotification = channel.unary_unary(
                '/AlertSender/SendNotification',
                request_serializer=alertsender__pb2.NotificationRequest.SerializeToString,
                response_deserializer=alertsender__pb2.Status.FromString,
                )


class AlertSenderServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendNotification(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AlertSenderServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendNotification': grpc.unary_unary_rpc_method_handler(
                    servicer.SendNotification,
                    request_deserializer=alertsender__pb2.NotificationRequest.FromString,
                    response_serializer=alertsender__pb2.Status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'AlertSender', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AlertSender(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendNotification(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AlertSender/SendNotification',
            alertsender__pb2.NotificationRequest.SerializeToString,
            alertsender__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
