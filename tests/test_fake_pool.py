"""Tests for FakePool and FakeRows."""

import pytest
from pyfakepg import FakePool, FakeRows, FakeConnection, FakeTransaction


async def test_acquire_yields_fake_connection():
    pool = FakePool()
    async with pool.acquire() as conn:
        assert isinstance(conn, FakeConnection)


async def test_single_row_fetchrow():
    pool = FakePool(
        FakeRows("SELECT * FROM users", {"id": "usr_1", "name": "Max Mustermann"}),
    )
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", "usr_1")
    assert row == {"id": "usr_1", "name": "Max Mustermann"}


async def test_multiple_rows_fetch():
    pool = FakePool(
        FakeRows(
            "SELECT * FROM tenants",
            {"id": "t_1", "name": "Acme GmbH"},
            {"id": "t_2", "name": "Beta AG"},
        ),
    )
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM tenants")
    assert len(rows) == 2
    assert rows[0]["name"] == "Acme GmbH"


async def test_multiple_fake_rows_resolved_by_substr():
    pool = FakePool(
        FakeRows("SELECT * FROM users", {"id": "usr_1", "name": "Max"}),
        FakeRows("SELECT * FROM tenants", {"id": "t_1", "name": "Acme"}),
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
        result = await conn.execute(
            "UPDATE users SET status = $1 WHERE id = $2", "online", "usr_1"
        )
    assert result == "OK"


async def test_close_is_noop():
    pool = FakePool()
    await pool.close()


async def test_empty_fake_rows_fetchrow_returns_none():
    pool = FakePool(FakeRows("SELECT * FROM users"))
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users")
    assert row is None


async def test_empty_fake_rows_fetch_returns_empty():
    pool = FakePool(FakeRows("SELECT * FROM users"))
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users")
    assert rows == []
