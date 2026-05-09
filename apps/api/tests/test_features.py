from services.features import extract_features, keyword_in_text


def test_extract_features_units_and_homes():
    features = extract_features(
        "Build 250 affordable homes near Stratford station with limited parking and new retail space."
    )
    assert features["unit_count"] == 250
    assert features["new_homes"] is True
    assert features["affordable_housing"] is True
    assert features["station_access"] is True
    assert features["limited_parking"] is True
    assert features["retail_space"] is True
    assert features["green_space_loss"] is False
    assert features["heritage_sensitive_design"] is False


def test_extract_features_word_boundary():
    # "delightful" shares the substring "light" but must NOT trigger the
    # `lighting` keyword used by safety_measures, because keyword_in_text
    # is anchored on \b boundaries.
    assert keyword_in_text("a delightful evening", "lighting") is False
    assert keyword_in_text("install proper lighting", "lighting") is True

    features = extract_features("a delightful evening on the high street")
    assert features["safety_measures"] is False


def test_extract_features_empty_text_all_false():
    features = extract_features("")
    assert features["unit_count"] is None
    boolean_keys = [k for k, v in features.items() if k != "unit_count"]
    for key in boolean_keys:
        assert features[key] is False, f"{key} should be False on empty input"
