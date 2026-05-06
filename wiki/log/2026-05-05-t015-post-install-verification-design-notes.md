---
title: "2026-05-05 — T015 design notes: post-install verification scope (what --check actually checks)"
type: log
domain: cross-domain
status: draft
confidence: medium
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: t015
    type: wiki
    file: wiki/backlog/tasks/T015-author-post-install-verification.md
  - id: t012
    type: wiki
    file: wiki/backlog/tasks/T012-author-install-sh.md
tags: [log, design-notes, t015, m003, post-install-verification, scaffold-stage]
---

# T015 — Post-install verification design notes (cycle 32 preliminary)

## Where verification lives

T015 says it could be `install.sh --check`, OR a separate `verify-foundation.sh`, OR `tools/verify-policy.py` from M004 (operator-decision pending).

**Recommend**: keep `--check` IN install.sh as the authoritative entry point + delegate per-aspect to small helpers. Single command-surface for operators ("re-run install.sh --check"); verification per-op is composable. M004's `tools/verify-policy.py` (Python) becomes optional richer mode.

## What --check verifies (per Done When)

For each operation install.sh installed (gated by profile + mode):

### endpoint safety policy (op 1)
- `~/.claude/settings.json` exists + is valid JSON + has `permissions.deny` array + has `hooks` object
- `~/.claude/hooks/{policy-block, malware-block, leak-detector, opt-write-block, session-orient, post-compact, session-start, session-summary}.sh` exist + executable + Python-shebang
- `bash -n ~/.claude/hooks/<each>.sh` parses cleanly
- No file matches `<path>.ghostproxy.bak.*` newer than the live file (drift indicator)

### opencode bridge (op 2)
- `~/.config/opencode/opencode.json` exists + valid JSON
- `~/.config/opencode/plugin/{claude-bridge.ts, package.json}` exist
- `opencode debug config | grep claude-bridge` non-empty (when opencode CLI installed)

### network bridge (op 3, when mode includes bridge)
- `/etc/systemd/network/{30-ghostproxy-bridge.netdev, 30-ghostproxy-bridge.network, 40-ghostproxy-bridge-members.network}` exist
- `networkctl list | grep gpbr0` shows bridge UP
- `ip link show gpbr0` reports state UP
- `bridge link` shows ≥2 member interfaces enslaved
- `ip addr show gpbr0` confirms NO IP assigned (passive L2)

### management wifi (op 4)
- wpa_supplicant config present
- nftables INPUT rules drop everything except established/related on the wifi interface

### integrity sentinel (op 5)
- Baseline JSON file exists
- Re-computing checksums of safety-policy artefacts matches baseline
- Operator-protected files unchanged since last sentinel write

## Exit codes

- 0 = all sub-checks pass
- 3 = at least one sub-check fails — output names the specific failure(s) per op

## Stage classification

T015 is in `test` stage of methodology — verification IS the test artefact. Stage-gate: T015 done when --check returns 0 on a real (non-dry-run) install.

## Cross-references

- T012 install.sh (this verification runs against the install)
- T017 foundation gate (compose: T015 verifier passes + T011/T013/T014 done = M003 gate clear)
- M004 tools/verify-policy.py (richer Python verifier; orthogonal to --check)
