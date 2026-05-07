---
title: "T016 — Document idempotency invariants of install.sh + post-install state"
type: task
status: in-progress
priority: P1
parent_module: "root-ghostproxy-m003-foundation-hardening"
parent_epic: "sfif-rollout-and-second-brain-integration"
current_stage: document
readiness: 75
sfif_stage: Foundation
created: 2026-05-04
updated: 2026-05-05
sources:
  - id: parent-module
    type: wiki
    file: wiki/backlog/modules/root-ghostproxy-m003-foundation-hardening.md
tags: [task, p1, t016, foundation, idempotency, documentation, m003]
---

# T016 — Document idempotency invariants

## Description

Document explicitly what install.sh creates, overwrites, and leaves alone — and what re-running install.sh on an already-installed host does. Per TOOLS.md tool invariants section: every project-authored tool is idempotent.

## Done When

- [x] List of files install.sh CREATES (`~/.claude/settings.json`, `~/.claude/hooks/*` (18 .sh + integrity.py), `~/.claude/agents/*`, `~/.claude/modes/*`, `~/.claude/rules/*`, `~/.claude/commands/*`, `~/.claude/skills/*`, `~/.claude/integrity.json`, `~/.config/opencode/plugin/claude-bridge.ts`, `~/tools/*`, `/etc/systemd/network/30-ghostproxy-*` + `40-ghostproxy-*`, `/etc/wpa_supplicant/wpa_supplicant-mgmt0.conf`, `/etc/nftables.d/management-wifi-outbound-only.nft`) — **landed 2026-05-07 cron F46** in `TOOLS.md` install.sh per-tool reference, Idempotency invariants subsection.
- [x] List of files install.sh OVERWRITES on re-run when out-of-sync (with backup pattern: `<dest>.ghostproxy.bak.<UTC-timestamp>`) — landed 2026-05-07 cron F46 (TOOLS.md "Files install.sh OVERWRITES on re-run when out-of-sync" subsection).
- [x] List of files/dirs install.sh LEAVES UNTOUCHED (operator's `.bashrc`/`.profile`/`.bash_history`/`.gitconfig`/`.ssh/*`, `/home/*` other users, project work outside `.claude/` + `.config/opencode/` + `tools/`, `*.ghostproxy.bak.*` preserved, `/etc/systemd/network/*` non-prefixed, `/etc/nftables.d/*` non-`management-wifi-*`, `/etc/nftables.conf` body content) — landed 2026-05-07 cron F46.
- [x] Re-run behavior: re-running install.sh on a consistent host outputs `unchanged: <path>` per file; exit 0; no state mutation — landed 2026-05-07 cron F46 with empirical evidence cross-ref to F35+F46 `--check` runs (13/16 PASS, 3 wifi-credentials gated per CONTEXT.md).
- [x] Documentation: lives at TOOLS.md per-tool reference section per literal (chosen primary location).
- [ ] Verification: idempotency claim is testable — `./install.sh; ./install.sh` produces the same end state and the second run is a no-op. **Operator-empirical pending** — full real-execute on Debian 13 host = T012 last 2% (D024 GREENLIT, operator-driven future-session).

## Dependencies

- T012 (install.sh authored) — invariants document what it does

## Relationships

- PART OF: [[root-ghostproxy-m003-foundation-hardening|M003]]
- BLOCKED BY: T012
- ENABLES: clear contract for operator + future-session about install.sh behavior
