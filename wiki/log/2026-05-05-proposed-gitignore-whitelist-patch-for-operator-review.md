---
title: "2026-05-05 — Proposed /root/.gitignore whitelist patch (FOR OPERATOR REVIEW, not applied)"
type: log
domain: cross-domain
status: draft
confidence: high
maturity: seed
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-gitignore-and-spec-driven
    type: directive
    file: /opt/devops-solutions-information-hub/raw/notes/2026-05-05-gitignore-audit-vendor-mapping-spec-driven-development.md
  - id: parent-module
    type: wiki
    file: wiki/backlog/modules/root-ghostproxy-m012-vendor-mapping-install-and-auto-detect.md
  - id: current-gitignore
    type: file
    file: /root/.gitignore
tags: [log, gitignore-audit, gitignore-patch, operator-review, m012-phase-a, spec-driven-development, awaiting-approval]
---

# Proposed /root/.gitignore whitelist patch — for operator review

> Status: **DRAFT. NOT APPLIED. Awaiting operator approval.** Per operator's no-conflate guard: `.gitignore` modifications affect repo-tracking policy, which is operator-territory (T006 + M012 Phase A).

## Audit context

**Why this exists**: per operator directive 2026-05-05, the current `/root/.gitignore` deny-all + whitelist correctly denies state/secrets/runtime-artifacts but EXCLUDES the agent-context spec authored this session. A `git init && git add .` would silently leave the spec untracked. This patch closes that gap while preserving the deny-all-toward-secrets posture.

## What's missing from the current whitelist

| Category | Files | Why they're spec (must be tracked) |
|---|---|---|
| Top-level brain files | CLAUDE.md, AGENTS.md, CONTEXT.md, ARCHITECTURE.md, DESIGN.md, TOOLS.md, SKILLS.md, SECURITY.md, BOOTSTRAP.md | Agent-context spec — every AI tool reads these. README.md + LICENSE already whitelisted. |
| Claude Code rules | `.claude/rules/*.md` (6 files: hook-architecture, methodology, routing, self-reference, words-are-sacrosanct, work-mode) | On-demand-loaded agent-context spec. Per Claude Code convention, lives at `.claude/rules/`. |
| Wiki tree | `wiki/config/*.yaml` (4 yamls) + `wiki/backlog/{epics,modules,tasks}/*.md` (~75 files) + `wiki/log/*.md` | Methodology engine spec + project-management spec (epic + 12 modules + 61 atomic tasks + log). |
| Templates | `open-interfaces.template` | Looks like a network-interfaces template (spec for install.sh to hydrate). |
| Documentation directory | `docs/` (currently empty) | Project documentation (spec). Whitelist if used. |

## Current whitelist (kept as-is)

The current whitelist (lines 14-47 in `/root/.gitignore`) is correct:

```gitignore
!/.gitignore
!/README.md
!/LICENSE
!/install.sh
!/uninstall.sh

!/.claude/
/.claude/*
!/.claude/settings.json
!/.claude/hooks/
/.claude/hooks/*
!/.claude/hooks/*.sh
!/.claude/hooks/*.py

!/.config/
/.config/*
!/.config/opencode/
/.config/opencode/*
!/.config/opencode/opencode.json
!/.config/opencode/plugin/
/.config/opencode/plugin/*
!/.config/opencode/plugin/*.ts
!/.config/opencode/plugin/*.json
!/.config/opencode/plugin/*.md
```

## Proposed additions

The lines below would be inserted into Section 2 + Section 3 of `/root/.gitignore`. **Not applied.**

