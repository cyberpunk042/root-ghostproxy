---
title: "2026-05-05 — Design sketch: unified trigger model (F-eval-11 + SB-069 + SB-070 + F-eval-11)"
type: log
domain: cross-domain
status: draft
confidence: medium
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: f-eval-11-operator-observation
    type: directive
    file: /root/wiki/log/2026-05-05-hooks-commands-tools-chained-at-gates-starts-ends.md
  - id: sb-069-smart-pacing-hook
    type: directive
    file: /root/wiki/log/2026-05-05-smart-pacing-hook-concept-scalable-pattern-advanced-harness.md
tags: [log, design-sketch, trigger-model, signal-based-hooks, methodology-events, scalable-pattern, dual-expert-cycle-14, f-eval-11, sb-069, sb-070]
---

# Unified trigger model — design sketch (cycle 14)

> Preliminary design pass per operator observation 2026-05-05 (F-eval-11 — *"hooks → commands → tools chained at gates/starts/ends"*) + SB-069 (smart pacing hook) + SB-070 (scalable signal pattern). Three operator inputs converge to ONE trigger-model architecture. NOT implementation — sketch generates material for operator review.

## Convergence (why these three are one design)

| Operator input | Aspect of unified model |
|---|---|
| F-eval-11: "hooks/commands/tools at gates/starts/ends" | Trigger SOURCE catalog: which events can fire actions |
| SB-069: smart pacing hook (duration + output-size signals) | SIGNAL OBSERVATION layer: detect cycle character |
| SB-070: scale to compaction-prep, mode-switch, escalation, etc. | GENERALIZED dispatch: any observed signal → any bound action |

All three are layers of the same architecture: **observe events/signals → classify → dispatch bound action(s)**.

## Three layers

### Layer 1 — Event/Signal source catalog

Sources of triggers:

| Source category | Examples | Currently wired? |
|---|---|---|
| Claude Code lifecycle | SessionStart, SessionEnd, PreToolUse, PostToolUse, PostCompact, UserPromptSubmit | YES (5 events × 7 hooks at /root/.claude/hooks/) |
| Methodology lifecycle | stage-transition (document→design→scaffold→implement→test), readiness-threshold-cross (0%→25%→75%→100%), milestone-close, epic-close, module-close, task-close | NO (defined as scenarios in loop-cron-lifecycle.md L2/L3/L5; no wiring) |
| Cycle/loop lifecycle | cycle-start, cycle-end, quick-cycle-detected, idle-cycle, blocked-cycle | PARTIAL (loop-cron-lifecycle.md scenarios; no auto-fire) |
| Operational signals | cycle-duration, output-size, files-edited count, tokens-used, error-rate, time-since-last-operator-message | NO (no observation layer; SB-069) |
| Operator-explicit | /log invocation, /mode-* switch, /cycle invocation, manual /loop | YES (slash-command harness) |

### Layer 2 — Signal observation (the SB-069 layer)

A `tools/signals.py` (proposed) that:
- Observes cycle behavior: duration, edit-count, output-line-count, time-deltas
- Maintains a rolling window of recent cycles
- Classifies cycle character: quick / standard / substantive / idle
- Exposes JSON via `tools.signals --json` for hooks/commands to consume

Implementation sketch:
```python
# tools/signals.py
def observe_cycle(start_time, end_time, edits, output_lines):
    duration_s = end_time - start_time
    return {
        "duration_s": duration_s,
        "edits": edits,
        "output_lines": output_lines,
        "character": classify(duration_s, edits, output_lines),
    }
def classify(duration, edits, lines):
    if duration < 30 and edits < 3 and lines < 50: return "quick"
    if duration < 120 and edits < 6: return "standard"
    if duration > 120 or edits > 6: return "substantive"
    return "idle"
```

### Layer 3 — Trigger → command/tool dispatch (the F-eval-11 layer)

A binding registry (proposed at `wiki/config/triggers.yaml`) that maps events → commands:

