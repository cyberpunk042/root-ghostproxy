---
title: "2026-05-05 — Design sketch: compound + waterfall directive cumulation mechanism (SB-057)"
type: log
domain: cross-domain
status: draft
confidence: medium
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-compound-waterfall-cumulation-strategy
    type: directive
    file: /root/wiki/log/2026-05-05-compound-waterfall-strategy-cumulating-inputs.md
tags: [log, design-sketch, compound-waterfall, directive-cumulation, sb-057, preliminary, dual-expert-cycle-6]
---

# Compound + waterfall directive cumulation — design sketch (cycle 6)

> Preliminary design pass per operator directive 2026-05-05 (*"we can take the time to think about it.. it too will deserve its own tasks"*). NOT implementation. Sketch generates material for operator review + decision.

## Problem

Across this session 2026-05-05 (test cycle), the agent repeatedly:
1. Received operator directive A (with sacrosanct quote)
2. Received operator directive B (refining or extending A)
3. Acted on B in a way that DROPPED or DISMISSED A's substance
4. Operator caught the over-correction and re-asserted A

Examples:
- A = "you can autonomously cancel loops when context-logical" (2026-05-05 early)
- B = "WHY IS EVERYTHING SO FUCKING UNCLEAR... NO LOOP TO PROGRESS" (2026-05-05 later)
- Agent's bad action: removed A's permission entirely instead of refining the trigger
- Operator: "going to extremes... dismissing other of my sacrosanct words"

Multiple cycles of this pattern → ~10 distinct over-correction bugs (SB-033, SB-034, SB-040, SB-054).

## Design intent

A structural mechanism that:
- KEEPS earlier directive permissions active even when later directives refine them
- Makes the cumulative directive STACK visible per cycle
- Verifies any rule-edit doesn't dismiss prior sacrosanct grants
- Composes with existing rules (#6 comments-don't-deroute, #12 don't-dismiss-sacrosanct, work-mode "additive not destructive")

## Two semantics

### Compound (additive layering)
- Each new operator directive adds to the active stack
- Old directives REMAIN active unless explicitly superseded by operator
- Stack is read in entirety, not just the latest

### Waterfall (priority + refinement)
- Directives have ordering (chronological default; operator-priority override possible)
- Later directives can REFINE the application conditions of earlier ones (e.g., tighten triggers)
- Later directives CANNOT remove permissions granted earlier without explicit operator-supersede

The two semantics interact: compound preserves grants; waterfall handles refinement-vs-overwrite.

## Proposed mechanism

### Layer 1 — Directive registry (data layer)

A registry at `/root/wiki/governance/directives.md` listing all operator-sacrosanct directives currently in effect:

```yaml
- id: D-2026-05-05-001
  date: 2026-05-05
  verbatim_file: /root/wiki/log/2026-05-05-loop-cron-lifecycle-policy-blockers-tools-and-bulletproof-mvp-directive.md
  status: active                      # active / refined / superseded
  refined_by: [D-2026-05-05-014]      # if refined
  superseded_by: null
  permissions_granted:
    - autonomous-loop-cancellation-when-context-logical
    - blocker-tool-augmentation
  triggers_refined:
    - "L4 trigger: workstream-caught-up alone is INSUFFICIENT (per D-2026-05-05-014)"
  notes: |
    Permission to autonomously cancel loops with hard ruling. Refined by D-...014:
    workstream-caught-up alone is not enough; needs operator-confirmed target + N stable cycles.
- id: D-2026-05-05-014
  ...
```

### Layer 2 — Tool (read/query layer)

`tools/directives.py`:
```
python3 -m tools.directives list                  # all active directives
python3 -m tools.directives stack                 # cumulative stack with refinements visible
python3 -m tools.directives check --rule <file>   # before editing <file>, list directives affecting it
python3 -m tools.directives diff <id-a> <id-b>    # show how B refines/relates to A
```

### Layer 3 — Pre-edit hook (verification layer)

Hook that fires on Edit/Write to `/root/.claude/rules/*.md` or other directive-bearing files:
1. Run `tools.directives check --rule <target>`
2. If any active directive grants permissions related to the rule: surface to agent
3. Agent must acknowledge: "this edit refines triggers / does NOT remove permissions" before proceeding
4. If edit DOES remove permissions: requires explicit `OPERATOR_SUPERSEDE_DIRECTIVE=<id>` env var

### Layer 4 — Cycle integration

Each /cycle fire reads the directive stack as part of orientation:
- "Active directives: 14 (3 compound, 11 refined)"
- Surfaced if the cycle's pick conflicts with a directive

### Layer 5 — Compose with rules

- Operating-principles.md #6 (comments don't deroute) → compound semantic
- Operating-principles.md #12 (don't dismiss sacrosanct via over-correction) → waterfall semantic
- Work-mode.md "additive, not destructive" → both
- Hard Rule #4 (operator words sacrosanct) → underlies all of it

## Trade-offs

| Pro | Con |
|---|---|
| Structural prevention of dismissal pattern | Adds tool + hook surface area |
| Visible directive stack per cycle | Maintenance: registry must stay in sync with /root/wiki/log/ |
| Verification step before rule edits | Slows down rule edits (intentional, but friction) |
| Cross-session retention | Pre-edit hook could over-fire if registry misclassifies |
| Composable with existing rules | New abstraction layer to learn |

## Open questions for operator

1. **Registry maintenance**: agent-authored from /root/wiki/log/ scan, OR operator-curated? Hybrid?
2. **Refinement granularity**: directive-id level, or sub-clause (specific permission/trigger)?
3. **Supersede mechanism**: explicit operator quote required ("supersede D-..."), or implicit via newer directive?
4. **Pre-edit hook strictness**: warn-only (advisory) vs deny-by-default (enforced)? Per `operating-principles.md` strictness graduation.
5. **Cross-project**: should second-brain have a parallel directive registry for ITS cumulation? Operator hinted at this.

## Action plan

1. Sketch reviewed by operator (this file).
2. If approved direction: incremental implementation
   - Phase A: registry data layer (manual curation initially)
   - Phase B: tools/directives.py read-only commands
   - Phase C: pre-edit hook (advisory tier first)
   - Phase D: cycle integration
   - Phase E: cross-project (second-brain) extension via gateway contribute
3. Each phase = its own SB or task; operator gates phase transitions.

## Cross-references

- /root/wiki/log/2026-05-05-compound-waterfall-strategy-cumulating-inputs.md (the directive)
- /root/wiki/governance/systemic-bugs.md SB-057
- /root/.claude/rules/operating-principles.md #6, #12
- /root/.claude/rules/work-mode.md "Additive, not destructive"
