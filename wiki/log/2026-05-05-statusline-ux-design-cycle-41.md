---
date: 2026-05-05
slug: statusline-ux-design-cycle-41
tags: [m011, ccstatusline, ux-design, statusline, sb-080, sb-082]
---

# Statusline UX Design — Cycle 41 / 41.5

## Why this log exists

Operator's verbatim cycle 41:

> "are you supposed to have updated the statusline ? I didn't any change btw.. still the same weird behavior on the third line and the lack of aligment and refine UX Design. take your time to do this right."

> "intermediary for example can be only two column instead of 3 and base only 1 column and both will obviously evolve too. the base and intermediary has probably evolved. and not only the third line you can fine-tune.."

> "better but we can continue to properly balance, fine-tune and properly render all this. like the third line has a weird spacing at the ned and things could be better aligned and such"

> "in the statusline too not everything need to be minimized.. like Bk is probably blocker and would look fine in its long form"

> "you went to the other extreme again.. a recurrent issue."

> "you dont need my go to fix the status bar I already told you what I needed... and you can even see the output..."

These directives drove cycle 41/41.5 statusline rewrites. This log captures the design intent so future cycles don't drift from it (counter-pattern to SB-077 deliver-before-spec).

## Information architecture (3 profiles)

| Profile | Columns/line | Lines | Audience | Identity |
|---|---|---|---|---|
| **base** | 1 (no flex) | 2 | LLM-billing minimal | model + ctx + speed / usage + resets |
| **intermediary** | 2 (1 flex) | 3 | AIDLC-aware | mode/task \| stage/readiness/blockers · model \| ctx/usage · git \| compact/cwd |
| **full-aidlc** | 3 (2 flex) | 3 | comprehensive | per-line breakdown below |

Per operator's cycle 41 directive: column count escalates with profile tier (base=1, intermediary=2, full-aidlc=3).

## Full-aidlc per-line design

### Line 1 — AIDLC project state

```
Mode: <mode-name>  │  Task: T### slug [readiness%]      SFIF: <tier>  ·  Stage: <stage>  ·  Model: <method-model>  ·  Readiness: %      Blockers: N  │  Bugs: open/recurring  │  Tasks: done/in-progress/not-started
```

| Zone | Widgets | Identity |
|---|---|---|
| LEFT (primary) | Mode + Task | what's the agent doing right now |
| MIDDLE (context) | SFIF + Stage + Model + Readiness | where in the lifecycle is the work |
| RIGHT (counters) | Blockers + Bugs + Tasks | what's outstanding / what's progress |

Separators: `│` between zones (heavy boundary), `·` within zone (light intra-group). Bold on Mode + Task + Blockers (priority signals).

### Line 2 — LLM session

```
Session-name  ·  Model: Opus 4.7  ·  Thinking: <effort>      [ctx bar]  <ctx%>      tokens-in tokens-out tokens-cached  ·  total-speed  ·  vim-mode
```

| Zone | Widgets | Identity |
|---|---|---|
| LEFT | Session-name + Model + Thinking | what model & effort |
| MIDDLE | ContextBar + Context% | how much context used |
| RIGHT | Tokens (in/out/cached) + Speed + Vim | session telemetry |

Separators: `·` everywhere (uniform — session info is a single semantic group).

### Line 3 — Engineering / DevOps

```
⎇ branch  status  ahead-behind  sha       Session: usage  ·  Weekly: usage  ·  $cost       ↻ compact  ·  cwd: /path
```

| Zone | Widgets | Identity |
|---|---|---|
| LEFT | branch + status-symbols + ahead-behind + sha | git position |
| MIDDLE | Session-usage + Weekly-usage + Session-cost | budget awareness |
| RIGHT | Compaction-counter + cwd | context counter + filesystem position |

Separators: `·` everywhere. Bold on Session-usage (primary budget signal).

## Verbosity calibration (SB-080 + SB-082)

Per operator cycle 41: "not everything need to be minimized" + "you went to the other extreme again". Settled on:

**Rule of thumb**: full-word labels, compact ratio values.

