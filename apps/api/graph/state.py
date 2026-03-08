from typing import Any
from typing_extensions import TypedDict


class BoroughSignalState(TypedDict, total=False):
    area_id: str
    proposal_text: str

    proposal_features: dict[str, Any]
    detected_issues: list[str]
    geography_warning: str | None

    area: dict[str, Any]
    segments: list[dict[str, Any]]
    evidence_docs: list[dict[str, Any]]
    filtered_evidence: list[dict[str, Any]]
    area_issue_modifiers: dict[str, float]

    segment_results: list[dict[str, Any]]
    overall_sentiment: str
    recommendation: str
    confidence: float

    proposal_id: str
    run_id: str
    recommendation_id: str

    response: dict[str, Any]
