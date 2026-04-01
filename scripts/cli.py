from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.hd03_pilot import initialize_hd03_scaffold, inspect_hd03_inputs
from scripts.hd03_toolchain import inspect_hd03_toolchain
from scripts.manifest_loader import load_case_manifest
from scripts.postgres_runner import PostgresRunner, write_environment_report
from scripts.smoke import run_smoke

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DIRS = [
    "cases",
    "packs",
    "systems",
    "verifiers",
    "engines",
    "policies",
    "results",
    "analysis",
    "docs",
    "scripts",
    "skills",
]


def _print_placeholder(target: str, todo: str) -> int:
    print(f"[{target}] placeholder target")
    print(f"[{target}] TODO: {todo}")
    return 0


def command_setup(_: argparse.Namespace) -> int:
    for name in REQUIRED_DIRS:
        path = ROOT / name
        path.mkdir(parents=True, exist_ok=True)
        print(f"[setup] ensured {path}")
    print("[setup] phase boundary intact: Phase 0/1 bootstrap only")
    return 0


def command_smoke(_: argparse.Namespace) -> int:
    return run_smoke(root=ROOT, mode="raw_output", policy=None)


def command_pack_freeze(_: argparse.Namespace) -> int:
    return _print_placeholder(
        target="pack-freeze",
        todo="Phase 2 is not started. No official pack membership freeze is performed by this bootstrap.",
    )


def command_eval_raw(_: argparse.Namespace) -> int:
    return run_smoke(root=ROOT, mode="raw_output", policy=None)


def command_eval_deploy(args: argparse.Namespace) -> int:
    return run_smoke(root=ROOT, mode="deployment_utility", policy=args.policy)


def command_verify_cases(_: argparse.Namespace) -> int:
    cases_root = ROOT / "cases"
    checked = 0
    for case_dir in sorted(path for path in cases_root.iterdir() if path.is_dir()):
        if not (case_dir / "manifest.yaml").exists():
            continue
        load_case_manifest(case_dir)
        checked += 1
        print(f"[verify-cases] ok {case_dir.name}")
    print(f"[verify-cases] checked={checked}")
    return 0


def command_tables(_: argparse.Namespace) -> int:
    return _print_placeholder(
        target="tables",
        todo="Wire normalized results into Phase 6 paper tables after Phase 2-5 artifacts exist.",
    )


def command_figures(_: argparse.Namespace) -> int:
    return _print_placeholder(
        target="figures",
        todo="Wire normalized results into Phase 6 figures after Phase 2-5 artifacts exist.",
    )


def command_postgres_env_check(_: argparse.Namespace) -> int:
    runner = PostgresRunner()
    report = runner.probe_environment(refresh=True)
    path = write_environment_report(ROOT, report, label="postgres-env-check")
    print(f"[postgres-env-check] report={path}")
    print(f"[postgres-env-check] readiness_status={report.readiness_status}")
    print(f"[postgres-env-check] phase1_status={report.phase1_status}")
    print(
        "[postgres-env-check] blockers="
        f"{json.dumps(report.blockers, ensure_ascii=False)}"
    )
    return 0


def command_artifact_preflight(_: argparse.Namespace) -> int:
    missing = [name for name in REQUIRED_DIRS if not (ROOT / name).exists()]
    required_docs = [
        ROOT / "docs" / "PHASE0_BOOTSTRAP_REPORT.md",
        ROOT / "docs" / "PHASE1_EXIT_CRITERIA.md",
        ROOT / "docs" / "ENVIRONMENT_READINESS.md",
        ROOT / "docs" / "OPEN_DECISIONS_STATUS.md",
        ROOT / "docs" / "POSTGRES_SETUP_CHECKLIST.md",
        ROOT / "docs" / "PHASE1_EXIT_REPORT_TEMPLATE.md",
        ROOT / "docs" / "GIT_WORKTREE_SETUP.md",
        ROOT / "docs" / "RESULT_SCHEMA.md",
        ROOT / "docs" / "REPO_LAYOUT.md",
        ROOT / "Makefile",
    ]
    missing_docs = [str(path.relative_to(ROOT)) for path in required_docs if not path.exists()]
    if missing or missing_docs:
        print(f"[artifact-preflight] missing_dirs={missing}")
        print(f"[artifact-preflight] missing_files={missing_docs}")
        return 1
    print("[artifact-preflight] bootstrap files present")
    print("[artifact-preflight] TODO: add full artifact completeness checks in later phases")
    return 0


