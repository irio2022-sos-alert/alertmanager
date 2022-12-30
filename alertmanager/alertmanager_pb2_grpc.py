# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import alertmanager_pb2 as alertmanager__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class AlertManagerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.handleAlert = channel.unary_unary(
                '/AlertManager/handleAlert',
                request_serializer=alertmanager__pb2.AlertRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.handleConfimation = channel.unary_unary(
                '/AlertManager/handleConfimation',
                request_serializer=alertmanager__pb2.ReceiptConfirmation.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class AlertManagerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def handleAlert(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def handleConfimation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AlertManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'handleAlert': grpc.unary_unary_rpc_method_handler(
                    servicer.handleAlert,
                    request_deserializer=alertmanager__pb2.AlertRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'handleConfimation': grpc.unary_unary_rpc_method_handler(
                    servicer.handleConfimation,
                    request_deserializer=alertmanager__pb2.ReceiptConfirmation.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'AlertManager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AlertManager(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def handleAlert(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AlertManager/handleAlert',
            alertmanager__pb2.AlertRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def handleConfimation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/AlertManager/handleConfimation',
            alertmanager__pb2.ReceiptConfirmation.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
