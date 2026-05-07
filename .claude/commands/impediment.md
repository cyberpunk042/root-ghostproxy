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

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/impediment` is part of the SB-118 objective layer triple)
- Companion objective-layer commands: [`/mission`](mission.md) (multi-cycle objective) · [`/focus`](focus.md) (sub-objective the impediment blocks) · [`/priorities`](priorities.md) (imminent-work hot-queue ABOVE objective layer per SB-127)
- Companion cursor command: [`/task`](task.md) (active backlog cursor — distinct layer; SB-124d)
- Backed by tool: [`tools/objective.py`](../../tools/objective.py) — set / clear / show subcommands
- State file: `$HOME/.claude/active-impediment` (one-line text; SB-118; comes-and-goes — empty = focus unblocked)
- Surfaces in: mode-enforcement banner (per-prompt) · end-of-cycle-stamp (per-turn) · /handoff and /terminate handoff docs · pre-compact.sh handoff
- Visibility discipline: [`.claude/rules/compound-and-waterfall.md`](../rules/compound-and-waterfall.md) — impediment row always-renders (even when empty), per SB-082 pendulum-recurrence guard (visibility ≠ presence)
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type (set/clear) OR **`read-only-audit`** action type (show) per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
