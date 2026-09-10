"""pyfakepg — Fake asyncpg objects for unit tests. No mocks, no database."""

from pyfakepg.connection import Connection
from pyfakepg.fake_connection import FakeConnection
from pyfakepg.fake_pool import FakePool
from pyfakepg.fake_transaction import FakeTransaction
from pyfakepg.pool import Pool
from pyfakepg.transaction import Transaction

__version__ = "0.1.0"

__all__ = [
    "__version__",
    # Protocols
    "Pool",
    "Connection",
    "Transaction",
    # Fakes
    "FakePool",
    "FakeConnection",
    "FakeTransaction",
]
