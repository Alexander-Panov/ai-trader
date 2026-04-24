import pytest

from agent.prompts import render_jinja_prompt
from config import STOCKS


@pytest.mark.usefixtures("arena_client", "finam_client")
async def test_render_prompt():
    result = await render_jinja_prompt()

    assert result
    for symbol in STOCKS:
        assert symbol in result

    assert "Денежные средства:" in result
    assert "Общий баланс (equity):" in result
    assert "BID" in result
    assert "ASK" in result


