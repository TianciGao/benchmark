from __future__ import annotations

from statistics import median


def decide_policy(
    policy: str,
    verdict: str,
    baseline_median_ms: float | None,
    candidate_samples_ms: list[float],
) -> str:
    if baseline_median_ms is None or not candidate_samples_ms:
        return "fallback_original"

    candidate_median_ms = median(candidate_samples_ms)
    if candidate_median_ms <= 0:
        return "fallback_original"

    speedup = baseline_median_ms / candidate_median_ms

    if verdict == "Unknown":
        return "fallback_original"

    if policy == "conservative":
        if verdict != "Proved":
            return "fallback_original"
        if speedup < 1.10:
            return "fallback_original"
        if any(sample > 1.02 * baseline_median_ms for sample in candidate_samples_ms):
            return "fallback_original"
        return "apply_candidate"

    if policy == "practical":
        if verdict not in {"Proved", "TestPassed"}:
            return "fallback_original"
        if speedup < 1.05:
            return "fallback_original"
        return "apply_candidate"

    raise ValueError(f"Unsupported policy: {policy}")
