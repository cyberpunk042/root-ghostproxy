---
title: "Epic E001 — Auto-Pilot Rework (cycle-skill + dependencies + priorities-driven action)"
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
  - id: operator-directive-2026-05-06-compact-args
    type: directive
    file: wiki/log/2026-05-06-173500-next-session-auto-pilot-forward-anchor.md
tags: [epic, auto-pilot, cycle-skill, priorities-driven, ai-natural]
---

# Epic E001 — Auto-Pilot Rework

> **Origin (operator-verbatim 2026-05-06 /compact args, repeated)**: *"mindful that next we want to fix the auto-pilot and its dependencies obviously which include all the current priorities which is part of the need to be improved. a lot of work and improvement needed. multiple iterations. multiple epics and tasks equivalent when you think about it.. maybe its one thing that could have helped us too. creating and selecting a task based on the priorities.. something to consider. but we love interliigence and when it can be determinities, automated as much as possible and properly adaptive and flexible and dynamic."*

## Goal

Transform `/cycle` from observation-only (orient + surface + report + stand by) into action-driven (observe → select-action-by-priority → execute → verify → record). Each cron-fire produces real work per priority order.

## Six design-values (operator-stated, sacrosanct)

1. Intelligent
2. Deterministic where possible
3. Automated as much as possible
4. Adaptive
5. Flexible
6. Dynamic

## Current gap (research-first observation, agent-flagged)

| Current `/cycle` (per `tools/cycle.py:32-65`) | Smooth-autopilot target |
|---|---|
| Per-mode step lists are observation-shaped (`orient`, `surface-decisions`, `backlog-status`, `risk-blocker-scan`, `progress-snapshot`, `architecture-review`) | Action-shaped: observe → select → execute → verify → record |
| Steps are string names | Action vocabulary needed (taxonomy already in mindfulness clause #6: SB-closure / verified-edit / drift-fix-with-empirical / explicit-standby-with-named-reason) |
| Priorities surfaced via banner only | Priorities consumed as input to action-selection (P1 first per mindfulness #5) |
| Operator drives task selection manually | AI selects task based on priorities (operator-stated *"creating and selecting a task based on the priorities"*) |

## Connection to E002 + E003

- E001 needs the task-creation primitive from **E002** to actually create a task when the cycle determines one is needed
- E001 needs the compound-retention layer + multi-group tool-call pattern from **E003** to retain requests across cycles + execute coherent batched operations

The three Epics are interlocking; cannot ship E001 without E002 + E003 substrate.

## Status

- Epic scaffold created 2026-05-06.
- Modules + tasks NOT decomposed (operator scope-pending).
- Implementation NOT started.

## Forward-anchor log (operator-verbatim primary source)

`wiki/log/2026-05-06-173500-next-session-auto-pilot-forward-anchor.md`
