from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NotificationRequest(_message.Message):
    __slots__ = ["content", "email_address", "subject"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    EMAIL_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    content: str
    email_address: str
    subject: str
    def __init__(self, email_address: _Optional[str] = ..., subject: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...
