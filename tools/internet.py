"""Internet search tool using Tavily API.

This module provides web search functionality powered by Tavily.
Extracted from main.py to enable modular tool organization.
"""

from typing import Literal
from tavily import TavilyClient

from config.settings import settings


# Initialize Tavily client with API key from settings
tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search using Tavily.

    This function searches the internet for information and returns
    structured results from Tavily's search API.

    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 5)
        topic: Search topic category - "general", "news", or "finance" (default: "general")
        include_raw_content: Whether to include raw page content (default: False)

    Returns:
        Dictionary containing search results with the following structure:
        {
            "query": str,
            "answer": str | None,
            "results": [
                {
                    "title": str,
                    "url": str,
                    "content": str,
                    "score": float,
                    "raw_content": str | None,  # if include_raw_content=True
                },
                ...
            ]
        }

    Example:
        >>> results = internet_search("Latest Android version", max_results=3)
        >>> for result in results["results"]:
        ...     print(f"{result['title']}: {result['url']}")
    """
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )
