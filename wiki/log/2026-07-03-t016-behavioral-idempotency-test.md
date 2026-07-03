# Session log — T016 behavioral idempotency test (2026-07-03)

> Work-block under operator goal directive: *"continue maturing root-ghostproxy"*.
> Branch `claude/ghostproxy-sovereign-os-prep-ole9ul`, restarted from `origin/main`
> after PR #9 merged. Pivot from the (now-complete) tool-coverage campaign to a
> different, higher-value maturation dimension: the FOUNDATION installer.

## Summary

Added `.claude/hooks/tests/test-t016-idempotency-smoke.py` (9 assertions) — the
first **behavioral** (not merely documentary) coverage of install.sh's
idempotency invariant, the methodology test-stage gate for IaC (*"idempotent
re-run is no-op"*). Advances T016 (DW#6a → implemented as DW#6c). Aggregate:
**383/383 → 392/392 across 21 files** (13 hook + 8 tool).

## Why this, and why it's safe

The tool-coverage campaign closed at PR #9 (8 tools; the remaining 4 need the
absent `mcp` package or heavy scaffolding). Rather than push into that fragile
tail, this pivots to the actual foundation deliverable — `install.sh` — which is
higher-value maturation.

T016 had documented the idempotency invariant + a testable recipe (DW#6a), but
the recipe was never *run as a test*. This closes that gap safely:
`install.sh --profile project --dest <tmpdir>` deploys only the agent brain +
tools into `--dest` and disables ALL OS-level ops (bridge / wifi / integrity /
ccstatusline / opencode), so the entire effect is confined to a throwaway temp
dir — no host state touched. Running it twice exercises the real installer.

## The invariant it locks (empirically discovered this session)

```
run 1 (fresh):   105 `installed:`   0 `unchanged:`   5 `skip:`
run 2 (re-run):    0 `installed:`  105 `unchanged:`   5 `skip:`   0 `updated:`   0 backups
```

The test asserts the relationships (not hardcoded 105, so it doesn't drift as
brain files are added): run 2 installs nothing, updates nothing, backs up
nothing, and reports every previously-installed file `unchanged:` (count matches
run 1), with a stable skip count. Plus structural checks that `.claude/` +
`tools/` actually landed in the isolated dest.

Note: the installer's post-install op_verify exits non-zero under `project`
profile (it checks OS-level artefacts project-mode intentionally doesn't
deploy), so the test asserts on ACTION lines, not the process exit code —
op_verify's project-mode behavior is a separate concern (T015's territory). This
is called out in the test's own docstring.

## T016 advanced

`wiki/backlog/tasks/T016-document-idempotency-invariants.md`:
- New Done-When item DW#6c (behavioral test landed).
- New Test-Plan row DW#6c with the gate command.
- Resolution addendum + `updated: 2026-05-16 → 2026-07-03`.
- DW#6b (full OS-level real-execute on a Debian 13 host) remains operator-territory
  per D024 — unchanged.

## Verification (inline, per Hard Rule 1 / P4)

```
$ python3 .claude/hooks/tests/test-t016-idempotency-smoke.py
  ... 9 assertions ...
  Result: 9/9 passed

$ HOME=<repo> python3 -m tools.run-tests
  ✓ test-t016-idempotency-smoke.py             9/  9
  ... (21 files)
AGGREGATE: 392/392 PASS across 21 files
```

## Productive output

`verified-edit` — first behavioral idempotency test of the foundation installer
(.claude/hooks/tests/test-t016-idempotency-smoke.py, 9 assertions via isolated
double-install), advancing T016 to behaviorally-tested; suite green at 392/392
across 21 files. T016 task page + brain-file counts refreshed.

## Cross-references

- Added: `.claude/hooks/tests/test-t016-idempotency-smoke.py`
- Task advanced: `wiki/backlog/tasks/T016-document-idempotency-invariants.md` (DW#6c)
- Installer under test: `install.sh` (M003 Foundation deliverable)
- Sibling install smoke tests: `.claude/hooks/tests/test-t014-endpoint-safety-smoke.py`,
  `test-t015-op-verify-smoke.py`
- Tool-coverage campaign (prior arc): the eight `wiki/log/2026-07-03-tool-test-coverage-*.md` +
  `2026-07-03-test-suite-hardening-and-count-drift-correction.md`
