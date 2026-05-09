from services.scoring import (
    compute_run_confidence,
    compute_segment_score,
    get_area_issue_modifiers,
    score_to_stance,
)


def _empty_features() -> dict:
    return {k: False for k in [
        "new_homes", "affordable_housing", "quantified_affordability",
        "station_access", "transport_mitigation", "limited_parking",
        "retail_space", "green_space_loss", "green_space_gain",
        "public_realm_improvements", "safety_measures",
        "local_character_risk", "heritage_sensitive_design",
    ]} | {"unit_count": None}


def test_score_to_stance_thresholds():
    assert score_to_stance(0.75) == "support"
    assert score_to_stance(0.74) == "mixed"
    assert score_to_stance(0.50) == "mixed"
    assert score_to_stance(0.49) == "oppose"


def test_get_area_issue_modifiers_profile_signals():
    profile = {
        "housing_pressure": "high",
        "public_transport_dependency": "moderate",
        "green_space_sensitivity": "moderate",
        "family_households": "low",
    }
    modifiers = get_area_issue_modifiers(profile)
    assert modifiers["affordability"] == 0.08
    assert modifiers["transport"] == 0.0
    assert modifiers["local_character"] == 0.03  # family_households == "low"
    assert modifiers["safety"] == 0.0


def test_compute_segment_score_combines_priorities_and_modifiers():
    features = _empty_features()
    features["new_homes"] = True
    features["affordable_housing"] = True
    features["station_access"] = True

    score, top_issue = compute_segment_score(
        segment_name="young_renters",
        priorities={"affordability": 0.9, "transport": 0.8},
        detected_issues=["affordability", "transport"],
        area_issue_modifiers={"affordability": 0.08, "transport": 0.0},
        features=features,
    )

    assert 0.0 <= score <= 1.0
    # young_renters care most about affordability (0.9 + area boost 0.08, clamped),
    # which exceeds transport (0.8 + 0.0).
    assert top_issue == "affordability"


def test_compute_run_confidence_geography_warning_penalty_and_clamp():
    features = _empty_features()

    # No issues, no features, no evidence -> base 0.35; clamped to 0.20 floor
    # once the geography warning subtracts 0.08.
    low = compute_run_confidence(
        detected_issues=[],
        features=features,
        evidence_count=0,
        geography_warning="mismatch",
    )
    assert low == 0.27  # 0.35 - 0.08, rounded; well above the 0.20 floor

    # Lots of signal -> capped at 0.95.
    features_active = {**features, "new_homes": True, "affordable_housing": True,
                       "station_access": True, "safety_measures": True}
    high = compute_run_confidence(
        detected_issues=["affordability", "transport", "safety", "green_space", "local_character"],
        features=features_active,
        evidence_count=20,
        geography_warning=None,
    )
    assert high == 0.95
