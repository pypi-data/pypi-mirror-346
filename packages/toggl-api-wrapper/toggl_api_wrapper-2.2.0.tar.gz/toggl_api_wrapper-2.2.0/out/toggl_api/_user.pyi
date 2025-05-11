from .meta import TogglEndpoint as TogglEndpoint
from _typeshed import Incomplete
from httpx import BasicAuth as BasicAuth, Client, Response as Response, Timeout as Timeout
from typing import Any

log: Incomplete

class UserEndpoint(TogglEndpoint[Any]):
    def __init__(self, auth: BasicAuth, *, client: Client | None = None, timeout: Timeout | int = 10, re_raise: bool = False, retries: int = 3) -> None: ...
    @staticmethod
    def verify_authentication(auth: BasicAuth, *, client: Client | None = None) -> bool: ...
    def get_details(self) -> dict[str, Any]: ...
