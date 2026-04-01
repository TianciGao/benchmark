# HD-03 Pilot Enablement Status

Date: 2026-04-01

## Scope

This note distinguishes four different readiness layers for `HD-03`.

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

### 3. Minimal Pilot-Smoke Executability

Meaning:

- the repo contains minimally executable load/timing SQL entry points
- runtime manifests point to real local asset files
- `psql` and PostgreSQL connection environment are sufficient for a local smoke check

Current local status:

- `not yet`

Validation command:

```bash
python -m scripts.cli hd03-pilot-toolchain-check --config results/hd03/<run_id>.inputs.json
```

### 4. Actual Pilot Executability

Meaning:

- the real local benchmark toolchain exists
- dataset generation tools are present for both benchmark families
- the minimally executable smoke layer is already in place
- PostgreSQL environment is available for non-interactive execution

## Current Known Local Findings

Found:

- `psql`
- PostgreSQL connection environment variables
- local machine build prerequisites: `gcc`, `make`, `tar`, `perl`
- real local driver SQL entry points under `sql/hd03/`
- benchmark asset-file layout under `sql/hd03/assets/tpch/` and `sql/hd03/assets/tpcds/`
- local vendor staging and binding path under `tools/hd03/vendor/` and `tools/hd03/bin/`

Missing or still non-final:

- `dbgen`
- `dsdgen`
- benchmark-faithful third-party generator binaries or source drops
- full benchmark-faithful generated data assets beyond the current benchmark-shaped pilot assets

## Interpretation

The repository is currently:

- input-complete for HD-03 preparation
- command-slot concrete for HD-03 preparation
- benchmark-shaped smoke-layer assets provisioned for HD-03 preparation
- not yet proven pilot-executable for a real HD-03 run

### Additional Toolchain Layers

`toolchain_present` means:

- `psql`, `dbgen`, and `dsdgen` are all locally resolvable

`toolchain_integrated` means:

- the repo contains runnable local entry points and runtime manifests that bind HD-03 load/timing commands to concrete repo paths

`minimal_pilot_smoke_executable` means:

- `psql` is locally resolvable
- PostgreSQL connection environment is present
- runtime manifests, driver SQL, and benchmark asset SQL all exist
- the local load/timing layer can be exercised as a smoke check without full benchmark data

`pilot_executable` means:

- toolchain is present
- toolchain is integrated
- the minimally executable smoke layer is already in place
- benchmark-generator binaries are available for real candidate-scale data generation

## Protocol Statement

`protocol changed: no`
