import abc
from .meta import BaseBody as BaseBody, RequestMethod as RequestMethod, TogglEndpoint as TogglEndpoint
from .models import TogglProject as TogglProject, TogglWorkspace as TogglWorkspace
from .utility import format_iso as format_iso
from _typeshed import Incomplete
from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import date
from httpx import BasicAuth as BasicAuth, Client as Client, Response as Response, Timeout as Timeout
from toggl_api._exceptions import DateTimeError as DateTimeError
from typing import Any, ClassVar, Generic, Literal, TypeVar

ReportFormats: Incomplete
T = TypeVar('T')

@dataclass(frozen=True)
class PaginationOptions:
    page_size: int = field(default=50)
    next_id: int | None = field(default=None)
    next_row: int | None = field(default=None)

@dataclass
class PaginatedResult(Generic[T]):
    result: T = field()
    next_id: int | None = field(default=None)
    next_row: int | None = field(default=None)
    def __post_init__(self) -> None: ...
    def next_options(self, page_size: int = 50) -> PaginationOptions: ...

class InvalidExtensionError(ValueError): ...

@dataclass
class ReportBody(BaseBody):
    start_date: date | None = field(default=None)
    end_date: date | None = field(default=None)
    client_ids: list[int | None] = field(default_factory=list)
    description: str | None = field(default=None)
    group_ids: list[int] = field(default_factory=list)
    grouping: str | None = field(default=None, metadata={'endpoints': frozenset(('summary_time_entries', 'summary_report_pdf', 'summary_report_csv'))})
    grouped: bool = field(default=False, metadata={'endpoints': frozenset(('detail_search_time', 'detail_report_pdf', 'detail_report_csv', 'detail_totals'))})
    include_time_entry_ids: bool = field(default=True, metadata={'endpoints': frozenset(('summary_time_entries', 'summary_report_pdf', 'summary_report_csv'))})
    max_duration_seconds: int | None = field(default=None)
    min_duration_seconds: int | None = field(default=None)
    project_ids: list[int | None] = field(default_factory=list)
    rounding: int | None = field(default=None)
    rounding_minutes: Literal[0, 1, 5, 6, 10, 12, 15, 30, 60, 240] | None = field(default=None)
    sub_grouping: str | None = field(default=None, metadata={'endpoints': frozenset(('summary_time_entries', 'summary_report_pdf', 'summary_report_csv'))})
    tag_ids: list[int | None] = field(default_factory=list)
    time_entry_ids: list[int] = field(default_factory=list)
    user_ids: list[int] = field(default_factory=list)
    date_format: Literal['MM/DD/YYYY', 'DD-MM-YYYY', 'MM-DD-YYYY', 'YYYY-MM-DD', 'DD/MM/YYYY', 'DD.MM.YYYY'] = field(default='YYYY-MM-DD', metadata={'endpoints': frozenset(('summary_report_pdf', 'detail_report_pdf', 'weekly_report_pdf'))})
    duration_format: Literal['classic', 'decimal', 'improved'] = field(default='classic', metadata={'endpoints': frozenset(('summary_report_pdf', 'summary_report_csv', 'detailed_report_pdf', 'detailed_report_csv', 'weekly_report_pdf'))})
    order_by: Literal['title', 'duration'] | None = field(default=None, metadata={'endpoints': frozenset(('summary_report_pdf', 'summary_report_csv', 'detail_search_time', 'detail_report_pdf', 'detail_report_csv'))})
    order_dir: Literal['ASC', 'DESC'] | None = field(default=None, metadata={'endpoints': frozenset(('summary_report_pdf', 'summary_report_csv', 'detail_search_time', 'detail_report_pdf', 'detail_report_csv'))})
    resolution: str | None = field(default=None, metadata={'endpoints': frozenset(('summary_report_pdf', 'detail_totals'))})
    enrich_response: bool = field(default=False, metadata={'endpoints': frozenset(('detail_search_time', 'detail_report'))})
    def format(self, endpoint: str, **body: Any) -> dict[str, Any]: ...

class ReportEndpoint(TogglEndpoint[Any], metaclass=abc.ABCMeta):
    BASE_ENDPOINT: ClassVar[str]
    workspace_id: Incomplete
    def __init__(self, workspace_id: TogglWorkspace | int, auth: BasicAuth, *, client: Client | None = None, timeout: Timeout | int = 10, re_raise: bool = False, retries: int = 3) -> None: ...
    @abstractmethod
    def search_time_entries(self, body: ReportBody, *args: Any, **kwargs: Any) -> Any: ...
    @abstractmethod
    def export_report(self, body: ReportBody, *args: Any, **kwargs: Any) -> Any: ...

class SummaryReportEndpoint(ReportEndpoint):
    def project_summary(self, project: TogglProject | int, start_date: date | str, end_date: date | str) -> dict[str, int]: ...
    def project_summaries(self, start_date: date | str, end_date: date | str) -> list[dict[str, int]]: ...
    def search_time_entries(self, body: ReportBody) -> list[dict[str, int]]: ...
    def export_report(self, body: ReportBody, extension: ReportFormats, *, collapse: bool = False) -> bytes: ...
    @property
    def endpoint(self) -> str: ...

class DetailedReportEndpoint(ReportEndpoint):
    def search_time_entries(self, body: ReportBody, pagination: PaginationOptions | None = None, *, hide_amounts: bool = False) -> PaginatedResult[list[dict[str, Any]]]: ...
    def export_report(self, body: ReportBody, extension: ReportFormats, pagination: PaginationOptions | None = None, *, hide_amounts: bool = False) -> PaginatedResult[bytes]: ...
    def totals_report(self, body: ReportBody, *, granularity: Literal['day', 'week', 'month'] = 'day', with_graph: bool = False) -> dict[str, int]: ...
    @property
    def endpoint(self) -> str: ...

class WeeklyReportEndpoint(ReportEndpoint):
    def search_time_entries(self, body: ReportBody) -> list[dict[str, Any]]: ...
    def export_report(self, body: ReportBody, extension: ReportFormats) -> bytes: ...
    @property
    def endpoint(self) -> str: ...
