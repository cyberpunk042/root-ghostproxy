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
