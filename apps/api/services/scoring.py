from typing import Any

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
