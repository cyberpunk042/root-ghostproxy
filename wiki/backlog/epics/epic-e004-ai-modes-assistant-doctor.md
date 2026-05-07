---
title: "Epic E004 — AI Modes Assistant ('doctor' watchdog) for mode enforcement + loop health detection"
type: epic
status: document-stage
priority: P3
parent_milestone: v0.2-ai-natural-task-management
current_stage: document
readiness: 5
created: 2026-05-07
sources:
  - id: operator-directive-2026-05-07-ai-modes-assistant
    type: directive
    quote: '"we can probably add an AI Modes Assistant that help to enforce the mode and help with the tracking and the progress and detect when there is no stamp update or when the AI is in a recursive or needless endless loop or such. A bit like the doctor notion in the second-brain and openfleet I guess. We can take the time to create an EPIC and think about it... if we are in a mode and its been X tiem and or X prompts that the stamp didn`t diff even one bit... with hhoks and all"'
tags: [epic, draft, ai-modes-assistant, doctor-pattern, watchdog, loop-health, mode-enforcement, stamp-diff-detection, recursive-loop-detection]
---

# Epic E004 — AI Modes Assistant ("doctor" watchdog)

> **Agent-DRAFT v1 per SB-095** — operator-directed Epic-level scope. Operator-revisable.

## Summary

A "doctor"-pattern watchdog inspired by the second-brain + openfleet implementations. Continuously monitors the active autopilot loop's health — enforces mode discipline, tracks progress signals, and DETECTS pathological loop conditions (stamp-no-diff over time/prompts; recursive cycles; endless meta-treadmill per SB-140; agent-self-imposed-false-gates per clause #8). Surfaces alerts to operator when health degrades. Compounds with existing mode-enforcement.sh + mindfulness.sh hooks but operates at a HIGHER tier (per-loop-window observation, not per-prompt reminder).

## Mission

Make the SB-140 frozen-loop / agent-self-imposed-false-gates pattern **structurally impossible** to recur silently. Operator's framing: *"that should never happens. shold not even be possible..."*. The doctor is the mechanism that catches what mindfulness clause-reminders alone can't — pattern-detection across time-windows.

## Operator directive (verbatim, sacrosanct)

> *"we can probably add an AI Modes Assistant that help to enforce the mode and help with the tracking and the progress and detect when there is no stamp update or when the AI is in a recursive or needless endless loop or such. A bit like the doctor notion in the second-brain and openfleet I guess. We can take the time to create an EPIC and think about it... if we are in a mode and its been X tiem and or X prompts that the stamp didn't diff even one bit... with hhoks and all"*

## Suggested module decomposition (DRAFT — operator-revisable)

### M-E004-1 — Research: doctor pattern (second-brain + openfleet) [document-stage]

Cross-project research-first per operating-principles.md #5. Read:
- `<second-brain>/wiki/...` — find the "doctor" notion implementation + framing
- `~/openfleet/...` — find the openfleet doctor pattern
- Synthesize the canonical pattern (signals · detection windows · alert mechanism · recovery loop)
- Author research-synthesis at `wiki/log/<ts>-doctor-pattern-research.md`

Sub-agent dispatch: Explore agent for cross-project read + synthesis.

### M-E004-2 — Stamp-diff watchdog [scaffold-stage; gated on M-E004-1]

Detect: stamp content unchanged across N consecutive cron-fires OR T elapsed time.
- Read `/tmp/.end-of-cycle-stamp-row-hashes.json` (per SB-136 row-hash cache)
- Compare across fires; if no diff for N=5 fires OR T=10 minutes → alert
- Hook layer: extend Stop hook OR new dedicated PostToolUse/Stop watchdog hook
- Tool layer: `tools/doctor.py` with `--check-stamp-diff`, `--alert-thresholds N T`

### M-E004-3 — Recursive/meta-loop detection [scaffold-stage; gated on M-E004-1]

Detect: same action-type emitted N times consecutively without diversity (anti-pattern from SB-140 loop run — F12-F16 = 5 consecutive sb-closures, F2-F11 = mostly meta-edits).
- Parse cycle-report last-line `Productive output: <type>` across recent fires
- If same type N>3 consecutive → flag for operator-attention
- If META-LAYER substance N>X consecutive without PROJECT-LAYER → SB-140 alert
- Layer: extend Stop hook OR new doctor-loop hook

### M-E004-4 — Mode-enforcement watchdog [scaffold-stage; gated on M-E004-1]

Detect: mode set but cycle/output-pattern doesn't match mode persona. E.g., dual-expert mode active but only one lens used per cycle for N consecutive fires.
- Hook reads mode-enforcement banner output history
- Compare against expected dual-lens cadence
- Alert if drift detected

