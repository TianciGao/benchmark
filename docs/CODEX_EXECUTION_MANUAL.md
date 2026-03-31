# Codex Execution Manual for the VLDB EA&B Project

Version: 1.0 (frozen unless humans explicitly revise it)

## 1. Purpose

This document is the permanent execution charter for Codex-driven development and experimentation in a PVLDB EA&B paper on SQL query rewriting evaluation.

The project goal is **not** to invent a stronger rewriter. The goal is to measure how much of the published **rewrite potential** of existing SQL rewriting approaches turns into **realized deployment utility** once the evaluation uses:

1. realistic workloads,
2. tiered verification evidence,
3. explicit fallback policies, and
4. workload-level all-query accounting.

Codex is allowed to accelerate engineering, reproducibility, data plumbing, and batch experimentation. Codex is **not** allowed to make scientific policy decisions that this manual reserves for humans.

---

## 2. Frozen scientific position

### 2.1 Paper identity
- Venue target: PVLDB Research Track, category `Experiment, Analysis & Benchmark`.
- Paper type: `experimental survey + workload characterization`.
- Main claim class: evaluation protocol and empirical insight.
- Main artifact class: reproducible harness + curated workload packs + result manifests.

### 2.2 Frozen thesis
Published SQL rewrite results often demonstrate **rewrite potential** rather than **realized deployment utility**. A deployment-aware evaluation must distinguish raw output quality from deployable output quality by using tiered verification evidence, explicit fallback policies, and realistic workloads.

### 2.3 Frozen research questions
- **RQ1**: How much do canonical benchmarks plus success-only reporting overestimate realized deployment utility?
- **RQ2**: Where is the main loss between raw rewrites and deployable rewrites: invalid SQL, non-executability, disproved equivalence, unknown equivalence, runtime regression, or evaluation overhead?
- **RQ3**: Which workload properties change conclusions or system rankings the most: canonical anchor, public-realistic, or semantic-risk workloads?

### 2.4 Non-goals
- No new query rewriting algorithm as the paper’s main contribution.
- No multi-engine core evaluation.
- No reliance on proprietary real production traces.
- No unified “overall score” that hides trade-offs.
- No cross-task leaderboard comparison against text-to-SQL or SQL debugging benchmarks.

---

## 3. Frozen scope

### 3.1 Task scope
- Analytical SQL-to-SQL rewriting.
- `SELECT` queries only.
- No DML, no transactions, no multi-query workflow agents.
- No text-to-SQL generation as a primary task.

### 3.2 DBMS scope
- Core engine: PostgreSQL.
- A second engine is allowed only as an enhancement study on a transfer subset, never as a dependency for the main paper.

### 3.3 Core system families
Core evaluation must include one representative from each of the following families:

- **S0**: Native optimizer / no rewrite.
- **S1**: Learned rule-order or search family.
- **S2**: LLM-guided rule-based family.
- **S3**: Evidence-guided LLM rewriting family.
- **S4**: Prompt-only free-form LLM rewrite baseline implemented in this project.

#### Primary candidate implementations
- S1 primary candidate: `LearnedRewrite`-style representative.
- S2 primary candidate: `LLM-R2`-style representative.
- S3 primary candidate: `R-Bot`-style representative.
- S4 primary candidate: controlled prompt-only baseline implemented from paper descriptions and frozen prompts.

#### Enhancement-only systems
These may strengthen the paper but must not be required for acceptance:
- `LITHE`
- `GenRewrite`
- `GRewriter`

### 3.4 Workload packs
The main paper uses exactly **three** packs.

#### Pack A: `anchor`
Purpose: community comparability.
Content:
- TPC-H: all 22 queries.
- TPC-DS: pre-registered slow-query slice.
- JOB: pre-registered slow-query slice.

#### Pack B: `public_realistic`
Purpose: realistic but public and reproducible workloads.
Content:
- 50 manually reviewed and system-neutralized SQLStorm-derived cases.

