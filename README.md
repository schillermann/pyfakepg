# pyfakepg

Fake [asyncpg](https://github.com/MagicStack/asyncpg) objects for unit tests. No mocks, no database.

While intended as an extension for [pyresponse](https://github.com/schillermann/pyresponse), `pyfakepg` can also be used completely standalone.

Inspired by [jcabi-dynamo](https://dynamo.jcabi.com/) and [Yegor Bugayenko's](https://www.yegor256.com/) principle of fake classes over mocking.

---

## Installation

```bash
pip install pyfakepg
```

---

## Why fake classes instead of mocks?

Mocks couple tests to implementation details — they break when internals change, not when behavior changes. A fake class is a real, lightweight alternative implementation of the same interface that runs entirely in memory.

```python
# ❌ Mock — fragile, couples to implementation
mock_pool = MagicMock()
mock_pool.acquire().__aenter__.return_value.fetchrow.return_value = {"id": "1"}

# ✅ Fake — clean, composable, no magic
pool = FakePool(
    FakeRows("SELECT * FROM users", {"id": "1", "name": "Max"}),
)
```

---

## Usage

### FakePool

`FakePool` accepts `FakeRows` objects as constructor arguments — one per query pattern.
`FakeRows` matches queries by substring and returns the registered rows.

```python
from pyfakepg import FakePool, FakeRows

pool = FakePool(
    FakeRows("SELECT * FROM users", {"id": "usr_1", "name": "Max Mustermann"}),
    FakeRows(
        "SELECT * FROM tenants",
        {"id": "t_1", "name": "Acme GmbH"},
        {"id": "t_2", "name": "Beta AG"},
    ),
)

async with pool.acquire() as conn:
    user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", "usr_1")
    tenants = await conn.fetch("SELECT * FROM tenants")
    status = await conn.execute("UPDATE users SET status = $1 WHERE id = $2", "online", "usr_1")
```

### Injecting into domain objects

Domain objects receive a `Pool` directly — no global session, no monkey-patching:

```python
class PgUser:
    def __init__(self, pool: Pool, user_id: str) -> None:
        self._pool = pool
        self._user_id = user_id

    async def name(self) -> str:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1", self._user_id
            )
        return row["name"]


# Production
user = PgUser(pool=asyncpg_pool, user_id="usr_1")

# Test — no database required
async def test_user_name():
    pool = FakePool(
        FakeRows("SELECT * FROM users", {"id": "usr_1", "name": "Max Mustermann"}),
    )
    user = PgUser(pool=pool, user_id="usr_1")
    assert await user.name() == "Max Mustermann"
```

### FakeTransaction

```python
async with pool.acquire() as conn:
    tx = conn.transaction()
    await tx.start()
    await conn.execute("INSERT INTO users ...")
    await tx.commit()

assert tx.started() is True
assert tx.committed() is True
assert tx.rolled_back() is False
```

---

## FAQ

### Does it validate SQL queries?

**No, and that is by design.** `pyfakepg` is not an in-memory SQL engine and does not parse or validate queries.

It is designed for the **unit test level** to test your application and domain logic in isolation:

| Level | Tool | What is tested |
|---|---|---|
| **Unit Tests** | `pyfakepg` | How does your Python/domain logic behave for given database results? (Edge cases, mapping, business rules). Runs in microseconds, 100% in-memory, no Docker or DB needed. |
| **Integration Tests** | Real PostgreSQL (e.g., [Testcontainers](https://testcontainers-python.readthedocs.io/)) | Is the SQL syntax valid? Do column names, types, constraints, and dialect features match the real schema? |

`FakeRows` matches queries via substring matching (`FakeRows("SELECT * FROM users", ...)`). It acts as a predictable fake data provider for your domain objects, not as a database emulator.

---

## License

[MIT](LICENSE)