### M-E004-5 — Progress-signal tracking [scaffold-stage; gated on M-E004-1]

Detect: `tools.progress` output stagnant across N fires (no readiness change · no module-status flip · no task-status flip · no decisions appended).
- Per-fire snapshot of progress.json output
- Diff snapshot N→N+1; flag if zero progress over N=10 fires
- Compounds with M-E004-2 stamp-diff (different signal: stamp = state visualization; progress = backlog state)

### M-E004-6 — Alert/recovery surface [scaffold-stage; gated on M-E004-2/3/4/5]

When watchdog detects pathology:
- Emit explicit operator-alert via `additionalContext` JSON (PostToolUse hook OR systemMessage layer)
- Format: `DOCTOR ALERT: <pattern> detected — <evidence> — recovery: <suggested-direction>`
- Optional: auto-cancel cron loop after N alerts unanswered (per loop-cron-lifecycle.md L1-L7)
- Operator can `/doctor-status` slash command to query state

### M-E004-7 — Doctor-config schema + slash commands [scaffold-stage; gated on M-E004-2/3/4/5]

Per pathway D7 artifact-preparation:
- `~/.claude/doctor-config.json` — thresholds (N fires, T elapsed, alert frequency)
- Slash commands: `/doctor-status` · `/doctor-thresholds <key> <value>` · `/doctor-pause` · `/doctor-resume`

### M-E004-8 — Tests + operator-empirical verification [test-stage; gated on M-E004-2-7]

Regression tests + operator-empirical sign-off.

## Open structural questions (operator scope-direction needed)

| Q | Question | Default per pathway D6 |
|---|---|---|
| Q1 | Which mechanism layer fires the watchdog — Stop hook (per-cycle) OR PostToolUse (per-action) OR independent cron (parallel observer)? | Stop hook (per-cycle) — natural cadence boundary |
| Q2 | Alert delivery — `systemMessage` to operator OR slash-command-pull (operator queries on demand) OR both? | Both — push for severe; pull for routine |
| Q3 | Auto-cancel-cron after N alerts unanswered — agent-authority? | Per loop-cron-lifecycle.md L1-L7 — operator-greenlit per scenario |
| Q4 | Compound axis — does doctor SHOW in stamp / mode-enforcement banner / new dedicated banner? | New dedicated row in stamp; OR new UserPromptSubmit hook with doctor-status banner |
| Q5 | Cross-project parity — does $HOME author canonical implementation, /opt second-brain inherit (per Hard Rule 12)? OR is /opt's doctor canonical and $HOME inherits? | Operator-decision; second-brain pre-existed so likely /opt canonical, $HOME inherits |

## Composition with existing layers

- **Mindfulness.sh** (per-prompt reminder, 8 clauses) — proactive baseline
- **Mode-enforcement.sh** (per-prompt persona injection) — proactive mode discipline
- **Output-discipline-guard.sh** (per-prompt anti-pattern detection) — reactive narrow trigger
- **End-of-cycle-stamp.sh** (per-Stop event state visualization) — passive surface
- **AI Modes Assistant / doctor (THIS Epic)** — temporal-window pattern detection over multiple fires
- **Loop-cron-lifecycle rule** — when to autonomously cancel (L1-L7 scenarios)

The doctor adds the TIME-WINDOW observation tier that single-prompt hooks can't see. Compounds, doesn't replace.

## Verification gate (when this Epic is "done")

- Doctor detects SB-140-pattern recurrence within N=5 fires (empirical: re-run a 18-fire meta-loop scenario; doctor alerts BEFORE operator catches it)
- Doctor detects stamp-no-diff over operator-set thresholds
- Doctor surfaces clear recovery direction
- Operator-empirical confirmation across 2-3 work-blocks

## Cross-references

- SB-140 (the bug this Epic structurally fixes): `wiki/governance/systemic-bugs.md`
- Mindfulness clause #8 (rule-layer mitigation): `.claude/hooks/mindfulness.sh`
- Loop-cron-lifecycle: `.claude/rules/loop-cron-lifecycle.md`
- Iterative-evolution-pathway D5+D9: `.claude/rules/iterative-evolution-pathway.md`
- Second-brain doctor pattern (research needed M-E004-1): `<second-brain>/wiki/...` — Explore-agent dispatch
- Openfleet doctor pattern (research needed M-E004-1): `~/openfleet/...` — Explore-agent dispatch
- Active milestone v0.2: `wiki/backlog/milestones/v0.2-ai-natural-task-management.md` — E004 joins E001/E002/E003
- M-E001-1 productive-cycle action vocabulary (consumed by M-E004-3 recursive detection): `wiki/log/2026-05-06-181500-auto-pilot-action-vocabulary-draft.md`
