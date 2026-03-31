# Practical Policy

Frozen policy summary:

- Apply only if verdict is `Proved` or `TestPassed`
- Candidate median speedup must be at least `1.05x`

Phase 1 note:

- The bootstrap smoke path uses a single-sample approximation only to wire the harness.
- Main-policy calibration loops remain TODO for later phases.
