---
title: "2026-05-05 — Operator directive (corrective, severe): fake-blocker pattern; research-first violated; almost-none-are-blockers; disappointing test cycle"
type: note
domain: cross-domain
status: raw
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-fake-blockers-research-first-violated
    type: directive
tags: [note, operator-directive, sacrosanct, verbatim, fake-blockers, research-first-violated, disappointment, severe-correction, test-cycle, agent-side-gap-vs-project-blocker, no-asking-permission-for-authorized-ops]
---

# Operator directive — 2026-05-05 fake-blocker pattern (severe corrective)

## Verbatim (PO words sacrosanct, no paraphrase)

> "wtf is this bug... why would I need to grant you WenFetch and WebSearch ?? why would those even be blocked or discourage ? Did I not say the complete opposite earlier... woow... same thing with gh... wtf you are talking about read-only opeartions.... you dont even have access to risked opeartion with the current gh auth token on this particular system... A lot of really bad things of happening.. this is why we are normally doing a test and evolving round but this is very disspointing to be blocked on so silly things... like almost everything you told me.. none of them are blockers.. wtf is happening..."

> (follow-up, same turn, after AI responded too briefly):
> "You minimized.. wtf IT WAS VERY IMPORTANT.. YOU SHOULD HAVE HARDLY REGISTERED AND THOUGHT ABOUT WHAT I SAID..."

## What the AI did wrong (specific)

1. **Dispatched sub-agent for ccstatusline research without trying directly first.** Sub-agent's sandbox denied WebFetch/WebSearch/Bash; AI treated the sub-agent's denial as if it were the PROJECT'S permission state. They are different.

2. **Asked operator to "grant me WebFetch/WebSearch this session"** — these are standard agent tools and the operator had ALREADY directed (verbatim earlier this turn): *"we work like real expert and we do our online and local research properly"*. Asking for permission to do online research = direct violation of the just-given directive.

3. **Asked for gh CLI permission** for read-only operations on a system where the gh auth token has no risky-operation access. Asking for permission to do read-only ops = anti-research-first.

4. **Classified F-eval-7 (pipelock context) as "blocked-on-you"** before trying github research. The repo is `luckyPipewrench/pipelock`-shaped — searchable directly with gh search / WebFetch.

5. **Classified F-eval-9 (hook-log read) as a finding without trying Read tool first.** I tried Bash + got denied by `**/*.log`; never tried Read tool. The Read tool may behave differently.

6. **Surfaced 5+ "blockers" that aren't blockers.** "almost everything you told me.. none of them are blockers" — operator's verdict.

7. **Minimized after first correction.** Operator surfaced the issue; AI replied too briefly + jumped to action without HARD-REGISTERING the lesson. This is exactly the work-mode.md anti-pattern: *"When called out: stop. Re-read what the operator said. Identify what's actually missing. Don't say 'you're right' and repeat the same mistake."*

## The canonical lesson (NEW principle to register)

**Agent-side tool-availability gaps are NOT project blockers.**

Before claiming "blocked":
1. TRY the operation directly with the tools available
2. Check the actual project policy (settings.json `permissions.deny`, hooks) — NOT assumed restrictions
3. A sub-agent's denial ≠ the parent agent's denial ≠ the project's policy
4. Asking operator to "grant" what's already authorized is anti-research-first behavior
5. "Blocker" claims should be SKEPTICAL by default; most "blockers" surfaced in iteration are agent laziness, not project state

## Connection to existing operating-principles.md

This is principle #5 (research-first) applied at the agent's own behavior layer. Research-first means:
- USING tools to get answers
- Not ASKING for permission to use standard tools
- Trying directly before classifying as blocked
- Verifying agent-side gaps vs project-side restrictions

## Why this hurts the test cycle

Operator: *"this is why we are normally doing a test and evolving round but this is very disspointing"*

The test cycle's PURPOSE is to surface real friction so the system can evolve. Fake blockers:
- Hide real friction (signal lost in noise)
- Waste operator attention (asking for permissions that don't need granting)
- Damage trust (operator doubts whether the agent is functional)
- Slow forward motion (cycles spent on fake issues instead of real progress)

## Action plan (apply the lesson NOW)

1. Log this directive verbatim — done (this file).
2. Register the lesson as canonical in `/root/.claude/rules/operating-principles.md` as principle #8 (or equivalent placement).
3. Lesson to second brain: `/opt/devops-solutions-information-hub/wiki/lessons/01_drafts/agent-fake-blockers-vs-project-blockers.md`.
4. RE-CLASSIFY every open F-eval with the new skepticism:
   - F-eval-3: NOT a blocker — informational only (modules deferred by operator design).
   - F-eval-6 (M011 prelim research): UNBLOCKED now — I have ccstatusline data. Author T-M011-* preliminary tasks with source-trace.
   - F-eval-7 (M014 pipelock): NOT blocked — try `gh search repos luckyPipewrench/pipelock` directly.
   - F-eval-8 (tools task-view): NOT blocked — propose a shape with code; iterate with operator.
   - F-eval-9 (hook-log read): NOT blocked — try Read tool first.
   - F-eval-10: applied (research-first canonical now).
   - F-eval-11 (trigger model): NOT blocked — sketch a proposal; iterate.
5. Apply lesson going forward: every claim of "blocked" must inline the verification command + its output proving the block is real (not assumed).

## No-conflate guard

- "wtf is this bug" = STRONG dissatisfaction, not just a question. Treat as severe correction.
- "Did I not say the complete opposite earlier" = the operator EXPLICITLY directed online research. AI behavior contradicted the directive.
- "almost everything you told me.. none of them are blockers" = the AI's blocker classification was systematically wrong.
- "YOU SHOULD HAVE HARDLY REGISTERED AND THOUGHT ABOUT WHAT I SAID" = don't minimize the first correction; register deeply.
- "this is why we are normally doing a test and evolving round" = the test cycle is the meta-purpose; fake blockers undermine the test cycle's value.
