"""FakePool — In-memory fake for asyncpg Pool."""

from contextlib import asynccontextmanager
from typing import AsyncIterator
from pyfakepg.fake_connection import FakeConnection
from pyfakepg.fake_rows import FakeRows


class FakePool:
    """
    In-memory fake implementation of Pool.
    Accepts FakeRows objects as constructor arguments — one per query pattern.
    acquire() returns a FakeConnection loaded with all registered FakeRows.
    100% Code-Free Constructor (Elegant Objects).

    Usage:
        pool = FakePool(
            FakeRows("SELECT * FROM users", {"id": "usr_1", "name": "Max"}),
            FakeRows("SELECT * FROM tenants", {"id": "t_1"}, {"id": "t_2"}),
        )
        async with pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", "usr_1")
    """

    def __init__(self, *rows: FakeRows) -> None:
        self._rows = rows

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[FakeConnection]:
        """Yield a FakeConnection loaded with all registered FakeRows."""
        yield FakeConnection(self._rows)

    async def close(self) -> None:
        """No-op — nothing to close in memory."""
        pass
