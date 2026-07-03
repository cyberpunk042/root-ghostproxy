# Session log — test-suite hardening + fabricated-count drift correction (2026-07-03)

> Work-block under operator goal directive: *"continue maturing root-ghostproxy"*.
> Branch `claude/ghostproxy-sovereign-os-prep-ole9ul`, restarted from `origin/main`
> after PR #3 merged (per the merged-PR rule: a merged PR is finished; follow-up
> work is a fresh change on the branch re-based to the latest default branch).

## Summary

Matured the regression-test layer (the `verified-edit` substrate per Hard Rule 14)
by fixing two real defects that made the aggregate both under-report and silently
false-green, then corrected a fabricated test-count that had propagated across four
brain files. Net: the runner now reports the true **224/224 across 12 test files**,
and the brain docs match empirical reality with a Hard Rule 15 timestamp.

## What was wrong, and the fix

### 1. `test-opt-write-block.py` — environment-coupling false-green (4/5 → 5/5)

The hook `opt-write-block.sh` resolves the second-brain root dynamically
(`RGP_SECOND_BRAIN_ROOT` env → `$HOME/devops-solutions-information-hub` → `/opt`
legacy). The test hardcoded `/opt/devops-solutions-information-hub` for its DENY
path but never told the hook to protect that same root. On any host where neither
`/opt/...` nor `$HOME/...-info-hub` exists, the hook's protected prefix and the
test's asserted path diverge — so the DENY case silently *allowed* and the test
scored the block as a pass-through. This is the SB-091 class (synthetic tests must
not silently depend on environment layout).

**Fix**: the test now pins `RGP_SECOND_BRAIN_ROOT` into every subprocess env and
derives its `OPT` path from the same value, so the prefix the hook protects and the
path the test asserts can never diverge. Deterministic regardless of ambient
filesystem.

### 2. `test-t015-op-verify-smoke.py` — aggregate under-count (0/0 → 20/20)

The suite passed 20/20 but printed `[T015-smoke] 20/20 tests passed` instead of the
canonical `Result: N/M passed` line that `tools.run-tests`' `RESULT_RE`
(`^Result:\s*(\d+)/(\d+)`) consumes. The runner counted the suite as 0/0 — green
check (rc 0), but its 20 assertions dropped out of the aggregate total silently.

**Fix**: the test now also emits the canonical `Result: 20/20 passed` line. The
aggregate went from a misleading 203/204 (opt-write-block failing, t015 uncounted)
to a true **224/224**.

### 3. `opt-write-block.sh` docstring — stale "NOT YET WIRED" (drift-fix)

The hook's own docstring said *"NOT YET WIRED in settings.json — operator approval
required"*, but `settings.json` wires it as a PreToolUse hook
(`Write|Edit|NotebookEdit → opt-write-block.sh`) and the rules docs
(hook-architecture.md, CLAUDE.md) list it as wired. Corrected to WIRED with an
empirical-verification stamp (P4 / Hard Rule 15).

### 4. Fabricated test-count across 4 brain files (Hard Rule 15)

CLAUDE.md, AGENTS.md, `.claude/rules/methodology.md`, and `.claude/rules/routing.md`
all claimed **"322/322 across 14 test files"** (AGENTS.md even split it into "9 hook
+ 5 tools test files" with a multi-step growth trace). `git ls-tree` on the recent
commits shows this tree only ever carried **11-12 hook test files and no
`tools/tests/` dir** — the 322/14 figure was never in committed history. This is
precisely the unverified count-drift Hard Rule 15 exists to catch (compounding a
count instead of measuring the source of truth).

**Fix**: all four live claims refreshed to the empirical **224/224 across 12 files
(all under `.claude/hooks/tests/`)**, each with an `empirically verified 2026-07-03`
stamp and a short note that the prior figure was never committed truth. The
append-only CONTEXT.md "Recent Work Completed" historical row (line ~262, which
narrated "→ 322/322 across 14 files" as truth-at-time-of-writing) was left
unmodified per CONTEXT.md's append-only discipline — drift in past rows is
acceptable; only live claims are corrected.

## Verification (inline, per Hard Rule 1 / P4)

```
$ HOME=<repo> python3 -m tools.run-tests
  ✓ test-opt-write-block.py                     5/  5
  ✓ test-t015-op-verify-smoke.py               20/ 20
  ... (12 files)
AGGREGATE: 224/224 PASS across 12 files
```

## Productive output

`verified-edit` — two test-layer defects fixed (opt-write-block env-coupling +
t015 aggregate under-count) + docstring drift-fix + 4-file fabricated-count
correction; regression suite green at 224/224, empirically verified.

## Cross-references

- Fixed files: `.claude/hooks/tests/test-opt-write-block.py`,
  `.claude/hooks/tests/test-t015-op-verify-smoke.py`,
  `.claude/hooks/opt-write-block.sh`, `CLAUDE.md`, `AGENTS.md`,
  `.claude/rules/methodology.md`, `.claude/rules/routing.md`
- Hard Rule 15 (empirical-count-verification before drift-claim): CLAUDE.md
- SB-091 (synthetic-tests-not-real-verification / environment coupling):
  `.claude/rules/work-mode.md`
