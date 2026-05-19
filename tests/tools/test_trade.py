from unittest.mock import patch

import pytest

from conftest import TEST_STOCK_SYMBOLS
from mock_arena_client import mock_arena_client, mock_portfolio
from trade.finam.models import Side
from tools.trade import buy, sell


@pytest.fixture(autouse=True)
def reset_portfolio():
    mock_portfolio.cash = 100_000.0
    mock_portfolio.positions.clear()
    yield
    mock_portfolio.cash = 100_000.0
    mock_portfolio.positions.clear()


@pytest.fixture(autouse=True)
def use_mock_arena_client():
    with patch("tools.trade.get_arena_client", return_value=mock_arena_client):
        yield


@pytest.mark.parametrize("symbol", TEST_STOCK_SYMBOLS)
async def test_buy(symbol):
    result = await buy.ainvoke({"symbol": symbol, "amount": 10})

    assert result.order.symbol == symbol
    assert result.order.side == Side.BUY
    assert mock_portfolio.positions[symbol] == 10
    assert mock_portfolio.cash < 100_000.0


@pytest.mark.parametrize("symbol", TEST_STOCK_SYMBOLS)
async def test_sell(symbol):
    await buy.ainvoke({"symbol": symbol, "amount": 10})
    result = await sell.ainvoke({"symbol": symbol, "amount": 10})

    assert result.order.symbol == symbol
    assert result.order.side == Side.SELL
    assert mock_portfolio.positions[symbol] == 0
    assert mock_portfolio.cash != 100_000.0


async def test_sell_without_position():
    symbol = TEST_STOCK_SYMBOLS[-1]

    with pytest.raises(Exception, match="Insufficient shares!"):
        await sell.ainvoke({"symbol": symbol, "amount": 10})


async def test_buy_insufficient_cash():
    symbol = TEST_STOCK_SYMBOLS[0]

    with pytest.raises(Exception, match="Insufficient cash!"):
        await buy.ainvoke({"symbol": symbol, "amount": 10_000})


async def test_error_get_price():
    symbol = TEST_STOCK_SYMBOLS[0]

    with patch("mock_arena_client.get_price", side_effect=Exception("not found")):
        with pytest.raises(Exception, match="not found"):
            await buy.ainvoke({"symbol": symbol, "amount": 10})