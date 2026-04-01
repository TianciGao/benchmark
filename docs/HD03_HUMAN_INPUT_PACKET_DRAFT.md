# HD-03 Human Input Packet Draft

Date: 2026-04-01

## Scope

This draft is for human input collection only for `HD-03`.

It does not run a pilot, does not choose final `TPC-H` or `TPC-DS` scale factors, does not start `HD-04` through `HD-07`, and does not modify any protocol file.

## Decision Boundary

Decision still reserved for humans:

- final `TPC-H` scale factor
- final `TPC-DS` scale factor

This packet exists only to collect the inputs required before a real pilot may run.

## Frozen Environment Reference

All HD-03 pilot work must stay on the frozen Phase 1 environment:

- hardware decision id: `HD-01`
- PostgreSQL/config decision id: `HD-02`
- host: `TCPC1`
- PostgreSQL version: `17.9`

These are already frozen and should not be edited in this packet.

## Current v0 Input State

The following v0 inputs are now recorded for HD-03 preparation.

They are candidate inputs only and do not constitute a final HD-03 decision.

### 1. Candidate Scale Lists

These are candidate values only, not final decisions.

- `TPC-H` candidate scale factors
- `TPC-DS` candidate scale factors

Fill-in slots:

- `TPC-H` candidates:
  - `10`
  - `30`
  - `100`
- `TPC-DS` candidates:
  - `10`
  - `30`
  - `50`

Additional note:

- `TPC-DS` scale `100` is escalation-only fallback.
- It is not part of the initial candidate list unless all initial `TPC-DS` candidates remain too fast.

JSON mapping:

- `human_inputs.candidate_scales.tpch`
- `human_inputs.candidate_scales.tpcds`

### 2. Acceptance Rules

These rules must be written before the pilot so the later decision is evidence-driven rather than post hoc.

- rule for "runtime avoids sub-second noise"
- rule for "runtime remains feasible for repeated experiments"

Fill-in slots:

- avoid-subsecond-noise rule:
  - A candidate scale remains eligible only if, on the frozen Phase 1 environment and under the fixed runtime protocol (`1` warmup + `5` measured runs, median as the primary statistic), at least `2` out of `3` pilot queries for that benchmark have median runtime `>= 1.0 second`, and no pilot query used as evidence has median runtime `< 0.5 second`. If all candidate scales violate this rule, the benchmark must escalate to the next larger candidate scale before any final HD-03 decision is made.
- feasibility rule:
  - A candidate scale remains feasible only if the pilot bundle for one benchmark (data ready or refresh, then `3` pilot queries timed with `1` warmup + `5` measured runs each) completes within `30 minutes` wall-clock, and the projected full-anchor baseline profiling effort for that benchmark on the frozen machine is expected to remain within `6 hours`. If two candidate scales both satisfy the noise rule, prefer the smaller one that still satisfies this feasibility rule.

JSON mapping:

- `human_inputs.acceptance_rules.avoid_subsecond_noise_rule`
- `human_inputs.acceptance_rules.feasibility_rule`

### 3. Pilot Query Subset

These are pilot-only query subsets for scale testing, not final pack membership and not final slice decisions.

- `TPC-H` pilot query IDs
- `TPC-DS` pilot query IDs

Fill-in slots:

- `TPC-H` pilot query subset:
  - `Q9`
  - `Q18`
  - `Q21`
- `TPC-DS` pilot query subset:
  - `Q64`
  - `Q72`
  - `Q95`

Additional note:

- The `TPC-DS` pilot subset is a provisional seed set for scale-sensitivity probing only.
- It is not the final slow slice.

JSON mapping:

- `human_inputs.pilot_query_subset.tpch`
- `human_inputs.pilot_query_subset.tpcds`

### 4. Command Binding Slots

These are exact command templates that future operators will use on the frozen machine.

They must be concrete commands by the time the real pilot starts.

Fill-in slots:

- `TPC-H` dataset generation or location command:
  - `TBD_LOCAL_BINDING: dbgen -vf -s {scale} -b dists.dss`
- `TPC-DS` dataset generation or location command:
  - `TBD_LOCAL_BINDING: dsdgen -FORCE -SCALE {scale} -DIR {out_dir}`
- PostgreSQL load or refresh command:
  - `TBD_LOCAL_BINDING: psql -v ON_ERROR_STOP=1 -v benchmark='{benchmark}' -v data_dir='{data_dir}' -v scale='{scale}' -f sql/hd03/load_anchor_${benchmark}.sql`
