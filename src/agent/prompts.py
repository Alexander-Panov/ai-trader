import asyncio

from jinja2 import Environment, FileSystemLoader

from config import PROJECT_DIR
from trade.arena.arena_client import get_arena_client
from trade.utils import get_stock_prices
from utils import now_str

env = Environment(loader=FileSystemLoader(PROJECT_DIR / 'src/agent/prompt_templates'))


async def render_jinja_prompt() -> str:
    template = env.get_template("ru.j2")

    account, stock_prices = await asyncio.gather(
        get_arena_client().get_account(),
        get_stock_prices(),
    )

    positions = [
        {
            "symbol": pos.symbol,
            "quantity": int(float(pos.quantity.value)),
            "current_price": float(pos.current_price.value),
            "unrealized_pnl": float(pos.unrealized_pnl.value),
            "value": int(float(pos.quantity.value)) * float(pos.current_price.value),
        }
        for pos in account.positions
    ]

    return template.render(
        datetime=now_str(),
        cash=float(account.cash.value),
        equity=float(account.equity.value),
        positions=positions,
        quotes=[sp.model_dump() for sp in stock_prices],
    )
