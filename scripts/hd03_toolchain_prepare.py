from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / "tools" / "hd03"
VENDOR_DIR = TOOLS_DIR / "vendor"
VENDOR_SRC_DIR = VENDOR_DIR / "src"
VENDOR_BIN_DIR = VENDOR_DIR / "bin"


def _source_tree(name: str) -> Path:
    mapping = {
        "tpch": VENDOR_SRC_DIR / "tpch-dbgen",
        "tpcds": VENDOR_SRC_DIR / "tpcds-kit",
    }
    return mapping[name]


def _default_build_commands(name: str, src: Path) -> list[list[str]]:
    if name == "tpch":
        return [
            ["make", "-C", str(src)],
        ]
    return [
        ["make", "-C", str(src)],
    ]


def _candidate_binary_paths(name: str, src: Path) -> list[Path]:
    if name == "tpch":
        return [
            src / "dbgen",
            src / "build" / "dbgen",
            VENDOR_BIN_DIR / "dbgen",
        ]
    return [
        src / "dsdgen",
        src / "tools" / "dsdgen",
        src / "build" / "dsdgen",
        VENDOR_BIN_DIR / "dsdgen",
    ]


def _run_command(command: list[str], execute: bool) -> int:
    print(f"[hd03-toolchain-prepare] command={command}")
    if not execute:
        print("[hd03-toolchain-prepare] dry_run_only=true")
        return 0
    completed = subprocess.run(command, check=False, env=dict(os.environ))
    return completed.returncode


def _prepare_one(name: str, execute: bool) -> int:
    src = _source_tree(name)
    binary = "dbgen" if name == "tpch" else "dsdgen"
    print(f"[hd03-toolchain-prepare] benchmark={name}")
    print(f"[hd03-toolchain-prepare] source_tree={src}")

    if not src.exists():
        print(f"[hd03-toolchain-prepare] source_tree_present=false")
        return 2
    print(f"[hd03-toolchain-prepare] source_tree_present=true")

    build_commands = _default_build_commands(name, src)
    status = 0
    for command in build_commands:
        rc = _run_command(command, execute=execute)
        if rc != 0:
            status = rc
            break

    candidates = [str(path) for path in _candidate_binary_paths(name, src)]
    found = next((path for path in _candidate_binary_paths(name, src) if path.exists()), None)
    print(f"[hd03-toolchain-prepare] binary_candidates={candidates}")
    print(f"[hd03-toolchain-prepare] resolved_binary={found}")

    if status != 0:
        return status
    return 0 if found else 3


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare local HD-03 benchmark generators from staged vendor source trees")
    parser.add_argument("--benchmark", choices=["tpch", "tpcds", "all"], default="all")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    selected = ["tpch", "tpcds"] if args.benchmark == "all" else [args.benchmark]
    final_rc = 0
    for name in selected:
        rc = _prepare_one(name, execute=args.execute)
        if rc != 0:
            final_rc = rc
    return final_rc


if __name__ == "__main__":
    raise SystemExit(main())
