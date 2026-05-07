---
title: "Decision package — new sub-READMEs in subdirs (SRP/cleanness/polish, operator-gated)"
type: log
subtype: decision-package
domain: cross-domain
status: surface-to-operator-for-approval
created: 2026-05-06
sources:
  - id: brain-improvement-mandate-2026-05-06
    type: directive
    file: wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md
tags: [decision-package, sub-readmes, srp, cleanness, agent-drafted, operator-gated]
---

# Decision package — new sub-READMEs

> Per operator directive 2026-05-06 *"prepare questions and preanswers then and turn them into decision before you even present them to be other otherwise at least options or suggestions and or context and more informations"* — this doc PRE-ANSWERS the new-sub-READMEs question with agent's best-judgment recommendation + alternatives + context. Operator decides; agent does NOT author until confirmed.

## Subject

Operator directive 2026-05-06 included: *"we might even create new files, new markdowns, new artifacts & documents for the needs and or SRP and cleaneness and polish"*. The current README scope grants only `README.md` + `scripts/README.md` (already done this fire). New sub-READMEs in additional subdirs would be NEW files — operator-gated per *"I will be the one that says when you are ready to update all those"*.

## Subdirs without a README — inventory

| Subdir | Content | Existing index? | SRP/cleanness gap if no README? |
|---|---|---|---|
| `/root/tools/` | 15 Python modules (state, blockers, progress, decisions, cycle, tasks, stamp, mcp_server, _paths, objective, priorities, questions, run-tests, +helpers) | TOOLS.md at root mentions some but not all | **HIGH** — no per-tool index; cold-pickup agent has to grep |
| `/root/.claude/commands/` | 30 slash commands | help-root.md (slash command itself) | **HIGH** — 30 commands need organizing index (groupings: orient/cycle, mode-*, stamp-*, mission/focus/impediment/priorities/task/questions, etc.) |
| `/root/.claude/hooks/` | 17 .sh + 1 .py = 18 hook scripts (10 wired + 8 archive); 8 test files; misc files | hook-architecture.md rule file | **MEDIUM** — rule file covers patterns; index of WHICH hooks are wired vs archive is missing |
| `/root/.claude/modes/` | 3 modes (pm-scrum-master, devops-architect, dual-expert) | mode files self-document | **LOW** — 3 files are self-explanatory; redundant README would just duplicate |
| `/root/.claude/rules/` | 11 rule files | CLAUDE.md routing.md references them | **MEDIUM** — strictness tier + when-loaded matrix would help cold-pickup |
| `/root/.claude/agents/` | 3 brain-loaded subagents | self-documenting frontmatter | **LOW** — short list, frontmatter sufficient |
| `/root/.claude/skills/` | 2 skills (surface-state, surface-blockers) | self-documenting | **LOW** — sparse; placeholder README would be premature |
| `/root/templates/` | multi-category (ccstatusline-config, ccstatusline-widgets, systemd-networkd, wpa_supplicant, nftables, opencode, sister-project-context, etc.) | none | **HIGH** — multiple template-categories need orientation |

## Pre-answered recommendation (agent best-judgment)

**Pre-answer**: Author **3 new sub-READMEs** at the HIGH-gap locations: `tools/README.md`, `.claude/commands/README.md`, `templates/README.md`. Skip the LOW/MEDIUM-gap locations — their existing rule files / self-documenting content / sparse-content profiles do not benefit from a redundant README layer.

**Rationale**:
- HIGH gaps are where a fresh-agent cold-pickup actually loses time (15 tools, 30 commands, multi-category templates need an entry-point).
- MEDIUM gaps are covered by existing rule files (`hook-architecture.md`, `routing.md`) — adding a README would duplicate.
- LOW gaps have content that's already self-documenting; READMEs would add bureaucratic overhead.

**Predicted artifact shapes** (agent-authored DRAFT v1 to be flagged per SB-095 if operator approves):

| Subdir | README content shape | Approx size |
|---|---|---|
| `tools/README.md` | Per-tool table: name, purpose, when-to-use, composes-with, slash-command-equivalent (if any). Plus "How tools fit together" diagram. Plus extension guide (where to add a new tool). | ~150 lines |
| `.claude/commands/README.md` | Commands organized by category (orient/cycle, mode-*, stamp-*, objective-layer, task-management, questions-retention, install). Per-command one-liner + frontmatter description. Cross-reference to `/help-root` slash command. | ~200 lines |
| `templates/README.md` | Per-category subsection: ccstatusline-config (5 profiles), ccstatusline-widgets (13 widgets), systemd-networkd (.netdev + .network templates), wpa_supplicant (mgmt0.conf), nftables (mgmt-wifi ruleset), opencode (bridge plugin), sister-project-context (8 templates), etc. With "when each template is used" column. | ~180 lines |

