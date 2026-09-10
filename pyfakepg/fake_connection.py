"""FakeConnection — In-memory fake for asyncpg Connection."""

from typing import Any
from pyfakepg.fake_transaction import FakeTransaction


class FakeConnection:
    """
    In-memory fake implementation of Connection.
    Matches queries against registered rows by substring.
    No database, no network — runs entirely in RAM.
    100% Code-Free Constructor (Elegant Objects).
    """

    def __init__(self, rows: tuple[tuple[str, list[dict[str, Any]]], ...]) -> None:
        self._rows = rows

    async def fetch(self, query: str, *args: Any) -> list[dict[str, Any]]:
        """Return all registered rows whose key is a substring of the query."""
        q = query.lower()
        for key, records in self._rows:
            if key.lower() in q:
                return list(records)
        return []

    async def fetchrow(self, query: str, *args: Any) -> dict[str, Any] | None:
        """Return the first registered row whose key is a substring of the query."""
        q = query.lower()
        for key, records in self._rows:
            if key.lower() in q:
                return dict(records[0]) if records else None
        return None

    async def execute(self, query: str, *args: Any) -> str:
        """Accept any DML statement and return a generic status string."""
        return "OK"

    def transaction(self) -> FakeTransaction:
        """Return a fresh FakeTransaction."""
        return FakeTransaction()
