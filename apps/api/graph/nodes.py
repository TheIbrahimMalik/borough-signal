from langsmith import traceable

from graph.state import BoroughSignalState
from services.persistence import persist_simulation_run
from services.simulation import (
    build_recommendation,
    build_segment_rationale,
    compute_run_confidence,
    compute_segment_score,
    detect_issues,
    detect_place_mismatch,
    extract_features,
    get_area_issue_modifiers,
    score_to_stance,
)
from services.surreal import get_db


@traceable(name="parse_proposal_node")
def parse_proposal_node(state: BoroughSignalState) -> dict:
    proposal_text = state["proposal_text"]
    area_id = state["area_id"]

    proposal_features = extract_features(proposal_text)
    detected_issues = detect_issues(proposal_text, proposal_features)
    geography_warning = detect_place_mismatch(area_id, proposal_text)

    return {
        "proposal_features": proposal_features,
        "detected_issues": detected_issues,
        "geography_warning": geography_warning,
    }


@traceable(name="retrieve_context_node")
def retrieve_context_node(state: BoroughSignalState) -> dict:
    db = get_db()

    area_id = state["area_id"]
    detected_issues = state["detected_issues"]

    area_result = db.query(f"SELECT * FROM area:{area_id};")
    if not area_result:
        raise ValueError(f"Area not found: {area_id}")

    area = area_result[0]
    segments = db.query("SELECT * FROM segment ORDER BY name;")
    evidence_docs = db.query("SELECT * FROM evidence_doc ORDER BY title;")
    area_issue_modifiers = get_area_issue_modifiers(area["profile"])

    filtered_evidence = [
        doc for doc in evidence_docs
        if doc.get("metadata", {}).get("issue") in detected_issues
    ]

    return {
        "area": {
            "id": area["id"].id,
            "name": area["name"],
            "borough_code": area["borough_code"],
            "profile": area["profile"],
        },
        "segments": segments,
        "evidence_docs": evidence_docs,
        "filtered_evidence": [
            {
                "id": doc["id"].id,
                "title": doc["title"],
                "snippet": doc["snippet"],
                "issue": doc.get("metadata", {}).get("issue"),
            }
            for doc in filtered_evidence
        ],
        "area_issue_modifiers": area_issue_modifiers,
    }


@traceable(name="simulate_segments_node")
def simulate_segments_node(state: BoroughSignalState) -> dict:
    area = state["area"]
    segments = state["segments"]
    proposal_features = state["proposal_features"]
    detected_issues = state["detected_issues"]
    filtered_evidence = state["filtered_evidence"]
    area_issue_modifiers = state["area_issue_modifiers"]
    geography_warning = state.get("geography_warning")

    segment_results = []
    support_score_total = 0.0

    for segment in segments:
        priorities = segment.get("attributes", {}).get("priorities", {})
        score, top_issue = compute_segment_score(
            segment_name=segment["name"],
            priorities=priorities,
            detected_issues=detected_issues,
            area_issue_modifiers=area_issue_modifiers,
            features=proposal_features,
        )

        stance = score_to_stance(score)

        if stance == "support":
            support_score_total += 1
        elif stance == "oppose":
            support_score_total -= 1

        segment_results.append({
            "segment_id": segment["id"].id,
            "segment_name": segment["name"],
            "label": segment.get("attributes", {}).get("label", segment["name"]),
            "stance": stance,
            "score": score,
            "top_issue": top_issue,
            "rationale": build_segment_rationale(
                segment_label=segment.get("attributes", {}).get("label", segment["name"]),
                detected_issues=detected_issues,
                top_issue=top_issue,
                area_name=area["name"],
                features=proposal_features,
            ),
        })

    overall_sentiment = "mixed"
    if support_score_total > 1:
        overall_sentiment = "support"
    elif support_score_total < -1:
        overall_sentiment = "oppose"

    recommendation = build_recommendation(detected_issues, proposal_features)
    confidence = compute_run_confidence(
        detected_issues=detected_issues,
        features=proposal_features,
        evidence_count=len(filtered_evidence),
        geography_warning=geography_warning,
    )

    return {
        "segment_results": segment_results,
        "overall_sentiment": overall_sentiment,
        "recommendation": recommendation,
        "confidence": confidence,
    }


@traceable(name="persist_run_node")
def persist_run_node(state: BoroughSignalState) -> dict:
    result = {
        "area": state["area"],
        "proposal_text": state["proposal_text"],
        "proposal_features": state["proposal_features"],
        "detected_issues": state["detected_issues"],
        "overall_sentiment": state["overall_sentiment"],
        "geography_warning": state.get("geography_warning"),
        "segment_results": state["segment_results"],
        "evidence": state["filtered_evidence"],
        "recommendation": state["recommendation"],
        "confidence": state["confidence"],
    }

    persisted_ids = persist_simulation_run(result)

    response = {
        **result,
        **persisted_ids,
    }

    return {
        "proposal_id": persisted_ids["proposal_id"],
        "run_id": persisted_ids["run_id"],
        "recommendation_id": persisted_ids["recommendation_id"],
        "response": response,
    }
