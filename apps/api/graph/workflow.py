from langgraph.graph import END, START, StateGraph

from graph.nodes import (
    parse_proposal_node,
    persist_run_node,
    retrieve_context_node,
    simulate_segments_node,
)
from graph.state import BoroughSignalState

builder = StateGraph(BoroughSignalState)

builder.add_node("parse_proposal", parse_proposal_node)
builder.add_node("retrieve_context", retrieve_context_node)
builder.add_node("simulate_segments", simulate_segments_node)
builder.add_node("persist_run", persist_run_node)

builder.add_edge(START, "parse_proposal")
builder.add_edge("parse_proposal", "retrieve_context")
builder.add_edge("retrieve_context", "simulate_segments")
builder.add_edge("simulate_segments", "persist_run")
builder.add_edge("persist_run", END)

boroughsignal_graph = builder.compile()
