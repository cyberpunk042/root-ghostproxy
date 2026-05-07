---
title: "Epic E002 — Piling Tasks (epic→sub-task / task→sub-sub-task / task-from-blocker)"
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
  - id: operator-directive-2026-05-06-research-elevation-piling-tasks
    type: directive
    file: wiki/log/2026-05-06-174500-research-elevation-and-piling-tasks-feature.md
tags: [epic, task-creation, piling, hierarchical-backlog]
---

# Epic E002 — Piling Tasks

> **Origin (operator-verbatim 2026-05-06)**: *"we should find an easy way to create piling tasks for an epic as sub-task or even a task-sub-task or a task based on blockers and whatnot"*

## Goal

Easy ergonomic creation of tasks at any hierarchy level: under an Epic, under another Task (sub-task), or spawned from a Blocker. Operator currently does this manually by authoring task `.md` files; this Epic delivers the tooling so the AI (and operator) can create tasks with one command.

## Three named patterns (operator-literal)

| Pattern | Source → target |
|---|---|
| **Epic → sub-task piling** | from an Epic, create sub-tasks under it |
| **Task → sub-sub-task piling** | from a Task, create deeper sub-tasks (multi-level hierarchy) |
| **Blocker → task creation** | from a row in `wiki/governance/blockers.md` or an SB, spawn a corresponding task |

Plus *"and whatnot"* — operator-acknowledged extensibility.

## Connects to E001 + E003

- E001's auto-pilot uses E002's primitives to **create the task** the cycle determines is needed
- E003's compound-retention layer can **drain into a task** via E002 when an operator-stated requirement crystalizes into actionable work

## Existing infrastructure to extend (research-first observation)

- `tools/tasks.py` — currently per-task drill-down (list/get/claimable); no creation verbs
- `wiki/backlog/tasks/T###-slug.md` — task page format with frontmatter
- `/task` slash command — manages active-task cursor, not a creation interface

## Status

- Epic scaffold created 2026-05-06.
- Modules + tasks NOT decomposed (operator scope-pending).
- Implementation NOT started.

## Forward-anchor log

`wiki/log/2026-05-06-174500-research-elevation-and-piling-tasks-feature.md`
