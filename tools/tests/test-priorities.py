#!/usr/bin/env python3
"""Regression tests for tools/priorities.py — the SB-127 imminent-work queue.

priorities.py drives the highest tier of the objective ladder (imminent >
mission/focus/impediment > cursor > PM blockers) and surfaces in the
mode-enforcement banner + stamp. Its mutation verbs (promote/demote/insert/
remove/update) are 1-based index arithmetic — exactly where an off-by-one
silently reorders or drops an operator's stated priorities. This suite locks
that arithmetic and the range-guard exit codes.

Isolation: each verb runs as a real subprocess (`python3 -m tools.priorities
...`) with HOME pointed at a fresh temp dir, so the state file
($HOME/.claude/active-priorities) is fully sandboxed and the real argparse CLI
is exercised end-to-end — no monkeypatching of the module-level PATH.

Emits the canonical `Result: N/M passed` line consumed by tools.run-tests.
Exit 0 iff all pass.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_REL = ".claude/active-priorities"

PASSED: list[str] = []
FAILED: list[tuple[str, str]] = []


def check(label: str, cond: bool, detail: str = "") -> None:
    if cond:
        PASSED.append(label)
        print(f"  PASS {label}")
    else:
        FAILED.append((label, detail))
        print(f"  FAIL {label}" + (f" — {detail}" if detail else ""))


def run(home: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "tools.priorities", *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
        env={"HOME": str(home), "PATH": __import__("os").environ.get("PATH", "")},
    )


def state(home: Path) -> list[str]:
    f = home / STATE_REL
    if not f.exists():
        return []
    return [ln for ln in f.read_text().splitlines() if ln.strip()]


def fresh():
    d = tempfile.mkdtemp(prefix="priorities-test-")
    return Path(d)


def test_add_show_order() -> None:
    h = fresh()
    run(h, "add", "first")
    run(h, "add", "second one")  # multi-word joins
    check("add appends in order", state(h) == ["first", "second one"])
    r = run(h, "show")
    check("show numbers 1-based highest-first", "P1: first" in r.stdout and "P2: second one" in r.stdout)
    check("add rc 0", run(h, "add", "third").returncode == 0)


def test_add_empty_rejected() -> None:
    h = fresh()
    r = run(h, "add", "   ")
    check("add empty/whitespace text → exit 2", r.returncode == 2)
    check("add empty leaves no state", state(h) == [])


def test_set_semicolon_split() -> None:
    h = fresh()
    run(h, "add", "will-be-replaced")
    run(h, "set", "a ; b ; c")
    check("set replaces whole list, splits on ';'", state(h) == ["a", "b", "c"])
    run(h, "set", "solo")
    check("set single item replaces all", state(h) == ["solo"])


def test_insert_shifts_down() -> None:
    h = fresh()
    run(h, "set", "a ; b ; c")
    run(h, "insert", "1", "top")
    check("insert@1 shifts rest down", state(h) == ["top", "a", "b", "c"])
    run(h, "insert", "3", "mid")
    check("insert@mid keeps head + shifts tail", state(h) == ["top", "a", "mid", "b", "c"])
    # valid range is 1..len+1 (append via insert at end+1)
    run(h, "insert", str(len(state(h)) + 1), "tail")
    check("insert@len+1 appends", state(h)[-1] == "tail")
    r = run(h, "insert", "99", "nope")
    check("insert out-of-range → exit 2", r.returncode == 2)
    check("insert out-of-range does not mutate", "nope" not in state(h))


def test_update_in_place() -> None:
    h = fresh()
    run(h, "set", "a ; b ; c")
    run(h, "update", "2", "B-new")
    check("update@2 replaces only that slot", state(h) == ["a", "B-new", "c"])
    r = run(h, "update", "0", "x")
    check("update position 0 → exit 2 (1-based)", r.returncode == 2)
    r = run(h, "update", "4", "x")
    check("update past end → exit 2", r.returncode == 2)


def test_remove_range() -> None:
    h = fresh()
    run(h, "set", "a ; b ; c")
    run(h, "remove", "2")
    check("remove@2 drops the middle", state(h) == ["a", "c"])
    r = run(h, "remove", "9")
    check("remove out-of-range → exit 2", r.returncode == 2)
    r = run(h, "remove", "0")
    check("remove 0 → exit 2 (1-based)", r.returncode == 2)


def test_promote_demote_swaps() -> None:
    h = fresh()
    run(h, "set", "a ; b ; c")
    run(h, "promote", "3")  # swap P3<->P2
    check("promote@3 swaps with P2", state(h) == ["a", "c", "b"])
    run(h, "demote", "1")   # swap P1<->P2
    check("demote@1 swaps with P2", state(h) == ["c", "a", "b"])
    check("promote P1 rejected (nothing above) → exit 2", run(h, "promote", "1").returncode == 2)
    last = len(state(h))
    check("demote last rejected (nothing below) → exit 2", run(h, "demote", str(last)).returncode == 2)


def test_clear() -> None:
    h = fresh()
    run(h, "set", "a ; b")
    check("state present before clear", state(h) == ["a", "b"])
    run(h, "clear")
    check("clear removes state file", not (h / STATE_REL).exists())
    check("clear on already-empty is rc 0", run(h, "clear").returncode == 0)


def test_show_empty() -> None:
    h = fresh()
    r = run(h, "show")
    check("show on empty reports none, rc 0", r.returncode == 0 and "none" in r.stdout.lower())


def main() -> int:
    print("=== tools.priorities regression tests ===")
    for t in (
        test_add_show_order, test_add_empty_rejected, test_set_semicolon_split,
        test_insert_shifts_down, test_update_in_place, test_remove_range,
        test_promote_demote_swaps, test_clear, test_show_empty,
    ):
        t()
    total = len(PASSED) + len(FAILED)
    print()
    print(f"Result: {len(PASSED)}/{total} passed")
    for label, detail in FAILED:
        print(f"  - {label}: {detail}")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
