# Open Decisions Status

Current reading of the decision register:

- No `approved`, `rejected`, or `superseded` decision records are present in the repository copy of `docs/HUMAN_DECISION_REGISTER.md`
- Therefore all listed `HD-xx` items are treated as still open

## By Phase

### Blocks Phase 1 Exit

- `HD-01` Reference hardware profile
  - Status: `open`
  - Phase impact: `Phase 1 exit blocker`
  - Human must fill:
    - reference machine or cloud instance
    - CPU model
    - core count
    - RAM
    - storage type
    - OS
    - container runtime
  - Decision template:
    ```text
    decision_id: HD-01
    status: open
    date:
    owner:
    decision:
    rationale:
    affected_files:
    freeze_phase: Phase 1
    ```
- `HD-02` PostgreSQL version and configuration
  - Status: `open`
  - Phase impact: `Phase 1 exit blocker`
  - Human must fill:
    - exact PostgreSQL release
    - shared_buffers
    - work_mem
    - effective_cache_size
    - jit on/off
    - parallel settings
    - planner knobs
  - Decision template:
    ```text
    decision_id: HD-02
    status: open
    date:
    owner:
    decision:
    rationale:
    affected_files:
    freeze_phase: Phase 1
    ```

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

## Immediate Impact

- Phase 0 is not blocked by any currently open `HD-xx`
- Phase 1 startup implementation is not blocked
- Phase 1 exit remains blocked until humans freeze `HD-01` and `HD-02`
- Even if the tiny anchor smoke path becomes technically runnable, formal Phase 1 exit still requires human approval records for `HD-01` and `HD-02`