#### Pack C: `semantic_risk`
Purpose: stress semantic fragility of rewrites.
Content:
- 40 curated cases across 8 risk families.

Target total: **162 original queries/cases**.

### 3.5 Semantic-risk families (fixed)
1. NULL / NOT IN / three-valued logic
2. outer join + filter movement
3. duplicates / DISTINCT / GROUP BY
4. aggregation / HAVING
5. EXISTS / IN / semi-join rewrites
6. window + ORDER BY / LIMIT
7. UNION / UNION ALL / EXCEPT / INTERSECT
8. string predicates / non-PK-FK joins / complex predicates

---

## 4. Frozen evaluation protocol

### 4.1 Two evaluation modes
#### Mode M1: `raw_output`
Evaluate each system’s top-1 rewrite as produced by the system, before deployment gating.

#### Mode M2: `deployment_utility`
Evaluate the same top-1 rewrite after applying a common evidence gate and a common fallback policy.

### 4.2 Two reporting universes
#### U1: `compatibility_subset`
Only cases that every core system can ingest and run end-to-end.
Use this for comparing method design under controlled compatibility.

#### U2: `full_subset`
All official frozen cases.
Use this for deployment realism.

Both universes must be reported.

### 4.3 Official verdict taxonomy (fixed)
Every candidate rewrite must end in exactly one verdict:
- `Invalid`
- `NonExecutable`
- `Disproved`
- `Proved`
- `TestPassed`
- `Unknown`

No other summary bucket may replace these in primary reporting.

### 4.4 Verification pipeline (fixed)
- **V0**: parse / dialect / executability
- **V1**: differential execution on the reference dataset
- **V2**: plan-aware generated tests
- **V3**: formal proving where supported

Implementation note:
- `QO-Verify`-style optimizer-assisted verification is optional and may be added as a plugin, but it is not a core dependency.

### 4.5 Comparison semantics (fixed)
Unless a human explicitly approves an exception, result comparison follows these rules:

1. Default semantics are **bag semantics**.
2. Row order is ignored **unless** the original query contains `ORDER BY`.
3. If `ORDER BY` is present, order is part of the contract.
4. `LIMIT/OFFSET` without deterministic ordering is excluded from the core benchmark unless manually adjudicated.
5. Exact match is required for integers, strings, booleans, dates, timestamps, and decimals.
6. Floating-point outputs use tolerance:
   - absolute tolerance: `1e-9`, or
   - relative tolerance: `1e-9`,
   whichever is larger.
7. `NULL` values must match exactly.
8. Column count, column order, and data type compatibility must match the original query contract.

### 4.6 Deployment policies (fixed)
#### Policy P1: `conservative`
Apply rewrite only if:
- verdict = `Proved`, and
- calibration median speedup >= `1.10x`, and
- no calibration run exceeds `1.02x` of the baseline median.

Otherwise fallback to the original query.

#### Policy P2: `practical`
Apply rewrite only if:
- verdict in `{Proved, TestPassed}`, and
- calibration median speedup >= `1.05x`.

Otherwise fallback to the original query.

`Unknown` is always rejected in core results.

### 4.7 Runtime measurement protocol (fixed)
#### Baseline runtime profile
For each original query:
- 1 warmup execution.
- 5 measured hot-cache executions.
- Use median as the baseline runtime.

#### Candidate calibration profile
For each rewrite candidate:
- 1 warmup execution.
- 3 measured hot-cache executions.
- Use median for policy gating.

#### Final reporting profile
For whichever query is ultimately executed under a policy (rewrite or fallback original):
- 1 warmup execution.
- 5 measured hot-cache executions.
- Use median for reporting.

#### Timeout
- Per execution timeout: `15 minutes`.
- Timeout counts as failure (`NonExecutable` if system-side, or policy fallback if caused during calibration after successful parsing).

#### Noise controls
- Same machine, same engine version, same container image, same configuration, same statistics snapshot.
- No workload co-tenancy during main experiments.
- CPU pinning and process isolation required if available.

