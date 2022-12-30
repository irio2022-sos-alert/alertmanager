from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReceiptConfirmation(_message.Message):
    __slots__ = ["notifcationId"]
    NOTIFCATIONID_FIELD_NUMBER: _ClassVar[int]
    notifcationId: int
    def __init__(self, notifcationId: _Optional[int] = ...) -> None: ...
