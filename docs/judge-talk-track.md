# BoroughSignal Judge Talk Track

## Opening

Hi, we built BoroughSignal, a stateful synthetic audience decision-support system for London planning proposals.

The problem is that planning proposals are often evaluated with shallow stakeholder assumptions and fragmented context. BoroughSignal gives teams a structured way to simulate how different audience segments may react, why they react that way, and how support changes after improving the proposal.

## Architecture

BoroughSignal uses LangGraph for workflow orchestration, SurrealDB as the persistent structured memory and graph data layer, and LangSmith for observability.

The workflow is:

1. parse proposal
2. retrieve borough, issue, and evidence context
3. simulate audience segments
4. persist the run

## Knowledge graph story

We model graph relationships such as:

- proposal -> AFFECTS -> issue
- segment -> CARES_ABOUT -> issue
- response -> CITES -> evidence

So the system is not just returning a label. It can explain the structured path behind the result.

## Demo flow

First I’ll run a planning proposal.

You can see:
- detected issues
- segment reactions
- evidence
- recommendation
- recent persisted runs

Then I’ll run the before/after comparison.

This generates an improved proposal, reruns the workflow, and shows:
- sentiment shift
- signal strength change
- segment deltas
- why scores changed

## Why it fits the hackathon

This project is strongly aligned with the hackathon goals because it shows:

- LangGraph agent workflow orchestration
- persistent state in SurrealDB
- graph-based relationships between proposals, issues, segments, and evidence
- practical real-world use
- LangSmith observability

## Closing

The key idea is that BoroughSignal is not a one-shot chatbot. It is a persistent, explainable, graph-backed decision system that helps users explore and improve proposals over time.
