from decimal import Decimal
from typing import Annotated

from pydantic import Field, BaseModel

Symbol = Annotated[
    str,
    Field(
        description="Symbol in format: TICKER@MIC",
        pattern=r"^[A-Za-z0-9._-]+@[A-Z_]+$",
        examples=["YDEX@MISX", "SBER@TQBR"],
    ),
]


class Stock(BaseModel):
    """Single stock configuration"""
    symbol: Symbol
    name: str


class Price(BaseModel):
    bid: Decimal
    ask: Decimal


class StockPrice(Stock, Price):
    pass



