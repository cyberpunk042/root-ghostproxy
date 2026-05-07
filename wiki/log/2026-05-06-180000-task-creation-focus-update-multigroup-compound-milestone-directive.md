---
title: "Task-creation + focus-update + multi/group-tool-calls — additive compound-layer Milestone (operator-named, multi-Epic)"
type: log
subtype: operator-directive
domain: cross-domain
status: registered-for-scope-confirmation
created: 2026-05-06
sources:
  - id: operator-directive-2026-05-06-task-creation-compound-milestone
    type: directive
    file: this file (operator-verbatim, sacrosanct)
tags: [operator-directive, sacrosanct, milestone, task-creation, focus-update, multi-group-tool-calls, compound-additive, waterfall-pending-query, ai-ergonomics]
---

# Task-creation + focus-update + multi/group-tool-calls — additive compound-layer Milestone

> Logged BEFORE acting per `.claude/rules/work-mode.md`. This directive is multi-Epic in operator's own framing — not single-fire-buildable. This file: verbatim quote + literal decomposition + structural questions for operator scope confirmation. Solution shape is operator-domain.

## Operator's verbatim words (sacrosanct — quote unchanged)

Stated 2026-05-06 (cron prompt context, dual-expert mode active):

> "what I said about tasks creation and focus update and multi/group tool calls is real too and very important.. we want to make things simpler for the AI.. avoid creating a nightmare prompt or polution and useless data or even negative information. again this is additive.. it should be adding to the compound list.. not to confuse with the priorities or the tasks. but it make sense sometimes to just create a task or even tasks to address the focus, the mission or even before that the priorities. you shouold in those case naturally use the tool to coumpound and when you will use the waterfall to ask what is pending to pass to a next task you will be able to get back on track and not lose track of any request or compound or demands or requirements or questions and whatnot. taek a deep time to think about all this. this is multiple Epics and tasks and you can even create a milestone and inside we will suggest this kind of evolution like I am currently driving manually but can be implied and directed and offered as options / tools and explained properly and such"

## Literal decomposition (no inference, no solution shape)

| # | Operator clause | Type | Literal content (preserved) |
|---|---|---|---|
| 1 | "what I said about tasks creation and focus update and multi/group tool calls is real too and very important" | emphasis | three named components: tasks creation, focus update, multi/group tool calls — **real** and **very important** |
| 2 | "we want to make things simpler for the AI" | design value | simplicity-for-AI is the goal |
| 3 | "avoid creating a nightmare prompt or polution and useless data or even negative information" | anti-pattern (4 named) | avoid: nightmare-prompt / pollution / useless-data / negative-information |
| 4 | "again this is additive.. it should be adding to the compound list" | placement | this layer is ADDITIVE to compound stack (per `.claude/rules/compound-and-waterfall.md`) |
| 5 | "not to confuse with the priorities or the tasks" | distinction | this is its OWN layer; NOT priorities (SB-127); NOT tasks (`wiki/backlog/tasks/`) |
| 6 | "but it make sense sometimes to just create a task or even tasks to address the focus, the mission or even before that the priorities" | concrete pattern | task creation can target: focus / mission / priorities (3 levels named) |
| 7 | "you shouold in those case naturally use the tool to coumpound" | expected behavior | when case arises, agent NATURALLY uses tool to compound (add to layered context) |
| 8 | "when you will use the waterfall to ask what is pending to pass to a next task you will be able to get back on track and not lose track of any request or compound or demands or requirements or questions and whatnot" | mechanism | on waterfall (cycle handoff), query "what is pending?" → answer comes from compound stack → no loss of: request / compound / demand / requirement / question / "whatnot" (6 named retention categories) |
| 9 | "taek a deep time to think about all this" | directive | TAKE TIME — don't rush |
| 10 | "this is multiple Epics and tasks" | scope | multi-Epic, multi-task |
| 11 | "you can even create a milestone and inside we will suggest this kind of evolution" | optional structural | a Milestone could contain Epics suggesting this evolution |
| 12 | "like I am currently driving manually" | current state | operator drives manually today |
| 13 | "but can be implied and directed and offered as options / tools and explained properly and such" | future state | should be: implied / directed / offered-as-options / offered-as-tools / explained-properly |

## What operator literally named (the components, not the build)

### Three named components (clause 1)

1. **Tasks creation** — programmatic creation of tasks at any level
2. **Focus update** — updating `active-focus` (and presumably `active-mission`, `active-impediment`) as work evolves
3. **Multi/group tool calls** — chain/batch tool operations (cousin to SB-131 chain-operations pattern operator already established)

### Four anti-patterns (clause 3)

| Anti-pattern | Literal name |
|---|---|
| 1 | nightmare prompt |
| 2 | pollution |
| 3 | useless data |
| 4 | negative information |

### Three task-creation targets (clause 6)

| Target tier | Source layer (already in project) |
|---|---|
| Focus | `$HOME/.claude/active-focus` (SB-118) |
| Mission | `$HOME/.claude/active-mission` (SB-118) |
| Priorities | `$HOME/.claude/active-priorities` (SB-127) |

