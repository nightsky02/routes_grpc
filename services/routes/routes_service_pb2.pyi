from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddRouteRequest(_message.Message):
    __slots__ = ("number", "route_start", "route_end", "stop_ids")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    ROUTE_START_FIELD_NUMBER: _ClassVar[int]
    ROUTE_END_FIELD_NUMBER: _ClassVar[int]
    STOP_IDS_FIELD_NUMBER: _ClassVar[int]
    number: int
    route_start: str
    route_end: str
    stop_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, number: _Optional[int] = ..., route_start: _Optional[str] = ..., route_end: _Optional[str] = ..., stop_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class RouteOperationResponse(_message.Message):
    __slots__ = ("error", "msg")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    error: bool
    msg: str
    def __init__(self, error: _Optional[bool] = ..., msg: _Optional[str] = ...) -> None: ...

class Route(_message.Message):
    __slots__ = ("number", "route_start", "route_end", "stop_ids")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    ROUTE_START_FIELD_NUMBER: _ClassVar[int]
    ROUTE_END_FIELD_NUMBER: _ClassVar[int]
    STOP_IDS_FIELD_NUMBER: _ClassVar[int]
    number: int
    route_start: str
    route_end: str
    stop_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, number: _Optional[int] = ..., route_start: _Optional[str] = ..., route_end: _Optional[str] = ..., stop_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class RouteListResponse(_message.Message):
    __slots__ = ("routes",)
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    routes: _containers.RepeatedCompositeFieldContainer[Route]
    def __init__(self, routes: _Optional[_Iterable[_Union[Route, _Mapping]]] = ...) -> None: ...