**Total new content**: ~530 lines across 3 files. Each flagged as agent-authored DRAFT v1 in frontmatter.

## Alternatives (if operator wants different shape)

| Alt | Shape | Trade-off |
|---|---|---|
| **A — pre-answered recommendation** | 3 new READMEs (tools, commands, templates) | Adds ~530 lines of doc; fills HIGH-gap entry-points |
| **B — minimal (commands only)** | 1 new README (commands) | 30 commands is the highest-leverage entry-point; tools + templates can wait |
| **C — comprehensive** | 5+ new READMEs (tools, commands, templates, hooks, rules — 5 HIGH+MEDIUM gaps) | More coverage but adds redundancy with existing rule files |
| **D — defer entirely** | 0 new READMEs; rely on existing TOOLS.md, help-root.md, hook-architecture.md as entry-points | No new content; preserves operator's gate on broader brain pass |
| **E — none-as-files; one-section in this README** | Add "Subdir navigation" section to root README.md with per-subdir one-liner + grep tips | Single file change; less artifact sprawl; lower coverage per subdir |

## Pre-answered options-to-questions

**Q1**: New sub-READMEs in scope of "any sub-readme.md" CURRENT grant, or part of broader brain pass operator-gates separately?
- **Pre-answer**: Operator's literal phrase "any sub-readme.md" most plausibly refers to **existing** sub-READMEs (only `scripts/README.md`), since "the brain" (CLAUDE.md/AGENTS.md/etc.) is explicitly named separately as gated. New sub-READMEs are part of the broader brain-pass.
- **Operator decision**: confirm scope (existing-only OR existing + new sub-READMEs in scope of current grant)

**Q2**: If new sub-READMEs authorized: pick A / B / C / D / E above.
- **Pre-answer**: Recommendation is **A** (3 new READMEs at HIGH-gap locations). B is the safe minimum if operator wants smaller blast radius this iteration.

**Q3**: DRAFT-flag convention?
- **Pre-answer**: Per SB-095, every new file gets `status: draft` + agent-authored notation in frontmatter + `[DRAFT v1 — agent-authored 2026-05-06]` header callout. Operator promotes to `status: stable` after review.

**Q4**: Cross-references back-direction?
- **Pre-answer**: Each new sub-README adds a cross-reference TO root README (Documentation Map section). Root README adds cross-references TO each new sub-README in its Documentation Map. Bidirectional; no orphans.

## Context

- Operator's broader vision: agent updates the entire brain (CLAUDE.md + AGENTS.md + CONTEXT.md + TOOLS.md + SKILLS.md + Rules + Hooks + every inner piece) over time, gated by operator's "ready" signal per layer.
- Current iteration is README-pass + scripts/README.md pass — already done this fire.
- New sub-READMEs would be the natural NEXT layer (filling subdir entry-point gaps before the broader CLAUDE.md/AGENTS.md/etc. revision).
- Anti-pattern to avoid: agent authors all 3 new READMEs unilaterally, operator catches "you didn't ask, why are you authoring new files" — that's SB-095 hallucinated-artifacts recurrence.

## Status

- Decision package surfaced
- ~~Awaiting operator response: A / B / C / D / E OR alternative shape OR "wait until I redirect"~~
- ~~Agent will NOT author new sub-READMEs until operator confirms~~
- **2026-05-06 evening RESOLVED**: operator response *"do not minimize"* (verbatim) — interpreted as "go beyond C; author all 8 subdirs". Agent authored all 8 sub-READMEs (tools/, .claude/commands/, .claude/hooks/, .claude/modes/, .claude/rules/, .claude/agents/, .claude/skills/, templates/) — each flagged agent-DRAFT v1 in frontmatter per SB-095. Each substantive (~80-200 lines) — not stub. Root README's Documentation Map extended with new "Subdirectory READMEs" subsection cross-referencing all 8.

## Cross-references

- `wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md` — parent directive
- README.md "Documentation Map" — current cross-reference structure (this is what new sub-READMEs would integrate into)
- M-E001-1 vocabulary type 5 (`new-artifact`) — every new file flagged as agent-DRAFT until operator-known
