from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlsplit, urlunsplit


@dataclass
class RunnerResult:
    ok: bool
    exec_status: str
    stdout: str
    stderr: str
    runtime_ms: Optional[float]


@dataclass
class PostgresEnvironmentReport:
    timestamp: str
    platform: str
    hostname: str
    config_sources_checked: list[str]
    private_config_status: str
    private_config_loaded_keys: list[str]
    private_config_error: Optional[str]
    psql_binary: str
    psql_found: bool
    psql_path: Optional[str]
    psql_resolution_source: str
    connection_target_source: str
    connection_target_hint: Optional[str]
    explicit_connection_parameters_available: bool
    pg_env: dict[str, Optional[str]]
    pgpassword_present: bool
    windows_service_probe: dict[str, Any]
    docker_probe: dict[str, Any]
    connectivity_ok: bool
    connectivity_status: str
    connectivity_stdout: str
    connectivity_stderr: str
    connectivity_runtime_ms: Optional[float]
    server_version: Optional[str]
    readiness_status: str
    phase1_status: str
    blockers: list[str]
    minimal_connection_test_commands: list[str]
    recommended_next_steps: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PostgresRunner:
    def __init__(self, dsn: Optional[str] = None, psql_bin: str = "psql") -> None:
        self._private_config_cache: Optional[dict[str, str]] = None
        self._private_config_status: str = "not_checked"
        self._private_config_error: Optional[str] = None
        self._private_config_loaded_keys: list[str] = []
        self.dsn = dsn or self._config_value("POSTGRES_DSN")
        self.psql_bin = self._config_value("PSQL_BIN") or psql_bin
        self._engine_version: Optional[str] = None
        self._probe_cache: Optional[PostgresEnvironmentReport] = None

    def _utc_timestamp(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    def _load_private_config(self) -> dict[str, str]:
        if self._private_config_cache is not None:
            return self._private_config_cache

        pointer = os.environ.get("POSTGRES_LOCAL_CONFIG")
        if not pointer:
            self._private_config_status = "not_configured"
            self._private_config_cache = {}
            return self._private_config_cache

        path = Path(pointer)
        if not path.exists():
            self._private_config_status = "missing_file"
            self._private_config_error = "POSTGRES_LOCAL_CONFIG points to a missing file"
            self._private_config_cache = {}
            return self._private_config_cache

        valid_keys = {
            "POSTGRES_DSN",
            "PGHOST",
            "PGPORT",
            "PGDATABASE",
            "PGUSER",
            "PGPASSWORD",
            "PSQL_BIN",
        }

        try:
            if path.suffix.lower() == ".json":
                payload = json.loads(path.read_text(encoding="utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("JSON private config must be an object")
                config = {
                    key: str(value).strip()
                    for key, value in payload.items()
                    if key in valid_keys and str(value).strip()
                }
            else:
                config = {}
                for raw_line in path.read_text(encoding="utf-8").splitlines():
                    line = raw_line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key in valid_keys and value:
                        config[key] = value

            self._private_config_status = "loaded"
            self._private_config_loaded_keys = sorted(config.keys())
            self._private_config_cache = config
            return self._private_config_cache
        except Exception as exc:
            self._private_config_status = "parse_error"
            self._private_config_error = str(exc)
            self._private_config_cache = {}
            return self._private_config_cache

    def _config_value(self, name: str) -> Optional[str]:
        process_value = os.environ.get(name)
        if process_value:
            return process_value
        return self._load_private_config().get(name)

    def _pg_env(self) -> dict[str, Optional[str]]:
        return {
            "PGHOST": self._config_value("PGHOST"),
            "PGPORT": self._config_value("PGPORT"),
            "PGDATABASE": self._config_value("PGDATABASE"),
            "PGUSER": self._config_value("PGUSER"),
        }

    def _resolve_psql_path(self) -> tuple[Optional[str], str]:
        env_override = self._config_value("PSQL_BIN")
        if env_override and Path(env_override).exists():
            source = "POSTGRES_LOCAL_CONFIG" if "PSQL_BIN" in self._private_config_loaded_keys else "PSQL_BIN"
            return env_override, source

        resolved = shutil.which(self.psql_bin)
        if resolved:
            return resolved, "PATH"

        if platform.system().lower() == "windows" and self.psql_bin == "psql":
            root = Path(r"C:\Program Files\PostgreSQL")
            if root.exists():
                matches = sorted(root.glob(r"*\bin\psql.exe"), reverse=True)
                if matches:
                    return str(matches[0]), "windows_fallback"

        return None, "unresolved"

    def _connection_target_source(self) -> tuple[str, Optional[str], bool]:
        if self.dsn:
            return "POSTGRES_DSN", redact_connection_target(self.dsn), True
        pg_env = self._pg_env()
        if any(value for value in pg_env.values()):
            parts = [f"{key}={value}" for key, value in pg_env.items() if value]
            return "PG* environment variables", ", ".join(parts), True
        return "psql defaults", None, False

    def _psql_base_command(self) -> list[str]:
        psql_path, _ = self._resolve_psql_path()
        command = [psql_path or self.psql_bin]
        if self.dsn:
            command.append(self.dsn)
        return command

    def _psql_runtime_env(self) -> dict[str, str]:
        env = dict(os.environ)
        for key in ("PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"):
            value = self._config_value(key)
            if value:
                env[key] = value
        env["PGCONNECT_TIMEOUT"] = "5"
        return env

    def _invoke_psql(self, sql: str, timeout_seconds: int) -> RunnerResult:
        psql_path, _ = self._resolve_psql_path()
        if not psql_path:
            return RunnerResult(
                ok=False,
                exec_status="engine_unavailable",
                stdout="",
                stderr=f"psql binary not found: {self.psql_bin}",
                runtime_ms=None,
            )

        command = self._psql_base_command() + [
            "-X",
            "-q",
            "-A",
            "-t",
            "-w",
            "-v",
            "ON_ERROR_STOP=1",
            "-c",
            sql,
        ]
        start = time.perf_counter()
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env=self._psql_runtime_env(),
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            runtime_ms = round((time.perf_counter() - start) * 1000.0, 3)
            return RunnerResult(
                ok=False,
                exec_status="timeout",
                stdout=(exc.stdout or "").strip(),
                stderr=((exc.stderr or "").strip() or "psql command timed out"),
                runtime_ms=runtime_ms,
            )

        runtime_ms = round((time.perf_counter() - start) * 1000.0, 3)
        exec_status = "ok" if completed.returncode == 0 else "execution_error"
        return RunnerResult(
            ok=completed.returncode == 0,
            exec_status=exec_status,
            stdout=completed.stdout.strip(),
            stderr=completed.stderr.strip(),
            runtime_ms=runtime_ms,
        )

    def _probe_windows_services(self) -> dict[str, Any]:
        if platform.system().lower() != "windows":
            return {
                "supported": False,
                "status": "skipped_non_windows",
                "services": [],
            }

        powershell = shutil.which("powershell.exe") or shutil.which("powershell")
        if not powershell:
            return {
                "supported": False,
                "status": "powershell_missing",
                "services": [],
            }

        command = [
            powershell,
            "-NoProfile",
            "-Command",
            "@(Get-Service *postgres* -ErrorAction SilentlyContinue | "
            "Select-Object Name,@{Name='Status';Expression={$_.Status.ToString()}},DisplayName) | "
            "ConvertTo-Json -Compress",
        ]
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if completed.returncode != 0 and not completed.stdout.strip() and not completed.stderr.strip():
            return {
                "supported": True,
                "status": "probe_failed",
                "stderr": "powershell service probe returned no output",
                "services": [],
            }
        stdout = completed.stdout.strip()
        if completed.returncode != 0:
            return {
                "supported": True,
                "status": "probe_failed",
                "stderr": completed.stderr.strip(),
                "services": [],
            }

        if not stdout:
            return {
                "supported": True,
                "status": "no_matching_services",
                "services": [],
            }

        try:
            services = json.loads(stdout)
        except json.JSONDecodeError:
            return {
                "supported": True,
                "status": "unparsed_output",
                "raw_stdout": stdout,
                "services": [],
            }
        if isinstance(services, dict):
            services = [services]
        return {
            "supported": True,
            "status": "ok",
            "services": services,
        }

    def _probe_docker(self) -> dict[str, Any]:
        docker_path = shutil.which("docker")
        if not docker_path:
            return {
                "cli_found": False,
                "status": "docker_missing",
                "containers": [],
            }

        command = [docker_path, "ps", "--format", "{{json .}}"]
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {
                "cli_found": True,
                "status": "probe_timeout",
                "containers": [],
            }
        if completed.returncode != 0:
            return {
                "cli_found": True,
                "status": "probe_failed",
                "stderr": completed.stderr.strip(),
                "containers": [],
            }

        containers: list[dict[str, Any]] = []
        for line in completed.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                containers.append(json.loads(line))
            except json.JSONDecodeError:
                containers.append({"raw": line})
        return {
            "cli_found": True,
            "status": "ok",
            "containers": containers,
        }

    def probe_environment(self, refresh: bool = False) -> PostgresEnvironmentReport:
        if self._probe_cache is not None and not refresh:
            return self._probe_cache

        psql_path, psql_resolution_source = self._resolve_psql_path()
        source, hint, explicit_params = self._connection_target_source()
        connectivity_result = self._invoke_psql("SELECT 1;", timeout_seconds=10)
        connectivity_ok = connectivity_result.ok and connectivity_result.stdout == "1"

        if not psql_path:
            connectivity_status = "psql_missing"
        elif connectivity_ok:
            connectivity_status = "ready"
        elif self.dsn:
            connectivity_status = "connection_failed_with_postgres_dsn"
        elif explicit_params:
            connectivity_status = "connection_failed_with_pg_environment"
        else:
            connectivity_status = "connection_failed_with_psql_defaults"

        server_version: Optional[str] = None
        if connectivity_ok:
            version_result = self._invoke_psql("SHOW server_version;", timeout_seconds=10)
            if version_result.ok and version_result.stdout:
                server_version = version_result.stdout.splitlines()[0].strip()
                self._engine_version = server_version

        blockers: list[str] = []
        if self._private_config_status == "missing_file":
            blockers.append("POSTGRES_LOCAL_CONFIG is set but its file is missing")
        if self._private_config_status == "parse_error":
            blockers.append("POSTGRES_LOCAL_CONFIG could not be parsed")
        if not psql_path:
            blockers.append("psql is not installed or not available in PATH")
        if psql_path and not connectivity_ok:
            blockers.append(
                "PostgreSQL connectivity probe failed; inspect connection parameters or local service/container state"
            )

        readiness_status = "ready" if connectivity_ok else "blocked"
        phase1_status = "Phase 1 environment ready" if connectivity_ok else "Phase 1 ready except environment"

        recommended_next_steps = build_recommended_next_steps(
            psql_found=bool(psql_path),
            explicit_params=explicit_params,
            connectivity_ok=connectivity_ok,
        )

        report = PostgresEnvironmentReport(
            timestamp=self._utc_timestamp(),
            platform=platform.platform(),
            hostname=platform.node(),
            config_sources_checked=["process environment", "POSTGRES_LOCAL_CONFIG"],
            private_config_status=self._private_config_status,
            private_config_loaded_keys=self._private_config_loaded_keys,
            private_config_error=self._private_config_error,
            psql_binary=self.psql_bin,
            psql_found=bool(psql_path),
            psql_path=psql_path,
            psql_resolution_source=psql_resolution_source,
            connection_target_source=source,
            connection_target_hint=hint,
            explicit_connection_parameters_available=explicit_params,
            pg_env=self._pg_env(),
            pgpassword_present=bool(self._config_value("PGPASSWORD")),
            windows_service_probe=self._probe_windows_services(),
            docker_probe=self._probe_docker(),
            connectivity_ok=connectivity_ok,
            connectivity_status=connectivity_status,
            connectivity_stdout=connectivity_result.stdout,
            connectivity_stderr=connectivity_result.stderr,
            connectivity_runtime_ms=connectivity_result.runtime_ms,
            server_version=server_version,
            readiness_status=readiness_status,
            phase1_status=phase1_status,
            blockers=blockers,
            minimal_connection_test_commands=build_minimal_connection_test_commands(
                psql_command=psql_path or self.psql_bin,
                dsn=self.dsn,
                pg_env=self._pg_env(),
            ),
            recommended_next_steps=recommended_next_steps,
        )
        self._probe_cache = report
        return report

    def availability(self) -> tuple[bool, str]:
        report = self.probe_environment()
        if report.connectivity_ok:
            return True, "ready"
        if report.blockers:
            return False, "; ".join(report.blockers)
        return False, report.connectivity_status

    def _run_sql(self, sql: str, timeout_seconds: int) -> RunnerResult:
        report = self.probe_environment()
        if not report.connectivity_ok:
            exec_status = "engine_unavailable" if not report.psql_found else "connection_unavailable"
            return RunnerResult(
                ok=False,
                exec_status=exec_status,
                stdout="",
                stderr="; ".join(report.blockers) or report.connectivity_status,
                runtime_ms=None,
            )
        return self._invoke_psql(sql=sql, timeout_seconds=timeout_seconds)

    def execute(self, sql: str, timeout_seconds: int = 30) -> RunnerResult:
        return self._run_sql(sql=sql, timeout_seconds=timeout_seconds)

    def engine_version(self) -> str:
        if self._engine_version is not None:
            return self._engine_version
        result = self._run_sql("SHOW server_version;", timeout_seconds=15)
        if result.ok and result.stdout:
            self._engine_version = result.stdout.splitlines()[0].strip()
        else:
            self._engine_version = "unavailable"
        return self._engine_version


def redact_connection_target(target: Optional[str]) -> Optional[str]:
    if not target:
        return None

    if "://" in target:
        parsed = urlsplit(target)
        if parsed.password is not None:
            userinfo = parsed.username or ""
            if parsed.password is not None:
                userinfo = f"{userinfo}:***"
            hostinfo = parsed.hostname or ""
            if parsed.port is not None:
                hostinfo = f"{hostinfo}:{parsed.port}"
            netloc = f"{userinfo}@{hostinfo}" if userinfo else hostinfo
            return urlunsplit((parsed.scheme, netloc, parsed.path, parsed.query, parsed.fragment))

    return re.sub(r"(password=)([^\s]+)", r"\1***", target, flags=re.IGNORECASE)


def build_minimal_connection_test_commands(
    psql_command: str,
    dsn: Optional[str],
    pg_env: dict[str, Optional[str]],
) -> list[str]:
    if dsn:
        redacted = redact_connection_target(dsn)
        return [
            f'"{psql_command}" "{redacted}" -X -w -c "SELECT 1;"',
            f'"{psql_command}" "{redacted}" -X -w -c "SHOW server_version;"',
        ]

    if any(value for value in pg_env.values()):
        return [
            f'"{psql_command}" -X -w -c "SELECT 1;"',
            f'"{psql_command}" -X -w -c "SHOW server_version;"',
        ]

    return [
        f'"{psql_command}" -X -w -d postgres -c "SELECT 1;"',
        '$env:POSTGRES_DSN="postgresql://USER:PASSWORD@HOST:5432/DBNAME"; '
        f'"{psql_command}" $env:POSTGRES_DSN -X -w -c "SELECT 1;"',
    ]


def build_recommended_next_steps(
    psql_found: bool,
    explicit_params: bool,
    connectivity_ok: bool,
) -> list[str]:
    if connectivity_ok:
        return [
            "Run `python -m scripts.cli smoke` to confirm S0 end-to-end on the tiny anchor subset",
            "Record HD-01 and HD-02 before claiming Phase 1 exit",
        ]

    steps: list[str] = []
    if not psql_found:
        steps.append("Install PostgreSQL client tools or add `psql` to PATH")
    if not explicit_params:
        steps.append(
            "Set `POSTGRES_DSN`, the standard `PGHOST` / `PGPORT` / `PGDATABASE` / `PGUSER` variables, "
            "or point `POSTGRES_LOCAL_CONFIG` to a private local config file"
        )
    steps.append("Start a local PostgreSQL service or a reachable PostgreSQL container")
    steps.append("Run `python -m scripts.cli postgres-env-check` again and inspect the JSON report under `results/environment/`")
    steps.append("After connectivity succeeds, rerun `python -m scripts.cli smoke`")
    return steps


def write_environment_report(
    root: Path,
    report: PostgresEnvironmentReport,
    label: str,
) -> Path:
    results_dir = root / "results" / "environment"
    results_dir.mkdir(parents=True, exist_ok=True)
    safe_timestamp = report.timestamp.replace(":", "").replace("+00:00", "z")
    path = results_dir / f"{label}-{safe_timestamp}.json"
    path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