```gitignore
# ---------------------------------------------------------------------------
# 2.5 Whitelist top-level brain files (agent-context spec)
#     These define how every AI tool (Claude Code, opencode, etc.) operates
#     on a host where root-ghostproxy is installed. Spec, not state.
# ---------------------------------------------------------------------------
!/CLAUDE.md
!/AGENTS.md
!/CONTEXT.md
!/BOOTSTRAP.md
!/ARCHITECTURE.md
!/DESIGN.md
!/TOOLS.md
!/SKILLS.md
!/SECURITY.md
!/open-interfaces.template

# ---------------------------------------------------------------------------
# 3.5 Whitelist .claude/rules/ — on-demand agent context
#     Per Claude Code convention. Loaded by topic when work touches it.
# ---------------------------------------------------------------------------
!/.claude/rules/
/.claude/rules/*
!/.claude/rules/*.md

# ---------------------------------------------------------------------------
# 7. Whitelist /wiki/ tree — methodology engine + backlog spec
#     This is the project-management + methodology source-of-truth.
#     Yamls + markdown only; no logs, no transcripts, no caches.
# ---------------------------------------------------------------------------
!/wiki/
/wiki/*
!/wiki/config/
/wiki/config/*
!/wiki/config/*.yaml
!/wiki/config/*.md
!/wiki/backlog/
/wiki/backlog/*
!/wiki/backlog/epics/
/wiki/backlog/epics/*
!/wiki/backlog/epics/*.md
!/wiki/backlog/modules/
/wiki/backlog/modules/*
!/wiki/backlog/modules/*.md
!/wiki/backlog/tasks/
/wiki/backlog/tasks/*
!/wiki/backlog/tasks/*.md
!/wiki/log/
/wiki/log/*
!/wiki/log/*.md

# ---------------------------------------------------------------------------
# 8. Whitelist /docs/ if used (currently empty; future module artefacts)
# ---------------------------------------------------------------------------
!/docs/
/docs/*
!/docs/*.md
```

## Hard-deny preserved (no changes proposed)

Section 6 of the current `.gitignore` (`.env`, `.credentials.json`, `.claude.json`, `claude-auth-url.txt`, `qr.code`, keys, certs, cloud creds, history files, SSH/GPG, tokens, editor files) — all correct. **No proposed changes to deny patterns.**

## Verification (post-patch, if applied)

After operator approval + patch applied, these checks should pass:

```bash
cd /root
git init  # if not already

# spec files visible to git
git ls-files --others --ignored --exclude-standard | wc -l   # should be ~0 spec files ignored
git status -uall 2>&1 | head -50

# specific files tracked
git check-ignore -v CLAUDE.md AGENTS.md BOOTSTRAP.md
# expected: each file is NOT ignored

# wiki tree fully tracked
find wiki/ -type f -name "*.md" -o -name "*.yaml" | xargs -I{} git check-ignore -v {} 2>&1 | head -20
# expected: all spec files NOT ignored

# secrets STILL denied
git check-ignore -v .env .credentials.json claude-auth-url.txt 2>&1
# expected: each file IS ignored (correct deny)
```

## Risks / considerations

1. **No regressions to deny patterns.** The proposed additions only widen the whitelist; they don't soften deny rules.
2. **Section ordering matters.** `.gitignore` is processed top-to-bottom; later patterns override earlier. The proposed whitelist additions sit before the hard-deny Section 6, which is correct (hard-deny wins over whitelist).
3. **Deny patterns inside whitelisted dirs.** Section 5 of current `.gitignore` explicitly catches `**/*.log`, `**/*.jsonl`, `**/sessions/`, `**/projects/`, `**/cache/`, `**/__pycache__/`. These remain in effect even inside the newly whitelisted `wiki/`. Validate that no `.log` / `.jsonl` files in `wiki/log/` were intended to be tracked (currently `wiki/log/*.md` is fine; nothing else in there).
4. **Future maturation.** As the project grows, new spec files will need explicit whitelisting (or the whitelist patterns broadened). M012 Phase A includes a follow-up "spec-completeness audit" recurring task.

## What this patch does NOT do

- Does NOT `git init` /root.
- Does NOT modify any deny pattern.
- Does NOT add or remove vendor-related patterns (vendor manifest is M012 Phase C).
- Does NOT modify hooks, settings, or any code path.

## Operator action requested

1. Review the proposed additions above.
2. Approve / modify / reject.
3. If approved: an atomic task under M012 (e.g., T-M012-A1) implements the patch.

## Cross-references

- M012 Phase A — [root-ghostproxy-m012-vendor-mapping-install-and-auto-detect.md](../backlog/modules/root-ghostproxy-m012-vendor-mapping-install-and-auto-detect.md)
- Operator directive verbatim — [/opt/.../raw/notes/2026-05-05-gitignore-audit-vendor-mapping-spec-driven-development.md](file:///opt/devops-solutions-information-hub/raw/notes/2026-05-05-gitignore-audit-vendor-mapping-spec-driven-development.md)
- Current .gitignore — `/root/.gitignore` (173 lines)
