---
title: "2026-05-05 — Operator directive: register-and-do-something + smart pacing hook (duration+output-size signals) + scalable pattern + advanced harness framing"
type: log
domain: cross-domain
status: active
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-smart-pacing-hook-and-advanced-harness
    type: directive
tags: [log, operator-directive, sacrosanct, verbatim, smart-pacing-hook, signal-based-hook, duration-size-signals, scalable-pattern, advanced-harness-config]
---

# Operator directive — 2026-05-05 smart-pacing-hook + scalable pattern + advanced harness framing

## Verbatim (4 messages, same turn)

> "again... its important to register this kind of comment and do something about... not that you were not a bit on track already. continue"

> "it could even mean a potential smart hook that look at the duration and the size of outputs and such"

> "which can also scale to other things now or in the future"

> "this is going to be a very advanced harness configuration project"

## Decomposition

### A — Register-and-do (re-emphasis of #6 + register-first)
- "its important to register this kind of comment and do something about"
- Operator catching me partial: I did register (SB-068 + log + rule update) but the depth was incomplete
- Pattern: register verbatim → decompose → apply → continue. Don't half-step.

### B — Smart pacing hook concept (NEW)
- "a potential smart hook that look at the duration and the size of outputs and such"
- A hook that observes signals (duration of operation, size of output) and uses them to make pacing decisions
- Beyond rule-text "if cycle was quick" — a structural mechanism that DETECTS "quick" empirically

### C — Scalable pattern (NEW)
- "which can also scale to other things now or in the future"
- Signal-based decision-making isn't limited to pacing
- Other applicable contexts: when to trigger compaction-prep, when to defer to second-brain, when to escalate to operator, when to pause vs continue, when to switch modes
- This is a meta-pattern: "agent observes its own behavior signals and adapts"

### D — Advanced harness configuration project (FRAMING)
- "this is going to be a very advanced harness configuration project"
- Operator framing: this isn't a basic project — it's a sophisticated harness-configuration project
- Embraces complexity; expect substantial harness-side mechanisms (hooks, tools, modes, signals)
- Implies: agent can/should design ambitiously within bounds

## Design space (preliminary)

### Smart pacing hook — concept

A hook (potentially PostToolUse or a new event) that:
- Observes signals: tool-call duration, output line-count, files-edited count, time-since-last-operator-msg
- Computes a "cycle character" classification (quick / standard / substantive / idle)
- Suggests pacing (chain-now / 90s-wakeup / 600s-wakeup / pause)
- Optionally: writes the suggestion to a state file the agent reads at end-of-cycle

### Scalable to other things

Same signal-observation pattern could drive:
- **Compaction-prep**: when total session token-use crosses threshold → auto-condense state into checkpoint
- **Second-brain deferral**: when /root work touches second-brain-territory → flag for contribute path
- **Mode-switch suggestion**: when activity pattern doesn't match active mode → suggest switch
- **Operator-escalation**: when N consecutive cycles produce no progress → flag for help
- **Failure-detection**: when error-rate spikes → invoke audit / recovery

### Advanced harness configuration

The systemic surface area:
- Hooks (currently 7 fires across 5 events) — could grow with smart hooks
- Tools (state/blockers/progress/decisions/cycle/tasks/mcp_server) — could grow with signal-aware tools
- Modes (3) — could grow with conditional/composed modes
- Commands (14) — could grow with smart-pacing-aware commands
- Skills (2) — could grow with auto-trigger skills
- Settings.json permissions / hooks — sophisticated configuration

## Action plan

1. Log this directive verbatim — done.
2. Add SB-069 (smart pacing hook concept) and SB-070 (scalable signal-pattern direction) to tracker.
3. Sketch design at high level (this log) — implementation deferred per SB-057 pattern (operator: "take time").
4. Continue current loop pacing per SB-068 heuristic (rule-based) until smart hook implementable.

## Cross-references

- SB-058 (close-pacing) + SB-068 (auto-chain quick cycles) — smart pacing hook would automate these
- SB-057 (compound+waterfall) — same "take time" design-pass discipline applies
- F-eval-11 (trigger-model unification) — adjacent: triggering events from signals
- /root/.claude/rules/loop-cron-lifecycle.md (current rule-based pacing home)
- /root/.claude/rules/hook-architecture.md (hook design pattern)
