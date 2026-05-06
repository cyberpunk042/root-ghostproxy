---
title: "2026-05-05 — Operator directive: input/output enhancement mode (toggleable, conditional) — context status at input, trail/stamp/status at end"
type: log
domain: cross-domain
status: active
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-io-enhancement-mode
    type: directive
tags: [log, operator-directive, sacrosanct, verbatim, io-enhancement, context-stamp, trail-stamp, status-block, toggleable-mode, conditional-mode, mode-composition]
---

# Operator directive — 2026-05-05 input/output enhancement mode

## Verbatim

> "Yeah that`s a new input. it might feel a like a bit of repetition but we can have an input and output enhancement mode that we can enable or disable and possible even make consitional such as when a mode is on an such. like a context status at input and a trail or stamp and status at the end"

## Decomposition

### A — Input-side enhancement: context status
- "context status at input"
- At the START of a response (when receiving operator input), agent shows its perception of state
- Compact stamp form: mode, cycle, loop state, open work counts, recent change

### B — Output-side enhancement: trail / stamp / status at end
- "a trail or stamp and status at the end"
- At the END of a response (or end of cycle), structured status block
- Counts of blocked + locations + verified-this-turn + next-pick

### C — Toggleable: enable/disable
- "enable or disable"
- Not always on; agent can turn it off when verbose-overhead isn't warranted

### D — Conditional: e.g., when mode is on
- "make conditional such as when a mode is on an such"
- Auto-enable when dual-expert / pm / architect modes active
- Auto-disable in no-mode state

### E — "A bit of repetition" (composition with SB-060/061)
- Operator notes this overlaps with prior SBs
- This is the FORMALIZATION of the prior style/status asks
- Compose with: SB-059 (blocker visibility), SB-060 (terminal style), SB-061 (end-of-cycle status block)

## Design (preliminary, deserves design pass)

### Toggle mechanism
- State file: `/root/.claude/io-enhancement` (similar to active-mode)
- Values: `on` / `off` / `auto` (auto = conditional on active-mode)
- Default: `auto`

### Input stamp format
```
[CONTEXT: mode=<mode> · cycle=<n> · loop=<state(+wakeup)> · open-SBs=<n> · pending-ops-decisions=<n> · just-added=<SB-XXX|none>]
```

### End-of-response status block format
```
═══════════════════════════════════════════════════════════
ROOT-GHOSTPROXY · END-OF-CYCLE STATUS · cycle <N> · <mode>
═══════════════════════════════════════════════════════════

LOOP        <alive|paused> · ScheduleWakeup +<delay> · <prompt>
MODE        <mode-name> · <persona-line>

BLOCKED · count · location
  pending-operator-decision  <n>   wiki/backlog/tasks/{...}.md
  open SBs                   <n>   wiki/governance/systemic-bugs.md (SB-IDs)
  recurring SBs              <n>   wiki/governance/systemic-bugs.md (SB-IDs)
  feature in-flight          <list with operator-gate notes>

VERIFIED THIS TURN
  <SB-id>  <one-line evidence>

NEXT PICK · cycle <N+1>
  systemic   <SB pick or "iterate through tracker">
  feature    <task pick or "operator-gated">

═══════════════════════════════════════════════════════════
```

### Conditional triggers
- mode=dual-expert → both stamp + block
- mode=pm-scrum-master → block (PM-emphasis)
- mode=devops-architect → block (Architect-emphasis with arch-specific fields)
- mode=none → off by default
- io-enhancement=on → forced on regardless
- io-enhancement=off → forced off regardless

## Action plan

1. Log this directive verbatim — done.
2. Add SB-062 to tracker.
3. Apply the pattern in current cycle (immediate; this turn already opens with stamp).
4. Author command: `/io-on` / `/io-off` / `/io-auto` (or extend existing /mode-* commands).
5. Author state file mechanism mirroring active-mode.
6. Update `tools/cycle.py` to emit the structured status block when invoked with `--status-block` flag (multi-consumer).
7. Iterate format per operator feedback over cycles.

## No-conflate guard

- "we can have" = OPTION grant, not mandate. Toggle exists; default may be `auto` or `off`.
- "it might feel a like a bit of repetition" = self-aware overlap with SB-060/061. The directive is to FORMALIZE the pattern as an enable/disable feature.
- "conditional such as when a mode is on an such" = modes auto-enable; other contexts opt-in.

## Cross-references

- SB-058/059/060/061 (close-pacing, blocker visibility, terminal style, end-of-cycle status)
- SB-057 (cumulation strategy — this directive demonstrates the pattern: prior + new layered)
- /root/.claude/active-mode (mechanism precedent)
- /root/wiki/governance/systemic-bugs.md (tracker)
