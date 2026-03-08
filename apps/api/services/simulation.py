import re
from typing import Any

from services.persistence import persist_simulation_run
from services.surreal import get_db

ISSUE_KEYWORDS = {
    "affordability": [
        "affordable",
        "housing",
        "homes",
        "house",
        "rent",
        "rents",
        "tenure",
        "cheap",
        "cost",
        "cost of living",
    ],
    "transport": [
        "station",
        "tube",
        "bus",
        "transport",
        "parking",
        "road",
        "traffic",
        "commute",
        "rail",
        "walking access",
    ],
    "green_space": [
        "park",
        "green",
        "trees",
        "open space",
        "air quality",
        "garden",
        "public realm",
    ],
    "safety": [
        "safe",
        "safety",
        "lighting",
        "crime",
        "traffic safety",
        "pedestrian",
        "safer walking routes",
    ],
    "local_character": [
        "heritage",
        "character",
        "high street",
        "community",
        "local identity",
        "neighbourhood",
        "neighborhood",
    ],
}

PLACE_TO_BOROUGH = {
    "stratford": "newham",
    "camden town": "camden",
    "king's cross": "camden",
    "waterloo": "southwark",
    "elephant and castle": "southwark",
    "westminster": "westminster",
    "soho": "westminster",
    "shoreditch": "hackney",
    "dalston": "hackney",
}

