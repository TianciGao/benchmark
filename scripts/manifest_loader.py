from __future__ import annotations

import json
from pathlib import Path

CASE_REQUIRED_FILES = [
    "original.sql",
    "manifest.yaml",
    "semantic_contract.yaml",
    "provenance.md",
    "risk_tags.yaml",
    "adjudication_log.md",
    "validation_assets",
]

MANIFEST_REQUIRED_FIELDS = [
    "case_id",
    "pack_id",
    "source",
    "dbms",
    "schema_version",
    "data_snapshot_id",
    "stats_snapshot_id",
    "query_features",
    "comparison_semantics",
    "exclusion_notes",
    "owner",
    "freeze_status",
]


def load_yaml_like(path: Path) -> dict:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"File is empty: {path}")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{path} is not JSON-subset YAML. Phase 1 skeleton intentionally supports "
            "JSON-compatible YAML only; extend loader before Phase 2."
        ) from exc
    if not isinstance(payload, dict):
        raise ValueError(f"Expected a mapping in {path}")
    return payload


def validate_case_assets(case_dir: Path) -> list[str]:
    missing: list[str] = []
    for name in CASE_REQUIRED_FILES:
        if not (case_dir / name).exists():
            missing.append(name)
    return missing


def load_case_manifest(case_dir: Path) -> dict:
    missing = validate_case_assets(case_dir)
    if missing:
        raise FileNotFoundError(f"Case assets missing for {case_dir.name}: {missing}")
    manifest = load_yaml_like(case_dir / "manifest.yaml")
    missing_fields = [field for field in MANIFEST_REQUIRED_FIELDS if field not in manifest]
    if missing_fields:
        raise ValueError(
            f"Manifest {case_dir / 'manifest.yaml'} missing required fields: {missing_fields}"
        )
    return manifest


def load_pack_manifest(path: Path) -> dict:
    manifest = load_yaml_like(path)
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError(f"Pack manifest {path} must contain a non-empty 'cases' list")
    return manifest
