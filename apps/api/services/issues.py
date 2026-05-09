from typing import Any

from services.features import keyword_in_text

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
