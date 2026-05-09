from services.recommendations import build_recommendation


def _empty_features() -> dict:
    return {k: False for k in [
        "new_homes", "affordable_housing", "quantified_affordability",
        "station_access", "transport_mitigation", "limited_parking",
        "retail_space", "green_space_loss", "green_space_gain",
        "public_realm_improvements", "safety_measures",
        "local_character_risk", "heritage_sensitive_design",
    ]} | {"unit_count": None}


def test_build_recommendation_suggests_quantification_when_unquantified():
    features = _empty_features()
    features["affordable_housing"] = True
    features["quantified_affordability"] = False

    text = build_recommendation(["affordability"], features)
    assert "quantify" in text.lower()


def test_build_recommendation_default_when_no_suggestions():
    text = build_recommendation([], _empty_features())
    assert text == "Clarify the practical local benefits of the proposal."
