# AGENTS.md

This repository contains the frozen execution protocol for a PVLDB EA&B paper on deployment-aware evaluation of SQL query rewriting.

## Read these first
- `docs/CODEX_EXECUTION_MANUAL.md`
- `docs/HUMAN_DECISION_REGISTER.md`

Do not start coding before reading both files.

## Mission
Build a reproducible evaluation harness and experimental artifact for:

**From Rewrite Potential to Realized Deployment Utility: Evaluating SQL Query Rewriting with Realistic Workloads, Tiered Verification Evidence, and Explicit Fallback Policies [Experiment, Analysis & Benchmark]**

The scientific target is **evaluation**, not a new rewriter.

## Frozen scope
- Main task: SQL-to-SQL rewriting for analytical `SELECT` queries.
- Main DBMS: PostgreSQL only.
- Main paper type: EA&B (`experimental survey + workload characterization`).
- Core workload packs: `anchor`, `public_realistic`, `semantic_risk`.
- Core evaluation modes: `raw_output`, `deployment_utility`.
- Core policies: `conservative`, `practical`.
- Core reporting universes: `compatibility_subset`, `full_subset`.
- Core verdicts: `Invalid`, `NonExecutable`, `Disproved`, `Proved`, `TestPassed`, `Unknown`.

## Non-goals
- Do not turn this repository into a new-rewriter project.
- Do not add a second core DBMS.
- Do not claim real production traces unless humans explicitly add them.
- Do not invent a single composite score.
- Do not silently change workload inclusion, verdict semantics, or metric definitions.

## Hard rules
1. **Plan first** for any non-trivial task. Write or update a short execution plan before coding.
2. **Never edit protocol files** without explicit human approval:
   - `AGENTS.md`
   - `docs/CODEX_EXECUTION_MANUAL.md`
   - `docs/HUMAN_DECISION_REGISTER.md`
   - `docs/PROTOCOL_FREEZE.md` (if present)
3. **One task, one branch/worktree.** Never mix protocol work, adapter work, and analysis work in the same change set.
4. **No hidden assumptions.** If a decision is not frozen in the manual, stop and escalate.
5. **No benchmark drift.** Do not add/drop queries after pack freeze, except human-approved label fixes.
6. **All-query denominator.** Never report workload-level speedup only on successful rewrites.
7. **Keep AGENTS concise.** Put details in `docs/` and reference them here.

## Repository contract
Expected top-level directories:
- `cases/`
- `packs/`
- `systems/`
- `verifiers/`
- `engines/`
- `policies/`
- `results/`
- `analysis/`
- `docs/`
- `scripts/`
- `skills/`

## Expected canonical entry points
If missing, create them before expanding functionality:
- `make setup`
- `make smoke`
- `make pack-freeze`
- `make eval-raw`
- `make eval-deploy`
- `make verify-cases`
- `make tables`
- `make figures`
- `make artifact-preflight`

## Working style
- Prefer small, reviewable diffs.
- Add tests or validation scripts for any new adapter, parser, or result transformation.
- Log every non-trivial run into machine-readable manifests.
- If a public system cannot be reproduced faithfully, document the blocker and stop for human approval before substituting a family representative.

## Done criteria for any task
A task is not done until:
- code/config/docs are updated together,
- the relevant validation command passes,
- outputs are written to the standard result schema,
- deviations from the manual are explicitly declared (normally this means stop and ask).
