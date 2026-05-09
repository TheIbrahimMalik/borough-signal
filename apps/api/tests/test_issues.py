from services.features import extract_features
from services.issues import detect_issues


def _empty_features() -> dict:
    return {k: False for k in [
        "new_homes", "affordable_housing", "quantified_affordability",
        "station_access", "transport_mitigation", "limited_parking",
        "retail_space", "green_space_loss", "green_space_gain",
        "public_realm_improvements", "safety_measures",
        "local_character_risk", "heritage_sensitive_design",
    ]} | {"unit_count": None}


def test_detect_issues_from_keywords():
    text = "A new tube link near the local park"
    features = extract_features(text)
    issues = detect_issues(text, features)
    assert "transport" in issues
    assert "green_space" in issues


def test_detect_issues_from_features_fallback():
    # No issue keywords in this text, but a feature flag forces the issue in.
    features = _empty_features()
    features["station_access"] = True
    issues = detect_issues("redacted", features)
    assert "transport" in issues


def test_detect_issues_default_when_nothing_matches():
    features = _empty_features()
    issues = detect_issues("redacted", features)
    assert issues == ["affordability", "transport"]
