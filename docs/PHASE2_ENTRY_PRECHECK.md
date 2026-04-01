# Phase 2 Entry Precheck

Date: 2026-04-01

## Scope

This document is a Phase 2 entry precheck only.

It does not begin Phase 2 workload curation, does not freeze any workload membership, and does not approve any human decision.

## Phase 1 Boundary

- `Phase 1 = exited`
- This precheck is prepared only because the formal Phase 1 closeout rerun succeeded

## Human Decisions Required Before and During Phase 2

Only the following decision inputs and approvals are required for the project to proceed through Phase 2:

### `HD-03` Dataset scale factors for anchor pack

Inputs needed:

- pilot runtime measurements on the frozen reference hardware
- candidate TPC-H scale factor options
- candidate TPC-DS scale factor options
- justification that chosen scales avoid sub-second noise on the slow-query slices while remaining experimentally feasible

Decision needed:

- approve the exact TPC-H and TPC-DS scale factors for the anchor pack

### `HD-04` Exact TPC-DS slice

Inputs needed:

- candidate slow-query slice definition for TPC-DS
- query IDs under consideration
- selection rule
- pilot measurements supporting the selection

Decision needed:

- approve the exact TPC-DS slow-query slice and query IDs

### `HD-05` Exact JOB slice

Inputs needed:

- candidate slow-query slice definition for JOB
- query IDs under consideration
- selection rule
- pilot measurements supporting the selection

Decision needed:

- approve the exact JOB slow-query slice and query IDs

### `HD-06` SQLStorm-derived public-realistic shortlist

Inputs needed:

- candidate SQLStorm-derived cases for the public-realistic pack
- provenance note for each candidate case
- adjudication record for each candidate case
- justification for the final shortlist size and inclusion choices

Decision needed:

- approve the final 50 SQLStorm-derived public-realistic cases

### `HD-07` Semantic-risk final case set

Inputs needed:

- candidate semantic-risk cases
- assigned risk family for each case
- explanation of the semantic failure mode each case stresses
- justification for the final set composition across the fixed risk families

Decision needed:

- approve the final 40 semantic-risk cases

## Entry Judgment

- Phase 2 may begin procedurally: `yes`
- Phase 2 may exit without new human decisions: `no`
- Required human-decision frontier for Phase 2: `HD-03` through `HD-07`

## Protocol Statement

`protocol changed: no`
