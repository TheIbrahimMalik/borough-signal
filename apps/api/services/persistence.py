import json
import uuid

from services.surreal import get_db


def make_record_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def record_array(table: str, record_ids: list[str]) -> str:
    if not record_ids:
        return "[]"
    return "[" + ", ".join(f"{table}:{record_id}" for record_id in record_ids) + "]"


def persist_simulation_run(result: dict) -> dict:
    db = get_db()

    proposal_record_id = make_record_id("proposal")
    run_record_id = make_record_id("run")
    recommendation_record_id = make_record_id("recommendation")

    extracted = {
        "detected_issues": result["detected_issues"],
        "geography_warning": result.get("geography_warning"),
        "proposal_features": result.get("proposal_features", {}),
    }

    db.query(
        f"""
        CREATE proposal:{proposal_record_id} CONTENT {{
            title: {json.dumps(f"{result['area']['name']} proposal")},
            raw_text: {json.dumps(result["proposal_text"])},
            extracted: {json.dumps(extracted)},
            area_id: area:{result["area"]["id"]}
        }};
        """
    )

    summary = {
        "overall_sentiment": result["overall_sentiment"],
        "detected_issues": result["detected_issues"],
        "geography_warning": result.get("geography_warning"),
        "segment_count": len(result["segment_results"]),
        "evidence_count": len(result["evidence"]),
        "proposal_text": result["proposal_text"],
        "proposal_features": result.get("proposal_features", {}),
    }

    db.query(
        f"""
        CREATE simulation_run:{run_record_id} CONTENT {{
            proposal_id: proposal:{proposal_record_id},
            area_id: area:{result["area"]["id"]},
            status: "completed",
            summary: {json.dumps(summary)},
            confidence: {float(result.get("confidence", 0.5))}
        }};
        """
    )

    for issue in result["detected_issues"]:
        db.query(
            f"""
            RELATE proposal:{proposal_record_id}->AFFECTS->issue:{issue} CONTENT {{
                weight: 1.0
            }};
            """
        )

    for segment_result in result["segment_results"]:
        response_record_id = make_record_id("response")

        matched_evidence_ids = [
            item["id"]
            for item in result["evidence"]
            if item["issue"] == segment_result["top_issue"]
        ][:1]

        scores = {
            "score": segment_result["score"],
            "top_issue": segment_result["top_issue"],
            "segment_id": segment_result["segment_id"],
            "label": segment_result["label"],
        }

        db.query(
            f"""
            CREATE response:{response_record_id} CONTENT {{
                run_id: simulation_run:{run_record_id},
                persona_id: NONE,
                stance: {json.dumps(segment_result["stance"])},
                rationale: {json.dumps(segment_result["rationale"])},
                cited_evidence_ids: {record_array("evidence_doc", matched_evidence_ids)},
                scores: {json.dumps(scores)}
            }};
            """
        )

        for evidence_id in matched_evidence_ids:
            db.query(
                f"""
                RELATE response:{response_record_id}->CITES->evidence_doc:{evidence_id};
                """
            )

    expected_shift = {
        "overall_sentiment": result["overall_sentiment"],
        "detected_issues": result["detected_issues"],
        "confidence": result.get("confidence"),
    }

    db.query(
        f"""
        CREATE recommendation:{recommendation_record_id} CONTENT {{
            run_id: simulation_run:{run_record_id},
            original_text: {json.dumps(result["proposal_text"])},
            rewritten_text: {json.dumps(result["recommendation"])},
            expected_shift: {json.dumps(expected_shift)}
        }};
        """
    )

    return {
        "proposal_id": proposal_record_id,
        "run_id": run_record_id,
        "recommendation_id": recommendation_record_id,
    }
