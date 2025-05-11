from common import Common_pb2 as _Common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccessLogConnectionTLSMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Plain: _ClassVar[AccessLogConnectionTLSMode]
    TLS: _ClassVar[AccessLogConnectionTLSMode]

class AccessLogHTTPProtocolVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HTTP1: _ClassVar[AccessLogHTTPProtocolVersion]
    HTTP2: _ClassVar[AccessLogHTTPProtocolVersion]

class AccessLogTraceInfoProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Zipkin: _ClassVar[AccessLogTraceInfoProvider]
    SkyWalking: _ClassVar[AccessLogTraceInfoProvider]

class AccessLogHTTPProtocolRequestMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Get: _ClassVar[AccessLogHTTPProtocolRequestMethod]
    Post: _ClassVar[AccessLogHTTPProtocolRequestMethod]
    Put: _ClassVar[AccessLogHTTPProtocolRequestMethod]
    Delete: _ClassVar[AccessLogHTTPProtocolRequestMethod]
    Head: _ClassVar[AccessLogHTTPProtocolRequestMethod]
    Patch: _ClassVar[AccessLogHTTPProtocolRequestMethod]
    Options: _ClassVar[AccessLogHTTPProtocolRequestMethod]
    Trace: _ClassVar[AccessLogHTTPProtocolRequestMethod]
    Connect: _ClassVar[AccessLogHTTPProtocolRequestMethod]

