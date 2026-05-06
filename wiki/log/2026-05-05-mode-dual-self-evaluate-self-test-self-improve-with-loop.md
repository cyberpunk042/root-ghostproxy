---
title: "2026-05-05 — Operator directive: /mode-dual + self-evaluate/self-test/self-improve + arm-loop-until-blocked + batch-process-accumulated"
type: note
domain: cross-domain
status: raw
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-mode-dual-self-improvement-loop
    type: directive
tags: [note, operator-directive, sacrosanct, verbatim, mode-dual, self-evaluation, self-test, self-improvement, autopilot-loop, batch-processing, accumulation, agent-modes-purpose]
---

# Operator directive — 2026-05-05 /mode-dual + self-improvement loop

## Verbatim (as `/mode-dual` arguments)

> "and self-evualuate and self-test and self-improve. there should be enough already defined work that you can iterate over it and be self-critical and improve and do this in iteration with me but at the same time enabling a loop for when till you are blocked and things can commulate and we can process them in batch when appropriate. Normally there is already a bunch of stuff in place but we can also keep evolving and adapting them or even adding to them. the goal of the agent modes is obviously to drive the development properly and offer an easy and strong loop and adaptive and progress tracking capabilities."

## Decomposition

### A — /mode-dual activation
- Slash-invoked: `/mode-dual` literal, with the long-form arguments above appended.
- Persona shift: PM Scrum Master + DevOps Architect simultaneously; lens-switched per question.

### B — Self-evaluate + self-test + self-improve (meta-directive)
- "self-evualuate and self-test and self-improve"
- Triple verb. Each cycle should perform all three.

### C — Iterate over already-defined work
- "there should be enough already defined work that you can iterate over it"
- 13 modules + 61 tasks + 9 rules + 13 commands + 7 hooks + 4 tools + MCP server + 3 governance docs + 3 modes ALREADY EXIST.
- Iterate over them — don't invent new scope unless needed.

### D — Be self-critical
- "be self-critical and improve"
- Critique own outputs honestly. Find weaknesses, gaps, drift, inconsistencies.

### E — Iteration with operator
- "do this in iteration with me"
- Not autonomous-only. Operator-in-the-loop pattern preserved.

### F — Loop until blocked + accumulate
- "but at the same time enabling a loop for when till you are blocked and things can commulate"
- Arm an autopilot loop.
- Loop continues UNTIL blocked.
- When blocked, things ACCUMULATE (don't lose findings).

### G — Batch-process when appropriate
- "and we can process them in batch when appropriate"
- Operator processes the accumulated batch when it makes sense (not every-cycle interruption).

### H — Already a bunch of stuff in place
- "Normally there is already a bunch of stuff in place"
- Acknowledgment: prior preparation work counts.

### I — Evolve / adapt / add
- "but we can also keep evolving and adapting them or even adding to them"
- Three valid actions: evolve existing, adapt existing, add new.

### J — Goal of agent modes (canonical statement)
- "the goal of the agent modes is obviously to drive the development properly and offer an easy and strong loop and adaptive and progress tracking capabilities"
- This is the OPERATOR's authoritative statement of WHY modes exist:
  1. Drive development PROPERLY
  2. Offer an EASY and STRONG loop
  3. ADAPTIVE
  4. Progress-tracking capabilities

## Action plan

1. Log this directive verbatim — done (this file).
2. Set `/root/.claude/active-mode` to `dual-expert`.
3. Read `/root/.claude/modes/dual-expert.md` for persona + lens-switching + /cycle sequence.
4. Self-arm a loop via the `loop` skill: `/loop /cycle` self-paced (per loop-cron-lifecycle.md the agent has standing permission to self-arm when context-logical, with reporting protocol).
5. First cycle runs immediately: dual-lens self-evaluation pass over the existing 13-module / 61-task / 9-rule / 13-command / 7-hook / 4-tool / MCP / 3-governance-doc surface area.
6. Findings accumulate in `/root/wiki/log/2026-05-05-mode-dual-self-improvement-iterations.md` (append-per-cycle).
7. Loop runs until: (a) operator interrupts, (b) Scenario L1/L4 triggers per loop-cron-lifecycle.md, or (c) the accumulated batch is large enough that operator-review is the next-best action.

## No-conflate guard

- "you can iterate over it" = permission to iterate; not a mandate to rewrite everything.
- "be self-critical" = honest critique, not destructive nuking. Critique → propose → operator approves before destructive changes.
- "till you are blocked" = run until blocked, not run forever. When blocked, pause + accumulate.
- "we can process them in batch when appropriate" = operator decides batch-processing timing, not agent.
- "keep evolving and adapting them or even adding to them" = additive/adaptive default; new additions need operator approval per work-mode.md PO approval boundary.
- "the goal of the agent modes is obviously to drive the development properly" = framing statement; doesn't override existing scope discipline.
