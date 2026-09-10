"""FakeRows — In-memory row set for a matching query substring."""

from typing import Any


class FakeRows:
    """
    A named set of rows responding to queries containing a given substring.
    Used as a constructor argument to FakePool.
    100% Code-Free Constructor (Elegant Objects).

    Usage:
        FakeRows("SELECT * FROM users", {"id": "1", "name": "Max"})
        FakeRows("SELECT * FROM users", {"id": "1"}, {"id": "2"})
    """

    def __init__(self, query_substr: str, *rows: dict[str, Any]) -> None:
        self._query_substr = query_substr
        self._rows = rows

    def matches(self, query: str) -> bool:
        """Return True if query contains the registered substring."""
        return self._query_substr.lower() in query.lower()

    def all(self) -> list[dict[str, Any]]:
        """Return all rows as a list of dicts."""
        return [dict(row) for row in self._rows]

    def first(self) -> dict[str, Any] | None:
        """Return the first row as a dict, or None if empty."""
        return dict(self._rows[0]) if self._rows else None
