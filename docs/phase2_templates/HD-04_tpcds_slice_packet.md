# HD-04 Evidence Packet Template

Decision target: approve the exact `TPC-DS` slow-query slice and query IDs for the `anchor` pack.

## Decision Boundary

- Decision owner:
- Decision date:
- Decision status: `open`
- Related decision id: `HD-04`

## Question

Which `TPC-DS` queries belong to the approved slow-query slice?

## Human Inputs Required

- slice-selection rule
- candidate query IDs considered
- exclusion rationale for rejected candidates
- final requested slow-query slice

## Pilot Evidence Required

- scale factor used, with reference to the approved `HD-03` choice
- baseline runtimes for candidate `TPC-DS` queries
- ranking method used to derive the slow slice
- evidence that the slice rule is reproducible and not ad hoc

## Reviewer Checks

- slice is tied to a stated rule, not informal choice
- all candidate IDs and rejected IDs are documented
- pilot measurements use the frozen Phase 1 environment
- final slice can be traced to raw pilot outputs

## Linked Machine-Readable Evidence

- pilot manifest path:
- raw result paths:
- summary table path:

## Requested Human Decision

- approve exact `TPC-DS` slice:
- approve included query IDs:

## Expected File Updates After Approval

- `docs/HUMAN_DECISION_REGISTER.md`
- `docs/OPEN_DECISIONS_STATUS.md`
- `packs/anchor/`
- `results/`
- `analysis/`

## Notes

- Do not define `JOB` membership here.
- Do not add case directories here.
