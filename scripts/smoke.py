from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from policies.deployment import decide_policy
from scripts.manifest_loader import load_case_manifest, load_pack_manifest
from scripts.postgres_runner import PostgresRunner, write_environment_report
from scripts.result_schema import NormalizedResultRecord, sha256_text, write_jsonl
from systems.s0_native.adapter import S0NativeAdapter


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _compare_outputs(original_stdout: str, rewrite_stdout: str) -> tuple[str, str]:
    if not original_stdout:
        return "NonExecutable", "Original query returned no output in smoke mode"
    if original_stdout == rewrite_stdout:
        return "TestPassed", "Smoke comparator observed byte-identical stdout"
    return "Disproved", "Smoke comparator observed output mismatch"


def run_smoke(root: Path, mode: str, policy: str | None) -> int:
    adapter = S0NativeAdapter()
    runner = PostgresRunner()
    pack_manifest = load_pack_manifest(root / "packs" / "anchor" / "tiny_smoke.yaml")
    env_report = runner.probe_environment(refresh=True)

    timestamp = _utc_timestamp()
    run_id = f"smoke-{mode}-{timestamp.replace(':', '').replace('+00:00', 'z')}"
    results_dir = root / "results" / "smoke"
    evidence_dir = results_dir / "evidence"
    env_report_path = write_environment_report(root, env_report, label=f"postgres-env-check-{mode}")
    records: list[NormalizedResultRecord] = []
    run_notes: list[str] = [
        "Phase 1 smoke-only fixture",
        "Not an official frozen pack membership file",
        env_report.phase1_status,
    ]

    for case_id in pack_manifest["cases"]:
        case_dir = root / "cases" / case_id
        manifest = load_case_manifest(case_dir)
        original_sql = (case_dir / "original.sql").read_text(encoding="utf-8").strip()
        raw_output = adapter.generate_rewrite(case_id=case_id, sql=original_sql, config={})
        normalized = adapter.normalize_output(raw_output)
        rewrite_sql = normalized["rewrite_sql"]
        available, availability_reason = runner.availability()

        evidence_payload: dict = {
            "case_id": case_id,
            "mode": mode,
            "policy": policy,
            "runner_availability": availability_reason,
            "environment_report_path": str(env_report_path.relative_to(root)),
            "environment_readiness_status": env_report.readiness_status,
            "phase1_status": env_report.phase1_status,
            "minimal_connection_test_commands": env_report.minimal_connection_test_commands,
            "recommended_next_steps": env_report.recommended_next_steps,
        }

        if not available:
            verdict = "NonExecutable"
            decision = "fallback_original" if mode == "deployment_utility" else "not_applicable"
            exec_status = "engine_unavailable" if not env_report.psql_found else "connection_unavailable"
            baseline_samples: list[float] = []
            candidate_samples: list[float] = []
            final_samples: list[float] = []
            evidence_payload["blocked"] = True
            evidence_payload["blocker"] = availability_reason
            notes = (
                "Smoke path blocked before SQL execution. "
                f"Reason: {availability_reason}. {env_report.phase1_status}."
            )
        else:
            baseline_result = runner.execute(original_sql)
            candidate_result = runner.execute(rewrite_sql)
            verdict, verdict_reason = _compare_outputs(
                original_stdout=baseline_result.stdout,
                rewrite_stdout=candidate_result.stdout,
            )
            exec_status = candidate_result.exec_status
            baseline_samples = (
                [baseline_result.runtime_ms] if baseline_result.runtime_ms is not None else []
            )
            candidate_samples = (
                [candidate_result.runtime_ms] if candidate_result.runtime_ms is not None else []
            )

            if mode == "deployment_utility":
                baseline_ms = baseline_samples[0] if baseline_samples else None
                candidate_ms = candidate_samples[0] if candidate_samples else None
                decision = decide_policy(
                    policy=policy or "conservative",
                    verdict=verdict,
                    baseline_median_ms=baseline_ms,
                    candidate_samples_ms=candidate_samples,
                )
                final_sql = rewrite_sql if decision == "apply_candidate" else original_sql
            else:
                decision = "not_applicable"
                final_sql = rewrite_sql

            final_result = runner.execute(final_sql)
            final_samples = [final_result.runtime_ms] if final_result.runtime_ms is not None else []
            if not baseline_result.ok or not candidate_result.ok or not final_result.ok:
                verdict = "NonExecutable"
                decision = "fallback_original" if mode == "deployment_utility" else "not_applicable"
                exec_status = "execution_error"

            evidence_payload.update(
                {
                    "blocked": False,
                    "verdict_reason": verdict_reason,
                    "baseline_stdout": baseline_result.stdout,
                    "candidate_stdout": candidate_result.stdout,
                    "final_stdout": final_result.stdout,
                    "baseline_stderr": baseline_result.stderr,
                    "candidate_stderr": candidate_result.stderr,
                    "final_stderr": final_result.stderr,
                    "decision": decision,
                }
            )
            notes = (
                "Single-sample smoke execution only; not the frozen runtime protocol for main experiments. "
                f"{env_report.phase1_status}."
            )

        evidence_path = _write_json(
            evidence_dir / f"{case_id}.{mode}.{policy or 'none'}.json",
            evidence_payload,
        )
        records.append(
            NormalizedResultRecord(
                run_id=run_id,
                case_id=case_id,
                system_id=adapter.system_id,
                system_family=adapter.system_family,
                mode=mode,
                universe="compatibility_subset",
                policy=policy,
                original_sql_hash=sha256_text(original_sql),
                rewrite_sql=rewrite_sql,
                rewrite_sql_hash=sha256_text(rewrite_sql),
                parse_status="ok",
                exec_status=exec_status,
                verdict=verdict,
                evidence_trace_path=str(evidence_path.relative_to(root)),
                baseline_runtime_samples=baseline_samples,
                candidate_runtime_samples=candidate_samples,
                final_runtime_samples=final_samples,
                decision=decision,
                engine_version=runner.engine_version(),
                stats_snapshot_id=manifest["stats_snapshot_id"],
                seed=0,
                timestamp=timestamp,
                notes=notes,
            )
        )

    results_path = write_jsonl(results_dir / f"{run_id}.jsonl", records)
    manifest_payload = {
        "run_id": run_id,
        "timestamp": timestamp,
        "mode": mode,
        "policy": policy,
        "system_id": adapter.system_id,
        "system_family": adapter.system_family,
        "pack_fixture": "packs/anchor/tiny_smoke.yaml",
        "environment_report_path": str(env_report_path.relative_to(root)),
        "environment_readiness_status": env_report.readiness_status,
        "phase1_status": env_report.phase1_status,
        "records_path": str(results_path.relative_to(root)),
        "case_count": len(records),
        "notes": run_notes,
    }
    _write_json(results_dir / f"{run_id}.manifest.json", manifest_payload)
    print(f"[smoke] wrote normalized results to {results_path}")
    print(f"[smoke] environment report: {env_report_path}")
    print(f"[smoke] phase1_status={env_report.phase1_status}")
    print(f"[smoke] run_id={run_id} mode={mode} policy={policy or 'none'} cases={len(records)}")
    return 0
