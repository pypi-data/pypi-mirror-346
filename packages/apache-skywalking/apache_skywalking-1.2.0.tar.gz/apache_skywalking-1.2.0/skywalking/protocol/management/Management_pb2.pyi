from common import Common_pb2 as _Common_pb2
from common import Command_pb2 as _Command_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InstanceProperties(_message.Message):
    __slots__ = ("service", "serviceInstance", "properties", "layer")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    service: str
    serviceInstance: str
    properties: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    layer: str
    def __init__(self, service: _Optional[str] = ..., serviceInstance: _Optional[str] = ..., properties: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ..., layer: _Optional[str] = ...) -> None: ...

class InstancePingPkg(_message.Message):
    __slots__ = ("service", "serviceInstance", "layer")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    service: str
    serviceInstance: str
    layer: str
    def __init__(self, service: _Optional[str] = ..., serviceInstance: _Optional[str] = ..., layer: _Optional[str] = ...) -> None: ...