```yaml
triggers:
  - event: stage-transition
    from: scaffold
    to: implement
    fires: /cycle  # full re-orient + verify gate
  - event: readiness-threshold-cross
    threshold: 75%
    fires: /progress  # surface near-completion state
  - event: cycle-character-quick + work-pending
    fires: chain-cycle-immediately  # SB-068 heuristic operationalized
  - event: cycle-character-substantive
    fires: schedule-wakeup-180s  # give review window
  - event: idle-cycle + no-operator-engagement-N=10
    fires: schedule-wakeup-1200s  # conserve cycles per L6
```

Detector mechanism:
- `tools/cycle.py` step 9 (already added) reads triggers.yaml + checks current state against bindings
- Fires bound commands via Skill tool / Bash invocation
- Logs each fire to `wiki/log/<date>-trigger-fires.md`

## Generalizability (SB-070)

Same architecture serves:
- **Pacing decisions**: cycle-character signal → wakeup-delay binding
- **Compaction-prep**: token-use threshold signal → checkpoint-write binding
- **Mode-switch suggestion**: activity-pattern signal → mode-suggestion binding
- **Escalation**: error-rate signal → operator-alert binding
- **Failure detection**: stagnation signal → audit binding
- **Stage gate auto-fire**: methodology stage-transition → gate-command binding

One mechanism, many applications. This is the "scale to other things" SB-070 named.

## Trade-offs

| Pro | Con |
|---|---|
| Unifies F-eval-11 + SB-069 + SB-070 into ONE coherent design | Significant surface area: tools/signals + triggers.yaml + dispatcher logic |
| Composable bindings — easy to add new event/action pairs | Risk of over-firing if bindings too broad |
| Signal observation enables emergent behaviors | Requires careful baseline definition (what's "quick" cycles?) |
| Methodology lifecycle gets structural fire-events | Methodology yaml stays simple; triggers yaml is the new surface |

## Open questions for operator

1. **Phasing**: implement Layer 1 (event catalog) first, OR Layer 2 (signal observation) first, OR Layer 3 (dispatch) first?
2. **Trigger fire authority**: agent fires bound commands autonomously, OR proposes-then-operator-approves first?
3. **triggers.yaml location**: `/root/wiki/config/` (with methodology yamls) OR `/root/.claude/triggers.yaml` (with active-mode)?
4. **Scope of initial implementation**: just pacing (SB-069 quickest path) OR full multi-application from day 1?
5. **Event taxonomy granularity**: per-stage transitions (5 stages = 4 transitions) vs per-readiness-step (4 thresholds)?

## Action plan (phased)

Per "take time to think about it" (operator's recurring framing for design-pass items):

- **Phase 0 (this sketch)**: register design + open questions for operator review.
- **Phase 1 (when operator approves)**: implement Layer 2 — `tools/signals.py` with cycle observation + classification.
- **Phase 2**: implement Layer 3 — `triggers.yaml` + dispatcher in `tools/cycle.py` step 9.
- **Phase 3**: implement Layer 1 — wire methodology lifecycle events into the dispatcher.
- **Phase 4**: extend bindings to compaction/mode-switch/escalation per SB-070.

Each phase = own SB or task; operator gates phase transitions.

## Cross-references

- F-eval-11 source observation: /root/wiki/log/2026-05-05-hooks-commands-tools-chained-at-gates-starts-ends.md
- SB-069 / SB-070 sources: /root/wiki/log/2026-05-05-smart-pacing-hook-concept-scalable-pattern-advanced-harness.md
- SB-068 pacing heuristic (rule-based; this sketch's signal observation would replace): /root/.claude/rules/loop-cron-lifecycle.md
- SB-057 directive registry sketch (parallel structural design): /root/wiki/log/2026-05-05-compound-waterfall-design-sketch-cycle-6.md
- /root/.claude/rules/hook-architecture.md (hook design pattern context)
- /root/wiki/config/methodology.yaml (methodology lifecycle source)
