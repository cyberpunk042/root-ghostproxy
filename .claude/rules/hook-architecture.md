# $HOME/.claude/rules/hook-architecture.md — Hook design + 2-layer architecture for root-ghostproxy

> Loaded on demand when hooks are designed, debugged, or invoked. CLAUDE.md + AGENTS.md have summaries; this file has the project-specific detail.
>
> **Strictness tier** (per `operating-principles.md`): **Strict** — the 2-layer architecture invariant + the 3-component hook design pattern (insertion point + reason + remediation) MUST hold. Bypass mechanism per hook is **Enforced** (deny + reason + remediation). Status notes (current vs draft) are **Advisory** until T006 reconciles.

## Two-layer hook architecture (this project)

Per AGENTS.md: machine-level hooks fire BEFORE project-level hooks.

| Layer | Path | Owner | Purpose |
|---|---|---|---|
| **Machine-level** | `$HOME/.claude/hooks/` | root user (this project's deliverable) | OS-level safety envelope: deny secrets, deny dangerous bash, leak-detection on output, session-start banner, session-end summary. Fires first regardless of which project the user is operating in. |
| **Project-level** | `/$HOME/.claude/hooks/` | per-project | Workflow-specific enforcement (ingestion gates, output discipline, etc.). Fires after machine-level. |

Currently this project has machine-level hooks only. Project-level hooks (e.g., for /root-as-a-project workflows) are scaffolded but unwired.

## Wired hooks (machine-level — currently 7 fires across 5 events)

Settings: `$HOME/.claude/settings.json`. All scripts at `$HOME/.claude/hooks/` and named `*.sh` but **are Python** (`#!/usr/bin/env python3` shebang) — extension is misleading but functional.

| Event | Matcher | Hook | Reason |
|---|---|---|---|
| PreToolUse | `Read\|Bash\|Edit\|Write\|NotebookEdit\|Glob\|Grep\|WebFetch\|WebSearch\|Agent\|TaskCreate\|TaskUpdate\|mcp__.*` | `policy-block.sh` (Python) | Deny reads of secret patterns (.env, *.pem, id_rsa, credentials, etc.). |
| PreToolUse | `Bash\|Edit\|Write\|NotebookEdit` | `malware-block.sh` (Python) | Block dangerous bash patterns (rm -rf /, fork bombs, etc.). |
| PostToolUse | `Read\|Bash\|WebFetch\|Grep` | `leak-detector.sh` (Python) | Scan tool output for leaked secret patterns; log to `$HOME/.claude/hooks/leaks.log`. |
| SessionStart | (any) | `session-start.sh` (Python) | Print one-line confirmation that policy hooks are active. |
| SessionStart | (any) | `session-orient.sh` (Python) | Project-priming via `additionalContext` JSON; directs agent to invoke `/orient` for the deterministic 21-step intel-gathering chain. Self-gates via BOOTSTRAP.md presence. |
| PostCompact | (any) | `post-compact.sh` (Python) | Warn about behavioral-state degradation post-compaction; chain to `/orient` to re-load brain. |
| SessionEnd | (any) | `session-summary.sh` (Python) | Print session-end summary. |

## Hook design pattern (every hook MUST follow)

Three load-bearing components:

1. **Logical insertion point** — fire at the right Claude Code lifecycle event with the right matcher. Wrong insertion = misses the rule or false-positives unrelated calls.
2. **Logical reason** — explain WHY it acted. A hook that blocks with no reason is a black box. Print: `BLOCKED: <action>. REASON: <rule>. <citation>`.
3. **Remediation offer** — offer the correct alternative. Print: `INSTEAD: <correct command>. BYPASS: <how to legitimately escalate>`.

## Bypass / escalation

Hooks must offer a documented bypass for legitimate cases. Blind enforcement creates its own failures. Patterns:
- Env-var bypass: `REASON=<reason>` env var on the bash call documents why a normally-blocked action is justified.
- Operator override: hook defers to operator approval if operator-PR-approved.
- Logged exception: hook allows but logs to `$HOME/.claude/hooks/<event>.log` for audit.

## Status (this project)

The 7 wired machine-level hook fires (5 distinct events) are functional but **not yet operator-confirmed canonical**. T006 (prior-debris reconciliation) decides which artefacts at /root are operator-authoritative vs prior-session debris. Until T006, the hooks fire actively but their canonical status is provisional. False-positive refinement queued at M003 task **T-M003-7**.

## Cross-references

- Universal hook architecture (canonical, second brain): `<second-brain>/.claude/rules/hook-architecture.md`
- AGENTS.md two-layer hook architecture section.
- ARCHITECTURE.md hook firing order section.