- pilot query timing command:
  - `TBD_LOCAL_BINDING: psql -X -w -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE -v benchmark='{benchmark}' -f sql/hd03/pilot_queries_${benchmark}.sql`

JSON mapping:

- `command_slots.tpch_dataset_generation_command_template`
- `command_slots.tpcds_dataset_generation_command_template`
- `command_slots.postgres_load_command_template`
- `command_slots.pilot_query_timing_command_template`

## Inputs Already Pre-Filled By Scaffolding

These fields are scaffolded and should normally remain unchanged unless there is a clear technical correction:

- `decision_id = HD-03`
- `official_decision_made = false`
- `frozen_reference_environment.hardware_decision_id = HD-01`
- `frozen_reference_environment.postgres_config_decision_id = HD-02`
- `frozen_reference_environment.hostname = TCPC1`
- `frozen_reference_environment.postgres_version = 17.9`
- `measurement_plan.warmups_per_query = 1`
- `measurement_plan.measured_runs_per_query = 5`
- `measurement_plan.primary_statistic = median`

## Collection Sequence Before Any Real Pilot Run

Collect the inputs in this exact order:

1. Confirm frozen-environment reference.
   - verify that `HD-01` and `HD-02` remain the active reference for the pilot
   - do not proceed if the intended pilot machine/config differs

2. Write the acceptance rules first.
   - record the current v0 avoid-subsecond-noise rule
   - record the current v0 feasibility rule
   - this must happen before candidate scales are evaluated so the decision rule is not retrofitted after seeing results

3. Provide candidate scale lists.
   - record the current `TPC-H` candidate list: `10, 30, 100`
   - record the current `TPC-DS` candidate list: `10, 30, 50`
   - record the escalation-only note for `TPC-DS` scale `100`
   - these are candidate inputs only and must not be mislabeled as approved scales

4. Provide pilot query subsets.
   - record the `TPC-H` pilot subset: `Q9, Q18, Q21`
   - record the `TPC-DS` pilot subset: `Q64, Q72, Q95`
   - record that the `TPC-DS` subset is provisional for scale-sensitivity probing only
   - these are pilot-only probe queries, not final slice or pack membership decisions

5. Bind the command slots.
   - record the current v0 command templates
   - bind the local SQL entry points to:
     - `sql/hd03/load_anchor_tpch.sql`
     - `sql/hd03/load_anchor_tpcds.sql`
     - `sql/hd03/pilot_queries_tpch.sql`
     - `sql/hd03/pilot_queries_tpcds.sql`
   - keep the `TBD_LOCAL_BINDING:` prefix so these are not mistaken for fully validated local commands

6. Initialize a scaffolded run bundle.
   - run `python -m scripts.cli hd03-pilot-init --run-label <human_label>`
   - this creates a timestamped input file, manifest file, and summary CSV path only

7. Copy the collected human inputs into the scaffolded config file.
   - populate the scaffolded `results/hd03/<run_id>.inputs.json`
   - do not run any dataset or timing commands yet

8. Check completeness.
   - run `python -m scripts.cli hd03-pilot-check-inputs --config results/hd03/<run_id>.inputs.json`
   - if any required fields remain missing, stop and fill them

Only after all eight steps are complete may a later task prepare to run a real HD-03 pilot.

## Matching Paths In The Current Repo

Human-facing evidence memo:

- `docs/phase2_templates/HD-03_anchor_scale_packet.md`

Machine-readable input template:

- `results/templates/hd03_anchor_scale_inputs.template.json`

Scaffolded per-run input file:

- `results/hd03/<run_id>.inputs.json`

Scaffolded per-run pilot manifest:

- `results/hd03/<run_id>.manifest.json`

Scaffolded per-run summary CSV:

- `analysis/phase2_outputs/<run_id>.summary.csv`

## Human Completion Checklist

Before the repo is allowed to proceed to a real HD-03 pilot, confirm:

- all candidate-scale placeholders are replaced with candidate values
- both acceptance rules are written
- both pilot query subsets are written
- all four command slots are populated at least to v0
- local SQL entry points exist for both benchmarks under `sql/hd03/`
- `official_decision_made` remains `false`
- no final scale choice is written anywhere in this packet
- no `TPC-DS` slice or `JOB` slice decision has been implied

## Out Of Scope

This packet does not:

- choose final scale factors
- authorize a real pilot run by itself
- define final `TPC-DS` slice membership
- define final `JOB` slice membership
- start `HD-04`, `HD-05`, `HD-06`, or `HD-07`

## Protocol Statement

`protocol changed: no`
