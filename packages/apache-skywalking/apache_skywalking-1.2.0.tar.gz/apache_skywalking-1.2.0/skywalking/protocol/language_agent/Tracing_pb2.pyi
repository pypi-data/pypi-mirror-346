from common import Common_pb2 as _Common_pb2
from common import Command_pb2 as _Command_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpanType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Entry: _ClassVar[SpanType]
    Exit: _ClassVar[SpanType]
    Local: _ClassVar[SpanType]

class RefType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CrossProcess: _ClassVar[RefType]
    CrossThread: _ClassVar[RefType]

class SpanLayer(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Unknown: _ClassVar[SpanLayer]
    Database: _ClassVar[SpanLayer]
    RPCFramework: _ClassVar[SpanLayer]
    Http: _ClassVar[SpanLayer]
    MQ: _ClassVar[SpanLayer]
    Cache: _ClassVar[SpanLayer]
    FAAS: _ClassVar[SpanLayer]
Entry: SpanType
Exit: SpanType
Local: SpanType
CrossProcess: RefType
CrossThread: RefType
Unknown: SpanLayer
Database: SpanLayer
RPCFramework: SpanLayer
Http: SpanLayer
MQ: SpanLayer
Cache: SpanLayer
FAAS: SpanLayer

class SegmentObject(_message.Message):
    __slots__ = ("traceId", "traceSegmentId", "spans", "service", "serviceInstance", "isSizeLimited")
    TRACEID_FIELD_NUMBER: _ClassVar[int]
    TRACESEGMENTID_FIELD_NUMBER: _ClassVar[int]
    SPANS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    ISSIZELIMITED_FIELD_NUMBER: _ClassVar[int]
    traceId: str
    traceSegmentId: str
    spans: _containers.RepeatedCompositeFieldContainer[SpanObject]
    service: str
    serviceInstance: str
    isSizeLimited: bool
    def __init__(self, traceId: _Optional[str] = ..., traceSegmentId: _Optional[str] = ..., spans: _Optional[_Iterable[_Union[SpanObject, _Mapping]]] = ..., service: _Optional[str] = ..., serviceInstance: _Optional[str] = ..., isSizeLimited: bool = ...) -> None: ...

class SegmentReference(_message.Message):
    __slots__ = ("refType", "traceId", "parentTraceSegmentId", "parentSpanId", "parentService", "parentServiceInstance", "parentEndpoint", "networkAddressUsedAtPeer")
    REFTYPE_FIELD_NUMBER: _ClassVar[int]
    TRACEID_FIELD_NUMBER: _ClassVar[int]
    PARENTTRACESEGMENTID_FIELD_NUMBER: _ClassVar[int]
    PARENTSPANID_FIELD_NUMBER: _ClassVar[int]
    PARENTSERVICE_FIELD_NUMBER: _ClassVar[int]
    PARENTSERVICEINSTANCE_FIELD_NUMBER: _ClassVar[int]
    PARENTENDPOINT_FIELD_NUMBER: _ClassVar[int]
    NETWORKADDRESSUSEDATPEER_FIELD_NUMBER: _ClassVar[int]
    refType: RefType
    traceId: str
    parentTraceSegmentId: str
    parentSpanId: int
    parentService: str
    parentServiceInstance: str
    parentEndpoint: str
    networkAddressUsedAtPeer: str
    def __init__(self, refType: _Optional[_Union[RefType, str]] = ..., traceId: _Optional[str] = ..., parentTraceSegmentId: _Optional[str] = ..., parentSpanId: _Optional[int] = ..., parentService: _Optional[str] = ..., parentServiceInstance: _Optional[str] = ..., parentEndpoint: _Optional[str] = ..., networkAddressUsedAtPeer: _Optional[str] = ...) -> None: ...

class SpanObject(_message.Message):
    __slots__ = ("spanId", "parentSpanId", "startTime", "endTime", "refs", "operationName", "peer", "spanType", "spanLayer", "componentId", "isError", "tags", "logs", "skipAnalysis")
    SPANID_FIELD_NUMBER: _ClassVar[int]
    PARENTSPANID_FIELD_NUMBER: _ClassVar[int]
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    REFS_FIELD_NUMBER: _ClassVar[int]
    OPERATIONNAME_FIELD_NUMBER: _ClassVar[int]
    PEER_FIELD_NUMBER: _ClassVar[int]
    SPANTYPE_FIELD_NUMBER: _ClassVar[int]
    SPANLAYER_FIELD_NUMBER: _ClassVar[int]
    COMPONENTID_FIELD_NUMBER: _ClassVar[int]
    ISERROR_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    SKIPANALYSIS_FIELD_NUMBER: _ClassVar[int]
    spanId: int
    parentSpanId: int
    startTime: int
    endTime: int
    refs: _containers.RepeatedCompositeFieldContainer[SegmentReference]
    operationName: str
    peer: str
    spanType: SpanType
    spanLayer: SpanLayer
    componentId: int
    isError: bool
    tags: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    logs: _containers.RepeatedCompositeFieldContainer[Log]
    skipAnalysis: bool
    def __init__(self, spanId: _Optional[int] = ..., parentSpanId: _Optional[int] = ..., startTime: _Optional[int] = ..., endTime: _Optional[int] = ..., refs: _Optional[_Iterable[_Union[SegmentReference, _Mapping]]] = ..., operationName: _Optional[str] = ..., peer: _Optional[str] = ..., spanType: _Optional[_Union[SpanType, str]] = ..., spanLayer: _Optional[_Union[SpanLayer, str]] = ..., componentId: _Optional[int] = ..., isError: bool = ..., tags: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ..., logs: _Optional[_Iterable[_Union[Log, _Mapping]]] = ..., skipAnalysis: bool = ...) -> None: ...

class Log(_message.Message):
    __slots__ = ("time", "data")
    TIME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    time: int
    data: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    def __init__(self, time: _Optional[int] = ..., data: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ...) -> None: ...

class ID(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[_Iterable[str]] = ...) -> None: ...

class SegmentCollection(_message.Message):
    __slots__ = ("segments",)
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[SegmentObject]
    def __init__(self, segments: _Optional[_Iterable[_Union[SegmentObject, _Mapping]]] = ...) -> None: ...

class SpanAttachedEvent(_message.Message):
    __slots__ = ("startTime", "event", "endTime", "tags", "summary", "traceContext")
    class SpanReferenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SKYWALKING: _ClassVar[SpanAttachedEvent.SpanReferenceType]
        ZIPKIN: _ClassVar[SpanAttachedEvent.SpanReferenceType]
    SKYWALKING: SpanAttachedEvent.SpanReferenceType
    ZIPKIN: SpanAttachedEvent.SpanReferenceType
    class SpanReference(_message.Message):
        __slots__ = ("type", "traceId", "traceSegmentId", "spanId")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        TRACEID_FIELD_NUMBER: _ClassVar[int]
        TRACESEGMENTID_FIELD_NUMBER: _ClassVar[int]
        SPANID_FIELD_NUMBER: _ClassVar[int]
        type: SpanAttachedEvent.SpanReferenceType
        traceId: str
        traceSegmentId: str
        spanId: str
        def __init__(self, type: _Optional[_Union[SpanAttachedEvent.SpanReferenceType, str]] = ..., traceId: _Optional[str] = ..., traceSegmentId: _Optional[str] = ..., spanId: _Optional[str] = ...) -> None: ...
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    TRACECONTEXT_FIELD_NUMBER: _ClassVar[int]
    startTime: _Common_pb2.Instant
    event: str
    endTime: _Common_pb2.Instant
    tags: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyStringValuePair]
    summary: _containers.RepeatedCompositeFieldContainer[_Common_pb2.KeyIntValuePair]
    traceContext: SpanAttachedEvent.SpanReference
    def __init__(self, startTime: _Optional[_Union[_Common_pb2.Instant, _Mapping]] = ..., event: _Optional[str] = ..., endTime: _Optional[_Union[_Common_pb2.Instant, _Mapping]] = ..., tags: _Optional[_Iterable[_Union[_Common_pb2.KeyStringValuePair, _Mapping]]] = ..., summary: _Optional[_Iterable[_Union[_Common_pb2.KeyIntValuePair, _Mapping]]] = ..., traceContext: _Optional[_Union[SpanAttachedEvent.SpanReference, _Mapping]] = ...) -> None: ...
