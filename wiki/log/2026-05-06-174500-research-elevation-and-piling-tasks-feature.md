---
title: "Research-elevation discipline + piling-tasks feature consideration (epic→sub-task, task-from-blocker)"
type: log
subtype: operator-directive
domain: cross-domain
status: registered
created: 2026-05-06
sources:
  - id: operator-directive-2026-05-06-research-elevation-piling-tasks
    type: directive
    file: this file (operator-verbatim, sacrosanct)
tags: [operator-directive, sacrosanct, research-first, second-brain-knowledge, piling-tasks, feature-consideration]
---

# Research-elevation discipline + piling-tasks feature consideration

> Logged BEFORE acting per `.claude/rules/work-mode.md` sacrosanct verbatim quoting rule. Operator's words quoted unchanged.

## Operator's verbatim words (sacrosanct)

Stated 2026-05-06 immediately after cancelling agent's empirical-count Bash command (operator confirmed cancellation was an error):

> "do not forget there is an endless knowledge in the second-brain to.. you can do multiple operations.. 30+ especially when doing research. local and or online... this is also to remember, and when you take time time to register liek when I say things like this you should continue after and that too you should register and we should do something about it adn we should find an easy way to create piling tasks for an epic as sub-task or even a task-sub-task or a task based on blockers and whatnot... Sorry I cancelled your last command it was an error. continue. make sure we elevate yourself and the project and dont be afraid to use the context and do operations especiatlly research operations. its important to be knowledgable. to be enlighted before acting uppon something. not just passing to the act without spec and readiness and a clear intelligence built and ready to use."

## Parse — directives + design principles

| # | Operator clause | Type | Action |
|---|---|---|---|
| 1 | "do not forget there is an endless knowledge in the second-brain to" | directive | REMEMBER second-brain has knowledge to consume |
| 2 | "you can do multiple operations.. 30+ especially when doing research. local and or online" | directive | USE many operations per cycle when researching; don't artificially self-cap |
| 3 | "when you take time time to register liek when I say things like this you should continue after" | directive | After registering a verbatim directive, CONTINUE substantive work — don't stop |
| 4 | "and that too you should register and we should do something about it" | directive | Register THIS directive AND act on it |
| 5 | "we should find an easy way to create piling tasks for an epic as sub-task or even a task-sub-task or a task based on blockers and whatnot" | feature-named | NEW work item: easy way to create piling/sub-tasks (epic→sub-task, task→sub-sub-task, task-from-blocker) |
| 6 | "Sorry I cancelled your last command it was an error. continue." | correction | The cancelled empirical-count Bash command was OK; continue the chain |
| 7 | "make sure we elevate yourself and the project and dont be afraid to use the context and do operations especiatlly research operations" | directive | ELEVATE — use the context, do operations, especially research |
| 8 | "its important to be knowledgable. to be enlighted before acting uppon something. not just passing to the act without spec and readiness and a clear intelligence built and ready to use" | design principle | RESEARCH-FIRST — be enlightened before acting; spec + readiness + intelligence BEFORE action |

## Cross-reference — research-first principle

Operator's "be enlighted before acting" + "spec and readiness and a clear intelligence built and ready to use" RESTATES (with elevation) `.claude/rules/operating-principles.md` principle #5 (research-first discipline). Adds emphasis on:

- Multi-operation scope: 30+ operations OK when research warrants
- Second-brain consumption: "endless knowledge" — actively reach for `<second-brain>/wiki/sources/`, `<second-brain>/wiki/spine/standards/`, MCP tools (`wiki_search`, `gateway query`)
- Online research: operator-authorized; WebFetch/WebSearch/gh CLI OK for context
- Pre-action discipline: spec → readiness → intelligence → THEN action

This elevates principle #5 from "advisory" to **operator-emphasized practice**: the agent's pattern of going-to-act without research is a discipline regression, not just a soft preference.

## Piling-tasks feature — what operator named (forward consideration)

> "we should find an easy way to create piling tasks for an epic as sub-task or even a task-sub-task or a task based on blockers and whatnot"

Three scoped task-creation patterns operator named:
1. **Epic → sub-task piling**: from an Epic, easily create sub-tasks that pile under it
2. **Task → sub-sub-task piling**: from a task, easily create deeper sub-tasks (multi-level hierarchy)
3. **Blocker → task creation**: from a blocker (e.g., a row in `wiki/governance/blockers.md` or an SB), easily spawn a corresponding task

Plus operator's "and whatnot" — leaves room for additional task-creation mechanisms operator hasn't fully specified.

Connects to:
- The forward auto-pilot rework directive (2026-05-06 `/compact` args): "creating and selecting a task based on the priorities" — same family
- Existing `tools/tasks.py` (per-task drill-down) but no creation verbs yet
- `/task` slash command (manage active-task cursor; not a creation interface)
- `wiki/backlog/{epics,modules,tasks}/` directory structure — task pages have frontmatter (status, parent_module, current_stage, readiness)

Forward-scope (NOT current grant): tooling + commands + UX for ergonomic task creation across these three patterns. Multi-Epic per operator's earlier "multiple epics and tasks equivalent when you think about it".

## Piling-tasks feature — registered as SB

Will register as SB-133 (next free row) in `wiki/governance/systemic-bugs.md` + add D037 in decisions logbook, in the same chain-fire as this log file (per SB-131 chain-batch pattern operator named).

## Cross-references

- `.claude/rules/operating-principles.md` principle #5 (research-first) — this directive elevates
- `.claude/rules/words-are-sacrosanct.md` (verbatim quoting + premise-confirmation gate)
- `.claude/rules/work-mode.md` (log directive BEFORE acting)
- 2026-05-06 forward-anchor log: `wiki/log/2026-05-06-173500-next-session-auto-pilot-forward-anchor.md` (related auto-pilot rework directive)
- `tools/tasks.py` (existing per-task drill-down; lacks creation verbs)
- `wiki/backlog/` (target directory for piled tasks)
