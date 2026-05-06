---
title: "T012 — Author /root/install.sh (idempotent, --dry-run, --check, --dest)"
type: task
status: in-progress
priority: P0
parent_module: "root-ghostproxy-m003-foundation-hardening"
parent_epic: "sfif-rollout-and-second-brain-integration"
current_stage: implement
readiness: 80
sfif_stage: Foundation
created: 2026-05-04
updated: 2026-05-05
sources:
  - id: parent-module
    type: wiki
    file: wiki/backlog/modules/root-ghostproxy-m003-foundation-hardening.md
  - id: tools-md
    type: wiki
    file: TOOLS.md
    description: "Planned install.sh invocations + invariants (idempotency, --dry-run support, exit codes, backups)"
tags: [task, p0, t012, foundation, install-sh, scaffold, m003]
---

# T012 — Author /root/install.sh

## Description

Author the foundation's idempotent installer. Takes a fresh Linux host (target: Debian 13) and brings it to foundation-tier root-ghostproxy state: endpoint AI agent safety policy installed at `~/.claude/`, bridge topology configured, management wifi configured, opencode bridge plugin installed.

## Done When

**Scaffold-stage (cycle 23 — partial):**
- [x] `/root/install.sh` exists, executable (`chmod 0755`) — greenfield authored cycle 23
- [x] `./install.sh --dry-run` previews; no state changes — STUBS list operations
- [x] `./install.sh --help` prints usage + all flags
- [x] `./install.sh --version` prints version
- [x] `./install.sh --check` mode wired (read-only stub)
- [x] `./install.sh --dest <path>` flag wired
- [x] Out-of-sync backup helper `backup_if_exists()` defined
- [x] Exit codes documented in --help (0/1/2/3/4 with semantics)
- [x] Prior `/root/install.sh` debris backed up to `install.sh.prior-debris.bak.<UTC-ts>` before greenfield overwrite (per T011 + T006 decisions)
- [x] Greenfield framing in file header explicitly cites T011 + T006 decisions

**Implement-stage (pending — requires operator approval to advance):**
- [ ] STUB: Debian 13 verification (`/etc/os-release VERSION_ID=13`)
- [ ] STUB: dependency check (python3, jq, nft, brctl/ip-link, wpa_supplicant)
- [ ] STUB: deploy `~/.claude/settings.json` + hook scripts
- [ ] STUB: deploy opencode bridge plugin (`~/.config/opencode/`)
- [ ] STUB: configure network bridge (ifupdown/netplan/systemd-networkd — operator-chosen)
- [ ] STUB: configure nftables rules (INPUT/FORWARD/OUTPUT)
- [ ] STUB: configure management wifi (outbound-only)
- [ ] STUB: integrity sentinel registration
- [ ] STUB: post-install verification
- [ ] Idempotency invariant: re-run = no-op when state matches (T016 covers)
- [ ] `bash -n install.sh` passes ✓ (verified cycle 23)
- [ ] `shellcheck install.sh` passes (TBD; not yet run)

## Dependencies

- T011 (greenfield vs extend decision) — gates the authoring approach.
- T006 (prior debris reconciliation) — informs whether the prior `/root/install.sh` is touchable as a starting point.
- T008 (CLAUDE.md methodology section already references install.sh's planned invocations — per Adoption Guide) ✓

## Stage-gate (Implement)

Per CLAUDE.md methodology section: stage `implement` requires the code compiles + lint passes + ≥1 existing file imports new code. For shell scripts: `bash -n install.sh` parses cleanly; `shellcheck install.sh` passes (or operator-set baseline); CLAUDE.md routing references install.sh.

## Relationships

- PART OF: [[root-ghostproxy-m003-foundation-hardening|M003]]
- BLOCKED BY: T011
- RELATES TO: [[T006-prior-debris-reconciliation|T006]]
- BLOCKS: T015 (post-install verification), T017 (foundation gate verification)
