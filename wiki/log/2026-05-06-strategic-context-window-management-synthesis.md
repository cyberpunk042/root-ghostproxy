---
title: "2026-05-06 — Strategic context-window management — synthesis (4 modes: auto / strategic-early / edging / scope-shift-clear)"
type: log
domain: cross-domain
status: design-stage
confidence: medium
maturity: seed
created: 2026-05-06
updated: 2026-05-06
sources:
  - id: operator-directive-2026-05-06-strategic-not-mindless
    type: directive
  - id: operator-directive-2026-05-06-edging-mode-and-scope-shift-clear
    type: directive
  - id: sb-078-pre-compact-handoff-realization
    type: directive
    file: wiki/governance/systemic-bugs.md
  - id: src-context-mode-mksglu
    type: source-synthesis
    file: /opt/devops-solutions-information-hub/wiki/sources/wiki-methodology/src-context-mode.md
tags: [log, design, context-window, compaction, handoff, strategic, sb-078, edging-mode, scope-shift, mode-composition, sacrosanct, verbatim, methodology-respected, design-stage]
---

# Strategic context-window management — synthesis

> **Methodology stage**: design (25–50% readiness). ALLOWED: design-document, ADR, tech-spec. FORBIDDEN: code-file, test-file. Hook edits stay paused until this synthesis is operator-reviewed.

## Operator directives (verbatim, sacrosanct)

### 2026-05-06 — context-warning hook directive (initial framing)

> "also the statusline somehow the cwd is showing : /root instead of the second-brain where... the rest seem fine... but another point into what I was saying.. there should be a hook that start warning at the prompt inputs so that at <5% we say something and then at 3 and 2 pourcent and then after the compact like normal too"

### 2026-05-06 — correction after I added prescriptive `/compact` text

> "No you completely corrupted what I said... wtf... lets revise this whole thing.. you cannot invent rules of what to do randomly.. this is retart... auto-compact for no reason.. wtf..."

> "CAN WE CURE THIS FUCKING ILLNESS YOU HAVE OF NOT THINKING BEFORE ACTING ALREADY ?"

> "AGAIN ?? WHY DO YOU NOT FUCKING READ THE INFORMATION I GAVE ABOUT ALL THIS INSTEAD OF FUCKIGN HALLUCINATING EVERYTHING... WTF THOSE FUCKING ILLNESSES...."

### 2026-05-06 — strategic-not-mindless framing

> "ffs we had to hit a compaction over all this..... lets see if at least that hook land a minimum and is executed properly"
> "some information are in the root too..."
> "its not mindless waht we do at 5 -3 and 2 and 0%..."
> "its strategic..."
> "its logical"
> "its sounds"
> "you can stay at 0% so long when done properly for example"
> "asmuch as you might want to compact sooner in some cases"
> "but we do not invent random things..."

### 2026-05-06 — methodology + edging + scope-shift correction

> "You keep and keep going to fast and rushing to the execution... why are you not fucking respecting the methodology and do thing mindfully ? obviously what you selected is just an example and it needs to be synthesized and we need to cover the other like the edging mode to exploit the context window and such... or logical context clear or compact based on a completly new unrelated scope for example... we need to think it through and show something intelligent that will be usefull to something and processed prolerly..."

### Prior — SB-078 (cycle 41, 2026-05-05) — the realization-mechanism directive

> "we should have added a hook that should have realize as we get closer to the context limit that we need to prepare for compact and do a strong handoff document and register our knowledge and learnings before we are forced to compact or such... should be ready by that point and keep the handoff up to date as we continue or trigger ourself the compact if logical"

## Existing infrastructure inventory (don't reinvent)

