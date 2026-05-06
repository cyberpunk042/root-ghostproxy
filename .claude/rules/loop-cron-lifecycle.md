# $HOME/.claude/rules/loop-cron-lifecycle.md — When agent may autonomously stop/update a loop or cron

> Loaded on demand when a loop/cron is firing AND the agent considers cancellation or modification. Per operator directive 2026-05-05 (sacrosanct, autonomous-management permission): *"when its really logical to remove or even possibly update a loop/cron you can but it has to be probably bound to some hard ruling about that it has to make sense in the context and be relative... lets continue till this feel like a proper bulletproof MVP."*
>
> **TRIGGER REFINEMENT 2026-05-05** per operator correction: the autonomous-cancellation PERMISSION (above) stands. The bug was the TRIGGERS — specifically L4's "workstream caught up" was activated by an "MVP target hit" assessment that was premature, killing the loop while iteration was still meaningful. Operator: *"WHY IS EVERYTHING SO FUCKING UNCLEAR... NO LOOP TO PROGRESS AND FIX THE SYSTEMTIC BUGS AND START WORKING AND EVOLVING IN ITERATION"*. Fix: keep the autonomous-cancellation option, but TIGHTEN the triggers so the loop runs longer through accumulating findings + iteration. Operator-absent-for-long is still a valid cancellation case (L6 N=30); workstream-caught-up alone is NOT (operator wants iteration to continue surfacing batches).

## The hard ruling (context-logical autonomous management)

The agent MAY autonomously call `CronDelete` or `CronUpdate` (or stop a self-paced `/loop`) **only when** ALL of these hold:

1. **A documented scenario applies** (see § Scenarios below)
2. **The scenario is currently TRUE in the live state** — not theoretically true; verifiable via `tools.state` / `tools.blockers` / `tools.progress`
3. **The active mode supports the scenario** — see § Mode-dependent gating
4. **The action is logged** — append a line to `wiki/log/<date>-cron-lifecycle.md` capturing: cron ID, action, scenario invoked, evidence, mode at time of action
5. **The agent reports the action to the operator** — silently cancelling a cron is forbidden; tell the operator what was done + why + how to re-arm

If ANY of these fail: do NOT autonomously cancel. Surface the situation to the operator + let them decide.

## Scenarios — the registered conditions for autonomous cancellation/update

### Scenario L1 — Completely blocked

**Trigger**: `tools.blockers --check` reports >0 active blockers AND `tools.progress --json` shows zero claimable tasks AND zero in-progress tasks AND no decisions resolved in the last N cycles.

**Action (default)**: KEEP loop running; cycle content shifts to surfacing the blockers + suggesting operator-decisions. The loop's value when blocked is to keep findings accumulating + surface batches.

**Cancel (rare)**: only on explicit operator direction. Autonomous cancellation here was the source of the 2026-05-05 dead-loop bug.

**Recovery**: keep iterating; when blocker resolves, the cycle naturally returns to feature work.

### Scenario L2 — Stage transition

**Trigger**: `tools.progress` shows a SFIF stage transition since the last cycle (e.g., Scaffold → Foundation, Foundation → Infrastructure, etc.).

