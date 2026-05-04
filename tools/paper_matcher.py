from typing import Optional, Literal

from tools.semantic_scholar_tool import search_semantic_scholar
from logic.filtering import SearchConstraints, filter_papers

Operator = Literal["<", "<=", "=", ">=", ">", "~"]


def find_matching_papers(
    topic: str,
    year_operator: Optional[Operator] = None,
    year_value: Optional[int] = None,
    citation_operator: Optional[Operator] = None,
    citation_value: Optional[int] = None,
    limit: int = 10,
) -> list[dict]:
    """
    Search Semantic Scholar and deterministically filter results.
    Returns only papers that satisfy the constraints.
    """
    papers = search_semantic_scholar(topic=topic, limit=limit)

    constraints = SearchConstraints(
        topic=topic,
        year_operator=year_operator,
        year_value=year_value,
        citation_operator=citation_operator,
        citation_value=citation_value,
    )

    filtered = filter_papers(papers, constraints)

    # Optional: sort by citation count descending
    filtered = sorted(
        filtered,
        key=lambda p: p.get("citation_count") if p.get("citation_count") is not None else -1,
        reverse=True,
    )

    return filtered[:5]