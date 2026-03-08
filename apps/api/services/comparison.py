from typing import Any


def build_improved_proposal_text(original_result: dict[str, Any]) -> str:
    original_text = original_result["proposal_text"].strip()
    features = original_result.get("proposal_features", {})
    detected_issues = original_result.get("detected_issues", [])

    additions: list[str] = []

    if "affordability" in detected_issues:
        if not features.get("affordable_housing"):
            additions.append("a meaningful affordable housing offer")
        if not features.get("quantified_affordability"):
            additions.append("clear quantified affordability commitments")

    if "transport" in detected_issues:
        if features.get("limited_parking"):
            additions.append("reduced parking with strong public transport mitigation and improved walking access")
        elif not features.get("transport_mitigation"):
            additions.append("improved station, bus, and walking access")

    if "green_space" in detected_issues:
        if features.get("green_space_loss"):
            additions.append("new trees, greenery, public open space, and public realm improvements")
        elif not features.get("green_space_gain"):
            additions.append("new trees, greenery, and public open space")

    if "safety" in detected_issues and not features.get("safety_measures"):
        additions.append("better lighting and safer walking routes")

    if "local_character" in detected_issues and not features.get("heritage_sensitive_design"):
        additions.append("design changes that respect local character and heritage")

    if not additions:
        additions.append("clearer practical local benefits for residents")

    joined = "; ".join(additions)
    return f"{original_text} Include: {joined}."


def sentiment_to_score(sentiment: str) -> int:
    if sentiment == "support":
        return 1
    if sentiment == "oppose":
        return -1
    return 0


def compare_simulation_results(
    original_result: dict[str, Any],
    improved_result: dict[str, Any],
) -> dict[str, Any]:
    original_segments = {
        item["segment_id"]: item for item in original_result["segment_results"]
    }
    improved_segments = {
        item["segment_id"]: item for item in improved_result["segment_results"]
    }

    segment_deltas = []

    for segment_id, original_segment in original_segments.items():
        improved_segment = improved_segments.get(segment_id)
        if not improved_segment:
            continue

        delta = round(improved_segment["score"] - original_segment["score"], 2)

        segment_deltas.append({
            "segment_id": segment_id,
            "label": original_segment["label"],
            "original_score": original_segment["score"],
            "improved_score": improved_segment["score"],
            "score_delta": delta,
            "original_stance": original_segment["stance"],
            "improved_stance": improved_segment["stance"],
            "top_issue_before": original_segment["top_issue"],
            "top_issue_after": improved_segment["top_issue"],
        })

    segment_deltas.sort(key=lambda x: x["score_delta"], reverse=True)

    sentiment_shift = (
        sentiment_to_score(improved_result["overall_sentiment"])
        - sentiment_to_score(original_result["overall_sentiment"])
    )

    confidence_delta = round(
        improved_result.get("confidence", 0.0) - original_result.get("confidence", 0.0),
        2,
    )

    avg_score_delta = 0.0
    if segment_deltas:
        avg_score_delta = round(
            sum(item["score_delta"] for item in segment_deltas) / len(segment_deltas),
            2,
        )

    support_balance_before = (
        sum(1 for s in original_result["segment_results"] if s["stance"] == "support")
        - sum(1 for s in original_result["segment_results"] if s["stance"] == "oppose")
    )
    support_balance_after = (
        sum(1 for s in improved_result["segment_results"] if s["stance"] == "support")
        - sum(1 for s in improved_result["segment_results"] if s["stance"] == "oppose")
    )
    support_balance_delta = support_balance_after - support_balance_before

    return {
        "overall_sentiment_before": original_result["overall_sentiment"],
        "overall_sentiment_after": improved_result["overall_sentiment"],
        "overall_shift": avg_score_delta,
        "sentiment_shift": sentiment_shift,
        "confidence_before": original_result.get("confidence", 0.0),
        "confidence_after": improved_result.get("confidence", 0.0),
        "confidence_delta": confidence_delta,
        "support_balance_before": support_balance_before,
        "support_balance_after": support_balance_after,
        "support_balance_delta": support_balance_delta,
        "segment_deltas": segment_deltas,
    }
