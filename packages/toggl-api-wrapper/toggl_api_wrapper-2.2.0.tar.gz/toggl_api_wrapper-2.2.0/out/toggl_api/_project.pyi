from .meta import BaseBody as BaseBody, RequestMethod as RequestMethod, TogglCachedEndpoint as TogglCachedEndpoint
from .models import TogglProject as TogglProject, TogglWorkspace as TogglWorkspace
from _typeshed import Incomplete
from dataclasses import dataclass, field
from datetime import date
from httpx import BasicAuth as BasicAuth, Client as Client, Timeout as Timeout
from toggl_api._exceptions import NamingError as NamingError
from toggl_api.meta.cache import Comparison as Comparison, TogglCache as TogglCache, TogglQuery as TogglQuery
from toggl_api.utility import format_iso as format_iso, get_timestamp as get_timestamp
from typing import Any, Final, Literal

log: Incomplete

@dataclass
class ProjectBody(BaseBody):
    name: str | None = field(default=None)
    active: bool | Literal['both'] = field(default=True)
    is_private: bool | None = field(default=True, metadata={'endpoints': frozenset(('edit', 'add'))})
    client_id: int | None = field(default=None, metadata={'endpoints': frozenset(('edit', 'add'))})
    client_name: str | None = field(default=None, metadata={'endpoints': frozenset(('edit', 'add'))})
    color: str | None = field(default=None, metadata={'endpoints': frozenset(('edit', 'add'))})
    start_date: date | None = field(default=None, metadata={'endpoints': frozenset(('edit', 'add'))})
    end_date: date | None = field(default=None, metadata={'endpoints': frozenset(('edit', 'add'))})
    since: date | int | None = field(default=None, metadata={'endpoints': frozenset(('collect',))})
    user_ids: list[int] = field(default_factory=list, metadata={'endpoints': frozenset(('collect',))})
    client_ids: list[int] = field(default_factory=list, metadata={'endpoints': frozenset(('collect',))})
    group_ids: list[int] = field(default_factory=list, metadata={'endpoints': frozenset(('collect',))})
    statuses: list[TogglProject.Status] = field(default_factory=list, metadata={'endpoints': frozenset(('collect',))})
    def format(self, endpoint: str, **body: Any) -> dict[str, Any]: ...

class ProjectEndpoint(TogglCachedEndpoint[TogglProject]):
    MODEL = TogglProject
    BASIC_COLORS: Final[dict[str, str]]
    workspace_id: Incomplete
    def __init__(self, workspace_id: int | TogglWorkspace, auth: BasicAuth, cache: TogglCache[TogglProject] | None = None, *, client: Client | None = None, timeout: Timeout | int = 10, re_raise: bool = False, retries: int = 3) -> None: ...
    @staticmethod
    def status_to_query(status: TogglProject.Status) -> list[TogglQuery[Any]]: ...
    def collect(self, body: ProjectBody | None = None, *, refresh: bool = False, sort_pinned: bool = False, only_me: bool = False, only_templates: bool = False) -> list[TogglProject]: ...
    def get(self, project_id: int | TogglProject, *, refresh: bool = False) -> TogglProject | None: ...
    def delete(self, project: TogglProject | int) -> None: ...
    def edit(self, project: TogglProject | int, body: ProjectBody) -> TogglProject: ...
    def add(self, body: ProjectBody) -> TogglProject: ...
    @classmethod
    def get_color(cls, name: str) -> str: ...
    @classmethod
    def get_color_id(cls, color: str) -> int: ...
    @property
    def endpoint(self) -> str: ...
