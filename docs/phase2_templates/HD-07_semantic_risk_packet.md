# HD-07 Evidence Packet Template

Decision target: approve the final 40 cases for the `semantic_risk` pack across the 8 fixed families.

## Decision Boundary

- Decision owner:
- Decision date:
- Decision status: `open`
- Related decision id: `HD-07`

## Question

Which candidate cases should be accepted into the final `semantic_risk` pack, and which fixed family does each accepted case belong to?

## Human Inputs Required

- candidate case pool
- assigned semantic-risk family for each candidate
- explanation of the failure mode each candidate stresses
- final requested set of 40 cases
- justification for family coverage across the fixed taxonomy

## Review Evidence Required

- candidate inventory with stable candidate IDs
- family assignment for each candidate
- semantic-failure rationale for each candidate
- ambiguity or overlap notes where a case could fit multiple families
- acceptance and rejection rationale for every candidate reviewed
- family-count summary for the requested final set

## Reviewer Checks

- every accepted case maps to one of the 8 fixed families
- family assignment and failure-mode explanation are explicit
- rejected candidates are logged
- no final set is implied before human approval

## Linked Machine-Readable Evidence

- review manifest path:
- candidate inventory path:
- family coverage summary path:

## Requested Human Decision

- approve final `semantic_risk` case count:
- approve accepted candidate IDs:

## Expected File Updates After Approval

- `docs/HUMAN_DECISION_REGISTER.md`
- `docs/OPEN_DECISIONS_STATUS.md`
- `packs/semantic_risk/`
- `cases/`
- `results/`
- `analysis/`

## Notes

- Do not alter the fixed semantic-risk family taxonomy.
- Do not create real case directories until approval and curation work begin.
