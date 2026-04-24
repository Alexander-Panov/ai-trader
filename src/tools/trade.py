from langchain_core.tools import tool
from pydantic import PositiveInt

from trade.arena.arena_client import get_arena_client
from trade.arena.models import OrderResponse
from trade.finam.models import Side, OrderCreateRequest, FinamDecimal
from trade.models import Symbol


@tool
async def buy(symbol: Symbol, amount: PositiveInt) -> OrderResponse:
    """Buy stock function"""
    order = OrderCreateRequest(symbol=symbol, quantity=FinamDecimal(value=str(amount)), side=Side.BUY)
    return await get_arena_client().place_order(order)


@tool
async def sell(symbol: Symbol, amount: PositiveInt) -> OrderResponse:
    """Sell stock function"""
    order = OrderCreateRequest(symbol=symbol, quantity=FinamDecimal(value=str(amount)), side=Side.SELL)
    return await get_arena_client().place_order(order)
