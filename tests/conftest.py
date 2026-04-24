import os

import pytest

from trade.arena.arena_client import initialize_arena_client
from trade.finam.finam_client import initialize_finam_client

os.environ['LANGSMITH_TRACING'] = "false"  # отключить трейсинг во время тестов

TEST_INVALID_SYMBOL = "INVALID@SYMBOL"
TEST_STOCK_SYMBOLS = ["AAPL@XNGS", "NVDA@XNGS", "YDEX@MISX", "SBER@MISX"]


@pytest.fixture(scope="session")
async def finam_client():
    """Initialize real Finam client. Use only in tests that hit the real API."""
    await initialize_finam_client()


@pytest.fixture(scope="session")
async def arena_client():
    await initialize_arena_client()
