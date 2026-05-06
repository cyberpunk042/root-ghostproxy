---
title: "2026-05-05 — Operator directive: install.sh assumptions too narrow (not only Debian 13; not only root user; not always bridge; etc.)"
type: log
domain: cross-domain
status: active
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-install-sh-too-narrow-assumptions
    type: directive
tags: [log, operator-directive, sacrosanct, verbatim, install-sh, scope-broadening, multi-os, multi-user, optional-bridge, install-profiles, sb-073]
---

# Operator directive — 2026-05-05 install.sh too-narrow assumptions

## Verbatim

> "oh but there is massive bug.. this project is not limited to being on debian 13.. ubuntu too is debian and its not always the user root and its not always a bridge... and its not always..."

## Decomposition

### A — NOT limited to Debian 13
- Ubuntu is also Debian-derived ("ubuntu too is debian")
- Could support Debian 11+, 12, 13; Ubuntu 20.04+, 22.04, 24.04, 26.04
- Possibly broader Linux family (RHEL/Fedora? — operator may indicate later)

### B — NOT always the user root
- Operator earlier: "WHy root ? since it could have been jfortin install too.. since its an operating system IaC project, even in a user such as jfortin it would remain a root-type project"
- "type=root" is SCOPE (configures OS-level), not USER (must be root)
- Install supports any user with $HOME; root-required steps detected per-operation

### C — NOT always a bridge
- Network bridge is ONE use-case, not always present
- Some installs may be endpoint-only (Claude Code + opencode + safety policy)
- Some installs may be bridge-only
- Some installs full (endpoint + bridge + modules)
- Bridge config must be OPTIONAL / profile-driven / detected

### D — "and its not always..." (continuation pattern)
- More assumptions to surface as discovered
- Other potentially-too-narrow: management wifi, opencode bridge plugin, integrity sentinel
- Each operation should be optional / opt-in / detected

## What install.sh assumed wrongly

| Assumption I made | Reality |
|---|---|
| Hardcoded Debian 13 header | Should be Debian-family detection |
| `require_debian_13()` STUB | Should be `detect_os_family()` returning supported/unsupported |
| Single install path (all operations always run) | Should be profile-driven OR per-operation toggles |
| `~/.claude/` always at `$HOME` | OK for $HOME (works for any user); BUT system-level deployments may differ |
| Network bridge as fixed step in main() | Should be optional (e.g., `--with-bridge` flag or `--profile=full`) |
| Management wifi as fixed step | Same — optional |
| Opencode bridge plugin as fixed step | Same — optional (some users don't use opencode) |

## Action plan

1. Log this directive — done.
2. Add SB-073 to tracker.
3. Revise install.sh:
   - Header: "Linux host (Debian-family supported; broader Linux possible)" instead of "Debian 13"
   - OS detection: `/etc/os-release` parsing → ID + VERSION_ID; reject if unsupported with helpful message
   - Profile mechanism: `--profile <name>` with named profiles (foundation-endpoint / foundation-bridge / foundation-full / custom)
   - Per-operation toggles: `--no-bridge`, `--no-wifi`, `--no-opencode`, `--no-hooks` for fine-grained
   - Detected operations: skip when prerequisites absent (e.g., no wifi hardware → skip wifi config)
4. Decision package: surface profile mechanism shape question.

## Cross-references

- T011 (greenfield decision) — still applies; this revises HOW greenfield install.sh is shaped
- T012 (install.sh authoring) — this is the revision-pass
- AGENTS.md self-reference: type=root means scope, not user
- Identity profile at /opt/.../wiki/ecosystem/project_profiles/root-ghostproxy/identity-profile.md (canonical)
