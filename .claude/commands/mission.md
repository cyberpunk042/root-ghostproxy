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
