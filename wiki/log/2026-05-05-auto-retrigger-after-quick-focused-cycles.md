---
title: "2026-05-05 — Operator directive: auto-retrigger after quick focused cycles (don't artificially delay progress)"
type: log
domain: cross-domain
status: active
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-auto-retrigger-quick-cycles
    type: directive
tags: [log, operator-directive, sacrosanct, verbatim, auto-retrigger, cycle-pacing, useless-delay, quick-cycle-chain]
---

# Operator directive — 2026-05-05 auto-retrigger after quick focused cycles

## Verbatim

> "when you see you did a quick focused loop like this it could be relevant to automatically retrigger instead of wait.. is was so short and fast and now the real progress is kinf of postponed to the next loop because of this... its useless delay"

## Decomposition

### A — Quick focused loop pattern observed
- Cycle 12 made structural changes (3 file edits) but finished fast
- Agent immediately ScheduleWakeup'd at +90s
- Operator perception: real progress postponed; the +90s is useless delay

### B — Auto-retrigger heuristic
- When cycle was quick + focused → the agent should chain immediately
- Don't wait the standard 90s if more work is ready

### C — Useless delay framing
- Wakeup delays serve a purpose ONLY when:
  - operator may engage (give them a window)
  - cycle was substantive (give operator time to read)
  - no clear next-work without operator input (don't spam)
- When cycle was quick + clear next work + operator already engaged → delay is pure overhead

### D — Composes with SB-058 (close-pacing when engaged)
- SB-058 said: 90s close-pacing when operator engaged (vs 600s when away)
- This adds: when cycle was quick AND clear next work → chain immediately (effectively 0s delay)
- Pacing is now THREE-tier:
  - Operator away / cycle substantive: 600-1800s wakeup
  - Operator engaged / standard cycle: 90s close-pace
  - Operator engaged / quick cycle + work pending: chain immediately (this directive)

## Heuristics (preliminary — agent judgment)

| Cycle character | Pacing |
|---|---|
| Substantive design pass + needs operator review | 90s wakeup (give review window) |
| Quick mechanical fix + clear next-work + operator engaged | CHAIN immediately (this directive) |
| Idle / no clear pick / awaiting operator decision | 600s+ (don't spam) |
| Operator stepped away (no message in 5+ min) | 1200-1800s |

## Action plan

1. Log directive — done.
2. Add SB-068 to tracker.
3. Update loop-cron-lifecycle.md / cycle.md / dual-expert.md to capture the auto-retrigger heuristic.
4. Apply NOW: cycle 12 was quick + cycle 13 has clear pick (SB-057 phase A) + operator engaged → chain into cycle 13 in same turn.

## Cross-references

- SB-058 (close-pacing when engaged) — this directive layers on top
- SB-067 (cycle integration) — auto-retrigger is a pacing decision the cycle owns
- /root/.claude/rules/loop-cron-lifecycle.md (pacing rules home)
