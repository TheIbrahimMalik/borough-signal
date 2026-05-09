from typing import Any


def build_recommendation(detected_issues: list[str], features: dict[str, Any]) -> str:
    suggestions = []

    if "affordability" in detected_issues and not features["affordable_housing"]:
        suggestions.append("make the affordability offer more explicit")
    elif "affordability" in detected_issues and not features["quantified_affordability"]:
        suggestions.append("quantify affordability commitments")

    if "transport" in detected_issues:
        if features["limited_parking"] and not features["transport_mitigation"]:
            suggestions.append("explain reduced parking through better bus, walking, and station access")
        elif not features["transport_mitigation"]:
            suggestions.append("address transport access and disruption")

    if "green_space" in detected_issues:
        if features["green_space_loss"] and not features["public_realm_improvements"]:
            suggestions.append("offset green space loss with public realm improvements")
        elif not features["green_space_gain"]:
            suggestions.append("protect or improve green space")

    if "safety" in detected_issues and not features["safety_measures"]:
        suggestions.append("include visible safety and lighting measures")

    if "local_character" in detected_issues and not features["heritage_sensitive_design"]:
        suggestions.append("show how the proposal respects local character")

    if not suggestions:
        return "Clarify the practical local benefits of the proposal."

    return "To improve support, " + ", and ".join(suggestions) + "."
