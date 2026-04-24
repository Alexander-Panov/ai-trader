import pytest
from langchain_core.tools import ToolException

from tools.calculate import bash_python, session


@pytest.fixture(autouse=True)
def clear_session():
    session.clear()
    yield
    session.clear()


def test_basic_operations():
    assert bash_python.invoke({"code": "print('Hello')"}) == "Hello"
    assert bash_python.invoke({"code": "print(2 + 2)"}) == "4"
    assert bash_python.invoke({"code": "x = 10\ny = 20\nprint(x + y)"}) == "30"
    assert bash_python.invoke({"code": "import math\nprint(math.sqrt(16))"}) == "4.0"


def test_error_handling():
    with pytest.raises(ToolException, match="ZeroDivisionError"):
        bash_python.invoke({"code": "1 / 0"})

    with pytest.raises(ToolException, match="SyntaxError"):
        bash_python.invoke({"code": "print('unclosed"})


def test_empty_output():
    assert bash_python.invoke({"code": "x = 42"}) == ""


def test_return_last_expression():
    assert bash_python.invoke({"code": "2 + 2"}) == "4"

    result = bash_python.invoke({"code": "print('Computing...')\nx = 10\nx * 5"})
    assert "Computing..." in result
    assert "50" in result


def test_dict_comprehension():
    code = """
prices = {'AAPL': 150.0, 'MSFT': 300.0}
weights = {'AAPL': 0.5, 'MSFT': 0.5}
allocations = {s: 10000 * weights[s] for s in weights}
total = sum(allocations[s] / prices[s] for s in allocations)
print(f"{total:.2f}")
"""
    assert "50.00" in bash_python.invoke({"code": code})


def test_session_persists():
    bash_python.invoke({"code": "x = 42"})
    assert bash_python.invoke({"code": "x + 1"}) == "43"


def test_no_session_between_tests():
    """Переменные из других тестов не должны просачиваться (fixture сбрасывает session)"""
    with pytest.raises(ToolException, match="NameError"):
        bash_python.invoke({"code": "x"})