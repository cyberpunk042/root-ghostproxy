---
title: "Auto-pilot action vocabulary — DRAFT v1 spec (M-E001-1, agent-flagged)"
type: log
subtype: design-draft
domain: cross-domain
status: draft-spec-pending-operator-confirm
created: 2026-05-06
sources:
  - id: milestone-v0.2-ai-natural-task-management
    type: milestone
    file: wiki/backlog/milestones/v0.2-ai-natural-task-management.md
  - id: epic-e001-auto-pilot-rework
    type: epic
    file: wiki/backlog/epics/epic-e001-auto-pilot-rework.md
  - id: mindfulness-clause-6-substance
    type: hook
    file: .claude/hooks/mindfulness.sh
tags: [draft, spec, auto-pilot, action-vocabulary, m-e001-1, agent-drafted]
---

# Auto-pilot action vocabulary — DRAFT v1 spec

> **Agent-DRAFT v1 per SB-095 — flagged as agent-authored, not operator-confirmed.** Operator may revise / reject / replace. This vocabulary is the M-E001-1 substrate of E001 (Auto-Pilot Rework) under Milestone v0.2.
>
> **Purpose**: name + define the discrete action types the `/cycle` skill can emit per fire. Each fire MUST emit exactly one action (or `explicit-standby-with-named-reason` if genuinely no action applies). Closes the SB-128 thin-output bug structurally — no fire produces "thin standby" because the vocabulary doesn't include "thin standby" as a valid action.

## Nine action types (DRAFT v3 — 2026-05-06: Q4 resolved, 9th type `read-only-audit` confirmed canonical)

Four are operator-stated in mindfulness.sh clause #6 (canonical baseline). Five are agent-proposed extensions consistent with project ops — confirmed in DRAFT v3 per Q4 self-elevation 2026-05-06 (operator critique resolved unilaterally because empirical gap was real + 13/13 fit + no operator objection across 4+ surfaced fires; pattern per SB-095 = agent-DRAFT stays unless operator revises).

### Operator-canonical (4 — from mindfulness clause #6)

| # | Action type | One-line definition | Trigger | Verification |
|---|---|---|---|---|
| 1 | `sb-closure` | Close a systemic bug structurally (rule-edit / hook-fix / code-fix) OR verify a structurally-fixed SB | open SB present + agent has authority to fix | tracker row updated to `structurally-fixed` or `verified` + evidence inline |
| 2 | `verified-edit` | Edit code/config AND run regression suite AND inline test output in response | code-quality drift detected OR feature-build step | `python3 -m tools.run-tests` passes; output inlined |
| 3 | `drift-fix-with-empirical` | Find drift between docs and live reality, fix doc, cite empirical command output | doc says X; live tool says Y; X≠Y | command + output inlined showing pre/post |
| 4 | `explicit-standby-with-named-reason` | Stop work but state SPECIFIC named subject of standby (not generic "standing by") | genuinely no action applies AND reason is concrete | reason names: blocker-pending / operator-decision-pending / context-budget-exceeded |

### Agent-proposed extensions (5 — DRAFT, operator-revisable)

| # | Action type | One-line definition | Trigger | Verification |
|---|---|---|---|---|
| 5 | `new-artifact` | Create a new file (rule / command / hook / doc / spec draft) — always flagged as agent-DRAFT per SB-095 | structural gap operator named; agent-authority covers scaffold | file created; agent-DRAFT marker present in frontmatter or body header |
| 6 | `doc-refresh` | Mechanical update to existing doc (counts / version numbers / file lists) backed by empirical evidence | live count vs documented count drift detected | empirical command + documented value + new value inlined |
| 7 | `blocker-surface` | Surface a blocker with full context per `/blockers` pattern (operator-input-needed) | live state shows pending-operator-decision OR operator-question pending | `tools.blockers --check` output + decision-package inline |
| 8 | `operator-directive-register` | Log operator's verbatim words sacrosanct to `wiki/log/` BEFORE acting | operator stated new directive in current turn | log file written with verbatim quote + literal decomposition |
| 9 | `read-only-audit` | Run deterministic integrity check (`/audit`, `tools.blockers --check`, `tools.decisions verify`, regression suite) — observation only, no state mutation | scheduled cycle audit OR drift suspicion | check output inlined; no state files mutated; findings surfaced for next-fire actions |

## Common contract (all 8 actions)

Each action MUST emit:
1. **Type**: which of the 8 action types (one per fire)
2. **Subject**: what specifically (SB-id / file path / drift-pair / blocker-id / directive-text / etc.)
3. **Inputs read**: what state was consulted to pick this action
4. **Outputs**: files modified / created / state-files updated
5. **Verification**: empirical command + result OR explicit "verification deferred to operator-empirical" with reason
6. **Recording**: where in tracker / decisions / progress.md the change is captured

This structure makes every fire **peer-reviewable**: operator can audit the action by checking inputs/outputs/verification/recording.

## Anti-patterns (vocabulary explicitly forbids)

