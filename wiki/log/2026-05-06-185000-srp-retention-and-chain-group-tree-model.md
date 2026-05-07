---
title: "Operator answers Q1 + Q2 — SRP retention / chain+group+tree operations model"
type: log
subtype: operator-directive
domain: cross-domain
status: registered
created: 2026-05-06
sources:
  - id: operator-directive-2026-05-06-srp-chain-group-tree
    type: directive
    file: this file (operator-verbatim, sacrosanct)
tags: [operator-directive, sacrosanct, srp, chain-operations, group-calls, tree-of-operations, cursor-files, aidlc, q1-answered, q2-clarified]
---

# Operator answers Q1 + Q2 — SRP retention + chain/group/tree operations

## Operator's verbatim words (sacrosanct)

> "about your Q1 btw, I love SRP... we group things / share / and or create bridge / relationship files when needed. cursor file are important in aidlc. Q2 its multiple things dont just minimize.. I feel like the presweep on the questions is not done or maybe its because I dont see all the data available to them lets make this claer... I know I could maybe have used the /questions but I wanted to just speak it out and I am not sure what it would have outputted and if it would have satisfied me anyway... but to help if that was not clear a group call and chain calls is just a way to create a tree of operations for example triggering the equivalent of multiple tools and updating multiple things like PM file and cursor files and aidlc related things and such in a group effect / cascade call that maek it much simpler for Ends and Start and just casualy operation in general... like passing through the stage of one document for specs or someting else for example and such. again the second-brain must have knowledge about all this we have other project that do those things to higher levels thought. for example updating tasks and such where we know that the task should imply than more than just one operation, its a chain. and then there can be logic and dependency and then group call is that we have multiple chain inter-dependant or not and then there is obviousy also possible commands to force trigger them or wrap their usage and such or chain things at a higher level for the before and after amongs other things"

## Decoded answers

### Q1 ANSWERED — retention design = SRP per-category + bridges

Operator: *"I love SRP... we group things / share / and or create bridge / relationship files when needed. cursor file are important in aidlc"*.

**Decision**: per-category parallel state files (one file per concern), plus bridge / relationship files when groupings are warranted. Single-monolithic-state-file is REJECTED. Cursor files (like `active-task`) are operator-confirmed important pattern — keep that convention.

**Implication for E003 M-E003-1**: build per-category retention files for the 6 categories operator named (request / compound / demand / requirement / question / "whatnot") — possibly `active-{requests,demands,requirements,...}` — plus bridge files for cross-category groupings. Mirrors existing pattern: `active-mission` + `active-focus` + `active-impediment` already are SRP per-layer.

### Q2 CLARIFIED — multi-group tool calls = ALL of the above

Operator: *"Q2 its multiple things dont just minimize"*.

**Decision**: not a binary choice between new tool / extension / rule-only — it is **all three**:
1. Tool layer (e.g. `tools/group.py` or extensions to existing tools)
2. Command layer (commands that wrap chains for force-trigger / before-after)
3. Rule layer (governance for when to compose / chain)

### Operator's explicit model — chain / group / tree

| Concept | Operator's definition | Mechanism in this project |
|---|---|---|
| **Chain** | Sequential operations with logic + dependencies. Example operator gave: *"updating tasks and such where we know that the task should imply than more than just one operation, its a chain"* | Already partial in SB-131 (chain-batched fires per coherent change). Needs explicit primitive. |
| **Group call** | *"multiple chain inter-dependant or not"* — parallel composition of chains, with or without dependencies between chains | Not yet built. |
| **Tree of operations** | *"a way to create a tree of operations for example triggering the equivalent of multiple tools and updating multiple things like PM file and cursor files and aidlc related things and such in a group effect / cascade call that maek it much simpler for Ends and Start and just casualy operation in general"* | Composition surface above chain + group. |
| **Higher-level wrappers** | *"commands to force trigger them or wrap their usage and such or chain things at a higher level for the before and after amongs other things"* | Slash commands or skills that bundle chain/group/tree as a single operator-invokable unit. |

Concrete example operator named: *"passing through the stage of one document for specs or someting else"* — multi-file, multi-stage operation that should be a chain (or group of chains).

### Presweep critique — questions need richer context

Operator: *"I feel like the presweep on the questions is not done or maybe its because I dont see all the data available to them lets make this claer"*.

Current `tools.questions` stores one line per question — text only. Operator can't see context, options, stakes, what's at risk, what defaults could be picked. **The presweep is missing**.

**Fix path**: enrich question schema with context / options / stakes / suggested-default fields. Operator needs to see WHY each question matters + WHAT the choices are + WHAT defaults agent would pick if directed to act unilaterally.

### Research-first pointer

Operator: *"again the second-brain must have knowledge about all this we have other project that do those things to higher levels thought"*.

Sister projects in the second brain implement chain/group/tree at higher levels. Before designing root-ghostproxy's version, query second-brain for existing patterns. Per principle #5 research-first elevation 2026-05-06: be enlightened before acting.

## Actions chain-batched this fire

1. This log file (verbatim quote sacrosanct).
2. Q1 in active-questions queue → remove (answered: SRP per-category + bridges).
3. Q2 in queue → update text to reflect operator's "not binary, all-three" expansion.
4. Forward-anchor: presweep enrichment of questions schema (next-fire scope; design pending second-brain research).
5. Forward-anchor: chain/group/tree primitives (E003 multi-Epic, second-brain research-first before design).

## Cross-references

- `wiki/backlog/milestones/v0.2-ai-natural-task-management.md` (E003 retention now Q1-resolved → SRP shape)
- `wiki/backlog/epics/epic-e003-compound-retention-and-multi-group.md`
- `tools/questions.py` (presweep enrichment scope)
- `.claude/rules/operating-principles.md` principle #5 (research-first; second-brain consult)
