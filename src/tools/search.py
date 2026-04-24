from langchain_core.tools import tool
from pydantic import Field, BaseModel
from tavily import TavilyClient

from config import TAVILY_API_KEY


class SearchResult(BaseModel):
    title: str = Field(..., description="The title of the search result.")
    content: str = Field(..., description="A short description of the search result.")


class SearchResponse(BaseModel):
    answer: str | None = Field(None, description="A short answer")
    results: list[SearchResult]


tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def search(query: str) -> SearchResponse:
    """Use search tool to scrape and return main content information related to specified query in a structured way."""
    response = tavily_client.search(query, max_results=5, topic="general", search_depth="basic", country="russia")
    return SearchResponse.model_validate(response)
