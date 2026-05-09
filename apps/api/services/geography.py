from services.features import keyword_in_text

PLACE_TO_BOROUGH = {
    "stratford": "newham",
    "camden town": "camden",
    "king's cross": "camden",
    "waterloo": "southwark",
    "elephant and castle": "southwark",
    "westminster": "westminster",
    "soho": "westminster",
    "shoreditch": "hackney",
    "dalston": "hackney",
}


def format_area_name(area_id: str) -> str:
    return area_id.replace("_", " ").title()


def detect_place_mismatch(area_id: str, proposal_text: str) -> str | None:
    text = proposal_text.lower()

    for place, expected_area_id in PLACE_TO_BOROUGH.items():
        if keyword_in_text(text, place) and expected_area_id != area_id:
            return (
                f"This proposal mentions {place.title()}, which is usually associated "
                f"with {format_area_name(expected_area_id)}, not {format_area_name(area_id)}."
            )

    return None
