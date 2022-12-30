from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EmailNotifactionRequest(_message.Message):
    __slots__ = ["addressee", "content", "subject"]
    ADDRESSEE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    addressee: str
    content: str
    subject: str
    def __init__(self, addressee: _Optional[str] = ..., subject: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class NotifcationRequest(_message.Message):
    __slots__ = ["emailRequests"]
    EMAILREQUESTS_FIELD_NUMBER: _ClassVar[int]
    emailRequests: _containers.RepeatedCompositeFieldContainer[EmailNotifactionRequest]
    def __init__(self, emailRequests: _Optional[_Iterable[_Union[EmailNotifactionRequest, _Mapping]]] = ...) -> None: ...
