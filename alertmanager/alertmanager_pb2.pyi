from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AlertRequest(_message.Message):
    __slots__ = ["serviceId"]
    SERVICEID_FIELD_NUMBER: _ClassVar[int]
    serviceId: int
    def __init__(self, serviceId: _Optional[int] = ...) -> None: ...

class ReceiptConfirmation(_message.Message):
    __slots__ = ["serviceId"]
    SERVICEID_FIELD_NUMBER: _ClassVar[int]
    serviceId: int
    def __init__(self, serviceId: _Optional[int] = ...) -> None: ...
