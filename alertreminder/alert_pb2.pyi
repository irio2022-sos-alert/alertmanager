from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class AlertRequest(_message.Message):
    __slots__ = ["serviceId"]
    SERVICEID_FIELD_NUMBER: _ClassVar[int]
    serviceId: int
    def __init__(self, serviceId: _Optional[int] = ...) -> None: ...

class NotificationRequest(_message.Message):
    __slots__ = ["content", "email_address", "subject"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    EMAIL_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    content: str
    email_address: str
    subject: str
    def __init__(
        self,
        email_address: _Optional[str] = ...,
        subject: _Optional[str] = ...,
        content: _Optional[str] = ...,
    ) -> None: ...

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
