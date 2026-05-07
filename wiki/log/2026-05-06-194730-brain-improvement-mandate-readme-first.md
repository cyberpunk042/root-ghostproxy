---
title: "Brain-improvement mandate — operator directive 2026-05-06: README-first, then full brain pass"
type: log
subtype: operator-directive-register
domain: cross-domain
status: directive-active
created: 2026-05-06
sources:
  - id: operator-directive-2026-05-06-brain-improvement-readme-first
    type: directive
    medium: in-session-prompt
tags: [directive, brain-improvement, readme, agent-as-external-updater, sacrosanct]
---

# Brain-improvement mandate — operator directive 2026-05-06

## Sacrosanct verbatim quote

> "you are going to be the one from the external that update the brain of the root project. Claude.md + Agents, and Context and Tools and Skills and Rules and Hooks and every inner piece and tools and vision about with what I will answer to support... but the thing is. I will be the one that says when you are ready to update all those, start with the main readme.md actually and any sub-readme.md, you are even gonna allow yourself to add notes and remarks and admonitions and such where you see fit, you can take notes of your personal learnings progress here, there is such a room for system project even a root one. so yeah you can get started. fell free to do operations, 30+ for sure and prepare questions and preanswers then and turn them into decision befoer you even present them to be other otherwise at least options or suggestions and or context and more informations. we will need to do a great job, it will help the project progress.. we might even create new files, new markdowns, new artifacts & documents for the needs and or SRP and cleaneness and polish. This is a big task do not minimize.. we have plently of room to achieve this in the context."

## Literal decomposition (do NOT infer beyond the words)

| Clause | Operator literal grant |
|---|---|
| **Role** | "the one from the external that update the brain of the root project" — agent is external updater; fresh-perspective lens |
| **Eventual scope** | Claude.md + AGENTS.md + CONTEXT.md + TOOLS.md + SKILLS.md + Rules + Hooks + every inner piece + tools + "vision about with what I will answer to support" |
| **Operator-gated** | "I will be the one that says when you are ready to update all those" — operator gates the broader brain pass |
| **CURRENT IMMEDIATE GRANT** | "start with the main readme.md actually and any sub-readme.md" |
| **Authority** | "allow yourself to add notes and remarks and admonitions and such where you see fit" + "you can take notes of your personal learnings progress here" |
| **Workspace framing** | "there is such a room for system project even a root one" — agent's notes/remarks have their place in this brain |
| **Go-ahead** | "so yeah you can get started" |
| **Scale** | "30+ for sure" — DO NOT minimize |
| **Decision discipline** | "prepare questions and preanswers then and turn them into decision before you even present them to be other otherwise at least options or suggestions and or context and more informations" |
| **Quality bar** | "we will need to do a great job, it will help the project progress" |
| **New artifacts allowed** | "we might even create new files, new markdowns, new artifacts & documents for the needs and or SRP and cleaneness and polish" |
| **Anti-minimization** | "This is a big task do not minimize.. we have plently of room to achieve this in the context" |

## What this grants RIGHT NOW (vs gated)

| Granted now | Gated on operator confirm |
|---|---|
| Update README.md (1030 lines) | Update CLAUDE.md / AGENTS.md / CONTEXT.md / TOOLS.md / SKILLS.md / ARCHITECTURE.md / DESIGN.md / SECURITY.md / BOOTSTRAP.md |
| Update scripts/README.md (320 lines) | Update .claude/rules/*.md |
| Author new READMEs in subdirs lacking them (SRP/cleanness) | Update .claude/hooks/*.sh |
| Add admonitions, notes, agent-learning callouts where they fit | Update .claude/commands/*.md (beyond current already-edited /task /cycle) |
| Author new artifacts (markdowns / docs / specs) supporting README work | Update .claude/modes/*.md |
| Surface decisions with pre-answers/options/context | Update tools/*.py |

## Scope inventory (READMEs in this project)

```
/root/README.md                              1030 lines  primary
/root/scripts/README.md                       320 lines  sub-README
                                            ─────
                                             1350 lines  total in scope NOW
```

Subdirs WITHOUT README (potential new-artifact opportunities per operator-allowed "create new files for SRP/cleanness/polish"):

- `/root/tools/` — 12 .py modules; no README
- `/root/.claude/commands/` — 29 commands; no README (slash-command index could help)
- `/root/.claude/hooks/` — 14 wired hooks; no README (hook architecture index)
- `/root/.claude/modes/` — 3 modes; no README
- `/root/.claude/rules/` — N rule files; no README
- `/root/.claude/agents/` — 3 subagents; no README
- `/root/.claude/skills/` — none built; no README (placeholder?)
- `/root/templates/` — multiple template categories; no README (each subdir varies)
- `/root/wiki/` — has _index.md not README (different convention)

## Decision-discipline methodology (per operator)

For every question that arises during this work:

1. **Pre-answer**: best-judgment answer based on available context
2. **Turn into decision**: ground in evidence + cite operator-stated principles
3. **If decision-too-far**: surface as option (≥2) with: context + recommendation + alternatives
4. **NEVER**: bare-question wall (operator caught me on Q1-Q7 freezing)

This methodology operates within the additive principle (work-mode Hard Rule 4a — "adding ≠ discarding"): improvements LAYER ON existing content, do not replace.

## Personal-learning notes (operator-allowed)

Per operator: *"you can take notes of your personal learnings progress here, there is such a room for system project even a root one"*. This is permission to leave agent-perspective callouts in the README work where they help future agents. To be flagged as agent-authored (per SB-095) so operator distinguishes operator-stated content from agent-perspective.

## Plan (this fire opens; chain-style operations expected per SB-131)

1. Log this directive (THIS file) ✓
2. Read /root/README.md in full
3. Read /root/scripts/README.md in full
4. Audit pass — identify drift / staleness / clarity / SRP / cleanness / polish / admonitions / agent-learning opportunities
5. Apply improvements ADDITIVELY (per operator catch this turn)
6. Surface decisions (pre-answered / options-with-context) where appropriate
7. Identify candidates for new READMEs in subdirs (operator-allowed; gated on operator-confirm before authoring)

Cycle continues until natural break or operator redirect. Per "30+ operations for sure" — substance scale is real.

## Anti-patterns to avoid (operator-caught patterns I keep falling into)

- SB-082/093 going-to-extremes: don't replace the 1030-line README with a 200-line "polished" version; layer additively
- SB-090 premise-construction: don't infer what operator wants beyond literal directive
- SB-095 hallucinated-artifacts: any new file I author = flag as agent-DRAFT until operator accepts
- SB-099 abdication-as-freeze: don't bring raw questions; pre-answer per directive
- SB-128 thin-output: substance per fire; this is a 30+-op directive, treat as one
- SB-131 chain-operations: batch coherent changes per fire, not single-edit-per-cycle

## Status

Directive registered (this file = `operator-directive-register` action type from M-E001-1 vocabulary). Next action: read both READMEs in full.
