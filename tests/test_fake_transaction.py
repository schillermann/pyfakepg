"""Tests for FakeTransaction."""

import pytest
from pyfakepg import FakePool, FakeTransaction


async def test_transaction_initial_state():
    pool = FakePool()
    async with pool.acquire() as conn:
        tx = conn.transaction()
    assert isinstance(tx, FakeTransaction)
    assert tx.started() is False
    assert tx.committed() is False
    assert tx.rolled_back() is False


async def test_transaction_start():
    pool = FakePool()
    async with pool.acquire() as conn:
        tx = conn.transaction()
        await tx.start()
    assert tx.started() is True
    assert tx.committed() is False
    assert tx.rolled_back() is False


async def test_transaction_commit():
    pool = FakePool()
    async with pool.acquire() as conn:
        tx = conn.transaction()
        await tx.start()
        await tx.commit()
    assert tx.started() is True
    assert tx.committed() is True
    assert tx.rolled_back() is False


async def test_transaction_rollback():
    pool = FakePool()
    async with pool.acquire() as conn:
        tx = conn.transaction()
        await tx.start()
        await tx.rollback()
    assert tx.started() is True
    assert tx.committed() is False
    assert tx.rolled_back() is True
