"""Tests for FakePool."""

import pytest
from pyfakepg import FakePool, FakeConnection, FakeTransaction


async def test_acquire_yields_fake_connection():
    pool = FakePool()
    async with pool.acquire() as conn:
        assert isinstance(conn, FakeConnection)


async def test_with_row_single_fetchrow():
    pool = FakePool().with_row(
        "SELECT * FROM users",
        {"id": "usr_1", "name": "Max Mustermann"},
    )
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", "usr_1")
    assert row == {"id": "usr_1", "name": "Max Mustermann"}


async def test_with_rows_fetch_all():
    pool = FakePool().with_rows(
        "SELECT * FROM tenants",
        [
            {"id": "t_1", "name": "Acme GmbH"},
            {"id": "t_2", "name": "Beta AG"},
        ],
    )
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM tenants")
    assert len(rows) == 2
    assert rows[0]["name"] == "Acme GmbH"


async def test_multiple_mappings_resolved_by_substr():
    pool = (
        FakePool()
        .with_row("SELECT * FROM users", {"id": "usr_1", "name": "Max"})
        .with_row("SELECT * FROM tenants", {"id": "t_1", "name": "Acme"})
    )
    async with pool.acquire() as conn:
        user = await conn.fetchrow("SELECT * FROM users WHERE id = $1", "usr_1")
        tenant = await conn.fetchrow("SELECT * FROM tenants WHERE id = $1", "t_1")
    assert user["name"] == "Max"
    assert tenant["name"] == "Acme"


async def test_fetchrow_returns_none_for_unknown_query():
    pool = FakePool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", "missing")
    assert row is None


async def test_fetch_returns_empty_list_for_unknown_query():
    pool = FakePool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM unknown_table")
    assert rows == []


async def test_execute_returns_ok():
    pool = FakePool()
    async with pool.acquire() as conn:
        result = await conn.execute("UPDATE users SET status = $1 WHERE id = $2", "online", "usr_1")
    assert result == "OK"


async def test_close_is_noop():
    pool = FakePool()
    await pool.close()  # must not raise


async def test_with_row_immutable_builder():
    base = FakePool()
    extended = base.with_row("SELECT * FROM users", {"id": "usr_1"})
    # base must remain unchanged
    async with base.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users")
    assert row is None

    async with extended.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users")
    assert row == {"id": "usr_1"}
