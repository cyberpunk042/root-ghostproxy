# Session log — tool-layer test coverage: tools.stamp (2026-07-03)

> Work-block under operator goal directive: *"continue maturing root-ghostproxy"*.
> Branch `claude/ghostproxy-sovereign-os-prep-ole9ul`, restarted from `origin/main`
> after PR #7 merged. Seventh tool-layer regression test.

## Summary

Added `tools/tests/test-stamp.py` (18 assertions) covering `tools/stamp.py` — the
SB-115 persistent stamp-render config ($HOME/.claude/stamp-config.json). The
end-of-cycle-stamp.sh hook reads this file on every Stop event to decide layout /
enabled / density, so its **defensive sanitization** is load-bearing: an invalid
or corrupt value must be coerced back to a safe default, never propagated to the
render hook. Zero coverage until now. Aggregate: **348/348 → 366/366 across 19
files** (12 hook + 7 tool).

## What it covers

The standout is `load_config()`'s robustness — the distinct invariant this tool
adds to the suite (prior tool tests locked arithmetic / independence / parsing;
this one locks config-sanitization):

- **absent** file → `DEFAULT_CONFIG`.
- **valid** values load through; a **partial** config keeps defaults for the
  missing keys (the `{**DEFAULT, **data}` merge).
- **invalid** `layout` / `enabled` / `density` values → each independently
  coerced back to its default (the per-field validation fallbacks).
- **corrupt** (non-JSON) → `DEFAULT_CONFIG` (the exception path).
- **wrong-type** (valid JSON that is a list, not a dict) → `DEFAULT_CONFIG`.
- **save → load** round-trips values (incl. `highlight_deltas` bool).

CLI (HOME-isolated subprocess): `configure --layout` persists;
`--highlight-deltas true|false` coerces the string to a real bool; an invalid
`--enabled` is rejected by argparse choices (exit 2); re-setting the same value
reports "unchanged"; `clear` removes the file (defaults reapply) and is rc 0 on
an already-absent file.

## Verification (inline, per Hard Rule 1 / P4)

```
$ HOME=<repo> python3 -m tools.run-tests
  ✓ test-stamp.py                              18/ 18
  ... (19 files)
AGGREGATE: 366/366 PASS across 19 files
```

## Productive output

`verified-edit` — seventh tool-layer regression test (tools/tests/test-stamp.py, 18
assertions on the stamp-config load/save, centered on load_config's defensive
sanitization — invalid/corrupt/wrong-type all fall back to safe defaults — plus
the configure/clear CLI + highlight-deltas bool coercion); suite green at 366/366
across 19 files. Counts refreshed across CLAUDE.md / AGENTS.md / methodology.md /
routing.md.

## Cross-references

- Added: `tools/tests/test-stamp.py`
- Tool under test: `tools/stamp.py` (SB-115 stamp config; read by end-of-cycle-stamp.sh Stop hook)
- Sibling increments: the six prior `wiki/log/2026-07-03-tool-test-coverage-*.md` +
  `2026-07-03-test-suite-hardening-and-count-drift-correction.md`