def command_hd03_pilot_init(args: argparse.Namespace) -> int:
    scaffold = initialize_hd03_scaffold(root=ROOT, run_label=args.run_label)
    print(f"[hd03-pilot-init] run_id={scaffold.run_id}")
    print(f"[hd03-pilot-init] config={scaffold.config_path}")
    print(f"[hd03-pilot-init] manifest={scaffold.manifest_path}")
    print(f"[hd03-pilot-init] summary={scaffold.summary_path}")
    print("[hd03-pilot-init] real pilot work not started")
    return 0


def command_hd03_pilot_check_inputs(args: argparse.Namespace) -> int:
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    report = inspect_hd03_inputs(root=ROOT, config_path=config_path)
    print(f"[hd03-pilot-check-inputs] run_id={report['run_id']}")
    print(f"[hd03-pilot-check-inputs] config={report['config_path']}")
    print(f"[hd03-pilot-check-inputs] ready_for_real_pilot={str(report['ready_for_real_pilot']).lower()}")
    print(
        "[hd03-pilot-check-inputs] missing_inputs="
        f"{json.dumps(report['missing_inputs'], ensure_ascii=False)}"
    )
    print(
        "[hd03-pilot-check-inputs] linked_outputs="
        f"{json.dumps(report['linked_outputs'], ensure_ascii=False)}"
    )
    return 0 if report["ready_for_real_pilot"] else 2


def command_hd03_pilot_toolchain_check(args: argparse.Namespace) -> int:
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    report = inspect_hd03_toolchain(root=ROOT, config_path=config_path)
    print(f"[hd03-pilot-toolchain-check] config={report['config_path']}")
    print(
        "[hd03-pilot-toolchain-check] readiness="
        f"input_complete={str(report['input_completeness_ready']).lower()} "
        f"command_slots_concretized={str(report['command_slot_concretized']).lower()} "
        f"pilot_executable={str(report['pilot_executable']).lower()}"
    )
    print(
        "[hd03-pilot-toolchain-check] resolved_tools="
        f"{json.dumps(report['resolved_tools'], ensure_ascii=False)}"
    )
    print(
        "[hd03-pilot-toolchain-check] pg_environment_present="
        f"{json.dumps(report['pg_environment_present'], ensure_ascii=False)}"
    )
    print(
        "[hd03-pilot-toolchain-check] missing_components="
        f"{json.dumps(report['missing_components'], ensure_ascii=False)}"
    )
    print(
        "[hd03-pilot-toolchain-check] actual_pilot_blockers="
        f"{json.dumps(report['actual_pilot_blockers'], ensure_ascii=False)}"
    )
    return 0 if report["pilot_executable"] else 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="VLDB EA&B harness bootstrap CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    command_map = {
        "setup": command_setup,
        "smoke": command_smoke,
        "pack-freeze": command_pack_freeze,
        "eval-raw": command_eval_raw,
        "eval-deploy": command_eval_deploy,
        "verify-cases": command_verify_cases,
        "tables": command_tables,
        "figures": command_figures,
        "postgres-env-check": command_postgres_env_check,
        "artifact-preflight": command_artifact_preflight,
        "hd03-pilot-init": command_hd03_pilot_init,
        "hd03-pilot-check-inputs": command_hd03_pilot_check_inputs,
        "hd03-pilot-toolchain-check": command_hd03_pilot_toolchain_check,
    }

    for name in command_map:
        subparser = subparsers.add_parser(name)
        subparser.set_defaults(handler=command_map[name])

    subparsers.choices["eval-deploy"].add_argument(
        "--policy",
        choices=["conservative", "practical"],
        default="conservative",
        help="Deployment policy for the smoke fixture",
    )
    subparsers.choices["hd03-pilot-init"].add_argument(
        "--run-label",
        default=None,
        help="Optional human-readable label for the scaffolded HD-03 run",
    )
    subparsers.choices["hd03-pilot-check-inputs"].add_argument(
        "--config",
        required=True,
        help="Path to a scaffolded HD-03 input config JSON",
    )
    subparsers.choices["hd03-pilot-toolchain-check"].add_argument(
        "--config",
        required=True,
        help="Path to a populated HD-03 input config JSON",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
