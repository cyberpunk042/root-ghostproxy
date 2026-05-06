---
title: "2026-05-05 — T016 idempotency invariants for /root/install.sh (preliminary doc)"
type: log
domain: cross-domain
status: draft
confidence: medium
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: t016
    type: wiki
    file: wiki/backlog/tasks/T016-document-idempotency-invariants.md
  - id: t012
    type: wiki
    file: wiki/backlog/tasks/T012-author-install-sh.md
tags: [log, design-notes, t016, m003, idempotency, scaffold-stage]
---

# T016 — Idempotency invariants for install.sh (cycle 32 preliminary)

## What idempotency means here

Re-running `install.sh` on an already-installed host MUST be a no-op (or cleanly apply any drift). Specifically:

1. **Same input → same output**: install.sh with same flags produces same target state regardless of prior state.
2. **Re-run safe**: invoking install.sh twice doesn't double-apply or break.
3. **Drift-resilient**: if files have drifted from spec, install.sh detects + corrects + reports.
4. **Backup-on-change**: never silent overwrite — any change to a pre-existing file produces a `.ghostproxy.bak.<UTC-ts>` backup.

## Per-operation idempotency invariants

### File deployments (ops 1, 2, 3)
- `install_file(src, dst)` checks: if dst doesn't exist → install fresh; if dst matches src → "unchanged" (no-op); if dst differs → backup + overwrite.
- This is already in place in install.sh from cycle 27 forward.

### Directory creation (`mkdir -p`)
- Already idempotent by `mkdir -p` semantics.

### Permissions (`chmod`)
- chmod is idempotent: setting 0644 on a file already 0644 = no-op.

### systemd-networkd reload (op 3)
- `networkctl reload` is idempotent: applies new config files; no-op if config matches running state.
- `networkctl up gpbr0` is idempotent: brings bridge up if not already up.

### nftables rules (op 3 + op 4)
- Trickier: `nft add rule` is NOT idempotent — adding the same rule twice creates duplicates.
- Pattern: use `nft -f /etc/nftables-ghostproxy.conf` (declarative file); `nft flush ruleset` first if needed.
- Or: nft `flush table ghostproxy` then re-add — still net-idempotent if the table contains exactly the spec rules.

### Integrity sentinel (op 5)
- Baseline JSON write is idempotent: same content → same hash → no actual change.
- Re-running `--check` against an unchanged baseline returns 0.

## Cross-cutting invariants

- **No-prompts default**: install.sh never prompts unless --interactive profile or operator-input-required. Idempotent re-run must be silent-success.
- **Atomic per-op**: each op_install_X function either fully succeeds or backs out cleanly. No half-applied state.
- **--dry-run is pure**: --dry-run NEVER mutates state. Always idempotent (no-ops).
- **Exit code 0 on no-op**: re-run on already-installed = exit 0, "all unchanged" output.

## What's NOT idempotent (caveat)

- Backups themselves: each install run produces NEW timestamped backups if files differ. The TIMESTAMP changes per run. This is intentional — backups are append-only history.
- Logs: each run writes new log entries. Append-only.

## Verification pattern (composes with T015)

`install.sh --check` returns 0 iff `install.sh` (no --check flag) would produce zero changes if invoked. That's the strongest idempotency test.

## Stage classification

T016 is `document` stage — this design doc is the artefact. T016 done when this doc exists + operator reviews + invariants encoded as comments in install.sh.

## Cross-references

- T012 install.sh (uses the install_file idempotent helper)
- T015 post-install verify (runs the idempotency check test)
- T017 foundation gate (idempotent re-run is part of gate)
