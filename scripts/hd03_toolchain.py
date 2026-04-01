from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / "tools" / "hd03"
VENDOR_BIN_DIR = TOOLS_DIR / "vendor" / "bin"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _driver_sql_paths(root: Path) -> dict[str, Path]:
    return {
        "load_anchor_tpch": root / "sql" / "hd03" / "load_anchor_tpch.sql",
        "load_anchor_tpcds": root / "sql" / "hd03" / "load_anchor_tpcds.sql",
        "pilot_queries_tpch": root / "sql" / "hd03" / "pilot_queries_tpch.sql",
        "pilot_queries_tpcds": root / "sql" / "hd03" / "pilot_queries_tpcds.sql",
    }


def _runtime_manifest_paths(root: Path) -> dict[str, Path]:
    return {
        "tpch_load_manifest": root / "sql" / "hd03" / "runtime" / "tpch.load.json",
        "tpcds_load_manifest": root / "sql" / "hd03" / "runtime" / "tpcds.load.json",
        "tpch_pilot_manifest": root / "sql" / "hd03" / "runtime" / "tpch.pilot.json",
        "tpcds_pilot_manifest": root / "sql" / "hd03" / "runtime" / "tpcds.pilot.json",
    }


def _contains_scaffolding_marker(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8").lower()
    return "scaffolding only" in text or "placeholder" in text


def _resolve_tool(binary: str) -> str | None:
    env_override = os.environ.get("PSQL_BIN") if binary == "psql" else None
    if env_override and Path(env_override).exists():
        return env_override
    local_bound = ROOT / "tools" / "hd03" / "bin" / binary
    if local_bound.exists():
        return str(local_bound)
    staged_local = VENDOR_BIN_DIR / binary
    if staged_local.exists():
        return str(staged_local)
    return shutil.which(binary)


def _vendor_source_status(root: Path) -> dict[str, dict[str, Any]]:
    targets = {
        "vendor_bin_dbgen": root / "tools" / "hd03" / "vendor" / "bin" / "dbgen",
        "vendor_bin_dsdgen": root / "tools" / "hd03" / "vendor" / "bin" / "dsdgen",
        "tpch_source_tree": root / "tools" / "hd03" / "vendor" / "src" / "tpch-dbgen",
        "tpcds_source_tree": root / "tools" / "hd03" / "vendor" / "src" / "tpcds-kit",
    }
    return {
        key: {
            "path": str(path.relative_to(root)),
            "exists": path.exists(),
        }
        for key, path in targets.items()
    }


def render_hd03_commands(config_path: Path) -> dict[str, str]:
    payload = _read_json(config_path)
    slots = payload.get("command_slots", {})
    return {
        "tpch_dataset_generation_command_template": slots.get("tpch_dataset_generation_command_template", ""),
        "tpcds_dataset_generation_command_template": slots.get("tpcds_dataset_generation_command_template", ""),
        "postgres_load_command_template": slots.get("postgres_load_command_template", ""),
        "pilot_query_timing_command_template": slots.get("pilot_query_timing_command_template", ""),
    }


def _asset_file_status(root: Path, runtime_manifests: dict[str, Path]) -> dict[str, dict[str, Any]]:
    files: dict[str, dict[str, Any]] = {}
    for manifest_path in runtime_manifests.values():
        if not manifest_path.exists():
            continue
        manifest = _read_json(manifest_path)
        driver_rel = manifest["driver_sql"]
        driver_path = root / driver_rel
        files[driver_rel] = {
            "path": driver_rel,
            "exists": driver_path.exists(),
            "scaffolding_only": _contains_scaffolding_marker(driver_path),
        }
        for item in manifest.get("required_files", []):
            rel = item["path"]
            path = root / rel
            files[rel] = {
                "path": rel,
                "exists": path.exists(),
                "scaffolding_only": _contains_scaffolding_marker(path),
            }
    return files


def inspect_hd03_toolchain(root: Path, config_path: Path) -> dict[str, Any]:
    commands = render_hd03_commands(config_path)
    driver_sql_files = {
        key: {
            "path": str(path.relative_to(root)),
            "exists": path.exists(),
            "scaffolding_only": _contains_scaffolding_marker(path),
        }
        for key, path in _driver_sql_paths(root).items()
    }
    runtime_manifest_paths = _runtime_manifest_paths(root)
    runtime_manifests = {
        key: {
            "path": str(path.relative_to(root)),
            "exists": path.exists(),
        }
        for key, path in runtime_manifest_paths.items()
    }
    asset_sql_files = _asset_file_status(root, runtime_manifest_paths)

    tools = {
        "psql": _resolve_tool("psql"),
        "dbgen": _resolve_tool("dbgen"),
        "dsdgen": _resolve_tool("dsdgen"),
    }

    env_status = {
        key: bool(os.environ.get(key))
        for key in ("PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD")
    }
    vendor_sources = _vendor_source_status(root)

    missing_components: list[str] = []
    if not tools["psql"]:
        missing_components.append("psql")
    if not tools["dbgen"]:
        missing_components.append("dbgen")
    if not tools["dsdgen"]:
        missing_components.append("dsdgen")
    for key, meta in driver_sql_files.items():
        if not meta["exists"]:
            missing_components.append(key)
    for rel, meta in asset_sql_files.items():
        if not meta["exists"]:
            missing_components.append(rel)

    toolchain_present = bool(tools["psql"] and tools["dbgen"] and tools["dsdgen"])
    toolchain_integrated = (
        all(meta["exists"] for meta in runtime_manifests.values())
        and all(meta["exists"] for meta in driver_sql_files.values())
        and all(meta["exists"] for meta in asset_sql_files.values())
    )

    pilot_smoke_blockers: list[str] = []
    if not tools["psql"]:
        pilot_smoke_blockers.append("psql not found")
    if not all(env_status.values()):
        pilot_smoke_blockers.append("PostgreSQL connection environment is incomplete for non-interactive psql execution")
    if not all(meta["exists"] for meta in runtime_manifests.values()):
        pilot_smoke_blockers.append("Runtime manifests for load/timing entry points are incomplete")
    if any(meta["scaffolding_only"] for meta in driver_sql_files.values()):
        pilot_smoke_blockers.append("Driver SQL entry points still contain scaffold markers")
    if not all(meta["exists"] for meta in asset_sql_files.values()):
        pilot_smoke_blockers.append("Benchmark asset SQL files are incomplete")
    if any(meta["scaffolding_only"] for meta in asset_sql_files.values()):
        pilot_smoke_blockers.append("Benchmark asset SQL files still contain scaffold markers")

    minimal_pilot_smoke_executable = not pilot_smoke_blockers

    actual_pilot_blockers = list(pilot_smoke_blockers)
    if not tools["dbgen"]:
        actual_pilot_blockers.append("TPC-H dataset generation tool `dbgen` not found")
    if not tools["dsdgen"]:
        actual_pilot_blockers.append("TPC-DS dataset generation tool `dsdgen` not found")
    if not tools["dbgen"] and not (
        vendor_sources["vendor_bin_dbgen"]["exists"] or vendor_sources["tpch_source_tree"]["exists"]
    ):
        actual_pilot_blockers.append("No local TPCH kit binary or source tree is staged under tools/hd03/vendor")
    if not tools["dsdgen"] and not (
        vendor_sources["vendor_bin_dsdgen"]["exists"] or vendor_sources["tpcds_source_tree"]["exists"]
    ):
        actual_pilot_blockers.append("No local TPCDS kit binary or source tree is staged under tools/hd03/vendor")

    return {
        "config_path": str(config_path.relative_to(root) if not config_path.is_absolute() else config_path),
        "rendered_commands": commands,
        "resolved_tools": tools,
        "pg_environment_present": env_status,
        "sql_files": driver_sql_files,
        "asset_sql_files": asset_sql_files,
        "runtime_manifests": runtime_manifests,
        "vendor_source_status": vendor_sources,
        "input_completeness_ready": True,
        "command_slot_concretized": True,
        "toolchain_present": toolchain_present,
        "toolchain_integrated": toolchain_integrated,
        "minimal_pilot_smoke_executable": minimal_pilot_smoke_executable,
        "pilot_smoke_blockers": pilot_smoke_blockers,
        "pilot_executable": minimal_pilot_smoke_executable and toolchain_present,
        "missing_components": missing_components,
        "actual_pilot_blockers": actual_pilot_blockers,
    }
