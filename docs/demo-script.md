# BoroughSignal Demo Script

## 2-minute version

Hi, we built **BoroughSignal**, a synthetic audience copilot for London planning proposals.

The problem we wanted to solve is that planning proposals are often judged with shallow stakeholder assumptions and fragmented context. Teams can describe a proposal, but they usually do not have a structured way to simulate how different local audience segments might respond, why they respond that way, or how support changes after improving the proposal.

BoroughSignal uses **LangGraph** for workflow orchestration, **SurrealDB** as the persistent data layer, and **LangSmith** for observability.

Here’s how it works.

A user selects a London borough and enters a proposal. The workflow parses the proposal into structured features like affordable housing, station access, parking changes, green-space tradeoffs, safety measures, and local-character risk.

Then BoroughSignal retrieves borough context, issue taxonomy, evidence snippets, and audience segment data from SurrealDB. It simulates how segments like young renters, family renters, commuters, homeowners, older residents, and local business workers respond.

Each run is persisted in SurrealDB as structured state: proposal, simulation run, recommendation, responses, and graph relationships to issues and evidence.

Here’s a sample proposal in Southwark. We can see the detected issues, segment reactions, evidence used, and the recommendation.

Now the important part: BoroughSignal can run a **before/after comparison**. It generates an improved proposal version, reruns the workflow, and shows how signal strength and segment scores shift.

So instead of a one-shot chatbot answer, we built a stateful decision-support system with structured memory, persistent runs, workflow observability, and proposal iteration.

## Live demo flow

1. Open the app homepage
2. Click a sample scenario
3. Run a simulation
4. Show:
   - detected issues
   - segment reactions
   - evidence
   - recommendation
5. Scroll to recent runs
6. Click Compare before / after
7. Show:
   - original vs improved proposal
   - signal strength change
   - segment deltas
8. Mention LangSmith traces
9. Mention SurrealDB persistence survives restarts

## 30-second backup version

BoroughSignal is a synthetic audience copilot for London planning proposals. It uses LangGraph to orchestrate parsing, context retrieval, simulation, and persistence; SurrealDB to store structured state and graph relationships; and LangSmith for observability. Users can simulate a proposal, inspect segment reactions, then compare the original proposal against an improved version to see how support changes.
