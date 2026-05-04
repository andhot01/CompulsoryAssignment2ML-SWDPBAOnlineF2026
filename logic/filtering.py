from dataclasses import dataclass
from typing import Optional, Literal, List, Dict, Any


ComparisonOperator = Literal["<", "<=", "=", ">=", ">", "~"]


@dataclass
class SearchConstraints:
    topic: Optional[str] = None

    year_operator: Optional[ComparisonOperator] = None
    year_value: Optional[int] = None

    citation_operator: Optional[ComparisonOperator] = None
    citation_value: Optional[int] = None


def compare_numeric(
    actual: Optional[int],
    operator: Optional[ComparisonOperator],
    target: Optional[int],
    approx_tolerance: float = 0.20,
) -> bool:
    """
    Compare a numeric value against a target using a supported operator.

    Supported operators:
    <, <=, =, >=, >, ~
    where ~ means 'approximately equal' within approx_tolerance.
    """
    if operator is None or target is None:
        return True

    if actual is None:
        return False

    if operator == "<":
        return actual < target
    if operator == "<=":
        return actual <= target
    if operator == "=":
        return actual == target
    if operator == ">=":
        return actual >= target
    if operator == ">":
        return actual > target
    if operator == "~":
        lower = int(target * (1 - approx_tolerance))
        upper = int(target * (1 + approx_tolerance))
        return lower <= actual <= upper

    raise ValueError(f"Unsupported operator: {operator}")


def paper_satisfies_constraints(
    paper: Dict[str, Any],
    constraints: SearchConstraints,
    approx_tolerance: float = 0.20,
) -> bool:
    """
    Return True if the paper satisfies all deterministic constraints.
    """
    year_ok = compare_numeric(
        actual=paper.get("year"),
        operator=constraints.year_operator,
        target=constraints.year_value,
        approx_tolerance=approx_tolerance,
    )

    citation_ok = compare_numeric(
        actual=paper.get("citation_count"),
        operator=constraints.citation_operator,
        target=constraints.citation_value,
        approx_tolerance=approx_tolerance,
    )

    return year_ok and citation_ok


def filter_papers(
    papers: List[Dict[str, Any]],
    constraints: SearchConstraints,
    approx_tolerance: float = 0.20,
) -> List[Dict[str, Any]]:
    """
    Return only papers that satisfy the deterministic constraints.
    """
    return [
        paper
        for paper in papers
        if paper_satisfies_constraints(paper, constraints, approx_tolerance)
    ]