| Bad (cryptic) | Bad (verbose) | Good (calibrated) |
|---|---|---|
| `Bk:0` | `Blockers: 0 active right now` | `Blockers: 0` |
| `SB:13/6` | `SystemicBugs: 13 open · 6 recurring` | `Bugs: 13/7` |
| `Tasks:17d/1p/47n` | `Tasks: 17 done · 1 in-progress · 47 not-started` | `Tasks: 17/1/47` |
| `R:50%` | `Readiness: 50 percent done` | `Readiness: 50%` |
| `Mode:dual` | `Currently active mode: Dual Expert PM Scrum Master + DevOps Architect` | `Mode: Dual Expert` |

## Why the right zone of line 3 is minimal

Earlier iterations stuffed line 3 right zone with: block-reset-timer + weekly-reset-timer + compaction-counter + output-style + free-memory + cwd. Symptoms:
- Empty Anthropic-data widgets (block-reset-timer, weekly-reset-timer when no recent usage) caused renderer to drop the whole right zone
- Visual density made line 3 hard to scan

Final right zone: only 2 widgets (compaction-counter + cwd). Both have GUARANTEED non-empty output (counter always shows `↻ N`, cwd always shows `cwd: /path`) — so the right zone always renders.

Block-reset-timer moved to MIDDLE zone (billing semantics) — but later dropped because empty-block-reset still cascaded the right zone. Final design: budget timing lives in session-usage / weekly-usage values themselves.

## Anti-patterns avoided this cycle (per SB-082 extremes pendulum)

- ❌ Single-letter cryptic labels (Bk/SB/R/D)
- ❌ Sentence-y verbose labels ("SystemicBugs: 13 open · 6 recurring")
- ❌ All-caps labels (BLOCKERS / TASKS) — reads as shouting
- ❌ Emoji per widget (visual noise)
- ❌ Redundant widgets on same line (git-staged-files + git-status both show staged count)
- ❌ Color decoration without semantic meaning

## Design discipline going forward

Per SB-077 (deliver-before-spec) + SB-082 (extremes-pendulum): future statusline edits should
1. Re-read this log first (verifies intent vs proposed change)
2. Smoke-render BOTH the prior design and the proposed design (counter the pendulum)
3. Apply only if the proposal is closer to balanced-middle than prior
4. Update this log to reflect the new design intent

## Files touched cycle 41/41.5

- `/root/.config/ccstatusline/profile-base.json` (1-column rewrite)
- `/root/.config/ccstatusline/profile-intermediary.json` (2-column AIDLC + LLM + git)
- `/root/.config/ccstatusline/profile-full-aidlc.json` (3-column comprehensive)
- `/root/templates/ccstatusline-widgets/aidlc-mode.sh` (label "Mode: Dual Expert")
- `/root/templates/ccstatusline-widgets/aidlc-readiness.sh` ("Readiness: 50%")
- `/root/templates/ccstatusline-widgets/aidlc-blockers.sh` ("Blockers: 0")
- `/root/templates/ccstatusline-widgets/aidlc-open-sbs.sh` ("Bugs: 13/7")
- `/root/templates/ccstatusline-widgets/aidlc-tasks-progress.sh` ("Tasks: 17/1/47")
- `/root/templates/ccstatusline-widgets/aidlc-model.sh` ("Model: feature-dev")
- `/root/templates/ccstatusline-widgets/stage.sh` ("Stage: Scaffold")
- `/root/templates/ccstatusline-widgets/aidlc-sfif.sh` ("SFIF: Scaffold")
- `/root/templates/ccstatusline-widgets/selected-task.sh` ("Task: T012 slug [50%]")
- (synced to /root/.local/share/ccstatusline-widgets/ runtime)

## Cross-references

- SB-080 (over-minimization in statusline labels) — structurally-fixed via long-word-label calibration
- SB-082 (extremes pendulum) — recurring; cycle 41.5 calibration
- SB-077 (deliver-before-spec) — this log IS the spec, retroactively
- M011 (ccstatusline custom widget for Claude Code interface) — operator's stated priority order item #2
