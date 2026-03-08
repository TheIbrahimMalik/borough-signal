from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from graph.workflow import boroughsignal_graph
from services.comparison import (
    build_improved_proposal_text,
    compare_simulation_results,
)

router = APIRouter(tags=["simulate"])


class SimulationRequest(BaseModel):
    area_id: str
    proposal_text: str


@router.post("/simulate")
def simulate(request: SimulationRequest):
    try:
        final_state = boroughsignal_graph.invoke(
            {
                "area_id": request.area_id,
                "proposal_text": request.proposal_text,
            }
        )
        return final_state["response"]
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/simulate/compare")
def simulate_compare(request: SimulationRequest):
    try:
        original_state = boroughsignal_graph.invoke(
            {
                "area_id": request.area_id,
                "proposal_text": request.proposal_text,
            }
        )
        original_result = original_state["response"]

        improved_proposal_text = build_improved_proposal_text(original_result)

        improved_state = boroughsignal_graph.invoke(
            {
                "area_id": request.area_id,
                "proposal_text": improved_proposal_text,
            }
        )
        improved_result = improved_state["response"]

        comparison = compare_simulation_results(
            original_result=original_result,
            improved_result=improved_result,
        )

        return {
            "original": original_result,
            "improved_proposal_text": improved_proposal_text,
            "improved": improved_result,
            "comparison": comparison,
        }
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
