from tavily import TavilyClient
import os

_tavily = None


def _get_client() -> TavilyClient:
    global _tavily
    if _tavily is None:
        _tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    return _tavily


def searcher_node(state: dict) -> dict:
    """Run each search query via Tavily and collect results."""
    client = _get_client()
    results = []

    for query in state["search_queries"]:
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=4,
            include_answer=False,
        )
        for r in response.get("results", []):
            results.append(
                {
                    "query": query,
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", ""),
                }
            )

    return {"search_results": results}
