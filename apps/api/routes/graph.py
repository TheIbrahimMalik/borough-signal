from fastapi import APIRouter, HTTPException

from services.graph_view import get_proposal_graph_view

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("/proposal/{proposal_id}")
def graph_for_proposal(proposal_id: str):
    try:
        return get_proposal_graph_view(proposal_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
