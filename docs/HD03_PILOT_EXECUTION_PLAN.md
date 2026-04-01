# HD-03 Pilot Execution Plan

Date: 2026-04-01

## Scope

This note prepares the `HD-03` pilot only.

It does not choose final `TPC-H` or `TPC-DS` scale factors, does not start `HD-04` through `HD-07`, and does not modify any protocol file.

## Decision Boundary

Human decision still required:

- choose the final `TPC-H` scale factor
- choose the final `TPC-DS` scale factor

Codex may prepare:

- pilot execution steps
- command sequence
- output path conventions
- manifest population instructions
- summary-table filling instructions

## Frozen Environment Reference

This pilot must run on the frozen Phase 1 environment only:

- hardware decision: `HD-01`
- PostgreSQL/config decision: `HD-02`
- host: `TCPC1`
- PostgreSQL: `17.9`

The pilot must not be used to change the frozen hardware or PostgreSQL configuration.

## Pilot Objective

Produce reviewer-robust evidence that lets humans later answer:

- which candidate `TPC-H` scale factors are large enough to avoid sub-second noise and still feasible for repeated experiments
- which candidate `TPC-DS` scale factors are large enough to avoid sub-second noise and still feasible for repeated experiments

This pilot is about scale-factor viability only.

It must not:

- define the final `TPC-DS` slice
- define the final `JOB` slice
- freeze `anchor` membership

## Required Inputs Before Running

Humans must provide:

- candidate `TPC-H` scale factors to evaluate
- candidate `TPC-DS` scale factors to evaluate
- the acceptance rule for "avoids sub-second noise"
- the acceptance rule for "still feasible for repeated experiments"
- the pilot query subset to use for scale testing

Codex may record these inputs in the pilot manifest, but may not choose them autonomously.

## Repo Files Used By This Pilot

Human-readable evidence packet:

- `docs/phase2_templates/HD-03_anchor_scale_packet.md`

Machine-readable pilot manifest template:

- `results/templates/hd03_anchor_scale_pilot_manifest.template.json`

Summary-table template:

- `analysis/phase2_placeholders/hd03_anchor_scale_summary_template.csv`

Existing harness checks that should be run before the pilot:

- `make postgres-env-check`
- `make artifact-preflight`
- `make hd03-pilot-init`
- `make hd03-pilot-check-inputs CONFIG=<scaffolded_config_path>`

## Output Paths For A Real Pilot Run

When the pilot is actually executed later, use this path layout:

- pilot manifest:
  - `results/hd03/hd03_anchor_scale_pilot_manifest.<timestamp>.json`
- optional normalized query-level outputs, if produced by later pilot tooling:
  - `results/hd03/hd03_anchor_scale_probe.<timestamp>.jsonl`
- environment readiness snapshot:
  - `results/environment/postgres-env-check-<timestamp>.json`
- summary table filled from pilot outputs:
  - `analysis/phase2_outputs/hd03_anchor_scale_summary.<timestamp>.csv`

These files do not need to exist yet for this preparation step.

## Exact Pilot Preparation Commands

Run these commands before any future HD-03 pilot execution:

```bash
make postgres-env-check
make artifact-preflight
python -m scripts.cli hd03-pilot-init --run-label <human_label>
python -m scripts.cli hd03-pilot-check-inputs --config results/hd03/<run_id>.inputs.json
```

Then populate the copied manifest with:

- frozen environment reference
- candidate scale lists supplied by humans
- pilot query IDs supplied by humans
- measurement protocol fields
- acceptance-rule text supplied by humans
- command-slot bindings supplied by humans

The `hd03-pilot-init` scaffold creates:

- `results/hd03/<run_id>.inputs.json`
- `results/hd03/<run_id>.manifest.json`
- `analysis/phase2_outputs/<run_id>.summary.csv`

The `hd03-pilot-check-inputs` command reports whether the scaffolded input file is complete enough for a later real pilot run.

## Dataset-Build And Load Command Slots

This repository does not yet provide a dedicated `HD-03` pilot runner or dataset-generation command.

Therefore the future pilot operator must bind the following command slots to the actual `TPC-H` and `TPC-DS` toolchain used on the frozen machine:

```bash
# Slot A: build or locate TPC-H dataset at one candidate scale
<tpch_dataset_generation_command_for_scale>

# Slot B: build or locate TPC-DS dataset at one candidate scale
<tpcds_dataset_generation_command_for_scale>

# Slot C: load or refresh PostgreSQL objects for that candidate scale
<postgres_load_command_for_scale>

# Slot D: execute baseline timing probes for the agreed pilot query subset
<pilot_query_timing_command_for_scale>
```

These command slots must be recorded verbatim in the populated pilot manifest once the pilot is run.

## Required Measurement Discipline

The future HD-03 pilot should record:

- one row per `(candidate_family, scale_factor, query_id)` in the summary table
- warmup count
- measured run count
- median runtime in milliseconds
- a brief spread or noise note
- a brief cost-feasibility note

The measurement protocol should be consistent across all candidate scales.

If humans want the pilot to mirror the frozen runtime protocol as closely as practical, record:

- `1` warmup run
- `5` measured runs
- median runtime as the primary statistic

If a different pilot-only measurement count is used, the populated manifest must explain why.

## Result Schema Usage

Primary machine-readable record for HD-03:

- use the populated copy of `results/templates/hd03_anchor_scale_pilot_manifest.template.json`
- this is the authoritative HD-03 decision-support artifact

Use of the normalized result schema:

- `results/schemas/normalized_result.schema.json` and `scripts/result_schema.py` define query-level evaluation outputs for the core harness
- HD-03 is a scale-selection pilot, not yet a core system-comparison workload result
- therefore the pilot must not force all evidence into `NormalizedResultRecord` if the data are scale-comparison metadata rather than query-evaluation records

Allowed usage:

- if future pilot tooling emits query-level probe outputs with fields that naturally fit `NormalizedResultRecord`, those outputs may be stored as JSONL alongside the pilot manifest
- the populated HD-03 manifest should then link those JSONL files as supporting raw outputs

Not allowed:

- using the normalized result schema as a substitute for the HD-03 pilot manifest
- treating pilot scale measurements as official workload-level evaluation results

## Summary Table Filling Path

Fill `analysis/phase2_outputs/hd03_anchor_scale_summary.<timestamp>.csv` from the populated pilot manifest and any linked raw outputs.

Column mapping:

- `candidate_family`: `tpch` or `tpcds`
- `candidate_id`: stable identifier such as `tpch_sf10` or `tpcds_sf100`
- `scale_factor`: numeric scale factor under evaluation
- `query_id`: pilot query identifier used for that row
- `median_runtime_ms`: median measured runtime for that query at that scale
- `spread_note`: short note on variability or noise
- `estimated_total_cost_note`: short note on experiment feasibility at that scale
- `recommended_for_approval`: leave blank until humans are ready to request a decision packet; do not mark final approval here
- `review_notes`: concise rationale, caveat, or environment note

The summary CSV is a convenience table for review.

The populated pilot manifest remains the primary machine-readable source of truth.

## Human Review Packet Completion Checklist

Before asking for an `HD-03` decision later, ensure the packet contains:

- a populated `HD-03` evidence memo
- a populated `HD-03` pilot manifest
- linked raw outputs or timing logs
- a filled summary CSV
- explicit rejected candidate scales, not only the preferred ones
- the exact command slots used on the frozen environment

## Out Of Scope

This note does not:

- approve a final scale factor
- define the exact pilot query subset
- define `TPC-DS` slice membership
- define `JOB` slice membership
- add any workload cases

## Protocol Statement

`protocol changed: no`
