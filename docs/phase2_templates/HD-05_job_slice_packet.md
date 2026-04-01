# HD-05 Evidence Packet Template

Decision target: approve the exact `JOB` slow-query slice and query IDs for the `anchor` pack.

## Decision Boundary

- Decision owner:
- Decision date:
- Decision status: `open`
- Related decision id: `HD-05`

## Question

Which `JOB` queries belong to the approved slow-query slice?

## Human Inputs Required

- slice-selection rule
- candidate query IDs considered
- exclusion rationale for rejected candidates
- final requested slow-query slice

## Pilot Evidence Required

- baseline runtimes for candidate `JOB` queries
- ranking method used to derive the slow slice
- evidence that the slice rule is reproducible and not ad hoc
- environment reference showing frozen hardware/configuration alignment

## Reviewer Checks

- the same measurement discipline is used across all candidate queries
- rejected candidates are recorded, not silently omitted
- slice definition is explainable and reproducible

## Linked Machine-Readable Evidence

- pilot manifest path:
- raw result paths:
- summary table path:

## Requested Human Decision

- approve exact `JOB` slice:
- approve included query IDs:

## Expected File Updates After Approval

- `docs/HUMAN_DECISION_REGISTER.md`
- `docs/OPEN_DECISIONS_STATUS.md`
- `packs/anchor/`
- `results/`
- `analysis/`

## Notes

- Do not define `TPC-DS` membership here.
- Do not add case directories here.
