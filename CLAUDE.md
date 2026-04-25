# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

BoroughSignal — synthetic-audience copilot for London planning proposals. A LangGraph pipeline scores how demographic segments react to a proposal, persists runs to SurrealDB, and serves results via FastAPI to a Next.js frontend.

## Repo layout

- `apps/api/` — FastAPI + LangGraph backend (Python 3.12). Entry: `main.py`. Pipeline in `graph/workflow.py`, scoring in `services/simulation.py`.
- `apps/web/` — Next.js 16 + React 19 + Tailwind 4 frontend. Single-page UI in `src/app/page.tsx`, API client in `src/lib/api.ts`. **Has its own nested `.git/` — see Gotchas.**
- `db/` — `schema.surql`, `seed.surql`. No migration tool; schema/seed are applied manually.
- `scripts/dev-tmux.sh` — opens a 4-window tmux session for dev.
- `docs/` — pitch, demo script, judge Q&A.

## Electric Twin / Gleb Principles

These project rules take precedence over generic defaults. Apply them on every task.

- **README-first**: update or propose docs/README changes before major implementation.
- **Python-centric backend**: backend logic should be idiomatic, typed Python where practical.
- **SOLID design**: prefer small single-purpose modules, explicit interfaces, dependency injection where useful, and clear boundaries between ingestion, validation, storage, API, and presentation.
- **Collaboration-first**: behave like a careful peer reviewer. Explain trade-offs, flag risks, and avoid large unreviewed rewrites.
- **PR-style workflow**: before major code changes, summarise the proposed diff and testing plan.
- **Testing discipline**: when changing backend logic, add or update relevant tests and run the smallest useful test command.
- **Reproducibility**: flag missing dependency manifests and offer to create a clean `requirements.txt` or `pyproject.toml`, but do not blindly freeze `.venv` without approval.
- **Git safety**: do not commit, reset, clean, push, or restructure repos without explicit approval.
- **Frontend caution**: `apps/web` has a nested `.git` directory; do not commit or restructure frontend files without asking.
- **Senior review standard**: optimise for readable, maintainable, explainable code over cleverness or hackathon-style shortcuts.
- **Agentic future**: keep the architecture open to future MCP / persona-simulation integration, but do not over-engineer before the ingestion engine is stable.

## Dev commands

Backend (port 8001):
```bash
cd apps/api && source .venv/bin/activate
python3 -m uvicorn main:app --reload --port 8001
```

Frontend (port 3000, calls API at `http://127.0.0.1:8001`):
```bash
cd apps/web && npm run dev    # also: npm run build, npm run lint
```

SurrealDB (Docker, port 8000, RocksDB at `./surreal-data/`):
```bash
sudo docker run --rm --pull always --name surrealdb -p 8000:8000 \
  --user $(id -u) -v "$(pwd)/surreal-data:/mydata" \
  surrealdb/surrealdb:latest \
  start --log info --user root --pass root rocksdb:/mydata/boroughsignal.db
```

Full dev session: `./scripts/dev-tmux.sh`.

## Environment

Required env vars (see `.env.example`): `OPENAI_API_KEY`, `LANGSMITH_API_KEY`, `LANGSMITH_TRACING=true`, `LANGSMITH_PROJECT=boroughsignal`, `SURREALDB_URL=ws://localhost:8000/rpc`, `SURREALDB_USERNAME`, `SURREALDB_PASSWORD`, `SURREALDB_NAMESPACE=boroughsignal`, `SURREALDB_DATABASE=main`.

Backend reads `apps/api/.env`; root `.env` is for shared/example config.

## Pipeline shape

Linear LangGraph in `apps/api/graph/workflow.py`: `parse_proposal → retrieve_context → simulate_segments → persist_run`. Each node is `@traceable` for LangSmith. Mutate `state.py` (TypedDict) — don't change node signatures without updating the graph builder. Scoring modifiers live in `SEGMENT_FEATURE_MODIFIERS` and `PLACE_TO_BOROUGH` dicts in `services/simulation.py`; treat these as data, not logic.

## Gotchas

- **`apps/web/.git/` is a nested repo, not a submodule.** Frontend file changes appear in the main repo as `m apps/web` but are actually tracked in the inner repo. Never run git operations against frontend files without asking which repo to target.
- **No Python dep manifest.** `apps/api/` has no `requirements.txt` or `pyproject.toml` — deps are only in `.venv/`. When adding/upgrading a Python package, flag this and offer to generate a manifest (don't blindly `pip freeze`).
- **No backend tests yet.** Add tests alongside backend logic changes per the testing-discipline rule above.
- **No backend linter/formatter configured.** If introducing one, propose first (ruff is the obvious default) — don't reformat the tree silently.
- **Demo data is hardcoded.** 5 boroughs / 6 segments / ~50 evidence rows in `db/seed.surql`; place→borough mapping is a static dict in `simulation.py`. Recreating SurrealDB state means re-applying `schema.surql` then `seed.surql`.
- **Synchronous `/simulate` calls.** The frontend blocks until the LangGraph run completes (seconds). No background queue.
- **React Compiler is on** (`next.config.ts: reactCompiler: true`). Don't add manual `useMemo`/`useCallback` purely for memoization.
