from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DetectPoint(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    client: _ClassVar[DetectPoint]
    server: _ClassVar[DetectPoint]
    proxy: _ClassVar[DetectPoint]
client: DetectPoint
server: DetectPoint
proxy: DetectPoint

class KeyStringValuePair(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class KeyIntValuePair(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: int
    def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...

class CPU(_message.Message):
    __slots__ = ("usagePercent",)
    USAGEPERCENT_FIELD_NUMBER: _ClassVar[int]
    usagePercent: float
    def __init__(self, usagePercent: _Optional[float] = ...) -> None: ...

class Instant(_message.Message):
    __slots__ = ("seconds", "nanos")
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    seconds: int
    nanos: int
    def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...
