from datetime import datetime

from langchain_core.tools import tool

from trade.finam.finam_client import get_finam_client
from trade.finam.models import TimeFrame, BarsResponse
from trade.models import Symbol


@tool
async def get_price(
        symbol: Symbol, start_time: datetime, end_time: datetime, timeframe: TimeFrame
) -> BarsResponse:
    """Read OHLCV data for specified stock and datetime. Get historical information for specified stock."""
    return await get_finam_client().get_bars(symbol, start_time, end_time, timeframe)



