from services.recommendations import build_recommendation
from tests._helpers import empty_features


def test_build_recommendation_suggests_quantification_when_unquantified():
    features = empty_features()
    features["affordable_housing"] = True
    features["quantified_affordability"] = False

    text = build_recommendation(["affordability"], features)
    assert "quantify" in text.lower()


def test_build_recommendation_default_when_no_suggestions():
    text = build_recommendation([], empty_features())
    assert text == "Clarify the practical local benefits of the proposal."
