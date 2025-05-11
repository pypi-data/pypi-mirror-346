from ._async_sqlite_cache import AsyncSqliteCache as AsyncSqliteCache
from _typeshed import Incomplete
from abc import ABC
from collections.abc import Iterable
from httpx import AsyncClient, BasicAuth as BasicAuth, Headers, Request as Request, Response, Timeout, URL
from toggl_api._exceptions import NoCacheAssignedError as NoCacheAssignedError
from toggl_api.meta import RequestMethod as RequestMethod
from toggl_api.models import TogglClass as TogglClass
from typing import Any, ClassVar, Final, Generic, TypeVar

log: Incomplete
T = TypeVar('T', bound=TogglClass)

class TogglAsyncEndpoint(ABC, Generic[T]):
    BASE_ENDPOINT: ClassVar[URL]
    HEADERS: Final[Headers]
    MODEL: type[T] | None
    client: Incomplete
    re_raise: Incomplete
    retries: Incomplete
    def __init__(self, auth: BasicAuth, *, client: AsyncClient | None = None, timeout: Timeout | int = 10, re_raise: bool = False, retries: int = 3) -> None: ...
    async def request(self, parameters: str, headers: Headers | None = None, body: dict[str, Any] | list[dict[str, Any]] | None = None, method: RequestMethod = ..., *, raw: bool = False, retries: int | None = None) -> T | list[T] | Response | None: ...
    @classmethod
    def process_models(cls, data: list[dict[str, Any]]) -> list[T]: ...
    @staticmethod
    async def api_status() -> bool: ...

class TogglAsyncCachedEndpoint(TogglAsyncEndpoint[T]):
    def __init__(self, auth: BasicAuth, cache: AsyncSqliteCache[T] | None = None, *, client: AsyncClient | None = None, timeout: int = 10, re_raise: bool = False, retries: int = 3) -> None: ...
    async def request(self, parameters: str, headers: Headers | None = None, body: dict[str, Any] | list[Any] | None = None, method: RequestMethod = ..., *, refresh: bool = False, raw: bool = False) -> T | list[T] | Response | None: ...
    async def load_cache(self) -> Iterable[T]: ...
    async def save_cache(self, response: list[T] | T, method: RequestMethod) -> None: ...
    @property
    def cache(self) -> AsyncSqliteCache[T] | None: ...
    @cache.setter
    def cache(self, value: AsyncSqliteCache[T] | None) -> None: ...
