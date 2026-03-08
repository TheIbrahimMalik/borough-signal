# BoroughSignal Final 90-Second Pitch

Hi, we built BoroughSignal, a stateful synthetic audience decision-support system for London planning proposals.

The problem we wanted to solve is that planning proposals are often evaluated with shallow stakeholder assumptions and fragmented context. BoroughSignal gives teams a structured way to simulate how different local audience segments may react, why they react that way, and how support changes after improving the proposal.

Technically, the system uses LangGraph for workflow orchestration, SurrealDB as the persistent structured memory and graph data layer, and LangSmith for observability.

The workflow is simple but stateful:

1. parse the proposal into structured features
2. retrieve borough, issue, segment, and evidence context
3. simulate audience reactions
4. persist the run and graph relationships in SurrealDB

We model graph relationships such as proposal affecting issues, segments caring about issues, and responses citing evidence. That lets us explain not just the result, but the structured path behind the result.

On the frontend, a user selects a borough, runs a simulation, sees segment reactions and evidence, and then runs a before/after comparison. The system generates an improved proposal version, reruns the workflow, and shows how segment scores and overall signal change.

So the key idea is that BoroughSignal is not a one-shot chatbot. It is a persistent, explainable, graph-backed decision system for iterating on proposals over time.
