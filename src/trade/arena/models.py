import uuid
from datetime import datetime

from pydantic import BaseModel

from trade.finam.models import FinamDecimal, Side
from trade.models import Symbol


class PositionResponse(BaseModel):
    symbol: Symbol
    quantity: FinamDecimal
    average_price: FinamDecimal
    current_price: FinamDecimal
    unrealized_pnl: FinamDecimal


class AccountResponse(BaseModel):
    account_id: int
    cash: FinamDecimal
    available_cash: FinamDecimal
    unrealized_profit: FinamDecimal
    positions: list[PositionResponse]
    equity: FinamDecimal


class OrderInResponse(BaseModel):
    quantity: FinamDecimal
    symbol: Symbol
    side: Side
    execution_price: FinamDecimal
    commission: FinamDecimal


class OrderResponse(BaseModel):
    order_id: uuid.UUID
    order: OrderInResponse


class TradeRead(BaseModel):
    trade_id: uuid.UUID
    symbol: Symbol
    side: Side
    price: FinamDecimal
    size: FinamDecimal
    created_at: datetime


class TradesResponse(BaseModel):
    trades: list[TradeRead]
