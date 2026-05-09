from services.geography import detect_place_mismatch


def test_detect_place_mismatch_warns_when_borough_wrong():
    warning = detect_place_mismatch(
        area_id="camden",
        proposal_text="Build 250 homes near Stratford station.",
    )
    assert warning is not None
    assert "Stratford" in warning
    assert "Newham" in warning
    assert "Camden" in warning


def test_detect_place_mismatch_silent_when_borough_correct():
    warning = detect_place_mismatch(
        area_id="newham",
        proposal_text="Build 250 homes near Stratford station.",
    )
    assert warning is None
