---
title: "Epic E003 — Compound retention layer + Focus-update + Multi/Group tool calls"
type: epic
domain: cross-domain
status: draft
confidence: high
maturity: seed
priority: P1
parent_milestone: v0.2-ai-natural-task-management
task_type: epic
current_stage: document
readiness: 5
created: 2026-05-06
updated: 2026-05-06
sources:
  - id: operator-directive-2026-05-06-task-creation-compound-milestone
    type: directive
    file: wiki/log/2026-05-06-180000-task-creation-focus-update-multigroup-compound-milestone-directive.md
tags: [epic, compound-retention, focus-update, multi-group-tool-calls, ai-ergonomics]
---

# Epic E003 — Compound retention layer + Focus-update + Multi/Group tool calls

> **Origin (operator-verbatim 2026-05-06)**: *"what I said about tasks creation and focus update and multi/group tool calls is real too and very important.. we want to make things simpler for the AI.. avoid creating a nightmare prompt or polution and useless data or even negative information. again this is additive.. it should be adding to the compound list.. not to confuse with the priorities or the tasks. but it make sense sometimes to just create a task or even tasks to address the focus, the mission or even before that the priorities. you shouold in those case naturally use the tool to coumpound and when you will use the waterfall to ask what is pending to pass to a next task you will be able to get back on track and not lose track of any request or compound or demands or requirements or questions and whatnot."*

## Goal

Add a NEW additive compound layer that retains six categories of operator-stated content across cycles, plus the multi-group tool-call pattern that lets the agent execute coherent batched operations naturally, plus the focus-update channel that lets the AI update its own focus when a task closes.

## Three components (operator-named — clause 1 of directive)

1. **Compound retention layer** — additive state that retains: request / compound / demand / requirement / question / "whatnot" (6 categories operator named)
2. **Focus-update channel** — AI naturally updates `active-focus` (and possibly `active-mission`, `active-impediment`) as work evolves
3. **Multi/Group tool calls** — chain/batch tool operations as natural agent capability (cousin to SB-131 chain-operations pattern; this elevates it)

## Four anti-patterns (operator-named — clause 3)

The compound layer MUST NOT produce:
1. nightmare prompt
2. pollution
3. useless data
4. negative information

## Five future-state delivery channels (operator-named — clause 13)

The evolution should be:
1. **implied** (background detection by agent)
2. **directed** (cycle-driven action)
3. **offered-as-options** (UI-style: agent proposes; operator picks)
4. **offered-as-tools** (agent invokes deterministically)
5. **explained-properly** (each suggestion has rationale)

## Seven structural questions (operator scope-pending)

Captured in directive log; answers shape the build:
- Q1: Milestone vs Epic-alongside placement (resolved by this Milestone v0.2 creation)
- Q2: single retention state file vs per-category parallel files
- Q3: multi-group as new tool / extension / rule-only
- Q4: direct task write vs lightweight queue
- Q5: agent authority on focus updates
- Q6: trigger surfaces (what counts as "naturally")
- Q7: "what's pending" query surface (slash / cycle / MCP / handoff)

## Connection to E001 + E002

- **E001** auto-pilot needs E003's compound-retention to remember what's pending across cycles (otherwise "select action" loses prior context)
- **E001** auto-pilot uses E003's multi-group tool-call pattern to execute coherent batched fixes (per SB-131)
- **E002** piling-tasks creates the tasks E003's compound layer recommends crystalizing
- All three are interlocking — none can fully ship without the others

## Status

- Epic scaffold created 2026-05-06.
- Q1-Q7 await operator scope decisions.
- Modules + tasks NOT decomposed.
- Implementation NOT started.

## Forward-anchor log

`wiki/log/2026-05-06-180000-task-creation-focus-update-multigroup-compound-milestone-directive.md`
