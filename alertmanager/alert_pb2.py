# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: alert.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0b\x61lert.proto\x12\x05\x61lert"!\n\x0c\x41lertRequest\x12\x11\n\tserviceId\x18\x01 \x01(\x03"(\n\x13ReceiptConfirmation\x12\x11\n\tserviceId\x18\x01 \x01(\x03"\'\n\x06Status\x12\x0c\n\x04okay\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t"N\n\x13NotificationRequest\x12\x15\n\remail_address\x18\x01 \x01(\t\x12\x0f\n\x07subject\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t2\xc7\x01\n\x0c\x41lertManager\x12-\n\x05\x41lert\x12\x13.alert.AlertRequest\x1a\r.alert.Status"\x00\x12>\n\x16HandleResponseDeadline\x12\x13.alert.AlertRequest\x1a\r.alert.Status"\x00\x12H\n\x19handleReceiptConfirmation\x12\x1a.alert.ReceiptConfirmation\x1a\r.alert.Status"\x00\x32N\n\x0b\x41lertSender\x12?\n\x10SendNotification\x12\x1a.alert.NotificationRequest\x1a\r.alert.Status"\x00\x32T\n\x0e\x41lertConfirmer\x12\x42\n\x13\x63onfirmAlertReceipt\x12\x1a.alert.ReceiptConfirmation\x1a\r.alert.Status"\x00\x62\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "alert_pb2", globals())
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _ALERTREQUEST._serialized_start = 22
    _ALERTREQUEST._serialized_end = 55
    _RECEIPTCONFIRMATION._serialized_start = 57
    _RECEIPTCONFIRMATION._serialized_end = 97
    _STATUS._serialized_start = 99
    _STATUS._serialized_end = 138
    _NOTIFICATIONREQUEST._serialized_start = 140
    _NOTIFICATIONREQUEST._serialized_end = 218
    _ALERTMANAGER._serialized_start = 221
    _ALERTMANAGER._serialized_end = 420
    _ALERTSENDER._serialized_start = 422
    _ALERTSENDER._serialized_end = 500
    _ALERTCONFIRMER._serialized_start = 502
    _ALERTCONFIRMER._serialized_end = 586
# @@protoc_insertion_point(module_scope)
