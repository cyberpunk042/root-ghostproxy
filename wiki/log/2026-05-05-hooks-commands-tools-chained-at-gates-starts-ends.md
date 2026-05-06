---
title: "2026-05-05 — Operator observation: hooks → commands → tools chain at gates/starts/ends (unified trigger model)"
type: note
domain: cross-domain
status: raw
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-hooks-commands-tools-gate-trigger-pattern
    type: directive
tags: [note, operator-directive, sacrosanct, verbatim, hooks, commands, tools, determinism-ladder, gate-hooks, methodology-events, lifecycle-events, unified-trigger-model]
---

# Operator observation — 2026-05-05 hooks → commands → tools chained at gates/starts/ends

## Verbatim

> "somehow its a bit like the hook start and such we can even use commands and then also tools when needed.. sometimes triggered at gates or starts and end or such."

## Decomposition

### A — The pattern observed
- "its a bit like the hook start and such" → hooks (e.g., SessionStart) fire and direct.
- "we can even use commands" → from a fire, a COMMAND can be invoked (already happens: SessionStart → /orient).
- "and then also tools when needed" → and from a command, TOOLS can be called (already happens: /cycle → tools.cycle).
- "sometimes triggered at gates or starts and end or such" → trigger surface extends beyond Claude Code lifecycle:
  - **Gates** — methodology stage gates (document → design → scaffold → implement → test transitions)
  - **Starts** — start-of-anything (session, epic, milestone, module, task, work-block)
  - **Ends** — end-of-anything (session, epic, milestone, module, task, cycle)

### B — What this means architecturally
The determinism ladder is:
```
Event (hook OR methodology-gate OR milestone-edge)
  → Command (deterministic workflow)
    → Tools (deterministic atomic operations)
```
Currently wired:
- Claude Code `SessionStart` hook → `/orient` command → Reads + Bashes
- Claude Code `PostCompact` hook → `/orient` command
- Operator-typed `/cycle` command → `tools.cycle`
NOT wired (gap surfaced by this observation):
- Methodology stage transition (`document → design`, etc.) → no command auto-fires
- Milestone close → no command auto-fires
- Epic close → no command auto-fires (T061 is a TASK, not a triggered hook)
- Module close → no command auto-fires

### C — What "gate hooks" could look like (preliminary, no implementation yet)
- A meta-hook layer in `tools.cycle` (or new `tools.gate-detect`) that compares previous-state vs current-state per cycle:
  - Detects `stage_transition` events
  - Detects `milestone_close` events
  - Detects `epic_close` events
  - Detects `readiness_threshold_cross` events (already partly in loop-cron-lifecycle.md L5)
- Each event-type maps to a command via methodology config:
  - `methodology.yaml` could declare `events: { stage_transition: /<command>, milestone_close: /<command>, ... }`
  - Triggered fire calls the command + logs the trigger to a gate-events log
- Backstop: nothing fires destructively; gate-hook runs in observation/report mode first; operator approves promotion to fire-actual-action.

### D — Adjacency to existing structures
- `loop-cron-lifecycle.md` already defines scenarios L2/L3/L5 (stage transition, milestone transition, readiness threshold cross) — those are EVENT DEFINITIONS without bound commands. This observation suggests binding commands to them.
- `methodology.yaml` has `end_conditions` top-level key — could be the natural home for the event→command map.
- `wiki/governance/progress.md` planning section sketches future milestones — milestone-close detection is plausible.

## Action plan

1. Log this observation verbatim — done (this file).
2. Add F-eval-11 to iteration log.
3. **Do NOT implement** — preliminary scope only per operator directive 2026-05-05 ("not for development but only for doing the preliminary part").
4. Surface for operator-batch decision: should this become module M015 (gate-hooks / methodology-event-driven commands)? Or extend M013 (modes)? Or extend M004 (infrastructure tooling)?
5. Research-first if pursued: check Claude Code's hook events catalog (SessionStart/End, PreToolUse, PostToolUse, PostCompact, UserPromptSubmit are known; verify exhaustive set) before proposing event taxonomy.

## No-conflate guard

- "somehow its a bit like" = OBSERVATION, comparing patterns. Not a directive to implement.
- "sometimes triggered at gates or starts and end or such" = describing a possibility space, not a spec.
- "or such" = open-ended; let operator define the bounded set in a follow-up if pursued.
- Per "I specifically ask not for development but only for doing the preliminary part" (still binding from earlier this turn): this is preliminary surfacing, not implementation.
- Per "comments... not to deroute" (still binding): integrate as additive context, do not break iteration flow.
