from common import Common_pb2 as _Common_pb2
from common import Command_pb2 as _Command_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogData(_message.Message):
    __slots__ = ("timestamp", "service", "serviceInstance", "endpoint", "body", "traceContext", "tags", "layer")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    TRACECONTEXT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    service: str
    serviceInstance: str
    endpoint: str
    body: LogDataBody
    traceContext: TraceContext
    tags: LogTags
    layer: str
    def __init__(self, timestamp: _Optional[int] = ..., service: _Optional[str] = ..., serviceInstance: _Optional[str] = ..., endpoint: _Optional[str] = ..., body: _Optional[_Union[LogDataBody, _Mapping]] = ..., traceContext: _Optional[_Union[TraceContext, _Mapping]] = ..., tags: _Optional[_Union[LogTags, _Mapping]] = ..., layer: _Optional[str] = ...) -> None: ...

class LogDataBody(_message.Message):
    __slots__ = ("type", "text", "json", "yaml")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    JSON_FIELD_NUMBER: _ClassVar[int]
    YAML_FIELD_NUMBER: _ClassVar[int]
    type: str
    text: TextLog
    json: JSONLog
    yaml: YAMLLog
    def __init__(self, type: _Optional[str] = ..., text: _Optional[_Union[TextLog, _Mapping]] = ..., json: _Optional[_Union[JSONLog, _Mapping]] = ..., yaml: _Optional[_Union[YAMLLog, _Mapping]] = ...) -> None: ...

class TextLog(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class JSONLog(_message.Message):
    __slots__ = ("json",)
    JSON_FIELD_NUMBER: _ClassVar[int]
    json: str
    def __init__(self, json: _Optional[str] = ...) -> None: ...

class YAMLLog(_message.Message):
    __slots__ = ("yaml",)
    YAML_FIELD_NUMBER: _ClassVar[int]
    yaml: str
    def __init__(self, yaml: _Optional[str] = ...) -> None: ...

class TraceContext(_message.Message):
    __slots__ = ("traceId", "traceSegmentId", "spanId")
    TRACEID_FIELD_NUMBER: _ClassVar[int]
    TRACESEGMENTID_FIELD_NUMBER: _ClassVar[int]
    SPANID_FIELD_NUMBER: _ClassVar[int]
    traceId: str
    traceSegmentId: str
    spanId: int
    def __init__(self, traceId: _Optional[str] = ..., traceSegmentId: _Optional[str] = ..., spanId: _Optional[int] = ...) -> None: ...

class LogTags(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    def __init__(self, data: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ...) -> None: ...
