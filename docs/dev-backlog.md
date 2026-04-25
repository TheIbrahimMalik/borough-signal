# Development Backlog

> This backlog is a holding area for candidate work. It is not the sprint plan.
> Current execution should follow the locked BoroughSignal v2 scope, architecture, and priorities decided after repo audit.

## High priority
- Add backend dependency manifest (`requirements.txt` or `pyproject.toml`) instead of relying only on `.venv`.
- Add backend tests for ingestion, validation, simulation, and API behaviour.
- Add Ruff/linting config carefully; avoid mass reformatting without review.
- Decide how to handle `apps/web/.git` nested repo before committing frontend changes.
- Use PR-style development: branch, focused diff, tests, review summary.

## Medium priority
- Install/configure GitHub CLI (`gh`) when creating real GitHub PRs from terminal.
- Add GitHub Actions CI once tests/lint commands exist.
- Consider Claude skills/hooks once project commands stabilise.
- Consider git worktrees only if doing parallel agent/team development.

## Low priority
- Consider tmux-resurrect/continuum if tmux sessions become complex and long-running.
- Keep MCP/persona-simulation integration in mind, but do not over-engineer before ingestion is stable.
