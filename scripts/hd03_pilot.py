from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TEMPLATE_INPUT_CONFIG = "results/templates/hd03_anchor_scale_inputs.template.json"
TEMPLATE_MANIFEST = "results/templates/hd03_anchor_scale_pilot_manifest.template.json"
TEMPLATE_SUMMARY = "analysis/phase2_placeholders/hd03_anchor_scale_summary_template.csv"


@dataclass
class HD03ScaffoldPaths:
    run_id: str
    config_path: Path
    manifest_path: Path
    summary_path: Path


def _utc_timestamp_token() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%S%z")


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "hd03"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _copy_template(src: Path, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    return dest


def _build_run_id(run_label: str | None) -> str:
    token = _utc_timestamp_token()
    if run_label:
        return f"hd03-{_slugify(run_label)}-{token}"
    return f"hd03-{token}"


def initialize_hd03_scaffold(root: Path, run_label: str | None = None) -> HD03ScaffoldPaths:
    run_id = _build_run_id(run_label)
    results_dir = root / "results" / "hd03"
    analysis_dir = root / "analysis" / "phase2_outputs"

    config_path = results_dir / f"{run_id}.inputs.json"
    manifest_path = results_dir / f"{run_id}.manifest.json"
    summary_path = analysis_dir / f"{run_id}.summary.csv"

    config_template = root / TEMPLATE_INPUT_CONFIG
    manifest_template = root / TEMPLATE_MANIFEST
    summary_template = root / TEMPLATE_SUMMARY

    config_payload = _read_json(config_template)
    config_payload["run_id"] = run_id
    config_payload["status"] = "scaffold_initialized"
    config_payload["linked_outputs"] = {
        "pilot_manifest": str(manifest_path.relative_to(root)),
        "summary_csv": str(summary_path.relative_to(root)),
    }
    _write_json(config_path, config_payload)

    manifest_payload = _read_json(manifest_template)
    manifest_payload["status"] = "scaffold_initialized"
    manifest_payload["run_id"] = run_id
    manifest_payload["linked_docs"]["input_config"] = str(config_path.relative_to(root))
    _write_json(manifest_path, manifest_payload)

    _copy_template(summary_template, summary_path)

    return HD03ScaffoldPaths(
        run_id=run_id,
        config_path=config_path,
        manifest_path=manifest_path,
        summary_path=summary_path,
    )


def _missing_hd03_inputs(payload: dict[str, Any]) -> list[str]:
    missing: list[str] = []

    human_inputs = payload.get("human_inputs", {})
    candidate_scales = human_inputs.get("candidate_scales", {})
    if not candidate_scales.get("tpch"):
        missing.append("human_inputs.candidate_scales.tpch")
    if not candidate_scales.get("tpcds"):
        missing.append("human_inputs.candidate_scales.tpcds")

    acceptance_rules = human_inputs.get("acceptance_rules", {})
    if not acceptance_rules.get("avoid_subsecond_noise_rule"):
        missing.append("human_inputs.acceptance_rules.avoid_subsecond_noise_rule")
    if not acceptance_rules.get("feasibility_rule"):
        missing.append("human_inputs.acceptance_rules.feasibility_rule")

    pilot_query_subset = human_inputs.get("pilot_query_subset", {})
    if not pilot_query_subset.get("tpch"):
        missing.append("human_inputs.pilot_query_subset.tpch")
    if not pilot_query_subset.get("tpcds"):
        missing.append("human_inputs.pilot_query_subset.tpcds")

    command_slots = payload.get("command_slots", {})
    for key in (
        "tpch_dataset_generation_command_template",
        "tpcds_dataset_generation_command_template",
        "postgres_load_command_template",
        "pilot_query_timing_command_template",
    ):
        value = command_slots.get(key, "")
        if not value or "<" in value or ">" in value:
            missing.append(f"command_slots.{key}")

    output_paths = payload.get("linked_outputs", {})
    if not output_paths.get("pilot_manifest"):
        missing.append("linked_outputs.pilot_manifest")
    if not output_paths.get("summary_csv"):
        missing.append("linked_outputs.summary_csv")

    return missing


def inspect_hd03_inputs(root: Path, config_path: Path) -> dict[str, Any]:
    payload = _read_json(config_path)
    missing = _missing_hd03_inputs(payload)
    return {
        "config_path": str(config_path if config_path.is_absolute() else config_path.relative_to(root)),
        "ready_for_real_pilot": not missing,
        "missing_inputs": missing,
        "run_id": payload.get("run_id"),
        "linked_outputs": payload.get("linked_outputs", {}),
    }

