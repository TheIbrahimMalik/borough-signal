# BoroughSignal

**Author:** Ibrahim Malik

Synthetic audience copilot for London planning proposals.

BoroughSignal simulates how different audience segments may react to a planning proposal, using structured context, persistent state, and a LangGraph workflow backed by SurrealDB.

---

## Why This Matters

Planning proposals are often evaluated with fragmented context and shallow stakeholder assumptions. BoroughSignal helps teams explore how different local audience segments may respond to a proposal, why they respond that way, and how support may change after improving the proposal.

---

## What It Does

A user selects a London borough and enters a planning proposal. The system then:

1. Parses the proposal into structured features
2. Retrieves borough, issue, and evidence context from SurrealDB
3. Simulates how audience segments respond
4. Stores the run, proposal, recommendation, and graph relationships in SurrealDB
5. Generates an improved proposal version
6. Reruns the simulation and compares before vs after

---

## Stack

- **Frontend:** Next.js
- **Backend:** FastAPI
- **Workflow orchestration:** LangGraph
- **Observability:** LangSmith
- **Database:** SurrealDB
- **Containerisation:** Docker (for SurrealDB)

---

## Architecture

BoroughSignal uses a multi-step LangGraph workflow with persistent state in SurrealDB.

### LangGraph Workflow

- `parse_proposal`
- `retrieve_context`
- `simulate_segments`
- `persist_run`

### Persistent Entities in SurrealDB

- `area`
- `segment`
- `issue`
- `proposal`
- `simulation_run`
- `response`
- `recommendation`
- `evidence_doc`

### Graph Relationships

- `AFFECTS`
- `CARES_ABOUT`
- `CITES`
- `LIVES_IN`
- `BELONGS_TO`

---

## Key Features

- Structured synthetic audience simulation
- Borough-aware proposal analysis
- Geography mismatch warnings for known place/borough inconsistencies
- Persistent run history
- Before/after proposal comparison
- LangSmith traces for workflow observability
- Sample scenarios for reliable demo flow

---

## Example Use Cases

- Test support for affordable housing proposals
- Explore how transport changes affect different segments
- Compare original vs improved proposal wording
- Inspect how borough context changes audience reactions

---

## Demo Scenarios

The app includes curated sample scenarios:

- Newham housing near Stratford
- Southwark tower block trade-off
- Hackney safer streets and shops
- Camden homes near King's Cross

---

## How It Works

### 1. Proposal Parsing

The backend extracts structured proposal features such as new homes, affordable housing, quantified affordability, station access, transport mitigation, limited parking, retail space, green space loss/gain, public realm improvements, safety measures, local character risk, and heritage-sensitive design.

### 2. Context Retrieval

The system retrieves the borough profile, audience segments, issue taxonomy, and evidence snippets.

### 3. Segment Simulation

Each segment is scored using issue priorities, borough-specific issue modifiers, proposal feature modifiers, and feature-specific bonuses and penalties.

### 4. Persistence

Each run stores the proposal text, extracted features, detected issues, recommendation, segment results, confidence and signal strength, and graph relationships to issues and evidence.

### 5. Comparison

The app generates an improved proposal version and reruns the simulation to show how scores and sentiment change.

---

## Local Development

### Requirements

- Python 3
- Node.js / npm
- Docker
- SurrealDB CLI
- LangSmith account and API key

### Start the Backend

```bash
cd apps/api
source .venv/bin/activate
python3 -m uvicorn main:app --reload --port 8001
```

### Start the Frontend

```bash
cd apps/web
npm run dev
```

### Start SurrealDB

From the repo root:

```bash
sudo docker run --rm --pull always --name surrealdb \
  -p 8000:8000 \
  --user $(id -u) \
  -v "$(pwd)/surreal-data:/mydata" \
  surrealdb/surrealdb:latest \
  start --log info --user root --pass root rocksdb:/mydata/boroughsignal.db
```

### Environment Variables

The API uses a `.env` file at `apps/api/.env`:

```
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=...
LANGSMITH_PROJECT=boroughsignal
SURREALDB_URL=ws://localhost:8000
SURREALDB_USERNAME=root
SURREALDB_PASSWORD=root
SURREALDB_NAMESPACE=boroughsignal
SURREALDB_DATABASE=main
```

---

## Limitations

- This is a synthetic audience system, not real survey data
- Geographic validation is currently lightweight and curated, not full GIS-based
- Proposal understanding is partly rule-based
- Segment behaviour is modelled, not learned from real labelled response data
- Current evidence retrieval is small and curated

---

## Why This Is a Good Fit for the Hackathon

BoroughSignal aligns with the LangChain × SurrealDB hackathon goals by demonstrating:

- LangGraph agent workflow orchestration
- Structured persistent memory in SurrealDB
- Graph-style relationships between proposals, issues, segments, and evidence
- Practical, real-world decision support
- Observable workflow execution through LangSmith

---

## Future Work

- Richer retrieval from larger planning datasets
- Stronger place resolution and borough matching
- More expressive proposal parsing
- Learned calibration against real-world data
- Reusable open-source SurrealDB + LangGraph simulation components

---

## Naming Conventions

| Context | Value |
|---|---|
| Product name | `BoroughSignal` |
| GitHub repo | `borough-signal` |
| Internal/config slug | `boroughsignal` |

---

## Graph traversal example

BoroughSignal uses graph relationships in SurrealDB to explain how a proposal is connected to issues, segments, and evidence.

Example relationship path:

- `proposal -> AFFECTS -> issue`
- `segment -> CARES_ABOUT -> issue`
- `response -> CITES -> evidence_doc`

This lets the system explain not just the final result, but also the structured path behind it.

Example idea:

- proposal affects affordability and transport
- young renters care about affordability
- commuters care about transport
- responses cite evidence documents linked to those issues

---

## Output interpretation

BoroughSignal reports two different summary outputs: **overall sentiment** and **signal strength**.

### Overall sentiment

Overall sentiment is the aggregate direction of audience reaction: `support`, `mixed`, or `oppose`.

The system first assigns each audience segment a numeric score, then maps that score to a stance:

- `score >= 0.75` → `support`
- `0.50 <= score < 0.75` → `mixed`
- `score < 0.50` → `oppose`

These segment stances are then aggregated using:

- `support = +1`
- `mixed = 0`
- `oppose = -1`

If the total is:

- greater than `1` → overall sentiment = `support`
- less than `-1` → overall sentiment = `oppose`
- otherwise → overall sentiment = `mixed`

### Signal strength

Signal strength is a separate value in the range `0–1`. It is **not** a probability of support.

Instead, it reflects how much structured signal the system had for the analysis, based on factors such as:

- detected proposal features
- detected issues
- retrieved evidence
- geography consistency

This means a proposal can have **high signal strength** but still produce an **oppose** overall sentiment. In that case, the system is indicating that it found a strong structured basis for a negative result.

### Signal strength calculation

Signal strength is currently a heuristic score rather than a calibrated probability.

It is calculated from:

- a base score of `0.35`
- `+ 0.08 × number of detected issues`
- `+ 0.04 × number of active modeled features`
- `+ 0.03 × evidence count`
- `- 0.08` if a geography mismatch warning is triggered

The result is then clamped to the range `0.20–0.95` and rounded to 2 decimal places.

In practice, signal strength should be interpreted as a measure of **analysis richness and structured grounding**, not as a measure of whether a proposal is likely to be supported.

---

## Licence

MIT Licence.