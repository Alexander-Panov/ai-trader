from datetime import timedelta

import pytest

from trade.finam.models import TimeFrame, BarsResponse
from trade.finam.models import Side
from tools.calculate import bash_python
from tools.news import get_news
from tools.price import get_price
from tools.search import search, SearchResponse
from tools.trade import buy, sell
from utils import now


# --- bash_python ---

def test_bash_python_print():
    result = bash_python.invoke({"code": "print('ok')"})
    assert result == "ok"


def test_bash_python_expression():
    result = bash_python.invoke({"code": "2 ** 10"})
    assert result == "1024"


def test_bash_python_multiline():
    code = "import math\nresult = math.pi * 2\nprint(f'{result:.4f}')"
    result = bash_python.invoke({"code": code})
    assert "6.2832" in result


# --- get_news ---

def test_get_news_returns_list():
    result = get_news.invoke({})
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_news_items_are_strings():
    result = get_news.invoke({})
    assert all(isinstance(item, str) for item in result)


def test_get_news_items_nonempty():
    result = get_news.invoke({})
    assert all(len(item) > 0 for item in result)


# --- get_price_local ---

@pytest.mark.parametrize("symbol", ["SBER@MISX", "YDEX@MISX"])
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
    assert len(result.bars) > 0


async def test_get_price_local_bar_fields(finam_client):
    end_time = now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = end_time - timedelta(days=3)

    result = await get_price.ainvoke({
        "symbol": "GAZP@MISX",
        "start_time": start_time,
        "end_time": end_time,
        "timeframe": TimeFrame.TIME_FRAME_D,
    })

    bar = result.bars[0]
    assert float(bar.open.value) > 0
    assert float(bar.close.value) > 0
    assert float(bar.high.value) >= float(bar.low.value)


# --- search ---

def test_search_returns_response():
    result = search.invoke({"query": "Сбербанк акции"})
    assert isinstance(result, SearchResponse)
    assert len(result.results) > 0


def test_search_result_fields():
    result = search.invoke({"query": "ГАЗПРОМ дивиденды 2025"})
    for item in result.results:
        assert len(item.title) > 0
        assert len(item.content) > 0


# --- buy / sell ---

async def test_buy(arena_client):
    result = await buy.ainvoke({"symbol": "SBER@MISX", "amount": 1})
    assert result.symbol == "SBER@MISX"
    assert result.side == Side.BUY
    assert float(result.quantity.value) == 1


async def test_sell(arena_client):
    result = await sell.ainvoke({"symbol": "SBER@MISX", "amount": 1})
    assert result.symbol == "SBER@MISX"
    assert result.side == Side.SELL
    assert float(result.quantity.value) == 1