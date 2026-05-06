# /impediment

Manage active-impediment state file (`$HOME/.claude/active-impediment`). Impediment = the specific block on the current focus, when focus is stuck. Sub-level granularity: focus is the sub-objective, impediment is what's blocking it. Empty = focus is unblocked. Comes and goes (NOT a permanent layer).

Examples:
- focus = "install.sh real-execute on sandbox" + impediment = "awaiting D024 operator turn-on"
- focus = "ship hook X" + impediment = "policy-block false-positive on `.jsonl` extension"

Surfaces in mode-enforcement hook + handoff doc + (future) stamp.

Usage from operator: `/impediment <verb> [text]`

Verbs:
- `set <text>`   → write impediment text (multi-word OK)
- `clear`        → remove the impediment state file (focus is now unblocked)
- `show`         → display current impediment

Dispatch on `$ARGUMENTS`:

If `$ARGUMENTS` starts with `set ` → run `python3 -m tools.objective set impediment $REMAINING_TEXT`
If `$ARGUMENTS` is `clear`        → run `python3 -m tools.objective clear impediment`
If `$ARGUMENTS` is `show` or empty → run `python3 -m tools.objective show impediment`

Then report the tool's stdout to the operator. Brief — one line per state.
