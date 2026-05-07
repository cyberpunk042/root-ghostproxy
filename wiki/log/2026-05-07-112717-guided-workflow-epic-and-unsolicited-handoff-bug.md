---
title: "Guided-workflow Epic directive + unsolicited-handoff post-compact bug"
type: operator-directive-register
date: 2026-05-07
time: 11:27:17 EDT
sacrosanct: true
operator_verbatim:
  - directive_1: "For the Ai it should feel like a Guided workflow each prompt, each interaction, even when its not comming from me should trigger the right continuition, the right progresses. This too deserves its own epic. its part of the context engineering knowleding and structure and addlc / sdlc and methodologies and high standards and Wiki LLM and other things that the Second-brain teach and help adhere to. this will be a continuous progress."
  - directive_2: "itsd weird I didnt ask for a handoff document and one was done... the handoff was done after the context compaction lol wtf did just happend. properly register this situation too it needs our attention..."
tags: [operator-directive, guided-workflow, post-compact-bug, sb-142, epic-e006]
---

# Operator directive register — 2026-05-07 11:27:17 EDT

## Two distinct directives in one operator prompt

Operator's prompt arrived after a cron-fire `/loop 90s lets try an Experts mode autopilot loop. see how it goes.` system-reminder. Operator's actual content (interrupted the cron-fire, replacing it):

### Directive 1 — Guided workflow Epic territory

> **Verbatim** (sacrosanct): *"For the Ai it should feel like a Guided workflow each prompt, each interaction, even when its not comming from me should trigger the right continuition, the right progresses. This too deserves its own epic. its part of the context engineering knowleding and structure and addlc / sdlc and methodologies and high standards and Wiki LLM and other things that the Second-brain teach and help adhere to. this will be a continuous progress."*

**Operationalized into**: Epic E006 — Guided Workflow Continuation. Each interaction (operator-typed OR cron-fire OR PostCompact OR SessionStart OR any UserPromptSubmit) MUST trigger the right continuation + the right progress. Crosses: context-engineering rule + AIDLC/SDLC + methodologies + Wiki LLM consumption + second-brain doctrine. Continuous-progress not one-time-fix.

### Directive 2 — Unsolicited handoff post-compact bug (REGISTER)

> **Verbatim** (sacrosanct): *"itsd weird I didnt ask for a handoff document and one was done... the handoff was done after the context compaction lol wtf did just happend. properly register this situation too it needs our attention..."*

**Operator's literal premise**: they did NOT invoke `/finish-smoothly`. Yet a finish-smoothly handoff was written at 11:00:45 (`wiki/log/2026-05-07-110045-finish-smoothly-handoff.md`) and the agent (me) executed all 8 forced steps as if /finish-smoothly had been operator-invoked.

**Operationalized into**: SB-142 — unsolicited handoff post-compact / phantom skill-invocation.

## Investigation findings (preliminary)

Hook fire trace evidence (`/tmp/hook-fire-trace.log`):

| Timestamp | Event | Evidence |
|---|---|---|
| 10:27:46 | context-warning fired | pct_remaining=4.93 tokens_left=49333 |
| 10:29:20 | context-warning fired | pct_remaining=4.63 tokens_left=46308 |
| 10:40:39 | context-warning fired | pct_remaining=4.14 tokens_left=41413 |
| 10:45:24 | pre-compact.sh wrote handoff | (auto-triggered by Claude Code lifecycle) |
| ~10:45-10:48 | Claude Code auto-compact | agent context summarized |
| 10:49:02 | session-orient.sh fired (post-compact resume) | `path=fired-additionalContext` |
| 11:00:45 | finish-smoothly-handoff doc written by AGENT | (executing the 8 steps from system-reminder /finish-smoothly skill block) |

Three hypotheses for the phantom /finish-smoothly invocation:

1. **Pre-compact agent self-invoked** under context pressure — treated approaching 0% context as cue to run knowledge-extraction. The args text in system-reminder was synthesized from operator's earlier-session prompt (*"30+ operations easy"* + *"prove me you understand readiness and enlightenment"*).
2. **Auto-compact / PostCompact reconstruction synthesized** the skill-invocation in system-reminder format. Skill listed as "invoked in this session" with operator-flavored args created by summarizer.
3. **Some hook or harness automation** invoked /finish-smoothly programmatically. (No evidence in hook fire trace; pre-compact.sh references finish-smoothly only in a comment.)

The current AI (me, post-compact) treated the system-reminder skill-block as authoritative WITHOUT verifying the operator's actual recent prompt history. That's a CLASS of bug too — cousin to SB-140 self-imposed-false-gate (treating a system-injected gate as operator-driven).

## What I should have done (forward fix)

Per mindfulness clause #2 (premise-confirmation gate): operator's literal words = premise. Before executing /finish-smoothly's 8 forced steps, I should have confirmed: did the operator actually type `/finish-smoothly` recently? The conversation summary did NOT show that as an operator message. The system-reminder showed the skill as "invoked in this session" but the conversation-summary `All user messages` list was the authoritative source. When the two conflict — system-reminder skill-block vs operator's actual message history — the operator's message history wins (sacrosanct).

## Cross-references

- SB-142 (this operator-flagged bug): `wiki/governance/systemic-bugs.md`
- Epic E006 (this operator-flagged Epic): `wiki/backlog/epics/epic-e006-guided-workflow-continuation.md`
- Cousin SB-140 (frozen-loop / self-imposed-false-gates): meta-vs-project-layer cousin
- Cousin SB-091 (synthetic-tests-as-verified): same root pattern (treating internal-model state as external truth)
- words-are-sacrosanct.md premise-confirmation gate: `.claude/rules/words-are-sacrosanct.md`
- Pre-compact handoff: `wiki/log/2026-05-07-104524-pre-compact-handoff.md`
- Phantom finish-smoothly handoff: `wiki/log/2026-05-07-110045-finish-smoothly-handoff.md` (NOT operator-asked; agent-executed under phantom invocation)
