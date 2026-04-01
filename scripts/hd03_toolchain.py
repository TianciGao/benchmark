from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _required_sql_paths(root: Path) -> dict[str, Path]:
    return {
        "load_anchor_tpch": root / "sql" / "hd03" / "load_anchor_tpch.sql",
        "load_anchor_tpcds": root / "sql" / "hd03" / "load_anchor_tpcds.sql",
        "pilot_queries_tpch": root / "sql" / "hd03" / "pilot_queries_tpch.sql",
        "pilot_queries_tpcds": root / "sql" / "hd03" / "pilot_queries_tpcds.sql",
    }


def _contains_scaffolding_marker(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    return "scaffolding only" in text.lower() or "placeholder" in text.lower()


def _resolve_tool(binary: str) -> str | None:
    env_override = os.environ.get("PSQL_BIN") if binary == "psql" else None
    if env_override and Path(env_override).exists():
        return env_override
    return shutil.which(binary)


def render_hd03_commands(config_path: Path) -> dict[str, str]:
    payload = _read_json(config_path)
    slots = payload.get("command_slots", {})
    return {
        "tpch_dataset_generation_command_template": slots.get("tpch_dataset_generation_command_template", ""),
        "tpcds_dataset_generation_command_template": slots.get("tpcds_dataset_generation_command_template", ""),
        "postgres_load_command_template": slots.get("postgres_load_command_template", ""),
        "pilot_query_timing_command_template": slots.get("pilot_query_timing_command_template", ""),
    }


def inspect_hd03_toolchain(root: Path, config_path: Path) -> dict[str, Any]:
    commands = render_hd03_commands(config_path)
    sql_paths = _required_sql_paths(root)
    sql_files = {
        key: {
            "path": str(path.relative_to(root)),
            "exists": path.exists(),
            "scaffolding_only": _contains_scaffolding_marker(path),
        }
        for key, path in sql_paths.items()
    }

    tools = {
        "psql": _resolve_tool("psql"),
        "dbgen": _resolve_tool("dbgen"),
        "dsdgen": _resolve_tool("dsdgen"),
    }

    env_status = {
        key: bool(os.environ.get(key))
        for key in ("PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD")
    }

    missing_components: list[str] = []
    if not tools["psql"]:
        missing_components.append("psql")
    if not tools["dbgen"]:
        missing_components.append("dbgen")
    if not tools["dsdgen"]:
        missing_components.append("dsdgen")
    for key, meta in sql_files.items():
        if not meta["exists"]:
            missing_components.append(key)

    actual_pilot_blockers: list[str] = []
    if not tools["dbgen"]:
        actual_pilot_blockers.append("TPC-H dataset generation tool `dbgen` not found")
    if not tools["dsdgen"]:
        actual_pilot_blockers.append("TPC-DS dataset generation tool `dsdgen` not found")
    if sql_files["load_anchor_tpch"]["scaffolding_only"] or sql_files["load_anchor_tpcds"]["scaffolding_only"]:
        actual_pilot_blockers.append("Load SQL entry points are scaffolding-only stubs")
    if sql_files["pilot_queries_tpch"]["scaffolding_only"] or sql_files["pilot_queries_tpcds"]["scaffolding_only"]:
        actual_pilot_blockers.append("Pilot timing SQL entry points are scaffolding-only stubs")
    if not all(env_status.values()):
        actual_pilot_blockers.append("PostgreSQL connection environment is incomplete for non-interactive psql timing")

    return {
        "config_path": str(config_path.relative_to(root) if not config_path.is_absolute() else config_path),
        "rendered_commands": commands,
        "resolved_tools": tools,
        "pg_environment_present": env_status,
        "sql_files": sql_files,
        "input_completeness_ready": True,
        "command_slot_concretized": True,
        "pilot_executable": not actual_pilot_blockers,
        "missing_components": missing_components,
        "actual_pilot_blockers": actual_pilot_blockers,
    }
