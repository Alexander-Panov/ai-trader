import uuid
from datetime import datetime
from decimal import Decimal

from config import STOCKS
from trade.arena.models import AccountResponse, OrderInResponse, OrderResponse, PositionResponse
from trade.finam.models import FinamDecimal, QuoteResponse, Quote, Side
from trade.models import StockPrice

COMMISSION_RATE = Decimal("0.001")
DEFAULT_PRICE = "100.00"


def _fd(value: str | float) -> FinamDecimal:
    return FinamDecimal(value=str(value))


class MockPortfolio:
    def __init__(self):
        self.cash: float = 100_000.0
        self.positions: dict[str, int] = {}


mock_portfolio = MockPortfolio()


async def get_price(symbol: str) -> Decimal:
    return Decimal(DEFAULT_PRICE)


class MockArenaClient:
    async def get_account(self) -> AccountResponse:
        positions = [
            PositionResponse(
                symbol=symbol,
                quantity=_fd(qty),
                average_price=_fd(DEFAULT_PRICE),
                current_price=_fd(DEFAULT_PRICE),
                unrealized_pnl=_fd("0.0"),
            )
            for symbol, qty in mock_portfolio.positions.items()
            if qty > 0
        ]
        total_value = sum(float(DEFAULT_PRICE) * qty for qty in mock_portfolio.positions.values())
        return AccountResponse(
            account_id=1,
            cash=_fd(mock_portfolio.cash),
            available_cash=_fd(mock_portfolio.cash),
            unrealized_profit=_fd("0.0"),
            positions=positions,
            equity=_fd(mock_portfolio.cash + total_value),
        )

    async def get_last_quote(self, symbol: str) -> QuoteResponse:
        quote = Quote(
            symbol=symbol,
            timestamp=datetime.now(),
            ask=_fd("101.00"),
            ask_size=_fd("100"),
            bid=_fd("99.00"),
            bid_size=_fd("100"),
            last=_fd(DEFAULT_PRICE),
            turnover=_fd("0.0"),
            open=_fd("98.00"),
            close=_fd(DEFAULT_PRICE),
            high=_fd("102.00"),
            low=_fd("97.00"),
            change=_fd("2.00"),
        )
        return QuoteResponse(symbol=symbol, quote=quote)

    async def place_order(self, order) -> OrderResponse:
        symbol = order.symbol
        quantity = int(float(order.quantity.value))
        side = order.side

        price = await get_price(symbol)
        total = price * quantity
        commission = total * COMMISSION_RATE

        if side == Side.BUY:
            cost = total + commission
            if Decimal(str(mock_portfolio.cash)) < cost:
                raise Exception("Insufficient cash!")
            mock_portfolio.cash -= float(cost)
            mock_portfolio.positions[symbol] = mock_portfolio.positions.get(symbol, 0) + quantity
        else:
            current = mock_portfolio.positions.get(symbol, 0)
            if current < quantity:
                raise Exception("Insufficient shares!")
            mock_portfolio.positions[symbol] = current - quantity
            mock_portfolio.cash += float(total - commission)

        return OrderResponse(
            order_id=uuid.uuid4(),
            order=OrderInResponse(
                quantity=_fd(quantity),
                symbol=symbol,
                side=side,
                execution_price=_fd(DEFAULT_PRICE),
                commission=_fd(float(commission)),
            ),
        )


mock_arena_client = MockArenaClient()


async def mock_get_stock_prices() -> list[StockPrice]:
    return [
        StockPrice(symbol=symbol, name=name, bid=Decimal("99.00"), ask=Decimal("101.00"))
        for symbol, name in STOCKS.items()
    ]
