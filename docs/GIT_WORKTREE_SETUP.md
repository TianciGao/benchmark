# Git Worktree Setup

Current repository status:

- this workspace is **not** currently inside a git worktree

This means the project cannot yet fully satisfy the `one task, one branch/worktree` discipline from the frozen protocol.

## Minimal Local Setup

Do **not** create a remote repository unless humans ask for it.

Local-only setup steps:

```powershell
git init
git add .
git commit -m "Bootstrap Phase 1 harness skeleton"
```

## One Task, One Branch / Worktree

Recommended pattern after local initialization:

```powershell
git checkout -b phase1-exit-readiness
git worktree add ..\\Benchmark4VLDB-phase1 phase1-exit-readiness
```

Or, for later tasks:

```powershell
git checkout -b adapter-s1
git worktree add ..\\Benchmark4VLDB-adapter-s1 adapter-s1
```

## Branch Naming Guidance

- `phase1-exit-readiness`
- `adapter-s1`
- `verifier-v1`
- `analysis-rq1`

Keep protocol work, workload curation, adapter work, and analysis work in separate branches/worktrees.

## Validation

After local setup:

```powershell
git rev-parse --is-inside-work-tree
git branch --show-current
git worktree list
```

## Protocol Statement

`protocol changed: no`
