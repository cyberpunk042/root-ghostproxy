# /priorities

Manage active-priorities imminent-work queue (`$HOME/.claude/active-priorities`). Top-priorities = items that take precedence over PM-decision-tier work (real blockers / Epic-pending / behavioral). Operator-authored hot-list. Surfaces in mode-enforcement banner + stamp + (when wired) statusline.

Usage from operator: `/priorities <verb> [args]`

Verbs:
- `add <text>`            → append at lowest priority
- `show`                  → display numbered list (P1, P2, ...)
- `clear`                 → empty the list
- `remove <N>`            → drop priority N (1-based)
- `promote <N>`           → move priority N up one rank
- `demote <N>`            → move priority N down one rank
- `set <text>`            → replace entire list (semicolon-separated for multi)
- `insert <N> <text>`     → insert at position N, shifting rest down (SB-130)
- `update <N> <text>`     → replace text at position N without touching others (SB-130)

Dispatch on `$ARGUMENTS`:

If `$ARGUMENTS` starts with `add `       → run `python3 -m tools.priorities add $REMAINING`
If `$ARGUMENTS` is `show` or empty       → run `python3 -m tools.priorities show`
If `$ARGUMENTS` is `clear`               → run `python3 -m tools.priorities clear`
If `$ARGUMENTS` starts with `remove `    → run `python3 -m tools.priorities remove $N`
If `$ARGUMENTS` starts with `promote `   → run `python3 -m tools.priorities promote $N`
If `$ARGUMENTS` starts with `demote `    → run `python3 -m tools.priorities demote $N`
If `$ARGUMENTS` starts with `set `       → run `python3 -m tools.priorities set $REMAINING`

Then report tool stdout to operator. Brief — one line per priority.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/priorities` is the SB-127 imminent-work hot-queue tier ABOVE PM blockers)
- Tier hierarchy: priorities (imminent) > mission/focus/impediment (SB-118 objective) > backlog cursor (SB-124d /task) > PM blockers (B###) > general work
- Companion objective-layer commands: [`/mission`](mission.md) · [`/focus`](focus.md) · [`/impediment`](impediment.md)
- Companion cursor: [`/task`](task.md)
- Companion governance commands: [`/blockers`](blockers.md) (PM-decision-tier; priorities take precedence over these)
- Backed by tool: [`tools/priorities.py`](../../tools/priorities.py) — 9 verbs incl. SB-130 insert/update at-position
- State file: `$HOME/.claude/active-priorities` (one-priority-per-line; SB-127)
- Surfaces in: mode-enforcement banner · end-of-cycle-stamp · statusline (when wired) · /handoff and /terminate handoff docs · pre-compact.sh handoff
- Mindfulness clause #5 (P1-first): [`.claude/hooks/mindfulness.sh`](../hooks/mindfulness.sh) — agent must address top priority FIRST per cycle; jumping to lower-priority items = short-circuit (SB-128 family)
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type (mutations) OR **`read-only-audit`** action type (show) per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
