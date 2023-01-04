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

class Status(_message.Message):
    __slots__ = ["message", "okay"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OKAY_FIELD_NUMBER: _ClassVar[int]
    message: str
    okay: bool
    def __init__(self, okay: bool = ..., message: _Optional[str] = ...) -> None: ...
