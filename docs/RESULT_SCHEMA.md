# Result Schema

The normalized result format for this repository is JSONL.

- One line = one machine-readable run record for one `(run_id, case_id, system_id, mode, policy)` outcome
- Machine-readable schema file: `results/schemas/normalized_result.schema.json`
- Python implementation: `scripts/result_schema.py`

## Required Fields

- `run_id`
- `case_id`
- `system_id`
- `system_family`
- `mode`
- `universe`
- `policy`
- `original_sql_hash`
- `rewrite_sql`
- `rewrite_sql_hash`
- `parse_status`
- `exec_status`
- `verdict`
- `evidence_trace_path`
- `baseline_runtime_samples`
- `candidate_runtime_samples`
- `final_runtime_samples`
- `decision`
- `engine_version`
- `stats_snapshot_id`
- `seed`
- `timestamp`
- `notes`

## Frozen Enums Already Enforced

- `mode` must be one of `raw_output`, `deployment_utility`
- `universe` must be one of `compatibility_subset`, `full_subset`
- `policy` must be `null`, `conservative`, or `practical`
- `verdict` must be one of:
  - `Invalid`
  - `NonExecutable`
  - `Disproved`
  - `Proved`
  - `TestPassed`
  - `Unknown`

## Phase 1 Notes

- The smoke path currently uses single-sample execution only to validate wiring
- Main frozen runtime profiles from the execution manual are **not** yet implemented in full
- `decision` is currently stored as an engineering field for harness flow tracking and is not used to redefine any frozen scientific metric

## Output Location

Smoke and future evaluation runs should write:

- normalized records under `results/`
- evidence traces under a run-specific subdirectory
- a machine-readable run manifest beside the normalized results
