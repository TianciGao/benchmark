# Conservative Policy

Frozen policy summary:

- Apply only if verdict is `Proved`
- Candidate median speedup must be at least `1.10x`
- No calibration run may exceed `1.02x` of baseline median

Phase 1 note:

- The bootstrap smoke path uses a single-sample approximation only to wire the harness.
- Main-policy calibration loops remain TODO for later phases.
