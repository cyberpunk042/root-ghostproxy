---
title: "T032 — Verify /root git state is clean (no uncommitted changes that would mix with --connect-project diff)"
type: task
status: not-started
priority: P0
parent_module: "root-ghostproxy-m006-pre-connect-verification"
parent_epic: "sfif-rollout-and-second-brain-integration"
current_stage: test
readiness: 0
sfif_stage: Stream-1-Pre-Connect
created: 2026-05-04
updated: 2026-05-05
sources:
  - id: parent-module
    type: wiki
    file: wiki/backlog/modules/root-ghostproxy-m006-pre-connect-verification.md
tags: [task, p0, t032, stream-1, pre-connect, git-state, m006]
---

# T032 — Verify clean git state at /root

## Description

`--connect-project` writes 4 artefacts to /root (.mcp.json + tools/gateway.py + tools/view.py + AGENTS.md `## Second Brain Connection` block). For the connect-script's mutations to be reviewable as a single atomic diff, /root must start in a clean working-tree state.

## Done When

- [ ] `cd /root && git status --porcelain` returns empty (no uncommitted changes, no untracked files in the whitelisted set).
- [ ] If the working tree is dirty: commit pending work or stash before running --connect-project.
- [ ] Capture HEAD commit SHA for the audit log (so the connect-script's mutations diff cleanly from this baseline).

## Dependencies

- /root is git-init'd (per the deny-all + whitelist `.gitignore` invariant).

## Relationships

- PART OF: [[root-ghostproxy-m006-pre-connect-verification|M006]]
- BLOCKS: T037 (audit log), T038 (M007 connect)
