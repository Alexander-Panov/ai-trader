from datetime import datetime
from enum import Enum, StrEnum
from symtable import Symbol

from pydantic import Field, BaseModel

from trade.models import Symbol


class FinamDecimal(BaseModel):
    """
    A custom decimal type for Finam API responses.
    """
    value: str = "0.0"


class TimeFrame(str, Enum):
    TIME_FRAME_UNSPECIFIED = "TIME_FRAME_UNSPECIFIED"
    TIME_FRAME_M1 = "TIME_FRAME_M1"
    TIME_FRAME_M5 = "TIME_FRAME_M5"
    TIME_FRAME_M15 = "TIME_FRAME_M15"
    TIME_FRAME_M30 = "TIME_FRAME_M30"
    TIME_FRAME_H1 = "TIME_FRAME_H1"
    TIME_FRAME_H2 = "TIME_FRAME_H2"
    TIME_FRAME_H4 = "TIME_FRAME_H4"
    TIME_FRAME_H8 = "TIME_FRAME_H8"
    TIME_FRAME_D = "TIME_FRAME_D"
    TIME_FRAME_W = "TIME_FRAME_W"
    TIME_FRAME_MN = "TIME_FRAME_MN"
    TIME_FRAME_QR = "TIME_FRAME_QR"


class ErrorModel(BaseModel):
    code: int
    message: str
    details: list = Field(default_factory=list)


class BaseResponse(BaseModel):
    symbol: Symbol


class Bar(BaseModel):
    timestamp: datetime
    open: FinamDecimal
    close: FinamDecimal
    high: FinamDecimal
    low: FinamDecimal
    volume: FinamDecimal


class BarsResponse(BaseResponse):
    bars: list[Bar]


class Quote(BaseModel):
    symbol: Symbol | None = None
    timestamp: datetime
    ask: FinamDecimal
    ask_size: FinamDecimal
    bid: FinamDecimal
    bid_size: FinamDecimal
    last: FinamDecimal
    last_size: FinamDecimal | None = None
    volume: FinamDecimal | None = None
    turnover: FinamDecimal
    open: FinamDecimal
    close: FinamDecimal
    high: FinamDecimal
    low: FinamDecimal
    change: FinamDecimal


class QuoteResponse(BaseResponse):
    quote: Quote


class Side(StrEnum):
    """Сторона заявки"""
    BUY = "SIDE_BUY"
    SELL = "SIDE_SELL"


class OrderType(str, Enum):
    """Тип заявки"""
    UNSPECIFIED = "ORDER_TYPE_UNSPECIFIED"
    MARKET = "ORDER_TYPE_MARKET"
    LIMIT = "ORDER_TYPE_LIMIT"
    STOP = "ORDER_TYPE_STOP"
    STOP_LIMIT = "ORDER_TYPE_STOP_LIMIT"
    MULTI_LEG = "ORDER_TYPE_MULTI_LEG"


class OrderStatus(str, Enum):
    """Статус заявки"""
    UNSPECIFIED = "ORDER_STATUS_UNSPECIFIED"
    NEW = "ORDER_STATUS_NEW"
    PARTIALLY_FILLED = "ORDER_STATUS_PARTIALLY_FILLED"
    FILLED = "ORDER_STATUS_FILLED"
    DONE_FOR_DAY = "ORDER_STATUS_DONE_FOR_DAY"
    CANCELED = "ORDER_STATUS_CANCELED"
    REPLACED = "ORDER_STATUS_REPLACED"
    PENDING_CANCEL = "ORDER_STATUS_PENDING_CANCEL"
    REJECTED = "ORDER_STATUS_REJECTED"
    SUSPENDED = "ORDER_STATUS_SUSPENDED"
    PENDING_NEW = "ORDER_STATUS_PENDING_NEW"
    EXPIRED = "ORDER_STATUS_EXPIRED"
    FAILED = "ORDER_STATUS_FAILED"
    FORWARDING = "ORDER_STATUS_FORWARDING"
    WAIT = "ORDER_STATUS_WAIT"
    DENIED_BY_BROKER = "ORDER_STATUS_DENIED_BY_BROKER"
    REJECTED_BY_EXCHANGE = "ORDER_STATUS_REJECTED_BY_EXCHANGE"
    WATCHING = "ORDER_STATUS_WATCHING"
    EXECUTED = "ORDER_STATUS_EXECUTED"
    DISABLED = "ORDER_STATUS_DISABLED"
    LINK_WAIT = "ORDER_STATUS_LINK_WAIT"
    SL_GUARD_TIME = "ORDER_STATUS_SL_GUARD_TIME"
    SL_EXECUTED = "ORDER_STATUS_SL_EXECUTED"
    SL_FORWARDING = "ORDER_STATUS_SL_FORWARDING"
    TP_GUARD_TIME = "ORDER_STATUS_TP_GUARD_TIME"
    TP_EXECUTED = "ORDER_STATUS_TP_EXECUTED"
    TP_CORRECTION = "ORDER_STATUS_TP_CORRECTION"
    TP_FORWARDING = "ORDER_STATUS_TP_FORWARDING"
    TP_CORR_GUARD_TIME = "ORDER_STATUS_TP_CORR_GUARD_TIME"


