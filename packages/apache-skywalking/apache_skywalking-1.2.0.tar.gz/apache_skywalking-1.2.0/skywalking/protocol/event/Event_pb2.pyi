from common import Command_pb2 as _Command_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Normal: _ClassVar[Type]
    Error: _ClassVar[Type]
Normal: Type
Error: Type

class Event(_message.Message):
    __slots__ = ("uuid", "source", "name", "type", "message", "parameters", "startTime", "endTime", "layer")
    class ParametersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    UUID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    source: Source
    name: str
    type: Type
    message: str
    parameters: _containers.ScalarMap[str, str]
    startTime: int
    endTime: int
    layer: str
    def __init__(self, uuid: _Optional[str] = ..., source: _Optional[_Union[Source, _Mapping]] = ..., name: _Optional[str] = ..., type: _Optional[_Union[Type, str]] = ..., message: _Optional[str] = ..., parameters: _Optional[_Mapping[str, str]] = ..., startTime: _Optional[int] = ..., endTime: _Optional[int] = ..., layer: _Optional[str] = ...) -> None: ...

class Source(_message.Message):
    __slots__ = ("service", "serviceInstance", "endpoint")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    service: str
    serviceInstance: str
    endpoint: str
    def __init__(self, service: _Optional[str] = ..., serviceInstance: _Optional[str] = ..., endpoint: _Optional[str] = ...) -> None: ...
