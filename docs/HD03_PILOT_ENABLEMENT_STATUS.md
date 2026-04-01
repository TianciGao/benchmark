# HD-03 Pilot Enablement Status

Date: 2026-04-01

## Scope

This note distinguishes three different readiness layers for `HD-03`.

It does not run a real pilot and does not choose final scale factors.

## Readiness Layers

### 1. Input Completeness Readiness

Meaning:

- the human-input packet is filled
- the scaffolded HD-03 input JSON is populated
- the required input fields are present

Current local status:

- `yes`

Validation command:

```bash
python -m scripts.cli hd03-pilot-check-inputs --config results/hd03/<run_id>.inputs.json
```

### 2. Command-Slot Concretization

Meaning:

- all four HD-03 command slots point to concrete command patterns
- benchmark-specific local SQL entry-point paths are bound in the load/timing slots

Current local status:

- `yes`

Current local entry points:

- `sql/hd03/load_anchor_tpch.sql`
- `sql/hd03/load_anchor_tpcds.sql`
- `sql/hd03/pilot_queries_tpch.sql`
- `sql/hd03/pilot_queries_tpcds.sql`

### 3. Actual Pilot Executability

Meaning:

- the real local benchmark toolchain exists
- dataset generation tools are present
- bound SQL entry points are real pilot SQL rather than scaffolding-only stubs
- PostgreSQL environment is available for non-interactive execution

Current local status:

- `not yet`

Validation command:

```bash
python -m scripts.cli hd03-pilot-toolchain-check --config results/hd03/<run_id>.inputs.json
```

## Current Known Local Findings

Found:

- `psql`
- PostgreSQL connection environment variables
- scaffolded local SQL entry points under `sql/hd03/`

Missing or still non-final:

- `dbgen`
- `dsdgen`
- real benchmark load SQL
- real pilot query timing SQL

## Interpretation

The repository is currently:

- input-complete for HD-03 preparation
- command-slot concrete for HD-03 preparation
- not yet proven pilot-executable for a real HD-03 run

### Additional Toolchain Layers

`toolchain_present` means:

- `psql`, `dbgen`, and `dsdgen` are all locally resolvable

`toolchain_integrated` means:

- the repo contains runnable local entry points and runtime manifests that bind HD-03 load/timing commands to concrete repo paths

`pilot_executable` means:

- toolchain is present
- toolchain is integrated
- the benchmark-specific runtime assets are real rather than scaffold placeholders

## Protocol Statement

`protocol changed: no`
