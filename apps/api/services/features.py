import re
from typing import Any


def keyword_in_text(text: str, keyword: str) -> bool:
    pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
    return re.search(pattern, text.lower()) is not None


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
