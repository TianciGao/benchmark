# HD-03 Evidence Packet Template

Decision target: approve exact `TPC-H` and `TPC-DS` scale factors for the `anchor` pack.

## Decision Boundary

- Decision owner:
- Decision date:
- Decision status: `open`
- Related decision id: `HD-03`

## Question

What exact `TPC-H` and `TPC-DS` scale factors should be used on the frozen Phase 1 reference environment?

## Human Inputs Required

- candidate `TPC-H` scale factors
- candidate `TPC-DS` scale factors
- acceptance rule for "runtime is long enough to avoid sub-second noise"
- acceptance rule for "runtime remains feasible for repeated experiments"

## Pilot Evidence Required

- frozen hardware and PostgreSQL configuration reference
- exact dataset-generation method per candidate scale
- candidate query set used for scale testing
- baseline runtime measurements:
  - warmup count
  - measured run count
  - median runtime
  - optional spread summary
- estimated experiment-cost projection at each candidate scale

## Reviewer Checks

- same hardware and PostgreSQL configuration as Phase 1 freeze
- same measurement protocol across candidate scales
- chosen scales are justified by measured evidence, not preference
- report both accepted and rejected scale options

## Linked Machine-Readable Evidence

- pilot manifest path:
- raw result paths:
- summary table path:

## Requested Human Decision

- approve `TPC-H` scale factor:
- approve `TPC-DS` scale factor:

## Expected File Updates After Approval

- `docs/HUMAN_DECISION_REGISTER.md`
- `docs/OPEN_DECISIONS_STATUS.md`
- `packs/anchor/`
- `results/`
- `analysis/`

## Notes

- Do not define TPC-DS query membership here.
- Do not define JOB slice membership here.
