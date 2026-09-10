"""Connection Protocol — asyncpg-compatible database connection interface."""

from typing import Any, Protocol, runtime_checkable
from pyfakepg.transaction import Transaction


@runtime_checkable
class Connection(Protocol):
    """Protocol for an asyncpg-compatible database connection."""

    async def fetch(self, query: str, *args: Any) -> list[dict[str, Any]]:
        """Execute a query and return all rows as a list of dicts."""
        ...

    async def fetchrow(self, query: str, *args: Any) -> dict[str, Any] | None:
        """Execute a query and return a single row as a dict, or None."""
        ...

    async def execute(self, query: str, *args: Any) -> str:
        """Execute a DML statement and return the status string."""
        ...

    def transaction(self) -> Transaction:
        """Return a Transaction object for explicit transaction management."""
        ...
