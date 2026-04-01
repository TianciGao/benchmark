from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "sql" / "hd03" / "runtime"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_psql() -> str | None:
    env_override = os.environ.get("PSQL_BIN")
    if env_override and Path(env_override).exists():
        return env_override
    return shutil.which("psql")


def _runtime_manifest(kind: str, benchmark: str) -> Path:
    return RUNTIME_DIR / f"{benchmark}.{kind}.json"


def _load_runtime_manifest(kind: str, benchmark: str) -> dict[str, Any]:
    path = _runtime_manifest(kind, benchmark)
    payload = _read_json(path)
    payload["_manifest_path"] = str(path)
    return payload


def _resolve_required_paths(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    for item in manifest.get("required_files", []):
        rel = item["path"]
        path = ROOT / rel
        resolved.append(
            {
                "label": item["label"],
                "path": rel,
                "exists": path.exists(),
            }
        )
    return resolved


def _build_env() -> dict[str, str]:
    env = dict(os.environ)
    env["PGCONNECT_TIMEOUT"] = env.get("PGCONNECT_TIMEOUT", "5")
    return env


def _run_psql(command: list[str]) -> int:
    completed = subprocess.run(command, check=False, env=_build_env())
    return completed.returncode


def command_load(args: argparse.Namespace) -> int:
    manifest = _load_runtime_manifest("load", args.benchmark)
    required = _resolve_required_paths(manifest)
    psql_path = _resolve_psql()
    missing = [item["path"] for item in required if not item["exists"]]
    command = [
        psql_path or "psql",
        "-v",
        "ON_ERROR_STOP=1",
        "-v",
        f"benchmark={args.benchmark}",
        "-v",
        f"data_dir={args.data_dir}",
        "-v",
        f"scale={args.scale}",
        "-f",
        str(ROOT / manifest["driver_sql"]),
    ]
    print(f"[hd03-runner-load] benchmark={args.benchmark}")
    print(f"[hd03-runner-load] driver_sql={manifest['driver_sql']}")
    print(f"[hd03-runner-load] required_files={json.dumps(required, ensure_ascii=False)}")
    print(f"[hd03-runner-load] command={json.dumps(command, ensure_ascii=False)}")
    if missing:
        print(f"[hd03-runner-load] blocked_missing_files={json.dumps(missing, ensure_ascii=False)}")
        return 2
    if not args.execute:
        print("[hd03-runner-load] dry_run_only=true")
        return 0
    if not psql_path:
        print("[hd03-runner-load] blocked_reason=psql_missing")
        return 3
    return _run_psql(command)


def command_time(args: argparse.Namespace) -> int:
    manifest = _load_runtime_manifest("pilot", args.benchmark)
    required = _resolve_required_paths(manifest)
    psql_path = _resolve_psql()
    missing = [item["path"] for item in required if not item["exists"]]
    command = [
        psql_path or "psql",
        "-X",
        "-w",
        "-h",
        os.environ.get("PGHOST", ""),
        "-p",
        os.environ.get("PGPORT", ""),
        "-U",
        os.environ.get("PGUSER", ""),
        "-d",
        os.environ.get("PGDATABASE", ""),
        "-v",
        f"benchmark={args.benchmark}",
        "-f",
        str(ROOT / manifest["driver_sql"]),
    ]
    print(f"[hd03-runner-time] benchmark={args.benchmark}")
    print(f"[hd03-runner-time] driver_sql={manifest['driver_sql']}")
    print(f"[hd03-runner-time] required_files={json.dumps(required, ensure_ascii=False)}")
    print(f"[hd03-runner-time] command={json.dumps(command, ensure_ascii=False)}")
    if missing:
        print(f"[hd03-runner-time] blocked_missing_files={json.dumps(missing, ensure_ascii=False)}")
        return 2
    if not args.execute:
        print("[hd03-runner-time] dry_run_only=true")
        return 0
    if not psql_path:
        print("[hd03-runner-time] blocked_reason=psql_missing")
        return 3
    return _run_psql(command)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HD-03 local runner scaffolding")
    subparsers = parser.add_subparsers(dest="command", required=True)

    load = subparsers.add_parser("load")
    load.add_argument("--benchmark", choices=["tpch", "tpcds"], required=True)
    load.add_argument("--data-dir", required=True)
    load.add_argument("--scale", required=True)
    load.add_argument("--execute", action="store_true")
    load.set_defaults(handler=command_load)

    timing = subparsers.add_parser("time")
    timing.add_argument("--benchmark", choices=["tpch", "tpcds"], required=True)
    timing.add_argument("--execute", action="store_true")
    timing.set_defaults(handler=command_time)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
