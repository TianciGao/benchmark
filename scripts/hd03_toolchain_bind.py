from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BIN_DIR = ROOT / "tools" / "hd03" / "bin"


def _resolve_candidate(explicit: str | None, env_name: str, binary: str) -> Path | None:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        return path if path.exists() else None
    env_value = os.environ.get(env_name)
    if env_value:
        path = Path(env_value).expanduser().resolve()
        return path if path.exists() else None
    found = shutil.which(binary)
    return Path(found).resolve() if found else None


def _bind_tool(src: Path | None, target_name: str) -> tuple[bool, str]:
    if src is None:
        return False, "missing"
    BIN_DIR.mkdir(parents=True, exist_ok=True)
    target = BIN_DIR / target_name
    if target.exists() or target.is_symlink():
        target.unlink()
    target.symlink_to(src)
    return True, str(target)


def main() -> int:
    parser = argparse.ArgumentParser(description="Bind local HD-03 benchmark tools into tools/hd03/bin")
    parser.add_argument("--tpch-dbgen-bin", default=None)
    parser.add_argument("--tpcds-dsdgen-bin", default=None)
    args = parser.parse_args()

    dbgen_src = _resolve_candidate(args.tpch_dbgen_bin, "HD03_TPCH_DBGEN_BIN", "dbgen")
    dsdgen_src = _resolve_candidate(args.tpcds_dsdgen_bin, "HD03_TPCDS_DSDGEN_BIN", "dsdgen")

    ok_dbgen, dbgen_target = _bind_tool(dbgen_src, "dbgen")
    ok_dsdgen, dsdgen_target = _bind_tool(dsdgen_src, "dsdgen")

    print(f"[hd03-toolchain-bind] dbgen_source={dbgen_src}")
    print(f"[hd03-toolchain-bind] dsdgen_source={dsdgen_src}")
    print(f"[hd03-toolchain-bind] dbgen_bound={str(ok_dbgen).lower()} target={dbgen_target}")
    print(f"[hd03-toolchain-bind] dsdgen_bound={str(ok_dsdgen).lower()} target={dsdgen_target}")
    return 0 if ok_dbgen and ok_dsdgen else 2


if __name__ == "__main__":
    raise SystemExit(main())
