from .meta import BaseBody as BaseBody, RequestMethod as RequestMethod, TogglCachedEndpoint as TogglCachedEndpoint
from .meta.cache import TogglCache as TogglCache
from .models import TogglClient as TogglClient, TogglWorkspace as TogglWorkspace
from _typeshed import Incomplete
from dataclasses import dataclass, field
from httpx import BasicAuth as BasicAuth, Client as Client, Timeout as Timeout
from toggl_api._exceptions import NamingError as NamingError
from toggl_api.meta.cache import TogglQuery as TogglQuery
from typing import Any

log: Incomplete
CLIENT_STATUS: Incomplete

@dataclass
class ClientBody(BaseBody):
    name: str | None = field(default=None)
    status: CLIENT_STATUS | None = field(default=None)
    notes: str | None = field(default=None)
    def format(self, endpoint: str, **body: Any) -> dict[str, Any]: ...

class ClientEndpoint(TogglCachedEndpoint[TogglClient]):
    MODEL = TogglClient
    workspace_id: Incomplete
    def __init__(self, workspace_id: int | TogglWorkspace, auth: BasicAuth, cache: TogglCache[TogglClient] | None = None, *, client: Client | None = None, timeout: Timeout | int = 10, re_raise: bool = False, retries: int = 3) -> None: ...
    def add(self, body: ClientBody) -> TogglClient: ...
    def get(self, client_id: int | TogglClient, *, refresh: bool = False) -> TogglClient | None: ...
    def edit(self, client: TogglClient | int, body: ClientBody) -> TogglClient: ...
    def delete(self, client: TogglClient | int) -> None: ...
    def collect(self, body: ClientBody | None = None, *, refresh: bool = False) -> list[TogglClient]: ...
    @property
    def endpoint(self) -> str: ...
