# /mission

Manage active-mission state file (`$HOME/.claude/active-mission`). Mission = the multi-cycle objective the agent is driving toward. Surfaces in mode-enforcement hook + handoff doc + (future) stamp.

Usage from operator: `/mission <verb> [text]`

Verbs:
- `set <text>`   → write mission text (multi-word OK)
- `clear`        → remove the mission state file
- `show`         → display current mission

Dispatch on `$ARGUMENTS`:

If `$ARGUMENTS` starts with `set ` → run `python3 -m tools.objective set mission $REMAINING_TEXT`
If `$ARGUMENTS` is `clear`        → run `python3 -m tools.objective clear mission`
If `$ARGUMENTS` is `show` or empty → run `python3 -m tools.objective show mission`

Then report the tool's stdout to the operator. Brief — one line per state.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/mission` is part of the SB-118 objective layer triple)
- Companion objective-layer commands: [`/focus`](focus.md) (sub-objective inside mission) · [`/impediment`](impediment.md) (block on focus) · [`/priorities`](priorities.md) (imminent-work hot-queue ABOVE objective layer per SB-127)
- Companion cursor command: [`/task`](task.md) (active backlog cursor — distinct layer; SB-124d)
- Backed by tool: [`tools/objective.py`](../../tools/objective.py) — set / clear / show subcommands; same backing tool serves mission/focus/impediment
- State file: `$HOME/.claude/active-mission` (one-line text; SB-118)
- Surfaces in: mode-enforcement banner (per-prompt) · end-of-cycle-stamp (per-turn) · /handoff and /terminate handoff docs · pre-compact.sh handoff
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type (set/clear) OR **`read-only-audit`** action type (show) per Hard Rule 14
- Compound + waterfall: [`.claude/rules/compound-and-waterfall.md`](../rules/compound-and-waterfall.md) — mission is one of the always-rendered compound layers
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
