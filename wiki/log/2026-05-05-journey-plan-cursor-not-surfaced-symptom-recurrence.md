---
title: "2026-05-05 — Operator directive: journey/plan/cursor not visible in status blocks (recurring symptom)"
type: log
domain: cross-domain
status: active
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-journey-plan-cursor-not-clear
    type: directive
tags: [log, operator-directive, sacrosanct, verbatim, journey, plan, cursor, status-block, recurring-symptom, sb-075]
---

# Operator directive — 2026-05-05 journey/plan/cursor not visible (recurring symptom)

## Verbatim

> "this again reveal one other symtom I had talked about where the journey and plan and cursor in them does not seem clear."

## Decomposition

### A — Recurring symptom (operator-flagged earlier this session)
- Earlier directive: *"there should be a clear channel of the blockers that cummulate that require my inputs and the tracking of the progress and the view of journey and current position and planning"*
- Authored: governance/{blockers, progress, decisions}.md + slash commands
- BUT: status blocks emitted at end-of-cycle don't surface journey/plan/cursor
- Operator has to mentally reconstruct position each time

### B — What "journey and plan and cursor" means
- **Journey**: where we've been (cycle history, completed work, drifts + corrections)
- **Plan**: where we're going (operator's stated logical order, milestones, target end-state)
- **Cursor**: precisely where we are NOW + what's just-completed + what's-next

### C — What's missing in current status blocks
Current blocks show: counts (modules, tasks, SBs) + decisions logged + open items. Missing:
- Visual position indicator within the plan
- Recent journey trace (last N cycles)
- Cursor: the specific just-completed + next-up items

### D — How to fix structurally
Status block format needs new sections — JOURNEY (compact), PLAN (with progress bars), CURSOR (just-done + next).

## Action plan

1. Log directive — done.
2. Add SB-075 to tracker.
3. Extend tools/cycle.py status block emit with journey/plan/cursor sections.
4. Apply in this cycle's status block.

## Cross-references

- governance/progress.md (journey view doc — but rarely surfaced inline)
- /progress + /sync-progress slash commands
- SB-061 (status block) — this refines
- SB-071 (decision package) — operator-pending items
- SB-072 (auto-research filter)
- Operator earlier directive: "view of journey and current position and planning"
