from decimal import Decimal

from config import STOCKS
from trade.models import Symbol, Price, StockPrice
from trade.finam.finam_client import get_finam_client
from trade.finam.models import QuoteResponse
import asyncio


async def get_last_quote(symbol: Symbol) -> QuoteResponse:
    """Obtaining the latest quote for an instrument (bid/ask price, opening/closing price, last traded price, daily trading volume, bid/ask volume)"""
    return await get_finam_client().get_last_quote(symbol)


async def get_price(symbol: Symbol) -> Price:
    quote = await get_finam_client().get_last_quote(symbol)
    return Price(
        bid=Decimal(quote.quote.bid.value),
        ask=Decimal(quote.quote.ask.value)
    )


async def get_prices() -> tuple[Price, ...]:
    return await asyncio.gather(*[get_price(symbol) for symbol in STOCKS])


async def get_stock_prices() -> list[StockPrice]:
    prices = await get_prices()

    return [
        StockPrice(symbol=symbol, name=name, **price.model_dump())
        for (symbol, name), price in zip(STOCKS.items(), prices)
    ]