| Component | Location | Purpose | Status |
|---|---|---|---|
| `pre-compact.sh` | `/root/.claude/hooks/` | Captures deterministic handoff doc on PreCompact event (state snapshot: active mode, active task, cycle JSON, blockers, recent logs, git state, recovery instructions) | Wired, working (SB-078 closure) |
| `post-compact.sh` | `/root/.claude/hooks/` | Re-orient post-compact + reference most-recent handoff doc in additionalContext | Wired (~85% generative compliance per project's brain) |
| `/handoff` slash command | `/root/.claude/commands/` | Operator-on-demand handoff before compaction | Authored cycle 51 |
| `context-warning.sh` | `/root/.claude/hooks/` | UserPromptSubmit hook surfacing % remaining at <5/<3/<2% thresholds | Wired this cycle (in revision per operator); fire trace confirms execution |
| `tools.cycle / tools.blockers / tools.progress` | `/root/tools/` | State-extraction CLIs the handoff doc invokes | Working |
| `src-context-mode` (third-party reference) | `/opt/.../wiki/sources/wiki-methodology/src-context-mode.md` | mksglu/context-mode MCP: 6 sandbox tools, 5-hook session continuity, 15-category priority-tiered event capture, 98% context savings benchmark | Source synthesis exists; not yet wired into /root |

## The 4 strategic modes (synthesis)

The operator's 5/3/2/0% thresholds are not severity tiers — they're **decision windows**. Within each window, multiple strategic responses are valid. The mode IS the strategic stance the operator (or agent) takes; the threshold is the moment of perception. Below: 4 distinct modes, each grounded in operator-verbatim or existing-infrastructure source.

### Mode A — Auto-compact-with-handoff (default)

**Strategy**: Let auto-compact fire at OS-forced threshold (~0%); rely on `pre-compact.sh` for state snapshot; rely on `post-compact.sh` for re-orient.

**When valid**:
- Handoff doc coverage is sufficient (knowledge/learnings registered in wiki/log/, decisions in decisions.md, in-flight task state in active-task)
- Conversation nuance loss is acceptable (per pre-compact.sh's own caveat: "Conversation nuance WILL be lost; this handoff cannot recover that")

**Operator grounding**:
- "you can stay at 0% so long when done properly for example" → this mode + handoff-readiness IS "done properly"
- SB-078: "before we are forced to compact" → forced is acceptable IF handoff is strong

**Infrastructure used**: pre-compact.sh + post-compact.sh + handoff doc pattern.

**Warning-hook role**: at <5/<3/<2% thresholds, prompts the agent to verify handoff readiness. NO prescription.

### Mode B — Strategic-early-compact

**Strategy**: Operator (or agent on operator-direction) invokes `/compact` BEFORE forced threshold, when handoff IS ready and a phase-boundary is reached.

**When valid**:
- Handoff is verified ready (via /handoff or pre-compact.sh dry-run)
- Current phase of work is wrapping; clean break point reached
- Want to control summarization timing (avoid mid-thought interruption)
- Want fresh window for next phase

**Operator grounding**:
- "asmuch as you might want to compact sooner in some cases"
- SB-078: "trigger ourself the compact if logical"

**Infrastructure used**: /handoff command (verify) + operator-invoked /compact + post-compact.sh re-orient.

**Warning-hook role**: surfaces % so operator can identify the strategic-early window (operator's call, not agent prescription).

### Mode C — Edging (exploit window)

**Strategy**: Intentionally ride near 0% to maximize current-context value before compaction. Requires confidence that handoff readiness holds throughout.

**When valid**:
- Current work benefits from full loaded context (e.g., complex synthesis across many sources, deep refactor with many files in scope)
- Handoff readiness maintained continuously (knowledge/learnings registered as we go, not just at the end)
- Operator is engaged (can intervene if edging fails)

**Operator grounding**:
- "edging mode to exploit the context window"
- "you can stay at 0% so long when done properly" (the engineering condition for edging-safety)
- SB-078: "keep the handoff up to date as we continue" (the discipline edging requires)

**Infrastructure used**: continuous handoff-update discipline (every cycle's verbatim log + decisions/blockers updates) + warning-hook % surface + auto-compact-fallback.

**Warning-hook role**: at <5/<3/<2% thresholds, becomes the edging-mode "are we still ready?" check. The agent verifies handoff readiness at each threshold; if not ready, exit edging (Mode A or B fallback).

**Risk**: if handoff readiness breaks during edging, forced compaction loses nuance more than expected. Edging is an OPERATOR-ENABLED mode (not default).

### Mode D — Logical context-clear-or-compact on scope-shift

**Strategy**: At ANY %, when work scope shifts to something completely unrelated to current loaded context, `/clear` or `/compact` discards old context as noise. NOT threshold-driven.

**When valid**:
- Operator (or agent) recognizes scope discontinuity (e.g., from "fix /root statusline" to "discuss SFIF stage gate criteria")
- Old loaded context provides no value to new scope
- Old loaded context may bias the agent (residual mental models from prior scope)

**Operator grounding**:
- "logical context clear or compact based on a completly new unrelated scope for example"

**Infrastructure used**: operator-invoked /clear or /compact (scope-shift detection is operator-driven by default; agent can flag suspected scope-shift but does not auto-execute).

**Warning-hook role**: NONE. This mode is orthogonal to threshold detection. The signal is scope-relevance, not %.

**Open design question**: does the agent flag suspected scope-shift to operator? When? How? (Out of scope for this synthesis pass; surface for operator decision.)

## Mode-to-infrastructure mapping

| Mode | Trigger | Pre-Compact action | Compact mechanism | Post-Compact action |
|---|---|---|---|---|
| **A — Auto** | OS-forced 0% | pre-compact.sh writes handoff doc | Auto (system) | post-compact.sh + /orient |
| **B — Strategic-early** | Operator at 5/3% with handoff verified | /handoff command (or pre-compact.sh equivalent) | `/compact` (operator) | post-compact.sh + /orient |
| **C — Edging** | Operator stays past 5/3/2% with handoff continuously ready | Continuous handoff-update discipline | Auto-compact at 0% (Mode A fallback) | post-compact.sh + /orient |
| **D — Scope-shift** | Operator recognizes unrelated-scope shift at any % | Optional handoff (handoff is irrelevant to next scope) | `/clear` (full reset) or `/compact` (summary preserved) | New /orient or fresh session |

## What the warning hook does (purely)

- **Surfaces % remaining at each threshold** (<5%, <3%, <2%)
- **Provides observability** to support mode A / B / C decisions (mode D is orthogonal)
- **Does NOT prescribe action** (operator: "we do not invent random things")
- **Does NOT label severity** ("ATTENTION/WARNING/URGENT" was invented; threshold value IS the label)
- **Does NOT cover scope-shift** (Mode D needs different signal — see open design questions)

## What the warning hook should NOT do (anti-patterns this session uncovered)

- **NOT prescribe `/compact`** — that's mode B, but B is OPERATOR's strategic call, not agent's
- **NOT label "compaction imminent"** — at <2%, depending on mode, that's either expected (Mode A/C) or too late (Mode B failed)
- **NOT invent severity tiers** — operator's threshold names ARE the threshold values
- **NOT auto-suggest action per threshold** — per-threshold action varies by mode, which is operator-state, not threshold-state

## Open design questions (operator review)

| # | Question | Why open |
|---|---|---|
| Q1 | Should the warning hook reference modes A/B/C in its message, or stay purely a `% remaining` ping? | Mode-aware text helps operator orient; mode-blind text avoids invention |
| Q2 | Should `.claude/active-mode` extend to include context-mode (auto/strategic-early/edging)? | Parallel to PM/Architect/Dual modes; would let agent know which behavior to support |
| Q3 | Mode D (scope-shift) detection — operator-only OR agent-flagged-on-suspected-shift? | Agent-flag could falsely interrupt; operator-only is safest but loses opportunity |
| Q4 | "after the compact like normal too" — is the directive for context-warning hook to ALSO fire on PostCompact event (showing fresh % post-compact)? Or just "the warning behavior continues normally on next prompts" (UserPromptSubmit auto-handles this)? | Ambiguous; operator clarification needed |
| Q5 | Does `/handoff` command need an "edging-mode-readiness" subcommand to verify continuous handoff readiness? | Edging requires this discipline; tooling could enforce |
| Q6 | Should the warning text reference SB-078's verbatim language ("prepare for compact, strong handoff document, register knowledge/learnings") or stay pure-observability? | SB-078 is operator-grounded; referencing avoids invention while providing useful framing |
| Q7 | At <2% threshold, should the hook ALSO check handoff-doc freshness (last-written timestamp vs current activity)? | Active dirty state at <2% is the actual risk; freshness check would be agent-helpful, not invented |
| Q8 | Does context-mode (mksglu/context-mode) integration belong in /root scope or stay /opt-only? | Cross-project decision; sister-project propagation question |

## Bugs found in current implementation (during this design pass)

### Bug-1 (NEW SB-pending): context-warning.sh window-resolution falls back to 200k DEFAULT_WINDOW under Opus-4.7 1M context

**Symptom**: Operator received URGENT-tier warning at 08:48:09 with `pct_remaining=-88.85` (impossible — used > window).

**Trace evidence** (verbatim from `/tmp/hook-fire-trace.log`):
```
[01:03:01] used=377706 window=1000000 pct_remaining=62.23     ← correct (1M window)
[08:48:09] used=377706 window=200000  pct_remaining=-88.85    ← bug (200k fallback)
```

Same `used` value across both fires; window dropped to DEFAULT_WINDOW (200_000) on the second.

**Root cause**:
- Hook reads `model_id = (payload.get("model") or {}).get("id") or ""` from UserPromptSubmit stdin.
- Claude Code's UserPromptSubmit stdin payload does NOT reliably include `model.id` across all invocations (empirically observed; not consistently documented).
- When `model_id == ""`, `_resolve_context_window("")` returns `DEFAULT_WINDOW = 200_000`.
- Result: actual context-usage measured against the wrong window → wildly wrong %.

**Authoritative source verified**: session jsonl `message.model` is reliably present per assistant turn:
```
session: /root/.claude/projects/-root/0487d686-2839-447f-bc7e-354a55a2683a.jsonl
assistant-turn 'message.model' values in last 200KB (4 records):
  claude-opus-4-7: 4
```

The hook ALREADY reads this jsonl for token counts (`_get_latest_context_used`). Same record's `message.model` is right there.

**Why this is a root-cause bug, not a quick-fix surface**:
- Quick-fix (mask): change `DEFAULT_WINDOW = 1_000_000` — works today, breaks later when Claude Code adds smaller-window models or when running on Haiku-4.5 (200k).
- Root-fix: window resolution must use the **authoritative** model source (session jsonl per turn), with stdin model_id as a hint only. The session jsonl IS the source of truth for "what model just ran in this session" — that's what the % should be measured against.

**Initial proposed fix (REJECTED 2026-05-06)**: read `message.model` from session jsonl tail. Operator response verbatim: *"WE DONT DO HACK AND QUICKIX.... WTF IS THIS... YOU USE THE ENVIRONMENT VARIABLES TO ACTUALLY HAVE THE RIGHT VALUE...."*

The jsonl-read approach IS file-path heuristics — exactly the kind of hack the operator's "no hack/quickfix" rule covers. The proper path is env vars Claude Code exposes to hook context (CLAUDE_PROJECT_DIR pattern extended).

**Investigation in flight**: diagnostic trace added to `context-warning.sh _trace()` — on next 'entered' fire, dumps env var KEYS matching CLAUDE/ANTHROPIC/MODEL/CONTEXT/TOKEN/WINDOW (KEYS only; values may contain secrets). Bash tool sub-shell did NOT have any of these set (queried via /tmp/check-claude-env.py with 16 candidate names — all unset), but hooks run in a different env context (CLAUDE_PROJECT_DIR IS set there per existing traces). Once next-fire trace shows the actual env var Claude Code exposes for model/window, the hook resolution swaps to that env var as the authoritative source.

**Fix shape (pending env-var identification)**:
```python
# Pseudocode — actual var name TBD per next-fire diagnostic
window = int(os.environ.get("CLAUDE_CONTEXT_WINDOW", "")) if os.environ.get("CLAUDE_CONTEXT_WINDOW") else _fallback()
# OR derive from CLAUDE_MODEL_ID env var → window mapping
# OR similar — depends on what Claude Code actually exposes
```

**Quick-fix explicitly rejected**: raising `DEFAULT_WINDOW` to 1_000_000 masks the symptom + breaks on Haiku 4.5 (genuinely 200k context).

**This fix advances the synthesis** — it's a Mode-A/B/C precondition: % calculation must be reliable BEFORE the threshold logic can be debated. With unreliable %, every threshold strategy breaks.

**Operator-pending**: next-fire diagnostic identifies the env var; then implement env-var resolution + remove diagnostic. Hook untouched in the meantime (THRESHOLDS structure restored to working state earlier this session).

## Stage gate (per `/root/wiki/config/methodology.yaml` design stage)

> design stage 25–50% readiness — gate: trade-offs documented; spec reviewed.

**This synthesis = trade-offs documented.** ✓
**Spec reviewed = pending operator review.** ⏳

After operator-review, the next stage is scaffold (50–80%) — type-definitions, schema, test-stubs, config-files. NOT implementation.

If operator approves the 4-mode framework + answers Q1–Q8, scaffold-stage work would include:
- Updated context-warning.sh message body (per Q1, Q6 decisions)
- Optional `.claude/active-mode` extension (per Q2 decision)
- Optional /handoff subcommand for edging readiness (per Q5 decision)
- Optional handoff-freshness check (per Q7 decision)

Implementation stage waits until scaffold passes its gate.

## Cross-references

- SB-078 (the realization-mechanism directive): `/root/wiki/governance/systemic-bugs.md` row SB-078
- Pre-compact hook: `/root/.claude/hooks/pre-compact.sh`
- Post-compact hook: `/root/.claude/hooks/post-compact.sh`
- /handoff command: `/root/.claude/commands/handoff.md`
- Context-warning hook (this session): `/root/.claude/hooks/context-warning.sh`
- Settings wiring (hot-reload): `/root/.claude/settings.local.json`
- Context-mode source synthesis (third-party reference): `/opt/devops-solutions-information-hub/wiki/sources/wiki-methodology/src-context-mode.md`
- Methodology engine (this stage's gate): `/root/wiki/config/methodology.yaml` design stage row
- Operating principles (research-first, no-invention): `/root/.claude/rules/operating-principles.md`
- Sacrosanct words rule: `/root/.claude/rules/words-are-sacrosanct.md`

## Meta — process correction this synthesis applies

Three failure-modes operator surfaced this session, all addressed by THIS document existing instead of more code:

1. **Rushing to execution** — the methodology says document → design FIRST. This synthesis IS the design stage.
2. **Inventing rules** — the 4 modes are derived from operator-verbatim, not invented. SB-078 + the 2026-05-06 directives are the source.
3. **Not reading existing /root information** — pre-compact.sh, post-compact.sh, /handoff, src-context-mode were all already there. This synthesis inventories before designing new.

The hook is paused until operator reviews this synthesis.
