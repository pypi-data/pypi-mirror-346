from ._exceptions import DateTimeError as DateTimeError, NamingError as NamingError
from .meta import BaseBody as BaseBody, RequestMethod as RequestMethod, TogglCachedEndpoint as TogglCachedEndpoint
from .meta.cache import Comparison as Comparison, TogglCache as TogglCache, TogglQuery as TogglQuery
from .models import TogglWorkspace as TogglWorkspace
from .utility import get_timestamp as get_timestamp
from _typeshed import Incomplete
from dataclasses import dataclass, field
from datetime import datetime
from httpx import BasicAuth as BasicAuth, Client as Client, Response as Response, Timeout as Timeout
from toggl_api import TogglOrganization as TogglOrganization
from typing import Any, Literal, TypedDict

log: Incomplete

@dataclass
class WorkspaceBody(BaseBody):
    name: str | None = field(default=None)
    admins: list[int] = field(default_factory=list, metadata={'endpoints': frozenset(('add', 'edit'))})
    only_admins_may_create_projects: bool = field(default=False, metadata={'endpoints': frozenset(('add', 'edit'))})
    only_admins_may_create_tags: bool = field(default=False, metadata={'endpoints': frozenset(('add', 'edit'))})
    only_admins_see_billable_rates: bool = field(default=False, metadata={'endpoints': frozenset(('add', 'edit'))})
    only_admins_see_team_dashboard: bool = field(default=False, metadata={'endpoints': frozenset(('add', 'edit'))})
    projects_billable_by_default: bool = field(default=False, metadata={'endpoints': frozenset(('add', 'edit'))})
    projects_enforce_billable: bool = field(default=False, metadata={'endpoints': frozenset(('add', 'edit'))})
    projects_private_by_default: bool = field(default=False, metadata={'endpoints': frozenset(('add', 'edit'))})
    rate_change_mode: Literal['start-today', 'override-current', 'override-all'] | None = field(default=None, metadata={'endpoints': frozenset(('add', 'edit'))})
    reports_collapse: bool = field(default=False, metadata={'endpoints': frozenset(('add', 'edit'))})
    rounding: int | None = field(default=None, metadata={'endpoints': frozenset(('add', 'edit'))})
    rounding_minutes: int | None = field(default=None, metadata={'endpoints': frozenset(('add', 'edit'))})
    def __post_init__(self) -> None: ...
    def format(self, endpoint: str, **body: Any) -> dict[str, Any]: ...

class User(TypedDict):
    user_id: int
    name: str

class WorkspaceStatistics(TypedDict):
    admins: list[User]
    groups_count: int
    members_count: int

class WorkspaceEndpoint(TogglCachedEndpoint[TogglWorkspace]):
    MODEL = TogglWorkspace
    organization_id: Incomplete
    def __init__(self, organization_id: int | TogglOrganization, auth: BasicAuth, cache: TogglCache[TogglWorkspace] | None = None, *, client: Client | None = None, timeout: Timeout | int = 10, re_raise: bool = False, retries: int = 3) -> None: ...
    def get(self, workspace: TogglWorkspace | int, *, refresh: bool = False) -> TogglWorkspace | None: ...
    def add(self, body: WorkspaceBody) -> TogglWorkspace: ...
    def collect(self, since: datetime | int | None = None, *, refresh: bool = False) -> list[TogglWorkspace]: ...
    def edit(self, workspace_id: TogglWorkspace | int, body: WorkspaceBody) -> TogglWorkspace: ...
    def tracker_constraints(self, workspace_id: TogglWorkspace | int) -> dict[str, bool]: ...
    def statistics(self, workspace_id: TogglWorkspace | int) -> WorkspaceStatistics: ...
