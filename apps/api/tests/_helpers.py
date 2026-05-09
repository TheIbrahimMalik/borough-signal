from typing import Any


def empty_features() -> dict[str, Any]:
    """Return a feature dict with every boolean flag False and unit_count None.

    Mirrors the shape produced by services.features.extract_features so tests
    can mutate individual flags without re-listing the full schema.
    """
    return {k: False for k in [
        "new_homes", "affordable_housing", "quantified_affordability",
        "station_access", "transport_mitigation", "limited_parking",
        "retail_space", "green_space_loss", "green_space_gain",
        "public_realm_improvements", "safety_measures",
        "local_character_risk", "heritage_sensitive_design",
    ]} | {"unit_count": None}
