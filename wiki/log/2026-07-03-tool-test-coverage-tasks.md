# Session log — tool-layer test coverage: tools.tasks (2026-07-03)

> Work-block under operator goal directive: *"continue maturing root-ghostproxy"*.
> Branch `claude/ghostproxy-sovereign-os-prep-ole9ul`, restarted from `origin/main`
> after PR #6 merged. Sixth tool-layer regression test.

## Summary

Added `tools/tests/test-tasks.py` (25 assertions) covering `tools/tasks.py` — the
backlog task parser + SB-124d active-task cursor. It backs the `/task` command,
pre-compact.sh's snapshot, and tools.cycle. Its regex parsers (checkbox counting,
BLOCKED-BY extraction, quoted-frontmatter stripping) are the fiddly kind where a
silent regression would mis-report task readiness or hide a blocker. Zero
coverage until now. Aggregate: **323/323 → 348/348 across 18 files** (12 hook + 6
tool).

## What it covers

Two isolation styles:
- **Parsers / filters** run in-process against fixture `.md` files + hand-built
  dict lists (no repo backlog touched).
- **Active-task cursor** runs as a subprocess with `HOME` at a temp dir
  (ACTIVE_TASK_FILE is HOME-derived), so the cursor file is sandboxed.

Locked behavior:
- **parse_frontmatter** — key:value extraction, quote-stripping on values;
  non-frontmatter file → `{}`; missing file → `{}`.
- **parse_done_when** — counts `- [x]` / `- [X]` (case-insensitive) vs `- [ ]`;
  total = checked + unchecked; no section → all zero.
- **parse_blocked_by** — extracts the T-ids from `BLOCKED BY: T001, T002`; no
  Dependencies section → `[]`.
- **collect_task** — id from the filename stem (`T042` from `T042-*.md`), title
  from the `# Heading`, nests done_when + blocked_by.
- **filter_tasks** — by status / by module (case-insensitive substring) / by
  priority / no-filter passthrough.
- **claimable_tasks** — not-started AND no blocked_by (a blocked not-started task
  is correctly excluded).
- **active cursor** — `show` unset → `(none)`; `set <bogus>` → refused, rc 1, no
  cursor written (validated against the real backlog, so a bogus id is
  deterministically rejected); a stale cursor is *reported* not crashed; `clear`
  → rc 0.

## Verification (inline, per Hard Rule 1 / P4)

```
$ HOME=<repo> python3 -m tools.run-tests
  ✓ test-tasks.py                              25/ 25
  ... (18 files)
AGGREGATE: 348/348 PASS across 18 files
```

## Productive output

`verified-edit` — sixth tool-layer regression test (tools/tests/test-tasks.py, 25
assertions on the backlog parsers + filters + active-task cursor, incl. the
checkbox-count / blocked-by-extraction / claimable-derivation logic and the
cursor set-validation + stale-cursor handling); suite green at 348/348 across 18
files. Counts refreshed across CLAUDE.md / AGENTS.md / methodology.md / routing.md.

## Cross-references

- Added: `tools/tests/test-tasks.py`
- Tool under test: `tools/tasks.py` (backlog parser + SB-124d cursor; backs /task + pre-compact.sh + tools.cycle)
- Sibling increments: the five prior `wiki/log/2026-07-03-tool-test-coverage-*.md` +
  `2026-07-03-test-suite-hardening-and-count-drift-correction.md`