**Action**: PAUSE the cron (don't delete) for one operator turn; surface "stage transition detected; pausing autopilot for re-orient + mode re-evaluation." Operator decides: resume, switch mode, or stop entirely.

**Recovery**: operator confirms; resume via `CronUpdate` or new `CronCreate`.

### Scenario L3 — Milestone transition

**Trigger**: active milestone in `progress.md` advanced (e.g., v0.1 → v0.2).

**Action**: PAUSE autopilot; surface the milestone transition + reset the cycle frame; operator picks new mode for the new milestone phase.

### Scenario L4 — Mode-relevant state shift

**Trigger refinement (per 2026-05-05 correction)**: "workstream caught up" was previously triggering on agent self-assessment of "MVP target hit" — that's INSUFFICIENT. The valid trigger is now stricter: workstream-caught-up + operator-explicitly-confirmed-the-target-state + N consecutive cycles with no new findings. Workstream-caught-up alone keeps the loop running because iteration through accumulating findings is itself valuable.

**Trigger (PM mode example, REFINED)**: all active blockers resolved + 0 new blockers in last 3+ cycles + operator has confirmed workstream-target-met + no new operator directives in those cycles.

**Action (default — when refined trigger NOT met)**: KEEP loop running; cycle content suggests `/mode-architect` to operator (lens shift). Operator switches mode if/when they want; the loop self-pacing continues.

**Action (when refined trigger met)**: autonomous cancel is permitted per operator's 2026-05-05 grant; report per § Reporting protocol. Lessons-learned log retains the cancellation reasoning for audit.

**Trigger (Architect mode example, REFINED)**: current SFIF stage's last in-progress task transitioned to done + no claimable next-step tasks within mode scope + operator has confirmed stage-complete + N cycles of stability.

**Anti-pattern (the 2026-05-05 dead-loop bug)**: agent self-assessing "MVP target hit" or "workstream done" without operator confirmation, then cancelling the cron. This kills iteration. The corrective: tighter triggers above.

### Scenario L5 — Readiness threshold cross

**Trigger**: epic readiness crosses 0%→25% or 75%→100% threshold (per methodology engine's stage definitions).

**Action**: PAUSE autopilot; surface the threshold cross + recommend mode/cycle adjustment.

### Scenario L6 — Operator absence ceiling

**Trigger**: N consecutive cron firings without operator interaction (operator-absent for prolonged period).

**Action** (per ceiling — operator-configurable):
- N=10 cycles: warn operator (one-time message: "You haven't interacted in 10 cycles; the autopilot can stop if you want to come back fresh.")
- N=20 cycles: pause (preserve cron job; don't fire until operator returns)
- N=30 cycles: cancel (stop the cron job entirely)

This is the only scenario where autonomous cancellation happens WITHOUT a productive context-logical reason — purely a cost-management measure.

### Scenario L7 — Pre-compact conservation

**Trigger**: agent's context approaching compaction (pre-compact event signals).

**Action**: PAUSE autopilot for the compaction event; resume after PostCompact hook re-orients.

## Mode-dependent gating

Each mode has its own evaluation lens. A scenario triggers in one mode might NOT trigger in another:

| Scenario | PM Scrum Master | DevOps Architect | Dual Expert |
|---|---|---|---|
| L1 (completely blocked) | KEEP running by default; surface blockers each cycle | KEEP running; same | KEEP running; both lenses |
| L2 (stage transition) | PAUSE for one cycle; surface; operator decides resume/switch | PAUSE; surface | PAUSE; surface |
| L4 (workstream-idle, REFINED trigger) | KEEP running unless refined trigger met (operator-confirmed target + N stable cycles); only then autonomous cancel | Same | Same — both lenses must be at refined trigger |
| L6 (operator absent N=30) | Autonomous cancel permitted per operator's grant | Same | Same |
| L7 (pre-compact) | Pause across all modes | Same | Same |

## What is NEVER autonomously cancellable

- Loops with explicit operator-set non-expiring intent (rare; operator-flagged)
- Loops that ARE the work (e.g., a long-running data sync that is the deliverable; not applicable in $HOME currently)
- Hooks (hooks are not loops; never autonomously remove hooks)

## Reporting protocol

When agent autonomously cancels/updates a loop, the same response message MUST contain:
1. **What was done**: "Cancelled cron `<id>`" / "Updated cron `<id>` to <new-config>" / "Paused autopilot"
2. **Why (scenario invoked)**: e.g., "Scenario L1 — completely blocked: 6 active blockers, 0 claimable tasks, 0 progress in last 3 cycles"
3. **Evidence**: tool output snippet (e.g., `tools.blockers --check` exit code; `tools.progress --json` excerpt)
4. **Mode at time of action**: from `tools.state --field active-mode`
5. **Recovery instructions**: how operator re-arms ("`/loop 30m /cycle`" or "`/mode-pm` then re-arm")
6. **Log file path**: where the action was recorded for audit (`wiki/log/<date>-cron-lifecycle.md`)

## Operator opt-in (future feature)

Per operator directive: *"voluntered opt in at the install for the hooks"*. When M003 install.sh lands, it can offer:

```
[?] Enable agent-autonomous cron cancellation per loop-cron-lifecycle.md? [Y/n]
    Y = agent may stop/update loops when scenarios L1-L7 apply
    n = agent always asks operator first; never autonomously cancels
```

Default until operator-config is captured: agent uses this rule conservatively (asks for first cancellation; takes autonomous action on subsequent ones with clear reporting).

## Pacing heuristic (per SB-058 + SB-068, operator directives 2026-05-05)

The wakeup delay isn't fixed — the agent picks per-cycle based on context:

| Cycle character | Pacing | Rationale |
|---|---|---|
| Substantive design pass / new directive registered / needs operator review | 90-180s wakeup | Give operator a review window before next fire |
| Standard cycle / operator engaged / no urgent next-work | 90s wakeup (close-pace per SB-058) | Responsive without spamming |
| **Quick focused cycle + clear next-work + operator engaged** | **CHAIN immediately (per SB-068)** — skip wakeup delay; do cycle N+1 in the same turn OR set wakeup to 60s floor | Avoid useless delay; "real progress was postponed" pattern |
| Idle / no clear pick / awaiting operator decision-with-no-info | 600s+ wakeup | Don't spam |
| Operator stepped away (no message in 5+ min) | 1200-1800s wakeup | One cache miss buys real wait |
| Pre-compact event signaled | Pause (per L7) | Conserve through compaction |

**Quick-cycle detection**: cycle made <3 substantial edits, no operator-direction-pending output, clear next-pick already named in tracker → chain.

**Operator override**: operator can always set explicit cadence with `/loop <interval> /cycle`; the auto-chain heuristic only applies in dynamic-mode self-pacing.

## Cross-references

- Methodology engine (stage gates): `$HOME/wiki/config/methodology.yaml`
- Tools that drive evaluation: `tools.state`, `tools.blockers`, `tools.progress`
- Modes (per-mode cycle definitions): `$HOME/.claude/modes/<mode>.md`
- Determinism ladder: `$HOME/.claude/rules/hook-architecture.md`
- Operator directive (sacrosanct primary source): `$HOME/wiki/log/2026-05-05-loop-cron-lifecycle-policy-blockers-tools-and-bulletproof-mvp-directive.md` (also pre-existing copy at /opt/.../raw/notes/)
- SB-058 close-pacing: `$HOME/wiki/log/2026-05-05-close-timing-clear-blocker-output-style-and-end-of-cycle-status.md`
- SB-068 auto-retrigger: `$HOME/wiki/log/2026-05-05-auto-retrigger-after-quick-focused-cycles.md`
