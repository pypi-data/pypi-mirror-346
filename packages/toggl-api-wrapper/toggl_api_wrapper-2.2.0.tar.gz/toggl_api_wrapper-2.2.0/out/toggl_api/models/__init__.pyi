from ._models import TogglClass as TogglClass, TogglClient as TogglClient, TogglOrganization as TogglOrganization, TogglProject as TogglProject, TogglTag as TogglTag, TogglTracker as TogglTracker, TogglWorkspace as TogglWorkspace, WorkspaceChild as WorkspaceChild
from ._schema import register_tables as register_tables
from typing import Any

__all__ = ['TogglClass', 'TogglClient', 'TogglOrganization', 'TogglProject', 'TogglTag', 'TogglTracker', 'TogglWorkspace', 'WorkspaceChild', 'as_dict_custom', 'register_tables']

def as_dict_custom(obj: TogglClass) -> dict[str, Any]: ...