### 4.8 Overhead accounting (fixed)
Rewrite generation and verification overhead are always measured and reported separately.

Primary workload-level speedup **does not amortize or fold in** one-time rewrite generation cost. Instead the paper reports:
- realized execution utility, and
- median rewrite+verification overhead side by side.

Reason: rewrite generation is often offline or template-level, while query execution is online and repeatedly incurred.

---

## 5. Frozen metrics

### 5.1 Primary metrics
1. **Apply Rate**
   - `ApplyRate = |{q : decision(q)=apply}| / |Q|`
2. **Realized Workload Speedup**
   - `RWS = sum_q baseline_median(q) / sum_q final_median(q)`
   - `final_median(q)` is the policy result: rewrite runtime if applied, else original runtime.
3. **No-Regression Rate**
   - `NRR = |{q : applied(q) and final_median(q) <= 1.02 * baseline_median(q)}| / |{q : applied(q)}|`
4. **Evidence Profile**
   - proportions of `Proved`, `TestPassed`, `Unknown`, `Disproved`, `Invalid`, `NonExecutable`
5. **Median Rewrite+Verification Overhead**

### 5.2 Secondary metrics
- Raw Exec Rate
- Invalid Rate
- NonExecutable Rate
- Compatibility-vs-Full gap
- Conservative-vs-Practical gap

### 5.3 Hard metric rule
All workload-level metrics use the **all-query denominator** over the relevant universe (`compatibility_subset` or `full_subset`).

---

## 6. Data and workload governance

### 6.1 Case structure (required)
Each case directory must contain:
- `original.sql`
- `manifest.yaml`
- `semantic_contract.yaml`
- `provenance.md`
- `risk_tags.yaml`
- `validation_assets/`
- `adjudication_log.md`

### 6.2 Manifest fields (minimum)
- `case_id`
- `pack_id`
- `source`
- `dbms`
- `schema_version`
- `data_snapshot_id`
- `stats_snapshot_id`
- `query_features`
- `comparison_semantics`
- `exclusion_notes`
- `owner`
- `freeze_status`

### 6.3 Pack freeze rule
- Query membership freezes at the end of workload curation.
- After freeze, only label fixes and documentation fixes are allowed.
- Any add/drop/change requires explicit human approval and a version bump.

### 6.4 SQLStorm rule
SQLStorm may be used as a **candidate source**, never as a direct gold benchmark.
Every selected SQLStorm-derived query requires manual review and system-neutral cleanup before entering `public_realistic`.

---

## 7. Core engineering architecture

### 7.1 Repository layout (required)
- `cases/` — individual case assets
- `packs/` — pack manifests and selection logic
- `systems/` — adapter implementations for S0–S4 and enhancements
- `verifiers/` — V0–V3 adapters
- `engines/` — engine containers and setup
- `policies/` — deployment policy implementations
- `results/` — raw and normalized outputs
- `analysis/` — notebooks/scripts for figures and tables
- `scripts/` — command-line entry points
- `docs/` — protocol, logs, author notes
- `skills/` — Codex skills

### 7.2 Standard adapter interface
Each system adapter must expose:
- `prepare_case(case_id)`
- `generate_rewrite(case_id, sql, config)`
- `normalize_output(raw_output)`
- `emit_metadata()`

Each verifier adapter must expose:
- `verify(case_id, original_sql, rewrite_sql, context)`
- `emit_evidence_trace()`

Each policy must expose:
- `decide(case_id, evidence, calibration_runtime, baseline_runtime)`

### 7.3 Standard result schema (required)
Every system run must write a machine-readable record containing at least:
- `run_id`
- `case_id`
- `system_id`
- `system_family`
- `mode`
- `universe`
- `policy`
- `original_sql_hash`
- `rewrite_sql`
- `rewrite_sql_hash`
- `parse_status`
- `exec_status`
- `verdict`
- `evidence_trace_path`
- `baseline_runtime_samples`
- `candidate_runtime_samples`
- `final_runtime_samples`
- `decision`
- `engine_version`
- `stats_snapshot_id`
- `seed`
- `timestamp`
- `notes`

