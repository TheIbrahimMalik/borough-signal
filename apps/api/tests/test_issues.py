from services.features import extract_features
from services.issues import detect_issues
from tests._helpers import empty_features


def test_detect_issues_from_keywords():
    text = "A new tube link near the local park"
    features = extract_features(text)
    issues = detect_issues(text, features)
    assert "transport" in issues
    assert "green_space" in issues


def test_detect_issues_from_features_fallback():
    # No issue keywords in this text, but a feature flag forces the issue in.
    features = empty_features()
    features["station_access"] = True
    issues = detect_issues("redacted", features)
    assert "transport" in issues


def test_detect_issues_default_when_nothing_matches():
    features = empty_features()
    issues = detect_issues("redacted", features)
    assert issues == ["affordability", "transport"]
