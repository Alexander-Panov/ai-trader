import feedparser
import requests
from langchain_core.tools import tool

RSS_URL = "https://www.finam.ru/analysis/conews/rsspoint/"


@tool
def get_news() -> list[str]:
    """Fetch latest financial news headlines from Finam RSS feed."""
    response = requests.get(RSS_URL, timeout=10)
    response.raise_for_status()
    feed = feedparser.parse(response.text)
    return [(entry.title + ". " + entry.description.split('...')[0]) for entry in feed.entries]
