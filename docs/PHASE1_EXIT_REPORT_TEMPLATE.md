# Phase 1 Exit Report Template

Use this template after running the Phase 1 readiness checks.

## Summary

- Phase 1 technical readiness:
- Formal Phase 1 exit:
- Current environment status:
- protocol changed: no

## Commands Run

- `python --version`
- `python -m scripts.cli postgres-env-check`
- `python -m scripts.cli verify-cases`
- `python -m scripts.cli artifact-preflight`
- `python -m scripts.cli smoke`
- `python -m scripts.cli eval-deploy --policy conservative`

## Evidence

- latest environment report:
- latest smoke result:
- latest smoke manifest:
- latest evidence trace:

## Missing Items If Exit Is Blocked

- environment blocker:
- `HD-01` blocker:
- `HD-02` blocker:
- git/worktree blocker:

## HD-01 Template

```text
decision_id: HD-01
status: open
date:
owner:
decision:
rationale:
affected_files:
freeze_phase: Phase 1
```

## HD-02 Template

```text
decision_id: HD-02
status: open
date:
owner:
decision:
rationale:
affected_files:
freeze_phase: Phase 1
```
