"""FakePool — In-memory fake for asyncpg Pool."""

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator
from pyfakepg.fake_connection import FakeConnection


class FakePool:
    """
    In-memory fake implementation of Pool.
    Provides a composable builder API to register query-to-rows mappings.
    acquire() returns a FakeConnection loaded with all registered rows.
    100% Code-Free Constructor (Elegant Objects).

    Usage:
        pool = (
            FakePool()
            .with_rows("SELECT * FROM users", [{"id": "1", "name": "Max"}])
            .with_rows("SELECT * FROM tenants", [{"id": "t_1", "name": "Acme"}])
        )
        async with pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM users WHERE id = $1", "1")
    """

    def __init__(
        self,
        rows: tuple[tuple[str, list[dict[str, Any]]], ...] = (),
    ) -> None:
        self._rows = rows

    def with_rows(
        self,
        query_substr: str,
        rows: list[dict[str, Any]],
    ) -> "FakePool":
        """Return a new FakePool with an additional query-to-rows mapping."""
        return FakePool(self._rows + ((query_substr, rows),))

    def with_row(
        self,
        query_substr: str,
        row: dict[str, Any],
    ) -> "FakePool":
        """Return a new FakePool with an additional query-to-single-row mapping."""
        return FakePool(self._rows + ((query_substr, [row]),))

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[FakeConnection]:
        """Yield a FakeConnection loaded with all registered rows."""
        yield FakeConnection(self._rows)

    async def close(self) -> None:
        """No-op — nothing to close in memory."""
        pass