### Six retention categories (clause 8 — what compound MUST NOT lose)

1. request
2. compound
3. demand
4. requirement
5. question
6. "whatnot" (open-ended — operator-acknowledged extensibility)

### Five future-state delivery channels (clause 13)

1. implied (background detection by agent)
2. directed (cycle-driven action)
3. offered-as-options (UI-style: agent proposes; operator picks)
4. offered-as-tools (agent invokes deterministically)
5. explained-properly (each suggestion has rationale)

## Structural questions for operator scope confirmation (NOT solution shape)

Per "take a deep time to think" + "this is multiple Epics and tasks" — operator-domain decisions:

| # | Question | Why it matters |
|---|---|---|
| Q1 | Should this be the new top-level Milestone (e.g., v0.2 — AI-Natural Task Management) inside the existing Epic, OR a separate Epic alongside SFIF Rollout? | Affects backlog hierarchy + how progress.md tracks it |
| Q2 | The "compound layer" for retention — should it be a single state file (e.g., `$HOME/.claude/active-pending-queue` with structured rows for request/demand/requirement/question), OR multiple parallel files (one per retention category)? | Affects file count + parser complexity |
| Q3 | "Multi/group tool calls" — naming + scope: Does this become a new tool (`tools/group.py`?), an extension to existing tools (chain verbs added to each tool), or rule-only guidance (extend SB-131 rule with explicit chain-detection)? | Affects build vs document approach |
| Q4 | Task creation programmatically — does it write to `wiki/backlog/tasks/T###-slug.md` directly (full frontmatter + parent_module + sfif_stage), OR write to a lightweight queue first that operator then promotes? | Affects safety vs ergonomics tradeoff |
| Q5 | Focus update tool — currently `/focus set <text>` works. Does the AI gain authority to update focus on its own (mid-cycle) without operator confirmation, OR always propose-and-confirm? | Affects agent-authority boundary |
| Q6 | "Naturally use the tool to compound" — what triggers "naturally"? Operator asks question? Operator names new requirement? Cycle observes new SB? Each is a different trigger surface. | Affects trigger-design (per `.claude/rules/trigger-model.md`) |
| Q7 | "What is pending?" waterfall query — should this be a new slash command (`/pending`)? A view inside `/cycle`? An MCP tool? A section in handoff doc? | Affects discoverability |

## Connection to other already-registered forward directives

This Milestone overlaps with three already-logged directives:

1. **Auto-pilot rework** (`/root/wiki/log/2026-05-06-173500-next-session-auto-pilot-forward-anchor.md`): the auto-pilot's "select action" step is exactly the "naturally use the tool to compound + create task" pattern operator named here. Same family.

2. **Research-elevation + piling-tasks feature** (`/root/wiki/log/2026-05-06-174500-research-elevation-and-piling-tasks-feature.md`): the piling-tasks feature ("epic→sub-task / task-from-blocker") is the **task creation** component (#1) of this Milestone. Same family.

3. **Compound + waterfall** (`.claude/rules/compound-and-waterfall.md`): this Milestone EXTENDS the compound axis with an additional retention layer; extends the waterfall axis with a "what's pending" query channel.

The three forward directives + this Milestone form one coherent scope. Operator's framing is consistent: this is a multi-Epic delivery to make the agent operate **naturally** + **in compound** + **without losing track**, currently done **manually** by operator.

## What I am NOT doing this fire (per discipline)

- NOT creating the Milestone structure unilaterally (operator-domain Q1)
- NOT building the compound state file (operator-domain Q2)
- NOT writing tools/group.py or tools/task-create.py (operator-domain Q3, Q4)
- NOT extending agent authority on focus updates (operator-domain Q5)
- NOT designing trigger surfaces (operator-domain Q6)
- NOT writing /pending command (operator-domain Q7)

What I AM doing: registering verbatim, decomposing literally, surfacing structural questions for operator scope confirmation. Per "take a deep time to think" — thinking = considered analysis surfaced for confirmation, not unilateral construction.

## Cross-references

- `.claude/rules/words-are-sacrosanct.md` — verbatim quoting + premise-confirmation gate
- `.claude/rules/work-mode.md` — log directive BEFORE acting
- `.claude/rules/compound-and-waterfall.md` — compound (additive) + waterfall (sequential) axes this Milestone extends
- `.claude/rules/trigger-model.md` — trigger surface design (relevant to Q6)
- `.claude/rules/operating-principles.md` principle #5 (research-first elevation, operator 2026-05-06)
- Auto-pilot forward anchor: `/root/wiki/log/2026-05-06-173500-next-session-auto-pilot-forward-anchor.md`
- Research-elevation + piling-tasks: `/root/wiki/log/2026-05-06-174500-research-elevation-and-piling-tasks-feature.md`
- Post-/terminate delta handoff: `/root/wiki/log/2026-05-06-175000-post-terminate-delta-handoff.md`
- Existing layers this Milestone extends: SB-118 (mission/focus/impediment), SB-127 (priorities), SB-131 (chain-operations pattern), SB-123 (compound+waterfall axes)
- Existing tasks layer: `wiki/backlog/{epics,modules,tasks}/`
