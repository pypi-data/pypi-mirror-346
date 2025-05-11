from _typeshed import Incomplete
from datetime import datetime
from sqlalchemy import Dialect as Dialect
from sqlalchemy.types import TypeDecorator

class UTCDateTime(TypeDecorator[datetime]):
    impl: Incomplete
    cache_ok: bool
    def process_bind_param(self, value: datetime | None, _dialect: Dialect) -> datetime | None: ...
    def process_result_value(self, value: datetime | None, _dialect: Dialect) -> datetime | None: ...
