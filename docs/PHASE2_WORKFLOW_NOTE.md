# Phase 2 Workflow Note

Date: 2026-04-01

## Scope

This note defines the allowed Phase 2 scaffolding workflow only.

It does not approve any human decision, does not freeze any pack, and does not begin actual workload curation.

## What Humans Must Decide

Humans must make the following decisions:

- `HD-03`: exact `TPC-H` and `TPC-DS` scale factors for `anchor`
- `HD-04`: exact `TPC-DS` slow-query slice and query IDs
- `HD-05`: exact `JOB` slow-query slice and query IDs
- `HD-06`: final 50-case `SQLStorm`-derived shortlist for `public_realistic`
- `HD-07`: final 40-case set for `semantic_risk`

Humans also own the final accept or reject judgment for any proposed candidate set.

## What Codex May Prepare

Codex may prepare:

- evidence packet templates
- machine-readable pilot or review manifest templates
- placeholder pack metadata that clearly states no official membership exists yet
- analysis table shells
- non-binding workflow notes and file maps
- later, after explicit direction, pilot runs, candidate inventories, and documentation drafts

Codex may not, without explicit human approval:

- mark any `HD-03` through `HD-07` decision approved
- select a `TPC-DS` slice
- select a `JOB` slice
- approve a `SQLStorm` shortlist
- approve a `semantic_risk` final set
- freeze any pack membership

## Expected File Updates After Each HD Approval

### After `HD-03`

- update `docs/HUMAN_DECISION_REGISTER.md`
- update `docs/OPEN_DECISIONS_STATUS.md`
- add or update anchor scale metadata under `packs/anchor/`
- add populated pilot manifests under `results/`
- add populated summary tables under `analysis/`

### After `HD-04`

- update `docs/HUMAN_DECISION_REGISTER.md`
- update `docs/OPEN_DECISIONS_STATUS.md`
- add or update `TPC-DS` slice metadata under `packs/anchor/`
- add populated pilot manifests under `results/`
- add populated summary tables under `analysis/`

### After `HD-05`

- update `docs/HUMAN_DECISION_REGISTER.md`
- update `docs/OPEN_DECISIONS_STATUS.md`
- add or update `JOB` slice metadata under `packs/anchor/`
- add populated pilot manifests under `results/`
- add populated summary tables under `analysis/`

### After `HD-06`

- update `docs/HUMAN_DECISION_REGISTER.md`
- update `docs/OPEN_DECISIONS_STATUS.md`
- add or update pack metadata under `packs/public_realistic/`
- create approved case directories under `cases/`
- add populated review manifests under `results/`
- add populated shortlist summaries under `analysis/`

### After `HD-07`

- update `docs/HUMAN_DECISION_REGISTER.md`
- update `docs/OPEN_DECISIONS_STATUS.md`
- add or update pack metadata under `packs/semantic_risk/`
- create approved case directories under `cases/`
- add populated review manifests under `results/`
- add populated family coverage summaries under `analysis/`

## Recommended Minimal Execution Order

1. Prepare evidence packet and manifest templates.
2. Run `HD-03` pilot and secure the scale-factor approval.
3. Run `HD-04` and `HD-05` pilot work for the anchor slices.
4. Prepare `HD-07` and `HD-06` candidate-review packets without treating them as approved.
5. Obtain human approvals and only then begin real curation or case creation.

## Template Map

- `HD-03`: `docs/phase2_templates/HD-03_anchor_scale_packet.md`, `results/templates/hd03_anchor_scale_pilot_manifest.template.json`, `analysis/phase2_placeholders/hd03_anchor_scale_summary_template.csv`
- `HD-04`: `docs/phase2_templates/HD-04_tpcds_slice_packet.md`, `results/templates/hd04_tpcds_slice_pilot_manifest.template.json`, `analysis/phase2_placeholders/hd04_tpcds_slice_summary_template.csv`
- `HD-05`: `docs/phase2_templates/HD-05_job_slice_packet.md`, `results/templates/hd05_job_slice_pilot_manifest.template.json`, `analysis/phase2_placeholders/hd05_job_slice_summary_template.csv`
- `HD-06`: `docs/phase2_templates/HD-06_public_realistic_packet.md`, `results/templates/hd06_public_realistic_review_manifest.template.json`, `analysis/phase2_placeholders/hd06_public_realistic_shortlist_summary_template.csv`
- `HD-07`: `docs/phase2_templates/HD-07_semantic_risk_packet.md`, `results/templates/hd07_semantic_risk_review_manifest.template.json`, `analysis/phase2_placeholders/hd07_semantic_risk_coverage_summary_template.csv`

## Protocol Statement

`protocol changed: no`
