---
description: Manage agent-pending questions to operator. Questions accumulate in $HOME/.claude/active-questions and surface in mode-enforcement banner + stamp + pre-compact handoff. Per-question SRP detail companion files at $HOME/.claude/active-questions-detail/Q<N>.md (presweep enrichment). Operator directive 2026-05-06 — *"if there is question and I dont see them its about the same as if there was no question"*. Verbs: add/show/clear/remove/answer/promote/demote/set/update/insert/detail/solve (12 verbs). `solve <selector>` enters solving-mode view (selector = first|last|all|N|N,M|Q1).
argument-hint: [add <text> | show | clear | remove <N> | answer <N> | promote <N> | demote <N> | set <text> | update <N> <text> | insert <N> <text> | detail <N> [<text>] | solve [first|last|all|N|N,M|Q1]]
---

# /questions — agent-pending-questions accumulation layer

State file: `$HOME/.claude/active-questions` (one question per line).

Part of the E003 compound retention layer (Milestone v0.2). Closes operator-stated bug: *"questions that do not cummulate in a file like it should and surface to me"*.

## Verbs

| Verb | Action |
|---|---|
| `add <text>` | Append a new agent-pending question to the list |
| `show` | Display all pending questions numbered Q1..QN |
| `clear` | Empty the entire question list |
| `remove <N>` | Drop question N (1-based index) |
| `answer <N>` | Drop question N — semantic alias of remove (operator answered it) |
| `promote <N>` | Move question N up one rank |
| `demote <N>` | Move question N down one rank |
| `set <text>` | Replace whole list with semicolon-separated entries |
| `update <N> <text>` | Replace text of question N (position unchanged) |
| `insert <N> <text>` | Insert question at position N (shifts rest down) |
| `detail <N> [<text>]` | Show or write SRP detail companion file for question N |
| `solve [first\|last\|all\|N\|N,M\|Q1]` | Solving-mode view — selected Qs with full detail + answer hints (default: all) |

## Steps

```bash
ARG="$ARGUMENTS"
case "$ARG" in
  ""|"show") /opt/devops-solutions-information-hub/.venv/bin/python -m tools.questions show ;;
  "clear")   /opt/devops-solutions-information-hub/.venv/bin/python -m tools.questions clear ;;
  *)         /opt/devops-solutions-information-hub/.venv/bin/python -m tools.questions ${ARG} ;;
esac
```

## Composition

- Mode-enforcement banner surfaces pending questions inline so they appear every prompt
- Stamp surfaces question count + first 3 (forward-anchor for next-fire pickup)
- /handoff doc + PreCompact handoff doc include question list

## When to invoke

- Agent generates a scope/design question for operator → agent calls `/questions add <text>` so the question accumulates rather than vanishing into response prose
- Operator wants to see what's outstanding from the agent → `/questions show`
- Operator answers a question → `/questions answer <N>` to remove it from the queue

## Cross-references

- `tools/questions.py` (backing tool)
- `wiki/backlog/epics/epic-e003-compound-retention-and-multi-group.md` (parent Epic for retention layers)
- `.claude/commands/priorities.md` (parallel pattern: /priorities is operator-authored hot-queue; /questions is agent-authored input-needed queue)