JSONL is the default normalized format.

---

## 8. Codex operating model

### 8.1 What Codex may do autonomously
Codex may autonomously:
- scaffold repository structure,
- write adapters,
- write runners,
- write validators,
- write analysis scripts,
- prepare reproducibility scripts,
- execute frozen experiments,
- generate tables and figures,
- refactor code without changing scientific protocol.

### 8.2 What Codex must never decide autonomously
Codex must not autonomously decide:
- thesis changes,
- RQ changes,
- metric redefinitions,
- workload inclusion/exclusion after freeze,
- system-family substitutions,
- semantic comparison rule changes,
- policy threshold changes,
- page-budget-driven result cherry-picking,
- authorship or submission-related matters.

### 8.3 Mandatory stop-and-escalate conditions
Stop immediately and request human input if any of the following occurs:
1. A core system cannot be faithfully reproduced from public code or paper description.
2. A query’s semantic contract is ambiguous.
3. Verification output conflicts across layers in a way not covered by the manual.
4. Runtime variance makes policy decisions unstable on more than 20% of cases in a pack.
5. A planned change touches a frozen protocol file.
6. A result suggests adding or dropping cases from a frozen pack.
7. An evaluation choice would make the paper depend on a proprietary or private artifact.

### 8.4 Plan-first discipline
For any non-trivial task, Codex must:
1. inspect relevant files,
2. write a concise plan,
3. list the commands it expects to run,
4. state the success criteria,
5. only then begin implementation.

### 8.5 Branch and worktree discipline
- One task = one branch/worktree.
- Names must encode area and task, e.g. `adapter-rbot`, `verifier-v2`, `analysis-rq1`.
- Never combine protocol, workload curation, and experiment execution in one branch.

### 8.6 Review discipline
Every non-trivial change set must contain:
- summary of what changed,
- commands run,
- files generated,
- validation outcome,
- explicit statement: `protocol changed: yes/no`.

`protocol changed: yes` requires human approval.

---

## 9. Codex skills and subagent plan

### 9.1 Required skills (create exactly these five first)
1. **`add_system_adapter`**
   - Input: system family, source code/repo, adapter target.
   - Output: adapter module, smoke test, metadata export.
2. **`add_verifier_adapter`**
   - Input: verifier type and interface contract.
   - Output: verifier adapter, evidence trace schema, test case.
3. **`run_pack_eval`**
   - Input: pack, universe, mode, policy, system set.
   - Output: normalized result files and run manifest.
4. **`build_tables_figures`**
   - Input: normalized results.
   - Output: main paper tables, appendix tables, figures.
5. **`artifact_preflight`**
   - Input: repository state.
   - Output: completeness report for code/data/docs/reproduction.

### 9.2 Suggested subagent roles
Subagents are allowed for highly parallel work, but only under a coordinator.

Suggested roles:
- `repo-mapper`
- `engine-operator`
- `adapter-implementer`
- `verdict-auditor`
- `artifact-auditor`

Subagents may explore, code, and validate in parallel, but only the coordinator may merge the final change set.

---

## 10. Development phases with exit criteria

### Phase 0 — Protocol freeze
Deliverables:
- root `AGENTS.md`
- this manual
- human decision register
- paper skeleton
- result schema draft

Exit criteria:
- RQ, packs, verdicts, policies, universes, and metrics are frozen.

### Phase 1 — Harness skeleton
Deliverables:
- repository layout
- PostgreSQL runner
- case manifest loader
- normalized result writer
- smoke tests

Exit criteria:
- `S0` runs end-to-end on a tiny anchor subset.

### Phase 2 — Workload curation
Deliverables:
- Anchor pack manifests
- SQLStorm-derived candidate review pipeline
- semantic-risk pack assets
- adjudication logs

