from unittest.mock import MagicMock, patch

from tools.news import get_news


def make_feed(titles):
    entries = [MagicMock(title=t, description=f"{t} desc...rest") for t in titles]
    return MagicMock(entries=entries)


def test_get_news_returns_strings():
    with patch("tools.news.requests.get") as mock_get:
        mock_get.return_value.text = ""
        with patch("tools.news.feedparser.parse", return_value=make_feed(["A", "B"])):
            result = get_news.invoke({})

    assert all(isinstance(s, str) for s in result)
    assert any("A" in s for s in result)


def test_get_news_count():
    titles = [f"News {i}" for i in range(10)]
    with patch("tools.news.requests.get") as mock_get:
        mock_get.return_value.text = ""
        with patch("tools.news.feedparser.parse", return_value=make_feed(titles)):
            result = get_news.invoke({})

    assert len(result) == 10