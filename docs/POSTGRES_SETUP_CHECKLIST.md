# PostgreSQL Setup Checklist

Use this checklist only to satisfy Phase 1 environment readiness for the tiny anchor smoke path.

## 1. Client Tools

- Confirm `psql` is installed:
  - `where.exe psql`
- If missing, install PostgreSQL client tools and reopen the shell
- If installed but not in `PATH`, either:
  - add the PostgreSQL `bin` directory to `PATH`
  - or set `PSQL_BIN` to the full path of `psql.exe`

PowerShell example:

```powershell
$env:PSQL_BIN = "C:\Program Files\PostgreSQL\17\bin\psql.exe"
```

## 2. Server Availability

Choose one supported Phase 1 path:

- local PostgreSQL service
- reachable PostgreSQL container
- remote PostgreSQL instance reachable from this machine

Useful checks:

- Windows service probe:
  - `Get-Service *postgres*`
- Docker container probe:
  - `docker ps --format "{{.Names}} {{.Image}} {{.Status}}"`

## 3. Connection Parameters

Preferred options:

- set `POSTGRES_DSN`
- or set `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`
- or set `POSTGRES_LOCAL_CONFIG` to a private local `.env` or `.json` file

PowerShell example:

```powershell
$env:POSTGRES_DSN = "postgresql://USER:PASSWORD@HOST:5432/DBNAME"
```

Private local config example:

```powershell
$env:POSTGRES_LOCAL_CONFIG = "C:\private\benchmark4vldb-postgres.env"
```

Example private `.env` content:

```text
PGHOST=localhost
PGPORT=5432
PGDATABASE=postgres
PGUSER=postgres
PGPASSWORD=your-secret-password
PSQL_BIN=C:\Program Files\PostgreSQL\17\bin\psql.exe
```

## 4. Minimal Connection Tests

- With explicit DSN:

```powershell
& $env:PSQL_BIN $env:POSTGRES_DSN -X -w -c "SELECT 1;"
& $env:PSQL_BIN $env:POSTGRES_DSN -X -w -c "SHOW server_version;"
```

- With local defaults:

```powershell
& $env:PSQL_BIN -X -w -d postgres -c "SELECT 1;"
& $env:PSQL_BIN -X -w -d postgres -c "SHOW server_version;"
```

## 5. Repository Diagnostics

Run:

```powershell
python -m scripts.cli postgres-env-check
python -m scripts.cli smoke
```

Expected outcome:

- If ready, smoke writes real runtime samples and `S0` completes end-to-end
- If blocked, the JSON report under `results/environment/` explains what is missing

Current observed blocker on this machine:

- a PostgreSQL 17 Windows service is running
- `psql.exe` is discoverable under `C:\Program Files\PostgreSQL\17\bin\psql.exe`
- neither environment variables nor `POSTGRES_LOCAL_CONFIG` are currently configured
- the connection attempt currently fails with `fe_sendauth: no password supplied`

## 6. Phase Boundary Reminder

- Do not use this checklist to expand workloads
- Do not freeze official pack membership here
- Do not add new system families here
