#!/usr/bin/env python3
"""Regression tests for tools/objective.py — the SB-118 objective layer
(mission / focus / impediment state files).

objective.py manages three independent single-line state files that the
mode-enforcement banner + stamp read every prompt. The load-bearing invariant
is LAYER INDEPENDENCE: setting or clearing one layer must never touch another,
and `show` with no arg must always render all three (unset ones included) so
the operator sees the full objective state, not a collapsed subset (the SB-082
visibility-vs-presence lesson).

Isolation: each verb runs as a real subprocess (`python3 -m tools.objective
...`) with HOME pointed at a fresh temp dir, so the three state files under
$HOME/.claude/ are sandboxed and the real argparse CLI (with its `choices`
guards) is exercised end-to-end.

Emits the canonical `Result: N/M passed` line consumed by tools.run-tests.
Exit 0 iff all pass.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LAYERS = ("mission", "focus", "impediment")

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
        [sys.executable, "-m", "tools.objective", *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
        env={"HOME": str(home), "PATH": os.environ.get("PATH", "")},
    )


def layer_val(home: Path, layer: str) -> str | None:
    """Return the stored single-line value, or None if the file is absent."""
    f = home / ".claude" / f"active-{layer}"
    return f.read_text().strip() if f.exists() else None


def fresh() -> Path:
    return Path(tempfile.mkdtemp(prefix="objective-test-"))


def test_set_and_read_back() -> None:
    h = fresh()
    r = run(h, "set", "mission", "ship", "M003", "foundation")  # multi-word joins
    check("set mission rc 0", r.returncode == 0)
    check("set mission writes joined text", layer_val(h, "mission") == "ship M003 foundation")


def test_layer_independence() -> None:
    h = fresh()
    run(h, "set", "mission", "M")
    run(h, "set", "focus", "F")
    run(h, "set", "impediment", "I")
    check("all three set independently", (layer_val(h, "mission"), layer_val(h, "focus"), layer_val(h, "impediment")) == ("M", "F", "I"))
    # Clearing focus must not disturb mission or impediment.
    run(h, "clear", "focus")
    check("clear focus removes only focus", layer_val(h, "focus") is None)
    check("clear focus leaves mission intact", layer_val(h, "mission") == "M")
    check("clear focus leaves impediment intact", layer_val(h, "impediment") == "I")
    # Re-setting mission must not resurrect focus or touch impediment.
    run(h, "set", "mission", "M2")
    check("re-set mission does not touch impediment", layer_val(h, "impediment") == "I")
    check("re-set mission does not resurrect focus", layer_val(h, "focus") is None)


def test_show_all_renders_every_layer() -> None:
    h = fresh()
    run(h, "set", "mission", "only-mission")
    r = run(h, "show")  # no layer arg → all three
    check("show (no arg) renders mission value", "mission: only-mission" in r.stdout)
    check("show (no arg) renders focus as (unset)", "focus: (unset)" in r.stdout)
    check("show (no arg) renders impediment as (unset)", "impediment: (unset)" in r.stdout)
    check("show rc 0", r.returncode == 0)


def test_show_single_layer_and_verbose() -> None:
    h = fresh()
    run(h, "set", "focus", "the-focus")
    r = run(h, "show", "focus")
    check("show <layer> renders just that layer", "focus: the-focus" in r.stdout and "mission:" not in r.stdout)
    rv = run(h, "show", "focus", "-v")
    check("show -v prints the state-file path", "active-focus" in rv.stdout and "path:" in rv.stdout)


def test_set_empty_rejected() -> None:
    h = fresh()
    r = run(h, "set", "focus", "   ")
    check("set empty/whitespace → exit 2", r.returncode == 2)
    check("set empty writes nothing", layer_val(h, "focus") is None)


def test_clear_absent_is_ok() -> None:
    h = fresh()
    r = run(h, "clear", "impediment")  # never set
    check("clear absent layer is rc 0", r.returncode == 0)
    check("clear absent reports already-absent", "absent" in r.stdout.lower())


def test_invalid_layer_rejected() -> None:
    h = fresh()
    r = run(h, "set", "bogus", "x")  # argparse choices guard
    check("invalid layer rejected by argparse (exit 2)", r.returncode == 2)
    check("invalid layer names the valid choices", "mission" in (r.stderr + r.stdout))


def main() -> int:
    print("=== tools.objective regression tests ===")
    for t in (
        test_set_and_read_back, test_layer_independence, test_show_all_renders_every_layer,
        test_show_single_layer_and_verbose, test_set_empty_rejected, test_clear_absent_is_ok,
        test_invalid_layer_rejected,
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