class StopCondition(str, Enum):
    """Условие срабатывания стоп заявки"""
    UNSPECIFIED = "STOP_CONDITION_UNSPECIFIED"
    LAST_UP = "STOP_CONDITION_LAST_UP"
    LAST_DOWN = "STOP_CONDITION_LAST_DOWN"


class TimeInForce(str, Enum):
    """Срок действия заявки"""
    UNSPECIFIED = "TIME_IN_FORCE_UNSPECIFIED"
    DAY = "TIME_IN_FORCE_DAY"
    GOOD_TILL_CANCEL = "TIME_IN_FORCE_GOOD_TILL_CANCEL"
    GOOD_TILL_CROSSING = "TIME_IN_FORCE_GOOD_TILL_CROSSING"
    EXT = "TIME_IN_FORCE_EXT"
    ON_OPEN = "TIME_IN_FORCE_ON_OPEN"
    ON_CLOSE = "TIME_IN_FORCE_ON_CLOSE"
    IOC = "TIME_IN_FORCE_IOC"
    FOK = "TIME_IN_FORCE_FOK"


class ValidBefore(str, Enum):
    """Срок действия условной заявки"""
    UNSPECIFIED = "VALID_BEFORE_UNSPECIFIED"
    END_OF_DAY = "VALID_BEFORE_END_OF_DAY"
    GOOD_TILL_CANCEL = "VALID_BEFORE_GOOD_TILL_CANCEL"
    GOOD_TILL_DATE = "VALID_BEFORE_GOOD_TILL_DATE"


class Leg(BaseModel):
    """Лег"""
    symbol: str
    quantity: FinamDecimal
    side: Side


class Order(BaseModel):
    """Информация о заявке"""
    account_id: str
    symbol: str
    quantity: FinamDecimal
    side: Side
    type: OrderType
    time_in_force: TimeInForce | None = None
    limit_price: FinamDecimal | str | None = None
    stop_price: FinamDecimal | str | None = None
    stop_condition: StopCondition | None = None
    legs: list[Leg] = Field(default_factory=list)
    client_order_id: str | None = Field(default=None, max_length=64)
    valid_before: ValidBefore | None = None
    comment: str | None = Field(default=None, max_length=128)


class OrderState(BaseModel):
    """Состояние заявки"""
    order_id: str
    exec_id: str
    status: OrderStatus
    order: Order
    transact_at: datetime
    accept_at: datetime | None = None
    withdraw_at: datetime | None = None
    initial_quantity: FinamDecimal | str | None = None
    executed_quantity: FinamDecimal | str | None = None
    remaining_quantity: FinamDecimal | str | None = None


class Position(BaseModel):
    symbol: str
    quantity: FinamDecimal
    average_price: FinamDecimal
    current_price: FinamDecimal
    maintenance_margin: FinamDecimal | None = None
    daily_pnl: FinamDecimal | None = None
    unrealized_pnl: FinamDecimal


class FinamMoney(BaseModel):
    """
    A custom money type for Finam API responses.
    """
    currency_code: str
    units: str
    nanos: int


class GetAccountResponse(BaseModel):
    account_id: str
    type: str
    status: str
    positions: list[Position] = Field(default_factory=list)
    cash: list[FinamMoney] = Field(default_factory=list)
    open_account_date: datetime
    first_non_trade_date: datetime
    equity: FinamDecimal | None = None
    unrealized_profit: FinamDecimal | None = None

class Trade(BaseModel):
    """Информация о сделке"""
    trade_id: str
    symbol: str
    price: FinamDecimal
    size: FinamDecimal
    side: Side
    timestamp: datetime
    order_id: str
    account_id: str
    comment: str | None = None


class GetTradesResponse(BaseModel):
    trades: list[Trade] = Field(default_factory=list)


class OrderCreateRequest(BaseModel):
    quantity: FinamDecimal
    symbol: Symbol
    side: Side
