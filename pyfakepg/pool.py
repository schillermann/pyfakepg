"""Pool Protocol — asyncpg-compatible connection pool interface."""

from typing import AsyncContextManager, Protocol, runtime_checkable
from pyfakepg.connection import Connection


@runtime_checkable
class Pool(Protocol):
    """Protocol for an asyncpg-compatible connection pool."""

    def acquire(self) -> AsyncContextManager["Connection"]:
        """Acquire a connection from the pool as an async context manager."""
        ...

    async def close(self) -> None:
        """Close all connections in the pool."""
        ...