SEGMENT_FEATURE_MODIFIERS = {
    "young_renters": {
        "new_homes": 0.08,
        "affordable_housing": 0.12,
        "quantified_affordability": 0.06,
        "station_access": 0.05,
        "transport_mitigation": 0.05,
        "limited_parking": 0.02,
        "retail_space": 0.03,
        "green_space_loss": -0.03,
        "green_space_gain": 0.03,
        "public_realm_improvements": 0.03,
        "safety_measures": 0.04,
        "local_character_risk": -0.01,
        "heritage_sensitive_design": 0.01,
    },
    "family_renters": {
        "new_homes": 0.07,
        "affordable_housing": 0.13,
        "quantified_affordability": 0.07,
        "station_access": 0.02,
        "transport_mitigation": 0.05,
        "limited_parking": -0.03,
        "retail_space": 0.01,
        "green_space_loss": -0.10,
        "green_space_gain": 0.08,
        "public_realm_improvements": 0.05,
        "safety_measures": 0.08,
        "local_character_risk": -0.03,
        "heritage_sensitive_design": 0.02,
    },
    "homeowners": {
        "new_homes": -0.02,
        "affordable_housing": -0.03,
        "quantified_affordability": 0.00,
        "station_access": 0.01,
        "transport_mitigation": 0.03,
        "limited_parking": -0.12,
        "retail_space": 0.00,
        "green_space_loss": -0.12,
        "green_space_gain": 0.06,
        "public_realm_improvements": 0.04,
        "safety_measures": 0.04,
        "local_character_risk": -0.10,
        "heritage_sensitive_design": 0.08,
    },
    "commuters": {
        "new_homes": 0.01,
        "affordable_housing": 0.02,
        "quantified_affordability": 0.01,
        "station_access": 0.12,
        "transport_mitigation": 0.10,
        "limited_parking": 0.05,
        "retail_space": 0.03,
        "green_space_loss": -0.01,
        "green_space_gain": 0.01,
        "public_realm_improvements": 0.02,
        "safety_measures": 0.02,
        "local_character_risk": -0.01,
        "heritage_sensitive_design": 0.01,
    },
    "older_residents": {
        "new_homes": -0.01,
        "affordable_housing": 0.00,
        "quantified_affordability": 0.01,
        "station_access": 0.01,
        "transport_mitigation": 0.04,
        "limited_parking": -0.10,
        "retail_space": 0.00,
        "green_space_loss": -0.10,
        "green_space_gain": 0.06,
        "public_realm_improvements": 0.05,
        "safety_measures": 0.09,
        "local_character_risk": -0.08,
        "heritage_sensitive_design": 0.07,
    },
    "local_business_workers": {
        "new_homes": 0.03,
        "affordable_housing": 0.03,
        "quantified_affordability": 0.02,
        "station_access": 0.06,
        "transport_mitigation": 0.06,
        "limited_parking": -0.02,
        "retail_space": 0.12,
        "green_space_loss": -0.02,
        "green_space_gain": 0.01,
        "public_realm_improvements": 0.03,
        "safety_measures": 0.03,
        "local_character_risk": -0.02,
        "heritage_sensitive_design": 0.03,
    },
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def keyword_in_text(text: str, keyword: str) -> bool:
    pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
    return re.search(pattern, text.lower()) is not None


def format_area_name(area_id: str) -> str:
    return area_id.replace("_", " ").title()


def extract_first_number(text: str) -> int | None:
    match = re.search(r"\b(\d{1,5})\b", text)
    if match:
        return int(match.group(1))
    return None


def extract_features(proposal_text: str) -> dict[str, Any]:
    text = proposal_text.lower()
    unit_count = extract_first_number(text)

    features = {
        "unit_count": unit_count,
        "new_homes": any(keyword_in_text(text, kw) for kw in ["homes", "housing", "house", "houses", "flats", "apartments"]),
        "affordable_housing": any(keyword_in_text(text, kw) for kw in ["affordable", "cheap", "low cost", "social housing"]),
        "quantified_affordability": any(keyword_in_text(text, kw) for kw in ["quantified affordability", "affordability commitments", "affordable housing offer"]),
        "station_access": any(keyword_in_text(text, kw) for kw in ["station", "tube", "rail", "bus", "transport hub"]),
        "transport_mitigation": any(keyword_in_text(text, kw) for kw in ["transport mitigation", "improved bus access", "walking access", "public transport mitigation"]),
        "limited_parking": any(keyword_in_text(text, kw) for kw in ["limited parking", "car-free", "low parking", "reduced parking"]),
        "retail_space": any(keyword_in_text(text, kw) for kw in ["retail", "shops", "shop", "commercial space", "market"]),
        "green_space_loss": any(keyword_in_text(text, kw) for kw in ["remove park", "loss of green space", "build over park", "replace trees", "replacing green space"]),
        "green_space_gain": any(keyword_in_text(text, kw) for kw in ["new park", "green roof", "trees", "open space", "public garden"]),
        "public_realm_improvements": any(keyword_in_text(text, kw) for kw in ["public realm improvements", "public realm", "greenery", "public open space"]),
        "safety_measures": any(keyword_in_text(text, kw) for kw in ["lighting", "safe routes", "safer walking routes", "pedestrian crossing", "traffic calming", "cctv"]),
        "local_character_risk": any(keyword_in_text(text, kw) for kw in ["tower block", "high-rise", "demolish heritage", "replace historic", "change character", "exclusive skyscraper", "luxury tower"]),
        "heritage_sensitive_design": any(keyword_in_text(text, kw) for kw in ["respect local character", "respect heritage", "heritage-sensitive design", "design changes that respect local character"]),
    }

    return features


def detect_issues(proposal_text: str, features: dict[str, Any]) -> list[str]:
    text = proposal_text.lower()
    detected: list[str] = []

    for issue, keywords in ISSUE_KEYWORDS.items():
        if any(keyword_in_text(text, keyword) for keyword in keywords):
            detected.append(issue)

    if features["new_homes"] or features["affordable_housing"] or features["quantified_affordability"]:
        if "affordability" not in detected:
            detected.append("affordability")

    if features["station_access"] or features["limited_parking"] or features["retail_space"] or features["transport_mitigation"]:
        if "transport" not in detected:
            detected.append("transport")

    if features["green_space_loss"] or features["green_space_gain"] or features["public_realm_improvements"]:
        if "green_space" not in detected:
            detected.append("green_space")

    if features["safety_measures"]:
        if "safety" not in detected:
            detected.append("safety")

    if features["local_character_risk"] or features["heritage_sensitive_design"]:
        if "local_character" not in detected:
            detected.append("local_character")

    if not detected:
        detected = ["affordability", "transport"]

    return detected


def detect_place_mismatch(area_id: str, proposal_text: str) -> str | None:
    text = proposal_text.lower()

    for place, expected_area_id in PLACE_TO_BOROUGH.items():
        if keyword_in_text(text, place) and expected_area_id != area_id:
            return (
                f"This proposal mentions {place.title()}, which is usually associated "
                f"with {format_area_name(expected_area_id)}, not {format_area_name(area_id)}."
            )

    return None


def get_area_issue_modifiers(area_profile: dict[str, Any]) -> dict[str, float]:
    modifiers = {
        "affordability": 0.0,
        "transport": 0.0,
        "green_space": 0.0,
        "safety": 0.0,
        "local_character": 0.0,
    }

    if area_profile.get("housing_pressure") == "high":
        modifiers["affordability"] += 0.08

    if area_profile.get("public_transport_dependency") == "high":
        modifiers["transport"] += 0.08

    if area_profile.get("green_space_sensitivity") == "high":
        modifiers["green_space"] += 0.08

    if area_profile.get("family_households") == "moderate":
        modifiers["safety"] += 0.03
    elif area_profile.get("family_households") == "low":
        modifiers["local_character"] += 0.03

    return modifiers


def score_to_stance(score: float) -> str:
    if score >= 0.75:
        return "support"
    if score >= 0.5:
        return "mixed"
    return "oppose"


def build_segment_rationale(
    segment_label: str,
    detected_issues: list[str],
    top_issue: str,
    area_name: str,
    features: dict[str, Any],
) -> str:
    reasons = []

    if features["affordable_housing"]:
        reasons.append("affordability")
    if features["quantified_affordability"]:
        reasons.append("clear affordability commitments")
    if features["station_access"]:
        reasons.append("station access")
    if features["transport_mitigation"]:
        reasons.append("transport mitigation")
    if features["limited_parking"]:
        reasons.append("parking changes")
    if features["retail_space"]:
        reasons.append("retail space")
    if features["green_space_loss"]:
        reasons.append("green space loss")
    if features["green_space_gain"]:
        reasons.append("green space improvements")
    if features["public_realm_improvements"]:
        reasons.append("public realm improvements")
    if features["safety_measures"]:
        reasons.append("safety measures")
    if features["local_character_risk"]:
        reasons.append("local character concerns")
    if features["heritage_sensitive_design"]:
        reasons.append("heritage-sensitive design")

    if not reasons:
        reasons = [issue.replace("_", " ") for issue in detected_issues]

    reasons_text = ", ".join(reasons[:3])

    return (
        f"{segment_label} in {area_name} are likely to react to {reasons_text}, "
        f"with strongest sensitivity around {top_issue.replace('_', ' ')}."
    )


def build_recommendation(detected_issues: list[str], features: dict[str, Any]) -> str:
    suggestions = []

    if "affordability" in detected_issues and not features["affordable_housing"]:
        suggestions.append("make the affordability offer more explicit")
    elif "affordability" in detected_issues and not features["quantified_affordability"]:
        suggestions.append("quantify affordability commitments")

    if "transport" in detected_issues:
        if features["limited_parking"] and not features["transport_mitigation"]:
            suggestions.append("explain reduced parking through better bus, walking, and station access")
        elif not features["transport_mitigation"]:
            suggestions.append("address transport access and disruption")

    if "green_space" in detected_issues:
        if features["green_space_loss"] and not features["public_realm_improvements"]:
            suggestions.append("offset green space loss with public realm improvements")
        elif not features["green_space_gain"]:
            suggestions.append("protect or improve green space")

    if "safety" in detected_issues and not features["safety_measures"]:
        suggestions.append("include visible safety and lighting measures")

    if "local_character" in detected_issues and not features["heritage_sensitive_design"]:
        suggestions.append("show how the proposal respects local character")

    if not suggestions:
        return "Clarify the practical local benefits of the proposal."

    return "To improve support, " + ", and ".join(suggestions) + "."


def compute_segment_score(
    segment_name: str,
    priorities: dict[str, float],
    detected_issues: list[str],
    area_issue_modifiers: dict[str, float],
    features: dict[str, Any],
) -> tuple[float, str]:
    issue_scores = {}

    for issue in detected_issues:
        base = float(priorities.get(issue, 0.0))
        area_boost = area_issue_modifiers.get(issue, 0.0)
        issue_scores[issue] = clamp(base + area_boost)

    base_score = sum(issue_scores.values()) / max(len(issue_scores), 1)

    feature_modifiers = SEGMENT_FEATURE_MODIFIERS.get(segment_name, {})
    modifier_total = 0.0

    for feature_name, feature_value in features.items():
        if feature_name == "unit_count":
            continue
        if feature_value:
            modifier_total += feature_modifiers.get(feature_name, 0.0)

    unit_count = features.get("unit_count")
    if unit_count:
        if unit_count >= 200:
            if segment_name in {"young_renters", "family_renters"}:
                modifier_total += 0.03
            if segment_name in {"homeowners", "older_residents"}:
                modifier_total -= 0.02
        elif unit_count <= 20:
            if segment_name in {"young_renters", "family_renters"}:
                modifier_total -= 0.01

    final_score = clamp(base_score + modifier_total)
    top_issue = max(issue_scores, key=issue_scores.get)

    return round(final_score, 2), top_issue


def compute_run_confidence(
    detected_issues: list[str],
    features: dict[str, Any],
    evidence_count: int,
    geography_warning: str | None,
) -> float:
    active_feature_count = sum(
        1 for key, value in features.items()
        if key != "unit_count" and bool(value)
    )

    confidence = 0.35
    confidence += 0.08 * len(detected_issues)
    confidence += 0.04 * active_feature_count
    confidence += 0.03 * evidence_count

    if geography_warning:
        confidence -= 0.08

    return round(clamp(confidence, 0.2, 0.95), 2)


def run_simulation(area_id: str, proposal_text: str) -> dict[str, Any]:
    db = get_db()

    area_result = db.query(f"SELECT * FROM area:{area_id};")
    if not area_result:
        raise ValueError(f"Area not found: {area_id}")

    area = area_result[0]

    segments = db.query("SELECT * FROM segment ORDER BY name;")
    evidence_docs = db.query("SELECT * FROM evidence_doc ORDER BY title;")

    features = extract_features(proposal_text)
    detected_issues = detect_issues(proposal_text, features)
    geography_warning = detect_place_mismatch(area_id, proposal_text)
    area_issue_modifiers = get_area_issue_modifiers(area["profile"])

    filtered_evidence = [
        doc for doc in evidence_docs
        if doc.get("metadata", {}).get("issue") in detected_issues
    ]

    segment_results = []
    support_score_total = 0.0

    for segment in segments:
        priorities = segment.get("attributes", {}).get("priorities", {})
        score, top_issue = compute_segment_score(
            segment_name=segment["name"],
            priorities=priorities,
            detected_issues=detected_issues,
            area_issue_modifiers=area_issue_modifiers,
            features=features,
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
                features=features,
            ),
        })

    overall_sentiment = "mixed"
    if support_score_total > 1:
        overall_sentiment = "support"
    elif support_score_total < -1:
        overall_sentiment = "oppose"

    result = {
        "area": {
            "id": area["id"].id,
            "name": area["name"],
            "borough_code": area["borough_code"],
            "profile": area["profile"],
        },
        "proposal_text": proposal_text,
        "proposal_features": features,
        "detected_issues": detected_issues,
        "overall_sentiment": overall_sentiment,
        "geography_warning": geography_warning,
        "segment_results": segment_results,
        "evidence": [
            {
                "id": doc["id"].id,
                "title": doc["title"],
                "snippet": doc["snippet"],
                "issue": doc.get("metadata", {}).get("issue"),
            }
            for doc in filtered_evidence
        ],
        "recommendation": build_recommendation(detected_issues, features),
        "confidence": compute_run_confidence(
            detected_issues=detected_issues,
            features=features,
            evidence_count=len(filtered_evidence),
            geography_warning=geography_warning,
        ),
    }

    persisted_ids = persist_simulation_run(result)
    result.update(persisted_ids)

    return result
