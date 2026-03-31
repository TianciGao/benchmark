from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Optional

OFFICIAL_VERDICTS = {
    "Invalid",
    "NonExecutable",
    "Disproved",
    "Proved",
    "TestPassed",
    "Unknown",
}

OFFICIAL_MODES = {
    "raw_output",
    "deployment_utility",
}

OFFICIAL_UNIVERSES = {
    "compatibility_subset",
    "full_subset",
}

OFFICIAL_POLICIES = {
    "conservative",
    "practical",
}


@dataclass
class NormalizedResultRecord:
    run_id: str
    case_id: str
    system_id: str
    system_family: str
    mode: str
    universe: str
    policy: Optional[str]
    original_sql_hash: str
    rewrite_sql: str
    rewrite_sql_hash: str
    parse_status: str
    exec_status: str
    verdict: str
    evidence_trace_path: Optional[str]
    baseline_runtime_samples: list[float]
    candidate_runtime_samples: list[float]
    final_runtime_samples: list[float]
    decision: str
    engine_version: str
    stats_snapshot_id: str
    seed: int
    timestamp: str
    notes: str

    def validate(self) -> None:
        if self.mode not in OFFICIAL_MODES:
            raise ValueError(f"Unsupported mode: {self.mode}")
        if self.universe not in OFFICIAL_UNIVERSES:
            raise ValueError(f"Unsupported universe: {self.universe}")
        if self.policy is not None and self.policy not in OFFICIAL_POLICIES:
            raise ValueError(f"Unsupported policy: {self.policy}")
        if self.verdict not in OFFICIAL_VERDICTS:
            raise ValueError(f"Unsupported verdict: {self.verdict}")

    def to_dict(self) -> dict:
        self.validate()
        return asdict(self)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_jsonl(path: Path, records: Iterable[NormalizedResultRecord]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")
    return path
