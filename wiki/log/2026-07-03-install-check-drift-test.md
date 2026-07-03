# Session log — install.sh --check drift-detection test (2026-07-03)

> Work-block under operator goal directive: *"continue maturing root-ghostproxy"*.
> Branch `claude/ghostproxy-sovereign-os-prep-ole9ul`, restarted from `origin/main`
> after PR #11 merged. Third increment on the install.sh behavioral seam.

## Summary

Added `.claude/hooks/tests/test-install-check-drift.py` (8 assertions) locking
`install.sh --check`'s **drift / tamper detection** — the read-only verifier that
compares the deployed tree against source and reports per-file sync state. For a
type=root security project this IS the tamper-detection surface: if a safety hook
is modified out from under the policy, `--check` must catch it. Aggregate:
**403/403 → 411/411 across 23 files** (15 hook + 8 tool). All isolated to a
throwaway `--dest`.

## What it locks (distinct from t015)

t015 covers `--check`'s exit-code + summary-line shape. This covers the
DETECTION behavior + the read-only invariant:

- fresh project install into `--dest` → `--check` reports `hooks-in-sync: N`,
  `hooks-drifted: 0`, `settings.json: in-sync`; and targets the `--dest` tree.
- **tamper a deployed safety hook** (append a line to `policy-block.sh`) →
  `--check` reports `hooks-drifted: >= 1` and drops that hook from the in-sync
  count (N → N-1). This is the tamper-detection proof.
- **read-only invariant**: `--check` does NOT auto-repair — the tampered content
  is still present after the check (it reports, never mutates).
- `--wizard` on an installed dest classifies a `route=…` + offers next-actions +
  is report-only.

## Verification (inline, per Hard Rule 1 / P4)

```
$ python3 .claude/hooks/tests/test-install-check-drift.py
  ... 8 assertions ...
  Result: 8/8 passed

$ HOME=<repo> python3 -m tools.run-tests
  ✓ test-install-check-drift.py                8/  8
  ... (23 files)
AGGREGATE: 411/411 PASS across 23 files
```

## Productive output

`verified-edit` — install.sh --check drift/tamper-detection test
(.claude/hooks/tests/test-install-check-drift.py, 8 assertions via
install→tamper→check in an isolated --dest), proving the verifier surfaces a
modified safety hook and never auto-repairs; suite green at 411/411 across 23
files. Counts refreshed across CLAUDE.md / AGENTS.md / methodology.md / routing.md.

## Cross-references

- Added: `.claude/hooks/tests/test-install-check-drift.py`
- Installer surface under test: `install.sh --check` (drift/tamper detection) + `--wizard` (route)
- Complements: `test-t015-op-verify-smoke.py` (--check exit/summary shape),
  `test-t016-idempotency-smoke.py` (idempotency), `test-install-composition.py` (profile/mode/granular)
- Security relevance: tamper detection is the type=root fail-closed surface (SECURITY.md)
