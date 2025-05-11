from ._async_endpoint import TogglAsyncEndpoint as TogglAsyncEndpoint
from _typeshed import Incomplete
from httpx import AsyncClient as AsyncClient, BasicAuth as BasicAuth, Response as Response
from typing import Any

log: Incomplete

class AsyncUserEndpoint(TogglAsyncEndpoint[Any]):
    def __init__(self, auth: BasicAuth, *, client: AsyncClient | None = None, timeout: int = 10, re_raise: bool = False, retries: int = 3) -> None: ...
    async def get_details(self) -> dict[str, Any]: ...
