from _typeshed import Incomplete
from faker import Faker
from faker.typing import SeedType as SeedType
from random import Random
from toggl_api import ProjectEndpoint as ProjectEndpoint, TogglClient as TogglClient, TogglOrganization as TogglOrganization, TogglProject as TogglProject, TogglTag as TogglTag, TogglTracker as TogglTracker, TogglWorkspace as TogglWorkspace
from toggl_api.meta._enums import RequestMethod as RequestMethod
from toggl_api.meta.cache._json_cache import JSONCache as JSONCache
from toggl_api.models import TogglClass as TogglClass, WorkspaceChild as WorkspaceChild, register_tables as register_tables
from typing import NamedTuple, TypeVar, TypedDict

msg: str
sqlalchemy: bool
log: Incomplete

class RandomSpec(TypedDict):
    faker: Faker
    random: Random
    total: int

class WorkspaceSpec(RandomSpec):
    workspaces: list[TogglWorkspace]
T = TypeVar('T', bound=WorkspaceChild)
Model = TypeVar('Model', bound=TogglClass)

class FakeEndpoint(NamedTuple):
    MODEL: type[TogglClass]

def main() -> None: ...
