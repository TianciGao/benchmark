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

The following human decisions required before Phase 1 exit are now frozen:

- `HD-01` Reference hardware profile = `approved`
- `HD-02` PostgreSQL version and configuration = `approved`

These approvals are recorded in `docs/HUMAN_DECISION_REGISTER.md`.

Therefore, the remaining question for Phase 1 is purely technical: whether the Phase 1 closeout rerun can reproduce the ready state and end-to-end `S0` execution in the Codex execution context.

## Verified Local Technical Success (Human-Run Shell)

In a human-managed local PowerShell session with non-interactive PostgreSQL authentication configured, the following technical checks succeeded:

- `python -m scripts.cli postgres-env-check`
  - status: `ready`
  - phase1_status: `Phase 1 environment ready`
  - report:
    - `results/environment/postgres-env-check-2026-03-31T200700+0000.json`

- `python -m scripts.cli smoke`
  - successful normalized raw-output run produced
  - outputs:
    - `results/smoke/smoke-raw_output-2026-03-31T200701+0000.jsonl`
    - `results/environment/postgres-env-check-raw_output-2026-03-31T200701+0000.json`

- `python -m scripts.cli eval-deploy --policy conservative`
  - successful normalized deployment-utility run produced
  - outputs:
    - `results/smoke/smoke-deployment_utility-2026-03-31T200703+0000.jsonl`
    - `results/environment/postgres-env-check-deployment_utility-2026-03-31T200703+0000.json`

This human-run shell verification demonstrates that:

- PostgreSQL `17.9` is reachable
- non-interactive authentication can work
- `S0` can run end-to-end on the tiny anchor subset
- Phase 1 technical success is achievable on the frozen reference environment

## Codex Closeout Rerun Status

The most recent Codex closeout rerun did **not** reproduce the ready state in its own execution context.

Observed rerun status:

- `postgres-env-check`: `blocked`
- `phase1_status`: `Phase 1 ready except environment`
- `python -m scripts.cli smoke`: `NonExecutable`
- `python -m scripts.cli eval-deploy --policy conservative`: `NonExecutable`

Latest Codex-visible rerun artifacts:

- `results/environment/postgres-env-check-2026-03-31T215805+0000.json`
- `results/smoke/smoke-raw_output-2026-03-31T215806+0000.jsonl`
- `results/smoke/smoke-deployment_utility-2026-03-31T215806+0000.jsonl`

Exact technical failure reported in the latest Codex rerun:

- authentication failure
- client error: `fe_sendauth: no password supplied`

## Interpretation

The project no longer has a human-decision blocker for Phase 1.

The remaining blocker is that the Codex closeout rerun has not yet reproduced the already-demonstrated ready state in its own non-interactive execution context.

Therefore:

- the frozen hardware/profile decisions are complete
- the frozen PostgreSQL version/configuration decision is complete
- the harness has demonstrated technical viability in a human-managed shell
- but the formal Codex-side Phase 1 closeout is still pending because the latest rerun did not inherit or consume valid non-interactive PostgreSQL authentication

## Phase 1 Exit Decision

- Technical end-to-end `S0` execution on the tiny anchor subset:
  - `yes` in the verified human-run shell
  - `no` in the latest Codex closeout rerun
- Formal Phase 1 exit: `no`
- Current label: `Phase 1 pending formal closeout rerun`

## Minimal Remaining Fix

1. Ensure the same non-interactive PostgreSQL authentication that succeeded in the verified human-run shell is visible to the Codex closeout execution context
2. Rerun:
   - `python -m scripts.cli postgres-env-check`
   - `python -m scripts.cli smoke`
   - `python -m scripts.cli eval-deploy --policy conservative`
   - `python -m scripts.cli artifact-preflight`
3. If these reruns remain green in the Codex execution context, Phase 1 may be formally marked `exited`

## Protocol Statement

`protocol changed: no`