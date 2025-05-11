from ._enums import RequestMethod as RequestMethod
from _typeshed import Incomplete
from abc import ABC
from httpx import BasicAuth as BasicAuth, Client, Headers, Request as Request, Response as Response, Timeout
from toggl_api.models import TogglClass as TogglClass
from typing import Any, ClassVar, Final, Generic, TypeVar

log: Incomplete
T = TypeVar('T', bound=TogglClass)

class TogglEndpoint(ABC, Generic[T]):
    BASE_ENDPOINT: ClassVar[str]
    HEADERS: Final[Headers]
    MODEL: type[T] | None
    re_raise: Incomplete
    retries: Incomplete
    client: Incomplete
    def __init__(self, auth: BasicAuth, *, client: Client | None = None, timeout: Timeout | int = 10, re_raise: bool = False, retries: int = 3) -> None: ...
    def request(self, parameters: str, headers: Headers | None = None, body: dict[str, Any] | list[dict[str, Any]] | None = None, method: RequestMethod = ..., *, raw: bool = False, retries: int | None = None) -> T | list[T] | Response | None: ...
    @classmethod
    def process_models(cls, data: list[dict[str, Any]]) -> list[T]: ...
    @staticmethod
    def api_status() -> bool: ...
