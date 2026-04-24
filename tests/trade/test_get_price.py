import pytest

from conftest import TEST_STOCK_SYMBOLS, TEST_INVALID_SYMBOL
from trade.utils import get_price


@pytest.mark.parametrize("symbol", TEST_STOCK_SYMBOLS)
async def test_get_price(finam_client, symbol):
    result = await get_price(symbol)

    assert float(result.bid) > 0
    assert float(result.ask) > 0


async def test_get_price_invalid_symbol(finam_client):
    with pytest.raises(Exception):
        await get_price(TEST_INVALID_SYMBOL)