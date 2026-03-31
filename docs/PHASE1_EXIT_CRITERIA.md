# Phase 1 Exit Criteria

This file defines Phase 1 exit readiness only.

It does **not** authorize:

- Phase 2 workload curation
- official pack freeze
- new system-family integration
- verifier expansion
- workload expansion

## Required for Phase 1 Exit

- Repository layout from `AGENTS.md` is present
- Canonical entry points exist
- Windows-compatible no-`make` equivalents are documented
- Case manifest loader works on the tiny smoke fixture
- Normalized JSONL result writer works
- PostgreSQL runner exposes machine-readable environment diagnostics
- `S0` tiny anchor smoke path is implemented
- One of the following is true:
  - a real PostgreSQL instance is reachable and `S0` runs end-to-end on the tiny anchor subset
  - or the repository contains a complete machine-readable environment blocker report and explicit next-step commands, with status marked `Phase 1 ready except environment`
- `HD-01` is approved by humans
- `HD-02` is approved by humans
- Git workflow guidance exists for satisfying `one task, one branch/worktree`

## Exit Decision Rule

Phase 1 can exit only when both conditions hold:

1. Technical readiness is demonstrated.
2. Human decisions `HD-01` and `HD-02` are frozen.

## Current Boundary

This repository may reach `Phase 1 ready except environment` before formal Phase 1 exit if:

- the harness is ready,
- diagnostics are complete,
- but PostgreSQL connectivity is still unavailable in the current machine context.

## Protocol Statement

`protocol changed: no`
