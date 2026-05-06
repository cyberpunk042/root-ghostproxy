---
title: "2026-05-05 — Operator directive: compound + waterfall rule/strategy for cumulating inputs and never discarding prior tasks/inputs"
type: log
domain: cross-domain
status: active
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-compound-waterfall-cumulation-strategy
    type: directive
tags: [log, operator-directive, sacrosanct, verbatim, compound-strategy, waterfall-strategy, input-cumulation, no-discard, tools-augmentation, second-brain-evolution, deferred-work, comments-not-deroute]
---

# Operator directive — 2026-05-05 compound + waterfall input-cumulation strategy

## Verbatim

> "we might need a compound and waterfal rule and strategy so that we cummulate properly my inputs and make sure we never discard the tasks or inputs from before... we can take the time to think about it.. it too will deserve its own tasks (this is an input that should not deroute again... i mean there is claerly a path and if that still not claer and we are still not able to retain a claer view of it, this too need to be addressed, even if its second-brain that need to evolve too via contribution and defered work) we can add or augment tools when we need. there can be real needs. again just another input. you can continue (obvioulsy many changes comes with new or updated directives and instructions and config)"

## Decomposition

### A — Compound + waterfall rule/strategy (the core ask)
- **Compound**: new directives ADD to cumulative directive set; don't replace
- **Waterfall**: priority/sequence ordering; later directives REFINE earlier ones, don't overwrite sacrosanct grants
- **Cumulate properly**: the agent must retain the FULL stack of directives, not just the latest

### B — Never discard tasks or inputs from before
- The agent's pattern of dropping earlier sacrosanct grants when over-correcting is the failure
- Existing work-mode.md says "Additive, not destructive" — but evidently insufficient
- Need stronger structural mechanism to enforce non-discard

### C — Take time to think about it
- Operator explicitly says don't rush this. Quickfix forbidden (per separate operator directive).
- Plan: register → reflect → propose design → operator-feedback → implement
- Implies multiple cycles of iteration on this strategy

### D — Will deserve its own tasks
- This is BACKLOG-WORTHY
- Atomic tasks should track: compound design, waterfall design, tool support, integration
- Possibly a new module (M015?) or integrate into M013 (modes architecture)

### E — Comments-don't-deroute (re-emphasized)
- "this is an input that should not deroute again"
- Operator catches recurring need to remind agent of #6 principle
- Behavioral pattern recurring

### F — Second-brain may need to evolve too
- "even if its second-brain that need to evolve too via contribution and defered work"
- The compound+waterfall pattern may need cross-project support
- Second-brain's role: cumulating patterns across sister projects
- Channel: `tools.gateway contribute` (deferred until M007)

### G — Tools can be added/augmented
- "we can add or augment tools when we need"
- Permission to extend `tools/*.py` with new capabilities
- Real needs justify; not speculative

### H — Continue (additive, not blocking)
- "you can continue"
- Loop should keep running through systemic + iteration work
- Many changes coming via directives/instructions/config — agent must absorb them additively

## Why this matters (root cause framing)

The operator's pattern observed across this session:
- Operator gives directive A
- Agent acknowledges + acts
- Operator gives directive B (often refining A)
- Agent acts on B but DROPS A in the process (over-correction / extreme swing)
- Operator: "you dismissed my earlier sacrosanct words"

The compound+waterfall strategy makes A + B both retained, with B refining A's TRIGGERS not removing A's PERMISSION.

## Action plan

1. Log this directive verbatim — done (this file).
2. Register as SB-057 in `/root/wiki/governance/systemic-bugs.md`.
3. Add to backlog as a new SB or possible new module. Operator says "take the time to think about it" — proper design pass needed before implementation.
4. Strengthen `/root/.claude/rules/work-mode.md` "Additive, not destructive" section with compound+waterfall framing + verification step.
5. Consider tools augmentation: a `tools.directives` module that surfaces the cumulative directive stack (read all `/root/wiki/log/*.md` chronologically; show the open directives + their interactions).
6. Defer: second-brain contribution for cross-project cumulation pattern (gated on M007).

## No-conflate guard

- "we might need" = directive to consider design, not directive to implement immediately
- "take the time to think about it" = NO QUICKFIX. Design properly. Multiple cycles.
- "deserve its own tasks" = backlog this; not single-cycle work
- "you can continue" = additive context; don't pause iteration
- "obvioulsy many changes comes with new or updated directives and instructions and config" = expectation set: more directives coming; the system must absorb them additively
- "again just another input" = additive context per principle #6 (comments-don't-deroute)
