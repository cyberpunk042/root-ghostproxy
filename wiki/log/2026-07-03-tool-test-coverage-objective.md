# Session log — tool-layer test coverage: tools.objective (2026-07-03)

> Work-block under operator goal directive: *"continue maturing root-ghostproxy"*.
> Batched into the same PR as `test-priorities.py` (branch
> `claude/ghostproxy-sovereign-os-prep-ole9ul`) — a coherent "tool-layer
> coverage" pass rather than one PR per tool.

## Summary

Added `tools/tests/test-objective.py` (20 assertions) — the third tool-layer
regression test — covering `tools/objective.py`, the SB-118 objective layer
(mission / focus / impediment). These three single-line state files are read by
the mode-enforcement banner + stamp every prompt. Aggregate: **267/267 → 287/287
across 15 files** (12 hook + 3 tool).

## What it covers, and why

The load-bearing invariant here is **layer independence**: set/clear on one
layer must never touch another. A regression that coupled them (e.g. a shared
path bug, or a clear that truncated the wrong file) would silently corrupt the
operator's mission/focus/impediment view with no crash. The tests set all three,
clear one, and assert the other two are untouched — in both directions
(clear-focus-keeps-mission/impediment; re-set-mission-doesn't-resurrect-focus).

Also pinned:
- `show` with no arg renders **all three** layers, unset ones as `(unset)` — the
  SB-082 visibility-vs-presence lesson (operator must see the empty layer, not a
  collapsed subset).
- `show <layer>` renders only that layer; `-v` prints the state-file path.
- `set` empty/whitespace → exit 2, writes nothing.
- `clear` on an absent layer is rc 0 (reports already-absent).
- Invalid layer name rejected by argparse `choices` (exit 2), and the error
  names the valid choices.

Same subprocess-isolation pattern as test-priorities: real
`python3 -m tools.objective` invocations with `HOME` at a fresh temp dir.

## Verification (inline, per Hard Rule 1 / P4)

```
$ HOME=<repo> python3 -m tools.run-tests
  ✓ test-objective.py                          20/ 20
  ✓ test-priorities.py                         26/ 26
  ... (15 files)
AGGREGATE: 287/287 PASS across 15 files
```

## Productive output

`verified-edit` — third tool-layer regression test (tools/tests/test-objective.py,
20 assertions on the SB-118 mission/focus/impediment layer, centered on the
layer-independence invariant); suite green at 287/287 across 15 files. Counts
refreshed across CLAUDE.md / AGENTS.md / methodology.md / routing.md.

## Cross-references

- Added: `tools/tests/test-objective.py`
- Tool under test: `tools/objective.py` (SB-118 objective layer)
- Sibling increments: `wiki/log/2026-07-03-tool-test-coverage-priorities.md`,
  `wiki/log/2026-07-03-test-suite-hardening-and-count-drift-correction.md`