Exit criteria:
- 162 cases frozen and versioned.

### Phase 3 — Core system integration
Deliverables:
- S1, S2, S3, S4 adapters
- compatibility subset manifest
- baseline prompts/configs frozen

Exit criteria:
- all core systems produce top-1 rewrites on the compatibility subset.

### Phase 4 — Verification pipeline
Deliverables:
- V0–V3 adapters
- verdict resolver
- evidence-trace export

Exit criteria:
- every candidate lands in one of the six official verdicts.

### Phase 5 — Main experiments
Required studies:
- anchor vs public_realistic vs semantic_risk
- raw_output vs deployment_utility
- compatibility_subset vs full_subset
- conservative vs practical

Exit criteria:
- RQ1–RQ3 each answered with at least one main table/figure and one robustness check.

### Phase 6 — Analysis and paperization
Deliverables:
- main tables and figures
- appendix tables and figures
- threat model notes
- submission-ready narrative

Exit criteria:
- each claim in the draft points to a specific table or figure.

### Phase 7 — Artifact preflight
Deliverables:
- reproduction guide
- one-command or few-command rerun path
- public archival packaging
- availability checklist

Exit criteria:
- a clean machine can regenerate the main tables/figures from the published artifact path.

---

## 11. Required experiment set

### 11.1 Mandatory experiments
- **E1**: Canonical-vs-realistic pack comparison.
- **E2**: Raw-output-vs-deployment-utility comparison.
- **E3**: Compatibility-vs-full universe comparison.
- **E4**: Conservative-vs-practical policy comparison.

### 11.2 Strongly recommended robustness experiments
- **R1**: Verification-layer ablation (`V0+V1`, `V0+V1+V2`, `V0+V1+V2+V3`).
- **R2**: Controlled LLM backend study for all LLM-based systems.
- **R3**: Cold-cache sensitivity on a small fixed subset.

### 11.3 Enhancement experiments (not acceptance dependencies)
- transfer subset on a second engine,
- enhancement systems (`LITHE`, `GenRewrite`, `GRewriter`),
- optional private/anonymized validation slice.

---

## 12. Expected paper evidence map

The main paper should be supportable with approximately:
- 4 main figures
- 4 main tables
- supplemental appendix tables/figures in the artifact

Minimum evidence allocation:
- `RQ1` → at least 1 table + 1 figure
- `RQ2` → at least 1 table + 1 figure
- `RQ3` → at least 1 table + 1 figure
- reproducibility/artifact → at least 1 appendix overview table

---

## 13. Reproducibility requirements

This project must be engineered as an EA&B artifact from day one.

Required properties:
- pinned engine/container versions,
- deterministic seeds where applicable,
- dataset and stats snapshot versioning,
- raw logs preserved,
- normalized results preserved,
- provenance for each case,
- public archival repository for supplemental material,
- rerun instructions that a reviewer can actually follow.

Do not postpone artifact hygiene to the final writing phase.

---

## 14. Submission guardrails

Before submission, confirm all of the following:
1. The paper title includes `[Experiment, Analysis & Benchmark]`.
2. The SAR statement explicitly grounds the paper in data management:
   - query processing and optimization,
   - benchmarking and performance measurement,
   - SQL equivalence / verification under deployment policy.
3. The paper does not overclaim “real-world” workloads if the main packs are public-realistic rather than production traces.
4. The paper does not claim a universal equivalence oracle.
5. Every main conclusion is reproducible from the artifact.
6. Every deviation from original systems is documented.

---

## 15. Implementation priorities for Codex

When time is limited, prioritize in this order:
1. harness integrity,
2. workload governance,
3. core systems,
4. verification pipeline,
5. main experiments,
6. artifact preflight,
7. enhancement systems.

Never sacrifice protocol integrity for extra baseline count.

---

## 16. Final rule

If a proposed shortcut makes the project easier but weakens protocol credibility, reproducibility, or EA&B fit, **do not take the shortcut** without human approval.