class AccessLogKernelWriteSyscall(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Write: _ClassVar[AccessLogKernelWriteSyscall]
    Writev: _ClassVar[AccessLogKernelWriteSyscall]
    Send: _ClassVar[AccessLogKernelWriteSyscall]
    SendTo: _ClassVar[AccessLogKernelWriteSyscall]
    SendMsg: _ClassVar[AccessLogKernelWriteSyscall]
    SendMmsg: _ClassVar[AccessLogKernelWriteSyscall]
    SendFile: _ClassVar[AccessLogKernelWriteSyscall]
    SendFile64: _ClassVar[AccessLogKernelWriteSyscall]

class AccessLogKernelReadSyscall(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Read: _ClassVar[AccessLogKernelReadSyscall]
    Readv: _ClassVar[AccessLogKernelReadSyscall]
    Recv: _ClassVar[AccessLogKernelReadSyscall]
    RecvFrom: _ClassVar[AccessLogKernelReadSyscall]
    RecvMsg: _ClassVar[AccessLogKernelReadSyscall]
    RecvMmsg: _ClassVar[AccessLogKernelReadSyscall]

class AccessLogProtocolType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TCP: _ClassVar[AccessLogProtocolType]
    HTTP_1: _ClassVar[AccessLogProtocolType]
    HTTP_2: _ClassVar[AccessLogProtocolType]
Plain: AccessLogConnectionTLSMode
TLS: AccessLogConnectionTLSMode
HTTP1: AccessLogHTTPProtocolVersion
HTTP2: AccessLogHTTPProtocolVersion
Zipkin: AccessLogTraceInfoProvider
SkyWalking: AccessLogTraceInfoProvider
Get: AccessLogHTTPProtocolRequestMethod
Post: AccessLogHTTPProtocolRequestMethod
Put: AccessLogHTTPProtocolRequestMethod
Delete: AccessLogHTTPProtocolRequestMethod
Head: AccessLogHTTPProtocolRequestMethod
Patch: AccessLogHTTPProtocolRequestMethod
Options: AccessLogHTTPProtocolRequestMethod
Trace: AccessLogHTTPProtocolRequestMethod
Connect: AccessLogHTTPProtocolRequestMethod
Write: AccessLogKernelWriteSyscall
Writev: AccessLogKernelWriteSyscall
Send: AccessLogKernelWriteSyscall
SendTo: AccessLogKernelWriteSyscall
SendMsg: AccessLogKernelWriteSyscall
SendMmsg: AccessLogKernelWriteSyscall
SendFile: AccessLogKernelWriteSyscall
SendFile64: AccessLogKernelWriteSyscall
Read: AccessLogKernelReadSyscall
Readv: AccessLogKernelReadSyscall
Recv: AccessLogKernelReadSyscall
RecvFrom: AccessLogKernelReadSyscall
RecvMsg: AccessLogKernelReadSyscall
RecvMmsg: AccessLogKernelReadSyscall
TCP: AccessLogProtocolType
HTTP_1: AccessLogProtocolType
HTTP_2: AccessLogProtocolType

class EBPFAccessLogMessage(_message.Message):
    __slots__ = ("node", "connection", "kernelLogs", "protocolLog")
    NODE_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    KERNELLOGS_FIELD_NUMBER: _ClassVar[int]
    PROTOCOLLOG_FIELD_NUMBER: _ClassVar[int]
    node: EBPFAccessLogNodeInfo
    connection: AccessLogConnection
    kernelLogs: _containers.RepeatedCompositeFieldContainer[AccessLogKernelLog]
    protocolLog: AccessLogProtocolLogs
    def __init__(self, node: _Optional[_Union[EBPFAccessLogNodeInfo, _Mapping]] = ..., connection: _Optional[_Union[AccessLogConnection, _Mapping]] = ..., kernelLogs: _Optional[_Iterable[_Union[AccessLogKernelLog, _Mapping]]] = ..., protocolLog: _Optional[_Union[AccessLogProtocolLogs, _Mapping]] = ...) -> None: ...

class EBPFAccessLogNodeInfo(_message.Message):
    __slots__ = ("name", "netInterfaces", "bootTime", "clusterName", "policy")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NETINTERFACES_FIELD_NUMBER: _ClassVar[int]
    BOOTTIME_FIELD_NUMBER: _ClassVar[int]
    CLUSTERNAME_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    name: str
    netInterfaces: _containers.RepeatedCompositeFieldContainer[EBPFAccessLogNodeNetInterface]
    bootTime: _Common_pb2.Instant
    clusterName: str
    policy: EBPFAccessLogPolicy
    def __init__(self, name: _Optional[str] = ..., netInterfaces: _Optional[_Iterable[_Union[EBPFAccessLogNodeNetInterface, _Mapping]]] = ..., bootTime: _Optional[_Union[_Common_pb2.Instant, _Mapping]] = ..., clusterName: _Optional[str] = ..., policy: _Optional[_Union[EBPFAccessLogPolicy, _Mapping]] = ...) -> None: ...

class EBPFAccessLogPolicy(_message.Message):
    __slots__ = ("excludeNamespaces",)
    EXCLUDENAMESPACES_FIELD_NUMBER: _ClassVar[int]
    excludeNamespaces: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, excludeNamespaces: _Optional[_Iterable[str]] = ...) -> None: ...

class EBPFAccessLogNodeNetInterface(_message.Message):
    __slots__ = ("index", "mtu", "name")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    MTU_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    index: int
    mtu: int
    name: str
    def __init__(self, index: _Optional[int] = ..., mtu: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class AccessLogConnection(_message.Message):
    __slots__ = ("local", "remote", "role", "tlsMode", "protocol")
    LOCAL_FIELD_NUMBER: _ClassVar[int]
    REMOTE_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    TLSMODE_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    local: ConnectionAddress
    remote: ConnectionAddress
    role: _Common_pb2.DetectPoint
    tlsMode: AccessLogConnectionTLSMode
    protocol: AccessLogProtocolType
    def __init__(self, local: _Optional[_Union[ConnectionAddress, _Mapping]] = ..., remote: _Optional[_Union[ConnectionAddress, _Mapping]] = ..., role: _Optional[_Union[_Common_pb2.DetectPoint, str]] = ..., tlsMode: _Optional[_Union[AccessLogConnectionTLSMode, str]] = ..., protocol: _Optional[_Union[AccessLogProtocolType, str]] = ...) -> None: ...

class ConnectionAddress(_message.Message):
    __slots__ = ("kubernetes", "ip")
    KUBERNETES_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    kubernetes: KubernetesProcessAddress
    ip: IPAddress
    def __init__(self, kubernetes: _Optional[_Union[KubernetesProcessAddress, _Mapping]] = ..., ip: _Optional[_Union[IPAddress, _Mapping]] = ...) -> None: ...

class KubernetesProcessAddress(_message.Message):
    __slots__ = ("serviceName", "podName", "containerName", "processName", "port")
    SERVICENAME_FIELD_NUMBER: _ClassVar[int]
    PODNAME_FIELD_NUMBER: _ClassVar[int]
    CONTAINERNAME_FIELD_NUMBER: _ClassVar[int]
    PROCESSNAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    serviceName: str
    podName: str
    containerName: str
    processName: str
    port: int
    def __init__(self, serviceName: _Optional[str] = ..., podName: _Optional[str] = ..., containerName: _Optional[str] = ..., processName: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class IPAddress(_message.Message):
    __slots__ = ("host", "port")
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: int
    def __init__(self, host: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class AccessLogKernelLog(_message.Message):
    __slots__ = ("connect", "accept", "close", "read", "write")
    CONNECT_FIELD_NUMBER: _ClassVar[int]
    ACCEPT_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    READ_FIELD_NUMBER: _ClassVar[int]
    WRITE_FIELD_NUMBER: _ClassVar[int]
    connect: AccessLogKernelConnectOperation
    accept: AccessLogKernelAcceptOperation
    close: AccessLogKernelCloseOperation
    read: AccessLogKernelReadOperation
    write: AccessLogKernelWriteOperation
    def __init__(self, connect: _Optional[_Union[AccessLogKernelConnectOperation, _Mapping]] = ..., accept: _Optional[_Union[AccessLogKernelAcceptOperation, _Mapping]] = ..., close: _Optional[_Union[AccessLogKernelCloseOperation, _Mapping]] = ..., read: _Optional[_Union[AccessLogKernelReadOperation, _Mapping]] = ..., write: _Optional[_Union[AccessLogKernelWriteOperation, _Mapping]] = ...) -> None: ...

class AccessLogProtocolLogs(_message.Message):
    __slots__ = ("http",)
    HTTP_FIELD_NUMBER: _ClassVar[int]
    http: AccessLogHTTPProtocol
    def __init__(self, http: _Optional[_Union[AccessLogHTTPProtocol, _Mapping]] = ...) -> None: ...

class AccessLogHTTPProtocol(_message.Message):
    __slots__ = ("startTime", "endTime", "version", "request", "response")
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    startTime: EBPFTimestamp
    endTime: EBPFTimestamp
    version: AccessLogHTTPProtocolVersion
    request: AccessLogHTTPProtocolRequest
    response: AccessLogHTTPProtocolResponse
    def __init__(self, startTime: _Optional[_Union[EBPFTimestamp, _Mapping]] = ..., endTime: _Optional[_Union[EBPFTimestamp, _Mapping]] = ..., version: _Optional[_Union[AccessLogHTTPProtocolVersion, str]] = ..., request: _Optional[_Union[AccessLogHTTPProtocolRequest, _Mapping]] = ..., response: _Optional[_Union[AccessLogHTTPProtocolResponse, _Mapping]] = ...) -> None: ...

class AccessLogHTTPProtocolRequest(_message.Message):
    __slots__ = ("method", "path", "sizeOfHeadersBytes", "sizeOfBodyBytes", "trace")
    METHOD_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SIZEOFHEADERSBYTES_FIELD_NUMBER: _ClassVar[int]
    SIZEOFBODYBYTES_FIELD_NUMBER: _ClassVar[int]
    TRACE_FIELD_NUMBER: _ClassVar[int]
    method: AccessLogHTTPProtocolRequestMethod
    path: str
    sizeOfHeadersBytes: int
    sizeOfBodyBytes: int
    trace: AccessLogTraceInfo
    def __init__(self, method: _Optional[_Union[AccessLogHTTPProtocolRequestMethod, str]] = ..., path: _Optional[str] = ..., sizeOfHeadersBytes: _Optional[int] = ..., sizeOfBodyBytes: _Optional[int] = ..., trace: _Optional[_Union[AccessLogTraceInfo, _Mapping]] = ...) -> None: ...

class AccessLogHTTPProtocolResponse(_message.Message):
    __slots__ = ("statusCode", "sizeOfHeadersBytes", "sizeOfBodyBytes")
    STATUSCODE_FIELD_NUMBER: _ClassVar[int]
    SIZEOFHEADERSBYTES_FIELD_NUMBER: _ClassVar[int]
    SIZEOFBODYBYTES_FIELD_NUMBER: _ClassVar[int]
    statusCode: int
    sizeOfHeadersBytes: int
    sizeOfBodyBytes: int
    def __init__(self, statusCode: _Optional[int] = ..., sizeOfHeadersBytes: _Optional[int] = ..., sizeOfBodyBytes: _Optional[int] = ...) -> None: ...

class AccessLogTraceInfo(_message.Message):
    __slots__ = ("provider", "traceId", "traceSegmentId", "spanId")
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    TRACEID_FIELD_NUMBER: _ClassVar[int]
    TRACESEGMENTID_FIELD_NUMBER: _ClassVar[int]
    SPANID_FIELD_NUMBER: _ClassVar[int]
    provider: AccessLogTraceInfoProvider
    traceId: str
    traceSegmentId: str
    spanId: str
    def __init__(self, provider: _Optional[_Union[AccessLogTraceInfoProvider, str]] = ..., traceId: _Optional[str] = ..., traceSegmentId: _Optional[str] = ..., spanId: _Optional[str] = ...) -> None: ...

class AccessLogKernelConnectOperation(_message.Message):
    __slots__ = ("startTime", "endTime", "success")
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    startTime: EBPFTimestamp
    endTime: EBPFTimestamp
    success: bool
    def __init__(self, startTime: _Optional[_Union[EBPFTimestamp, _Mapping]] = ..., endTime: _Optional[_Union[EBPFTimestamp, _Mapping]] = ..., success: bool = ...) -> None: ...

class AccessLogKernelAcceptOperation(_message.Message):
    __slots__ = ("startTime", "endTime")
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    startTime: EBPFTimestamp
    endTime: EBPFTimestamp
    def __init__(self, startTime: _Optional[_Union[EBPFTimestamp, _Mapping]] = ..., endTime: _Optional[_Union[EBPFTimestamp, _Mapping]] = ...) -> None: ...

class AccessLogKernelCloseOperation(_message.Message):
    __slots__ = ("startTime", "endTime", "success")
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    startTime: EBPFTimestamp
    endTime: EBPFTimestamp
    success: bool
    def __init__(self, startTime: _Optional[_Union[EBPFTimestamp, _Mapping]] = ..., endTime: _Optional[_Union[EBPFTimestamp, _Mapping]] = ..., success: bool = ...) -> None: ...

class AccessLogKernelWriteOperation(_message.Message):
    __slots__ = ("startTime", "endTime", "syscall", "l4Metrics", "l3Metrics", "l2Metrics")
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    SYSCALL_FIELD_NUMBER: _ClassVar[int]
    L4METRICS_FIELD_NUMBER: _ClassVar[int]
    L3METRICS_FIELD_NUMBER: _ClassVar[int]
    L2METRICS_FIELD_NUMBER: _ClassVar[int]
    startTime: EBPFTimestamp
    endTime: EBPFTimestamp
    syscall: AccessLogKernelWriteSyscall
    l4Metrics: AccessLogKernelWriteL4Metrics
    l3Metrics: AccessLogKernelWriteL3Metrics
    l2Metrics: AccessLogKernelWriteL2Metrics
    def __init__(self, startTime: _Optional[_Union[EBPFTimestamp, _Mapping]] = ..., endTime: _Optional[_Union[EBPFTimestamp, _Mapping]] = ..., syscall: _Optional[_Union[AccessLogKernelWriteSyscall, str]] = ..., l4Metrics: _Optional[_Union[AccessLogKernelWriteL4Metrics, _Mapping]] = ..., l3Metrics: _Optional[_Union[AccessLogKernelWriteL3Metrics, _Mapping]] = ..., l2Metrics: _Optional[_Union[AccessLogKernelWriteL2Metrics, _Mapping]] = ...) -> None: ...

class AccessLogKernelWriteL4Metrics(_message.Message):
    __slots__ = ("totalDuration", "totalTransmitPackageCount", "totalRetransmitPackageCount", "lossPackageMetrics", "totalPackageSize")
    TOTALDURATION_FIELD_NUMBER: _ClassVar[int]
    TOTALTRANSMITPACKAGECOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTALRETRANSMITPACKAGECOUNT_FIELD_NUMBER: _ClassVar[int]
    LOSSPACKAGEMETRICS_FIELD_NUMBER: _ClassVar[int]
    TOTALPACKAGESIZE_FIELD_NUMBER: _ClassVar[int]
    totalDuration: int
    totalTransmitPackageCount: int
    totalRetransmitPackageCount: int
    lossPackageMetrics: _containers.RepeatedCompositeFieldContainer[AccessLogLossPackageMetrics]
    totalPackageSize: int
    def __init__(self, totalDuration: _Optional[int] = ..., totalTransmitPackageCount: _Optional[int] = ..., totalRetransmitPackageCount: _Optional[int] = ..., lossPackageMetrics: _Optional[_Iterable[_Union[AccessLogLossPackageMetrics, _Mapping]]] = ..., totalPackageSize: _Optional[int] = ...) -> None: ...

class AccessLogLossPackageMetrics(_message.Message):
    __slots__ = ("location", "count")
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    location: str
    count: int
    def __init__(self, location: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class AccessLogKernelWriteL3Metrics(_message.Message):
    __slots__ = ("totalDuration", "totalLocalDuration", "totalOutputDuration", "totalResolveMACCount", "totalResolveMACDuration", "totalNetFilterCount", "totalNetFilterDuration")
    TOTALDURATION_FIELD_NUMBER: _ClassVar[int]
    TOTALLOCALDURATION_FIELD_NUMBER: _ClassVar[int]
    TOTALOUTPUTDURATION_FIELD_NUMBER: _ClassVar[int]
    TOTALRESOLVEMACCOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTALRESOLVEMACDURATION_FIELD_NUMBER: _ClassVar[int]
    TOTALNETFILTERCOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTALNETFILTERDURATION_FIELD_NUMBER: _ClassVar[int]
    totalDuration: int
    totalLocalDuration: int
    totalOutputDuration: int
    totalResolveMACCount: int
    totalResolveMACDuration: int
    totalNetFilterCount: int
    totalNetFilterDuration: int
    def __init__(self, totalDuration: _Optional[int] = ..., totalLocalDuration: _Optional[int] = ..., totalOutputDuration: _Optional[int] = ..., totalResolveMACCount: _Optional[int] = ..., totalResolveMACDuration: _Optional[int] = ..., totalNetFilterCount: _Optional[int] = ..., totalNetFilterDuration: _Optional[int] = ...) -> None: ...

class AccessLogKernelWriteL2Metrics(_message.Message):
    __slots__ = ("totalDuration", "ifindex", "totalEnterQueueBufferCount", "totalReadySendDuration", "totalNetDeviceSendDuration")
    TOTALDURATION_FIELD_NUMBER: _ClassVar[int]
    IFINDEX_FIELD_NUMBER: _ClassVar[int]
    TOTALENTERQUEUEBUFFERCOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTALREADYSENDDURATION_FIELD_NUMBER: _ClassVar[int]
    TOTALNETDEVICESENDDURATION_FIELD_NUMBER: _ClassVar[int]
    totalDuration: int
    ifindex: int
    totalEnterQueueBufferCount: int
    totalReadySendDuration: int
    totalNetDeviceSendDuration: int
    def __init__(self, totalDuration: _Optional[int] = ..., ifindex: _Optional[int] = ..., totalEnterQueueBufferCount: _Optional[int] = ..., totalReadySendDuration: _Optional[int] = ..., totalNetDeviceSendDuration: _Optional[int] = ...) -> None: ...

class AccessLogKernelReadOperation(_message.Message):
    __slots__ = ("startTime", "endTime", "syscall", "l2Metrics", "l3Metrics", "l4Metrics")
    STARTTIME_FIELD_NUMBER: _ClassVar[int]
    ENDTIME_FIELD_NUMBER: _ClassVar[int]
    SYSCALL_FIELD_NUMBER: _ClassVar[int]
    L2METRICS_FIELD_NUMBER: _ClassVar[int]
    L3METRICS_FIELD_NUMBER: _ClassVar[int]
    L4METRICS_FIELD_NUMBER: _ClassVar[int]
    startTime: EBPFTimestamp
    endTime: EBPFTimestamp
    syscall: AccessLogKernelReadSyscall
    l2Metrics: AccessLogKernelReadL2Metrics
    l3Metrics: AccessLogKernelReadL3Metrics
    l4Metrics: AccessLogKernelReadL4Metrics
    def __init__(self, startTime: _Optional[_Union[EBPFTimestamp, _Mapping]] = ..., endTime: _Optional[_Union[EBPFTimestamp, _Mapping]] = ..., syscall: _Optional[_Union[AccessLogKernelReadSyscall, str]] = ..., l2Metrics: _Optional[_Union[AccessLogKernelReadL2Metrics, _Mapping]] = ..., l3Metrics: _Optional[_Union[AccessLogKernelReadL3Metrics, _Mapping]] = ..., l4Metrics: _Optional[_Union[AccessLogKernelReadL4Metrics, _Mapping]] = ...) -> None: ...

class AccessLogKernelReadL2Metrics(_message.Message):
    __slots__ = ("ifindex", "totalPackageCount", "totalPackageSize", "totalPackageToQueueDuration", "totalRcvPackageFromQueueDuration")
    IFINDEX_FIELD_NUMBER: _ClassVar[int]
    TOTALPACKAGECOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTALPACKAGESIZE_FIELD_NUMBER: _ClassVar[int]
    TOTALPACKAGETOQUEUEDURATION_FIELD_NUMBER: _ClassVar[int]
    TOTALRCVPACKAGEFROMQUEUEDURATION_FIELD_NUMBER: _ClassVar[int]
    ifindex: int
    totalPackageCount: int
    totalPackageSize: int
    totalPackageToQueueDuration: int
    totalRcvPackageFromQueueDuration: int
    def __init__(self, ifindex: _Optional[int] = ..., totalPackageCount: _Optional[int] = ..., totalPackageSize: _Optional[int] = ..., totalPackageToQueueDuration: _Optional[int] = ..., totalRcvPackageFromQueueDuration: _Optional[int] = ...) -> None: ...

class AccessLogKernelReadL3Metrics(_message.Message):
    __slots__ = ("totalDuration", "totalRecvDuration", "totalLocalDuration", "totalNetFilterCount", "totalNetFilterDuration")
    TOTALDURATION_FIELD_NUMBER: _ClassVar[int]
    TOTALRECVDURATION_FIELD_NUMBER: _ClassVar[int]
    TOTALLOCALDURATION_FIELD_NUMBER: _ClassVar[int]
    TOTALNETFILTERCOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTALNETFILTERDURATION_FIELD_NUMBER: _ClassVar[int]
    totalDuration: int
    totalRecvDuration: int
    totalLocalDuration: int
    totalNetFilterCount: int
    totalNetFilterDuration: int
    def __init__(self, totalDuration: _Optional[int] = ..., totalRecvDuration: _Optional[int] = ..., totalLocalDuration: _Optional[int] = ..., totalNetFilterCount: _Optional[int] = ..., totalNetFilterDuration: _Optional[int] = ...) -> None: ...

class AccessLogKernelReadL4Metrics(_message.Message):
    __slots__ = ("totalDuration",)
    TOTALDURATION_FIELD_NUMBER: _ClassVar[int]
    totalDuration: int
    def __init__(self, totalDuration: _Optional[int] = ...) -> None: ...

class EBPFTimestamp(_message.Message):
    __slots__ = ("offset",)
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    offset: EBPFOffsetTimestamp
    def __init__(self, offset: _Optional[_Union[EBPFOffsetTimestamp, _Mapping]] = ...) -> None: ...

class EBPFOffsetTimestamp(_message.Message):
    __slots__ = ("offset",)
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    offset: int
    def __init__(self, offset: _Optional[int] = ...) -> None: ...

class EBPFAccessLogDownstream(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
