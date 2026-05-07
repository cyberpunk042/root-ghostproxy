# /focus

Manage active-focus state file (`$HOME/.claude/active-focus`). Focus = the current sub-objective inside the mission. Surfaces in mode-enforcement hook + handoff doc + (future) stamp.

Usage from operator: `/focus <verb> [text]`

Verbs:
- `set <text>`   → write focus text (multi-word OK)
- `clear`        → remove the focus state file
- `show`         → display current focus

Dispatch on `$ARGUMENTS`:

If `$ARGUMENTS` starts with `set ` → run `python3 -m tools.objective set focus $REMAINING_TEXT`
If `$ARGUMENTS` is `clear`        → run `python3 -m tools.objective clear focus`
If `$ARGUMENTS` is `show` or empty → run `python3 -m tools.objective show focus`

Then report the tool's stdout to the operator. Brief — one line per state.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/focus` is part of the SB-118 objective layer triple)
- Companion objective-layer commands: [`/mission`](mission.md) (multi-cycle objective above focus) · [`/impediment`](impediment.md) (block on focus) · [`/priorities`](priorities.md) (imminent-work hot-queue ABOVE objective layer per SB-127)
- Companion cursor command: [`/task`](task.md) (active backlog cursor — distinct layer; SB-124d)
- Backed by tool: [`tools/objective.py`](../../tools/objective.py) — set / clear / show subcommands
- State file: `$HOME/.claude/active-focus` (one-line text; SB-118)
- Surfaces in: mode-enforcement banner (per-prompt) · end-of-cycle-stamp (per-turn) · /handoff and /terminate handoff docs · pre-compact.sh handoff
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type (set/clear) OR **`read-only-audit`** action type (show) per Hard Rule 14
- Compound + waterfall: [`.claude/rules/compound-and-waterfall.md`](../rules/compound-and-waterfall.md) — focus is one of the always-rendered compound layers
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
