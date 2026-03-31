# Repository Layout

This file documents the Phase 0/1 repository skeleton required by the frozen execution protocol.

## Top-Level Directories

- `cases/` individual case assets
- `packs/` pack manifests and smoke fixtures
- `systems/` system adapters
- `verifiers/` verifier adapters
- `engines/` engine setup assets
- `policies/` deployment policies
- `results/` normalized and raw outputs
- `analysis/` tables, figures, and later analysis scripts
- `docs/` protocol and bootstrap documentation
- `scripts/` command-line entry points and harness helpers
- `skills/` Codex skill scaffolds

## Canonical Entry Points

- `make setup`
- `make smoke`
- `make pack-freeze`
- `make eval-raw`
- `make eval-deploy`
- `make verify-cases`
- `make tables`
- `make figures`
- `make artifact-preflight`

Current implementation status:

- `setup`, `smoke`, `eval-raw`, `eval-deploy`, `verify-cases`, and `artifact-preflight` execute code paths
- `pack-freeze`, `tables`, and `figures` are explicit placeholders with TODO messages
- All commands route through `python -m scripts.cli ...`

## Smoke Path

The bootstrap smoke path uses:

- pack fixture: `packs/anchor/tiny_smoke.yaml`
- case fixture: `cases/smoke_anchor_q1/`
- system: `S0` native optimizer / no rewrite
- runner: `scripts/postgres_runner.py`
- output schema: `results/schemas/normalized_result.schema.json`
