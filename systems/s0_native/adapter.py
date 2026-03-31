from __future__ import annotations


class S0NativeAdapter:
    system_id = "s0_native"
    system_family = "S0"

    def prepare_case(self, case_id: str) -> dict:
        return {
            "case_id": case_id,
            "strategy": "native_optimizer_no_rewrite",
        }

    def generate_rewrite(self, case_id: str, sql: str, config: dict | None = None) -> dict:
        _ = self.prepare_case(case_id)
        return {
            "case_id": case_id,
            "rewrite_sql": sql,
            "metadata": {
                "system_id": self.system_id,
                "system_family": self.system_family,
                "strategy": "native_optimizer_no_rewrite",
                "config": config or {},
            },
        }

    def normalize_output(self, raw_output: dict) -> dict:
        return {
            "rewrite_sql": raw_output["rewrite_sql"],
            "metadata": raw_output["metadata"],
        }

    def emit_metadata(self) -> dict:
        return {
            "system_id": self.system_id,
            "system_family": self.system_family,
            "description": "Frozen S0 baseline: PostgreSQL native optimizer without rewrite",
        }
