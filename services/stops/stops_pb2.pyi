from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AddStopRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class OperationResponse(_message.Message):
    __slots__ = ("success", "stop_id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STOP_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    stop_id: int
    def __init__(self, success: _Optional[bool] = ..., stop_id: _Optional[int] = ...) -> None: ...

class StopIdRequest(_message.Message):
    __slots__ = ("stop_id",)
    STOP_ID_FIELD_NUMBER: _ClassVar[int]
    stop_id: int
    def __init__(self, stop_id: _Optional[int] = ...) -> None: ...

class StopNameResponse(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class StopIdListRequest(_message.Message):
    __slots__ = ("stop_ids",)
    STOP_IDS_FIELD_NUMBER: _ClassVar[int]
    stop_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, stop_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class StopNameListResponse(_message.Message):
    __slots__ = ("names",)
    NAMES_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, names: _Optional[_Iterable[str]] = ...) -> None: ...
