# Human Decision Register

Version: 1.0

This file lists decisions that Codex must never make autonomously. Each item must be decided by humans, recorded with date and rationale, and frozen before the corresponding project phase exits.

## HD-01 Reference hardware profile
- Decide the reference machine or cloud instance for all main experiments.
- Record CPU model, core count, RAM, storage type, OS, container runtime.
- Freeze before Phase 1 exits.

## HD-02 PostgreSQL version and configuration
- Choose the exact PostgreSQL release.
- Freeze core configuration: shared buffers, work_mem, effective_cache_size, jit on/off, parallel settings, planner knobs.
- Freeze before Phase 1 exits.

## HD-03 Dataset scale factors for anchor pack
- Choose TPC-H and TPC-DS scale factors after a pilot on the reference hardware.
- Selection criteria:
  - enough runtime to avoid sub-second noise on the chosen slow-query slices,
  - not so large that repeated experiments become infeasible.
- Freeze before Phase 2 exits.

## HD-04 Exact TPC-DS slice
- Choose the exact slow-query slice and query IDs.
- Record the selection rule and pilot measurements.
- Freeze before Phase 2 exits.

## HD-05 Exact JOB slice
- Choose the exact slow-query slice and query IDs.
- Record the selection rule and pilot measurements.
- Freeze before Phase 2 exits.

## HD-06 SQLStorm-derived public-realistic shortlist
- Approve the final 50 SQLStorm-derived cases.
- Each accepted case must have a provenance note and adjudication record.
- Freeze before Phase 2 exits.

## HD-07 Semantic-risk final case set
- Approve the final 40 semantic-risk cases.
- Record why each case belongs to a family and what failure mode it stresses.
- Freeze before Phase 2 exits.

## HD-08 Core family representatives
- Approve the exact representative implementation for S1, S2, S3.
- If the primary candidate is blocked, approve a same-family substitute before Phase 3 ends.
- Codex may document blockers but cannot decide the substitute.

## HD-09 LLM backend(s), model version(s), and budgets
- Decide the model(s), temperature, max retries, context limits, and cost/rate limits.
- Freeze separate settings for:
  - paper-faithful runs,
  - controlled-backend runs.
- Freeze before Phase 3 exits.

## HD-10 Prompt templates and system instructions
- Approve the frozen prompts for S4 and any descriptive-faithful baseline implementation.
- Freeze before Phase 3 exits.

## HD-11 Verification conflict resolution
- Decide the precedence rule if V1, V2, and V3 disagree in ways not already covered.
- Example questions:
  - if V3 cannot reason but V2 finds no counterexample,
  - if V1 passes on the reference dataset but V2 finds a mismatch.
- Freeze before Phase 4 exits.

## HD-12 Numeric comparison tolerance exceptions
- Approve any domain-specific exceptions to the default floating tolerance.
- Freeze before Phase 4 exits.

## HD-13 Timeout exceptions
- If any pack or system needs a timeout different from 15 minutes, approve it explicitly and document why.
- Freeze before Phase 4 exits.

## HD-14 Inclusion of enhancement systems
- Approve whether LITHE, GenRewrite, and GRewriter are included in the submission.
- These systems may strengthen the paper, but the main acceptance story must not depend on them.
- Decide before Phase 5 begins.

## HD-15 Second-engine transfer subset
- Decide whether to include a transfer study on a second engine.
- If yes, approve the engine, subset, and claim scope.
- Decide before Phase 5 begins.

## HD-16 Cold-cache sensitivity study
- Decide whether to include a cold-cache robustness subset in the main submission or supplemental artifact only.
- Decide before Phase 5 begins.

## HD-17 Authorship and related-submission compliance
- Approve the author list, qualified reviewer nomination, and related-submission disclosures.
- Freeze before submission.

## HD-18 Artifact repository and license
- Choose the public archival repository and artifact license.
- Confirm that all included code/data can legally be released.
- Freeze before Phase 7 exits.

## HD-19 Final claim scope
- Approve the exact wording of the paper’s top-line claim.
- Especially verify that the title and abstract use `realistic` / `production-like` rather than `real-world` unless production traces are genuinely included.
- Freeze during Phase 6.

## HD-20 Submission window
- Decide the target monthly submission cycle.
- Do not submit until the artifact passes the preflight checklist and the core story stands without enhancement systems.

## Required decision record format
For each approved item, add:
- `decision_id`
- `status` (`open`, `approved`, `rejected`, `superseded`)
- `date`
- `owner`
- `decision`
- `rationale`
- `affected_files`
- `freeze_phase`

Codex may read this file and surface undecided items, but must not mark an item approved.
## Approved Decision Record: HD-01
- decision_id: HD-01
- status: approved
- date: 2026-03-31
- owner: Tianci Gao
- decision: Main experiments use the reference machine `TCPC1` with CPU `13th Gen Intel(R) Core(TM) i9-13900K`, `32` logical cores, RAM `34087952384 bytes (~31.75 GiB / 32 GB class)`, storage type `local system drive (exact SSD/NVMe subtype not independently audited at Phase 1 closeout)`, OS `Microsoft Windows 11 Pro 10.0.26200`, container runtime `none` (current Phase 1 setup uses local PostgreSQL on Windows).
- rationale: Freeze the reference hardware profile before Phase 1 exit so all subsequent runtime measurements, workload slicing decisions, and reproducibility claims are grounded in a stable machine profile.
- affected_files:
  - docs/HUMAN_DECISION_REGISTER.md
  - docs/OPEN_DECISIONS_STATUS.md
  - docs/PHASE1_EXIT_REPORT.md
- freeze_phase: Phase 1

## Approved Decision Record: HD-02
- decision_id: HD-02
- status: approved
- date: 2026-03-31
- owner: Tianci Gao
- decision: Main experiments use PostgreSQL `17.9` installed locally on Windows. Frozen core configuration: shared_buffers=`128MB`, work_mem=`4MB`, effective_cache_size=`4GB`, jit=`on`, max_parallel_workers_per_gather=`2`, planner knobs=`default unless explicitly documented otherwise in later approved records`.
- rationale: Freeze the exact PostgreSQL release and core configuration before Phase 1 exit so baseline profiling and later evaluation results are reproducible and comparable.
- affected_files:
  - docs/HUMAN_DECISION_REGISTER.md
  - docs/OPEN_DECISIONS_STATUS.md
  - docs/PHASE1_EXIT_REPORT.md
- freeze_phase: Phase 1

