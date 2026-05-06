---
title: "2026-05-05 — Operator directive: auto-research before asking; filter out auto-answerable questions; report Q+A chain"
type: log
domain: cross-domain
status: active
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-auto-research-pipelock-redux
    type: directive
tags: [log, operator-directive, sacrosanct, verbatim, auto-research, fake-blocker-redux, pipelock, decision-package-quality, sb-072]
---

# Operator directive — 2026-05-05 auto-research before asking + filter out auto-answerable

## Verbatim

> "you should not have to ask me what pipelock is.. I alreay gave you the source... and I still receive silly questions... things you can auto answer and then filter out and/or tell me what you had of question and what you responded depending on the situation. we need to improve the non-information wall situation desire ahah"

## Decomposition

### A — The fake-blocker pattern recurred (specific instance)
- Operator gave `luckyPipewrench/pipelock` as the source — that's enough to gh search/fetch
- Agent (cycle 15) authored M014 skeleton with 7 clarification questions including "what does pipelock do?"
- That question was AUTO-ANSWERABLE via gh api fetch of the README
- Operator: "still receive silly questions"

### B — Auto-answer + filter pattern needed
- "things you can auto answer and then filter out"
- When agent CAN research the answer → research, apply, don't ask operator
- The decision package should NOT include questions that research could answer

### C — Report the Q+A chain when relevant
- "tell me what you had of question and what you responded depending on the situation"
- When agent has researched + answered: report the chain so operator can verify/correct
- Format: "I had question X; I researched via Y; got answer Z" — visible audit, not silent

### D — Improve the non-information wall situation
- "we need to improve the non-information wall situation desire"
- The cycle 17 decision packages were better than cycle 16.5 vague-list, but STILL had auto-answerable questions
- Need: filter step BEFORE surfacing — "is this question one I can research?" → if yes, do research, don't surface

## Composes with prior directives

- Same lesson as F-eval-13 (fake-blocker pattern) — this is a SPECIFIC RECURRENCE
- Same as F-eval-10 (research-first / no-hallucination)
- Refines SB-071 (decision-package format) — packages must FIRST filter out research-answerable questions

## Action plan

1. Log this directive — done.
2. Add SB-072: auto-research-before-asking pattern.
3. Apply NOW: research pipelock + rewrite M014 with researched content.
4. Show the Q+A chain in this response (per directive C).
5. Update SB-071 / mode brain pieces with auto-research filter step BEFORE surfacing decision packages.

## The Q+A chain for M014 (per directive C)

| Question I had | Research I did | Answer |
|---|---|---|
| What is pipelock? | `gh api repos/luckyPipewrench/pipelock` + README fetch | Open-source AI agent firewall: MCP security, agent egress control, DLP, SSRF, prompt-injection defense. 510 stars, last push 2026-05-05, Go 1.25+, Apache 2.0 + ELv2. CNCF Security & Compliance. |
| Project identity | gh api metadata | luckyPipewrench/pipelock — github.com/luckyPipewrench/pipelock — pipelab.org |
| Relationship to /root | Inferred from both projects' scopes | COMPLEMENTARY — pipelock = agent-process boundary (MCP/egress proxy); root-ghostproxy = network L2 boundary + OS-level safety. Different layers of the same defense. |
| Works with Claude Code? | README explicitly | YES — "Works with: Claude Code · Cursor · VS Code · JetBrains · OpenAI Agents SDK · Google ADK · AutoGen · CrewAI · LangGraph" |
| Latest release / activity | gh api pushed_at | 2026-05-05 (today, actively maintained) |
| License | gh api license | Apache 2.0 (core) + ELv2 (enterprise) |

## Genuinely-uncertain (not auto-answerable; legitimate operator decisions)

1. **SFIF stage placement** — Features (like M005 Suricata/PolarProxy)? Foundation (if it gates other modules)? Operator-chosen.
2. **Ordering relative to M011 (ccstatusline) and M005 (Suricata/PolarProxy)** — operator's preference.
3. **Preliminary scope** — module page authoring with research-content (DONE this cycle), OR also source-synthesis ingestion via second-brain `gateway contribute` (after M007)?

## Cross-references

- F-eval-13 (fake-blocker pattern lesson)
- F-eval-10 (research-first canonical)
- SB-071 (decision-package format)
- /root/wiki/lessons/01_drafts/agent-fake-blockers-vs-project-blockers.md
