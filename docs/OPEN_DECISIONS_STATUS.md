# Open Decisions Status

Current reading of the decision register:

- Approved decision records are now present for `HD-01` and `HD-02` in the repository copy of `docs/HUMAN_DECISION_REGISTER.md`
- Therefore `HD-01` and `HD-02` are no longer treated as open
- All remaining `HD-xx` items are treated as still open unless explicitly approved later

## By Phase

### Blocks Phase 1 Exit

- None from the decision register, provided that the technical Phase 1 exit criteria remain satisfied:
  - `S0` runs end-to-end on a tiny anchor subset
  - `artifact-preflight` passes
  - no protocol drift has occurred

### Blocks Phase 2 Exit

- `HD-03` Dataset scale factors for anchor pack
- `HD-04` Exact TPC-DS slice
- `HD-05` Exact JOB slice
- `HD-06` SQLStorm-derived public-realistic shortlist
- `HD-07` Semantic-risk final case set

### Blocks Phase 3 Exit

- `HD-08` Core family representatives
- `HD-09` LLM backend(s), model version(s), and budgets
- `HD-10` Prompt templates and system instructions

### Blocks Phase 4 Exit

- `HD-11` Verification conflict resolution
- `HD-12` Numeric comparison tolerance exceptions
- `HD-13` Timeout exceptions

### Must Be Decided Before Phase 5

- `HD-14` Inclusion of enhancement systems
- `HD-15` Second-engine transfer subset
- `HD-16` Cold-cache sensitivity study

### Later-Phase Human Decisions

- `HD-17` Authorship and related-submission compliance
- `HD-18` Artifact repository and license
- `HD-19` Final claim scope
- `HD-20` Submission window

## Approved Decisions Relevant to Current Phase

### HD-01 Reference hardware profile
- Status: `approved`
- Phase impact: `Phase 1 exit blocker cleared`
- Frozen by: human approval
- Notes:
  - reference machine frozen as `TCPC1`
  - CPU frozen as `13th Gen Intel(R) Core(TM) i9-13900K`
  - logical core count frozen as `32`
  - RAM frozen as `34087952384 bytes (~31.75 GiB / 32 GB class)`
  - OS frozen as `Microsoft Windows 11 Pro 10.0.26200`
  - container runtime frozen as `none`
  - storage type recorded as `local system drive (exact SSD/NVMe subtype not independently audited at Phase 1 closeout)`

### HD-02 PostgreSQL version and configuration
- Status: `approved`
- Phase impact: `Phase 1 exit blocker cleared`
- Frozen by: human approval
- Notes:
  - PostgreSQL release frozen as `17.9`
  - shared_buffers frozen as `128MB`
  - work_mem frozen as `4MB`
  - effective_cache_size frozen as `4GB`
  - jit frozen as `on`
  - max_parallel_workers_per_gather frozen as `2`
  - planner knobs frozen as `default unless explicitly documented otherwise in later approved records`

## Immediate Impact

- Phase 0 is not blocked by any currently open `HD-xx`
- Phase 1 startup implementation is not blocked
- Phase 1 decision-register blockers have been cleared because humans froze `HD-01` and `HD-02`
- A human-run technical verification has already reached:
  - `postgres-env-check` = `ready`
  - `phase1_status` = `Phase 1 environment ready`
  - `smoke` produced normalized raw-output results
  - `eval-deploy --policy conservative` produced normalized deployment-utility results
  - `S0` has run end-to-end on the tiny anchor subset
- However, the latest Codex closeout rerun did not reproduce that ready state in its own execution context, because non-interactive PostgreSQL authentication was not visible to that rerun
- Therefore Phase 1 is **not yet formally closed out**
- The remaining blocker is technical closeout reproducibility in the Codex execution context, not human decision status
- Phase 2 may begin only after Codex performs the formal Phase 1 closeout and writes the corresponding exit/precheck documents