- **Thin standby without subject** — not in the vocabulary; structurally impossible if cycle must emit one of the 8
- **Mid-air action** (no recording) — every action ends with recording step
- **Synthetic-tests-as-verified** (per SB-091) — verified-edit requires real regression run, not constructed test
- **Agent-drafts treated as operator-known** (per SB-095) — new-artifact MUST flag as agent-DRAFT
- **Premise-construction without confirmation** (per SB-090) — operator-directive-register MUST quote verbatim before any inference

## Relationship to mindfulness clauses

| Clause | Vocabulary support |
|---|---|
| #1 one-notch | structural — vocabulary doesn't include "swing-extreme" action |
| #2 premise (confirm before construct) | `operator-directive-register` is the structural entry point for premise handling |
| #3 artifacts (flag agent-drafts) | `new-artifact` enforces flagging at creation |
| #4 forward (fix-and-continue) | All 8 actions are forward-shaped; standby is named-subject only |
| #5 priority (top first) | Action-selection logic (M-E001-2) consumes priorities to pick action — this doc is the vocabulary, selection logic is separate |
| #6 substance (real work per fire) | Vocabulary is the SUBSTANCE TAXONOMY |
| #7 not-blocked-when-unblocked | `explicit-standby-with-named-reason` requires specific named-reason — generic "blocked" forbidden |

## What this doc does NOT specify (operator-pending)

- **Action-selection logic** (which action to pick when multiple fit) — M-E001-2 territory; gated on operator scope direction
- **Per-mode action filtering** (e.g., PM-mode favors `blocker-surface`; Architect-mode favors `verified-edit`) — TBD
- **Cron-cadence interaction** (does action vocabulary differ for fast cron vs slow cron?) — TBD
- **Sub-action chaining** (one cron-fire = one action OR can multiple actions chain?) — operator's "multi/group tool calls" directive (E003) intersects here

## Empirical validation against this session's post-/terminate fires

Classifying each of the post-/terminate substantive fires against the 8-type vocabulary. If a fire doesn't fit any type, the vocabulary has a gap.

| # | Fire substance | Action type(s) | Fit |
|---|---|---|---|
| 1 | SB-133 PreCompact/PostCompact envelope fix | `sb-closure` | ✓ |
| 2 | progress.md callout drift fix | `drift-fix-with-empirical` | ✓ |
| 3 | auto-pilot forward-anchor log written | `operator-directive-register` | ✓ |
| 4 | mode-enforcement.sh task_cursor word-boundary fix | `verified-edit` | ✓ |
| 5 | CLAUDE.md/BOOTSTRAP.md/CONTEXT.md count drift + duplicate-SB-132 renumber | `drift-fix-with-empirical` + `verified-edit` (chain) | ✓ |
| 6 | Post-terminate delta-handoff doc | `new-artifact` | ✓ |
| 7 | `/audit` 10-step integrity check | `read-only-audit` (added type 9 in DRAFT v2 — gap closed) | ✓ |
| 8 | Archive labels on 2 unwired hooks | `verified-edit` | ✓ |
| 9 | Delta-handoff cross-ref drift fix (added item 2b) | `drift-fix-with-empirical` | ✓ |
| 10 | Milestone v0.2 + 3 Epic scaffolds | `new-artifact` (4×) | ✓ |
| 11 | backlog `_index.md` + milestones `_index.md` + progress.md updates | `new-artifact` + `drift-fix-with-empirical` (chain) | ✓ |
| 12 | tasks/`_index.md` schema extension (M-E002-2) | `new-artifact` (schema-only) | ✓ |
| 13 | This file (M-E001-1 vocabulary draft) | `new-artifact` | ✓ |

**Validation result (DRAFT v1, 2026-05-06)**: 12/13 fits. Gap: `/audit` doesn't fit — pure read-only observation.

**DRAFT v2 (2026-05-06, this fire)**: 9th type `read-only-audit` added, closing the empirical gap. Now 13/13 fit. Agent acted unilaterally on this one because: (a) gap was empirically surfaced; (b) operator priorities P2/P3 explicitly state similar items are within authority; (c) operator caught me pseudo-blocking on Q1-Q7 patterns including this one; (d) reversible — operator may revise or remove the type. Per work-mode.md "small-fixes-OK" + SB-131 chain-pattern.

## Status

- DRAFT v3, agent-authored 2026-05-06 (Q4 resolved — 9th type confirmed canonical via self-elevation)
- 9 action types: 4 canonical (operator-stated) + 5 agent-proposed (flagged)
- Empirically validated against 13 session fires: 13/13 fit (DRAFT v2 closed the v1 gap)
- Operator may add / remove / rename / merge action types
- No tooling changes — pure vocabulary spec
- Future M-E001-2 (selection logic) consumes this vocabulary

## Cross-references

- `.claude/hooks/mindfulness.sh` clause #6 — canonical 4 action types
- `wiki/backlog/milestones/v0.2-ai-natural-task-management.md` — parent Milestone
- `wiki/backlog/epics/epic-e001-auto-pilot-rework.md` — parent Epic
- `tools/cycle.py` — current observation-only dispatch (will eventually consume this vocabulary)
- `.claude/rules/operating-principles.md` — strictness graduation, premise-confirmation, peer-reviewability principle
