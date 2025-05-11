from ._decorators import UTCDateTime as UTCDateTime
from ._models import TogglClient as TogglClient, TogglOrganization as TogglOrganization, TogglProject as TogglProject, TogglTag as TogglTag, TogglTracker as TogglTracker, TogglWorkspace as TogglWorkspace
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine as Engine

def register_tables(engine: Engine) -> MetaData: ...
