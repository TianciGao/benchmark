# Phase 1 Exit Report

Date: 2026-04-01

## Scope

This report covers only Phase 1 exit verification for:

- `S0` native optimizer / no rewrite
- tiny anchor smoke subset
- `raw_output`
- `deployment_utility` with `conservative` policy

No Phase 2 workload curation or system expansion was performed.

## Human Decision Status

The human decisions required before Phase 1 exit are frozen:

- `HD-01` Reference hardware profile = `approved`
- `HD-02` PostgreSQL version and configuration = `approved`

These approvals are recorded in `docs/HUMAN_DECISION_REGISTER.md`.

## Root Cause and Repair

The remaining Phase 1 blocker was an implementation mismatch in the PostgreSQL probe path.

- Manual connectivity that was already known to succeed used explicit connection flags:
  - `psql -w -h 172.17.160.1 -p 5432 -U postgres -d postgres -c 'SELECT 1;'`
- The probe/runner implementation used a different subprocess construction:
  - `['/usr/bin/psql', '-X', '-q', '-A', '-t', '-w', '-v', 'ON_ERROR_STOP=1', '-c', 'SELECT 1;']`
  - It relied on inherited `PGHOST` / `PGPORT` / `PGDATABASE` / `PGUSER` instead of passing the same explicit `-h` / `-p` / `-U` / `-d` flags as the manual command.

The runner was repaired so that, when `POSTGRES_DSN` is not used and `PG*` connection parameters are available, it now invokes `psql` with the explicit connection arguments matching the successful manual invocation semantics.

## Formal Codex Closeout Rerun

After the probe repair, the formal Phase 1 closeout rerun succeeded in the Codex execution context.

Successful rerun commands:

- `python -m scripts.cli postgres-env-check`
- `python -m scripts.cli verify-cases`
- `python -m scripts.cli smoke`
- `python -m scripts.cli eval-deploy --policy conservative`
- `python -m scripts.cli artifact-preflight`

Successful rerun artifacts:

- `results/environment/postgres-env-check-2026-04-01T110835+0000.json`
- `results/environment/postgres-env-check-raw_output-2026-04-01T111215+0000.json`
- `results/environment/postgres-env-check-deployment_utility-2026-04-01T111335+0000.json`
- `results/smoke/smoke-raw_output-2026-04-01T111215+0000.jsonl`
- `results/smoke/smoke-deployment_utility-2026-04-01T111335+0000.jsonl`

Observed rerun status:

- `postgres-env-check`: `ready`
- `phase1_status`: `Phase 1 environment ready`
- `verify-cases`: passed
- `python -m scripts.cli smoke`: successful normalized raw-output run produced
- `python -m scripts.cli eval-deploy --policy conservative`: successful normalized deployment-utility run produced
- `artifact-preflight`: passed current bootstrap check

This rerun demonstrates that:

- PostgreSQL `17.9` is reachable from the Codex execution path used for closeout
- non-interactive authentication works for the formal rerun
- `S0` runs end-to-end on the tiny anchor subset in both required Phase 1 modes
- the required Phase 1 bootstrap validations pass without protocol drift

## Phase 1 Exit Decision

- Technical end-to-end `S0` execution on the tiny anchor subset: `yes`
- Formal Phase 1 exit: `yes`
- Phase 1 status: `Phase 1 = exited`

## Phase Boundary Statement

Phase 1 is formally closed.

This report does not start Phase 2 workload curation. Entry into Phase 2 remains gated on the separate precheck of open human decisions `HD-03` through `HD-07`.

## Protocol Statement

`protocol changed: no`
