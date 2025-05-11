from common import Command_pb2 as _Command_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ajax: _ClassVar[ErrorCategory]
    resource: _ClassVar[ErrorCategory]
    vue: _ClassVar[ErrorCategory]
    promise: _ClassVar[ErrorCategory]
    js: _ClassVar[ErrorCategory]
    unknown: _ClassVar[ErrorCategory]
ajax: ErrorCategory
resource: ErrorCategory
vue: ErrorCategory
promise: ErrorCategory
js: ErrorCategory
unknown: ErrorCategory

class BrowserPerfData(_message.Message):
    __slots__ = ("service", "serviceVersion", "time", "pagePath", "redirectTime", "dnsTime", "ttfbTime", "tcpTime", "transTime", "domAnalysisTime", "fptTime", "domReadyTime", "loadPageTime", "resTime", "sslTime", "ttlTime", "firstPackTime", "fmpTime")
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SERVICEVERSION_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    PAGEPATH_FIELD_NUMBER: _ClassVar[int]
    REDIRECTTIME_FIELD_NUMBER: _ClassVar[int]
    DNSTIME_FIELD_NUMBER: _ClassVar[int]
    TTFBTIME_FIELD_NUMBER: _ClassVar[int]
    TCPTIME_FIELD_NUMBER: _ClassVar[int]
    TRANSTIME_FIELD_NUMBER: _ClassVar[int]
    DOMANALYSISTIME_FIELD_NUMBER: _ClassVar[int]
    FPTTIME_FIELD_NUMBER: _ClassVar[int]
    DOMREADYTIME_FIELD_NUMBER: _ClassVar[int]
    LOADPAGETIME_FIELD_NUMBER: _ClassVar[int]
    RESTIME_FIELD_NUMBER: _ClassVar[int]
    SSLTIME_FIELD_NUMBER: _ClassVar[int]
    TTLTIME_FIELD_NUMBER: _ClassVar[int]
    FIRSTPACKTIME_FIELD_NUMBER: _ClassVar[int]
    FMPTIME_FIELD_NUMBER: _ClassVar[int]
    service: str
    serviceVersion: str
    time: int
    pagePath: str
    redirectTime: int
    dnsTime: int
    ttfbTime: int
    tcpTime: int
    transTime: int
    domAnalysisTime: int
    fptTime: int
    domReadyTime: int
    loadPageTime: int
    resTime: int
    sslTime: int
    ttlTime: int
    firstPackTime: int
    fmpTime: int
    def __init__(self, service: _Optional[str] = ..., serviceVersion: _Optional[str] = ..., time: _Optional[int] = ..., pagePath: _Optional[str] = ..., redirectTime: _Optional[int] = ..., dnsTime: _Optional[int] = ..., ttfbTime: _Optional[int] = ..., tcpTime: _Optional[int] = ..., transTime: _Optional[int] = ..., domAnalysisTime: _Optional[int] = ..., fptTime: _Optional[int] = ..., domReadyTime: _Optional[int] = ..., loadPageTime: _Optional[int] = ..., resTime: _Optional[int] = ..., sslTime: _Optional[int] = ..., ttlTime: _Optional[int] = ..., firstPackTime: _Optional[int] = ..., fmpTime: _Optional[int] = ...) -> None: ...

class BrowserErrorLog(_message.Message):
    __slots__ = ("uniqueId", "service", "serviceVersion", "time", "pagePath", "category", "grade", "message", "line", "col", "stack", "errorUrl", "firstReportedError")
    UNIQUEID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    SERVICEVERSION_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    PAGEPATH_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    GRADE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    COL_FIELD_NUMBER: _ClassVar[int]
    STACK_FIELD_NUMBER: _ClassVar[int]
    ERRORURL_FIELD_NUMBER: _ClassVar[int]
    FIRSTREPORTEDERROR_FIELD_NUMBER: _ClassVar[int]
    uniqueId: str
    service: str
    serviceVersion: str
    time: int
    pagePath: str
    category: ErrorCategory
    grade: str
    message: str
    line: int
    col: int
    stack: str
    errorUrl: str
    firstReportedError: bool
    def __init__(self, uniqueId: _Optional[str] = ..., service: _Optional[str] = ..., serviceVersion: _Optional[str] = ..., time: _Optional[int] = ..., pagePath: _Optional[str] = ..., category: _Optional[_Union[ErrorCategory, str]] = ..., grade: _Optional[str] = ..., message: _Optional[str] = ..., line: _Optional[int] = ..., col: _Optional[int] = ..., stack: _Optional[str] = ..., errorUrl: _Optional[str] = ..., firstReportedError: bool = ...) -> None: ...
