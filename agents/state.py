from typing import Annotated, TypedDict
import operator


class ResearchState(TypedDict):
    question: str
    search_queries: list[str]
    search_results: Annotated[list[dict], operator.add]
    report: str
