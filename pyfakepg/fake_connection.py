"""FakeConnection — In-memory fake for asyncpg Connection."""

from typing import Any
from pyfakepg.fake_rows import FakeRows
from pyfakepg.fake_transaction import FakeTransaction


class FakeConnection:
    """
    In-memory fake implementation of Connection.
    Delegates query resolution to FakeRows objects.
    No database, no network — runs entirely in RAM.
    100% Code-Free Constructor (Elegant Objects).
    """

    def __init__(self, rows: tuple[FakeRows, ...]) -> None:
        self._rows = rows

    async def fetch(self, query: str, *args: Any) -> list[dict[str, Any]]:
        """Return all rows from the first FakeRows matching the query."""
        for fake_rows in self._rows:
            if fake_rows.matches(query):
                return fake_rows.all()
        return []

    async def fetchrow(self, query: str, *args: Any) -> dict[str, Any] | None:
        """Return the first row from the first FakeRows matching the query."""
        for fake_rows in self._rows:
            if fake_rows.matches(query):
                return fake_rows.first()
        return None

    async def execute(self, query: str, *args: Any) -> str:
        """Accept any DML statement and return a generic status string."""
        return "OK"

    def transaction(self) -> FakeTransaction:
        """Return a fresh FakeTransaction."""
        return FakeTransaction()
