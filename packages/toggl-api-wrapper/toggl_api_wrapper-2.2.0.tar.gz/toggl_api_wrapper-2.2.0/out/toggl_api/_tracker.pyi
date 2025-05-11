from ._exceptions import DateTimeError as DateTimeError, NamingError as NamingError
from .meta import BaseBody as BaseBody, RequestMethod as RequestMethod, TogglCachedEndpoint as TogglCachedEndpoint
from .meta.cache import Comparison as Comparison, TogglQuery as TogglQuery
from .models import TogglTracker as TogglTracker
from .utility import format_iso as format_iso, get_timestamp as get_timestamp
from _typeshed import Incomplete
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from httpx import BasicAuth as BasicAuth, Client as Client, Response as Response, Timeout as Timeout
from toggl_api import TogglWorkspace as TogglWorkspace
from toggl_api.meta.cache import TogglCache as TogglCache
from typing import Any, Final, Literal, NamedTuple, TypedDict

log: Incomplete

class BulkEditParameter(TypedDict):
    op: Literal['add', 'remove', 'replace']
    path: str
    value: Any

class Edits(NamedTuple):
    successes: list[int]
    failures: list[int]

@dataclass
class TrackerBody(BaseBody):
    description: str | None = field(default=None, metadata={'endpoints': frozenset(('add', 'edit', 'bulk_edit'))})
    duration: int | timedelta | None = field(default=None, metadata={'endpoints': ('add', 'edit')})
    project_id: int | None = field(default=None, metadata={'endpoints': ('add', 'edit')})
    start: datetime | None = field(default=None, metadata={'endpoints': ('add', 'edit', 'bulk_edit')})
    stop: datetime | None = field(default=None, metadata={'endpoints': ('add', 'edit', 'bulk_edit')})
    tag_action: Literal['add', 'remove'] | None = field(default=None, metadata={'endpoints': ('add', 'edit', 'bulk_edit')})
    tag_ids: list[int] = field(default_factory=list, metadata={'endpoints': ('add', 'edit')})
    tags: list[str] = field(default_factory=list, metadata={'endpoints': ('add', 'edit', 'bulk_edit')})
    shared_with_user_ids: list[int] = field(default_factory=list, metadata={'endpoints': ('add', 'edit')})
    created_with: str = field(default='toggl-api-wrapper', metadata={'endpoints': ('add', 'edit')})
    def format(self, endpoint: str, **body: Any) -> dict[str, Any]: ...

class TrackerEndpoint(TogglCachedEndpoint[TogglTracker]):
    MODEL = TogglTracker
    TRACKER_ALREADY_STOPPED: Final[int]
    TRACKER_NOT_RUNNING: Final[int]
    workspace_id: Incomplete
    def __init__(self, workspace_id: int | TogglWorkspace, auth: BasicAuth, cache: TogglCache[TogglTracker] | None = None, *, client: Client | None = None, timeout: Timeout | int = 10, re_raise: bool = False, retries: int = 3) -> None: ...
    def current(self, *, refresh: bool = True) -> TogglTracker | None: ...
    def collect(self, since: int | datetime | None = None, before: date | None = None, start_date: date | None = None, end_date: date | None = None, *, refresh: bool = False) -> list[TogglTracker]: ...
    def get(self, tracker_id: int | TogglTracker, *, refresh: bool = False) -> TogglTracker | None: ...
    def edit(self, tracker: TogglTracker | int, body: TrackerBody, *, meta: bool = False) -> TogglTracker: ...
    def bulk_edit(self, *trackers: int | TogglTracker, body: TrackerBody) -> Edits: ...
    def delete(self, tracker: TogglTracker | int) -> None: ...
    def stop(self, tracker: TogglTracker | int) -> TogglTracker | None: ...
    def add(self, body: TrackerBody) -> TogglTracker: ...
    @property
    def endpoint(self) -> str: ...
