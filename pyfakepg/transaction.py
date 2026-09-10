"""Transaction Protocol — asyncpg-compatible transaction interface."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Transaction(Protocol):
    """Protocol for an asyncpg-compatible database transaction."""

    async def start(self) -> None:
        """Begin the transaction."""
        ...

    async def commit(self) -> None:
        """Commit the transaction."""
        ...

    async def rollback(self) -> None:
        """Roll back the transaction."""
        ...
