from datetime import timedelta

import pytest

from conftest import TEST_STOCK_SYMBOLS, TEST_INVALID_SYMBOL
from tools.price import get_price
from trade.finam.models import TimeFrame, BarsResponse
from utils import now


@pytest.mark.parametrize("symbol", TEST_STOCK_SYMBOLS)
async def test_get_price_local(finam_client, symbol):
    end_time = now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=7)

    result = await get_price.ainvoke({
        "symbol": symbol,
        "start_time": start_time,
        "end_time": end_time,
        "timeframe": TimeFrame.TIME_FRAME_D,
    })

    assert isinstance(result, BarsResponse)
    assert result.symbol == symbol


async def test_get_price_local_invalid_symbol(finam_client):
    end_time = now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=7)

    with pytest.raises(Exception):
        await get_price.ainvoke({
            "symbol": TEST_INVALID_SYMBOL,
            "start_time": start_time,
            "end_time": end_time,
            "timeframe": TimeFrame.TIME_FRAME_D,
        })
