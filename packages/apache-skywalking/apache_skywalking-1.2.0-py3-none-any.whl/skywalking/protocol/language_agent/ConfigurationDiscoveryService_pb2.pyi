from common import Command_pb2 as _Command_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConfigurationSyncRequest(_message.Message):
    __slots__ = ("service", "uuid")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    service: str
    uuid: str
    def __init__(self, service: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...
