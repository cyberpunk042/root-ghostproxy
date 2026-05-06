---
title: "2026-05-05 — Operator directive: decision-presentation discipline (asks need context + guidance + recommendation, not just a wall of questions)"
type: log
domain: cross-domain
status: active
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-decision-presentation-context-guidance
    type: directive
tags: [log, operator-directive, sacrosanct, verbatim, decision-presentation, context, guidance, recommendation, anti-pattern-question-wall, sb-071]
---

# Operator directive — 2026-05-05 decision-presentation discipline

## Verbatim

> "this kind of situation we need a new feature /function / command and/or tools and way to do so that i am not just face to a wall of vague information and with lack of context and guidance"

## Decomposition

### A — The anti-pattern observed
- Cycle 16.5 emitted a list of 7 "direction asks" with sub-questions
- Operator reaction: "wall of vague information... lack of context and guidance"
- Each ask was a QUESTION (or set of questions) without context or agent-recommendation

### B — What's needed
- "new feature/function/command and/or tools and way to do so"
- Decisions surfaced to operator must include:
  - **CONTEXT**: enough background to make the decision without re-loading state
  - **GUIDANCE**: trade-offs / what depends on this
  - **RECOMMENDATION**: agent's suggested answer + why (operator can override but starts with a position to react to)

### C — Why the question-wall fails
- Operator has to load context PER question (vs receiving it pre-loaded)
- No agent-recommendation = operator must derive from scratch
- Vague questions don't expose what the answer would unblock

### D — Pattern needed (the new feature/function/way)

For each operator-pending decision:

```
DECISION: <one-line title>
CONTEXT: <2-3 lines of relevant background — what this decides for, why it's blocking, what's at stake>
GUIDANCE: <key trade-offs operator should weigh>
RECOMMENDATION: <agent's suggested answer + brief rationale>
ALTERNATIVES: <if multiple paths, the others briefly>
TO ANSWER: <minimal operator response shape — single word / phrase / yes-no>
```

This makes each decision a self-contained package the operator can decide ON-THE-SPOT without re-loading state.

## Apply NOW (cycle 17)

Re-present the 7 direction asks from cycle 16.5 in this format. Future cycles use this format by default.

## Action plan

1. Log this directive — done.
2. Add SB-071 to tracker.
3. Re-emit the 7 direction asks with the new format in cycle 17 response.
4. Update modes (pm-scrum-master.md surface step + dual-expert.md PM lens) to require this format when surfacing decisions.
5. Possibly: extend `tools/blockers.py` or `tools/cycle.py` with a `--decision-package` emit mode that auto-formats.

## Cross-references

- SB-059 (blockers clear in output) — this directive refines the SHAPE
- SB-061 (end-of-cycle status block) — decision packages compose into status blocks
- SB-062 (I/O enhancement mode) — decision-package format is part of the elevated style
- SB-068 (pacing heuristic) — substantive decisions vs quick acknowledgments
- /root/.claude/modes/pm-scrum-master.md /cycle step 3 (surface remaining pending decisions)
