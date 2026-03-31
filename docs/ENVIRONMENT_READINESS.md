# Environment Readiness

## Scope

This document records whether the current machine can execute the Phase 1 tiny anchor smoke path for `S0`.

## Windows / No-`make` Equivalents

Use these commands when `make` is not installed:

- `make setup` -> `python -m scripts.cli setup`
- `make smoke` -> `python -m scripts.cli smoke`
- `make pack-freeze` -> `python -m scripts.cli pack-freeze`
- `make eval-raw` -> `python -m scripts.cli eval-raw`
- `make eval-deploy` -> `python -m scripts.cli eval-deploy --policy conservative`
- `make verify-cases` -> `python -m scripts.cli verify-cases`
- `make tables` -> `python -m scripts.cli tables`
- `make figures` -> `python -m scripts.cli figures`
- `make artifact-preflight` -> `python -m scripts.cli artifact-preflight`
- optional diagnostic -> `python -m scripts.cli postgres-env-check`

## Phase 1 Readiness Fields

- Current status: `Phase 1 ready except environment`
- Latest machine-readable report: `results/environment/postgres-env-check-raw_output-2026-03-31T162257+0000.json`
- `make` availability: `missing in PATH`
- `psql` availability: `found via Windows fallback path`
- `psql` path: `C:\Program Files\PostgreSQL\17\bin\psql.exe`
- PostgreSQL Windows service probe: `postgresql-x64-17` is running
- Docker CLI availability: `missing in PATH`
- Config sources checked: `process environment`, `POSTGRES_LOCAL_CONFIG`
- Explicit connection config present: `no`
- Private local config status: `not configured`
- connectivity status: `blocked`
- current blocker: `fe_sendauth: no password supplied`
- recommended next step:
  - set `POSTGRES_DSN` or `PGHOST` / `PGPORT` / `PGDATABASE` / `PGUSER`
  - or set `POSTGRES_LOCAL_CONFIG` to a private local `.env` / `.json` file
  - provide credentials that can authenticate to the running PostgreSQL 17 service
  - rerun `python -m scripts.cli postgres-env-check`
  - rerun `python -m scripts.cli smoke`

## Current Observations

- This machine already has a running PostgreSQL Windows service.
- The harness can now discover `psql.exe` even though it is not in `PATH`.
- The harness now supports private local config via `POSTGRES_LOCAL_CONFIG` without writing secrets into git-tracked files.
- The smoke path still cannot run real SQL because the current connection attempt to `localhost:5432` is rejected for missing password.
- Therefore the repository is not claiming end-to-end database success; it is explicitly marked `Phase 1 ready except environment`.

## Expected Machine-Readable Output

- Environment report location: `results/environment/`
- Smoke result location: `results/smoke/`
- Latest smoke result: `results/smoke/smoke-raw_output-2026-03-31T162257+0000.jsonl`

## Protocol Statement

`protocol changed: no`
