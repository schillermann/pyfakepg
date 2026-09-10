"""FakeTransaction — In-memory fake for asyncpg Transaction."""


class FakeTransaction:
    """
    In-memory fake implementation of Transaction.
    Tracks start, commit and rollback calls without touching a database.
    100% Code-Free Constructor (Elegant Objects).
    """

    def __init__(self) -> None:
        self._started = False
        self._committed = False
        self._rolled_back = False

    async def start(self) -> None:
        """Mark the transaction as started."""
        self._started = True

    async def commit(self) -> None:
        """Mark the transaction as committed."""
        self._committed = True

    async def rollback(self) -> None:
        """Mark the transaction as rolled back."""
        self._rolled_back = True

    def started(self) -> bool:
        """Return True if start() was called."""
        return self._started

    def committed(self) -> bool:
        """Return True if commit() was called."""
        return self._committed

    def rolled_back(self) -> bool:
        """Return True if rollback() was called."""
        return self._rolled_back
