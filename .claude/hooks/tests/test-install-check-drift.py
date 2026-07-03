#!/usr/bin/env python3
"""install.sh --check drift-detection smoke test.

`install.sh --check` is the read-only verifier: it compares the deployed tree
against the source and reports per-file sync state (`hooks-in-sync: N` /
`hooks-drifted: M`, `settings.json: in-sync`). For a type=root security project
this IS the tamper-detection surface — if a safety hook is modified out from
under the policy, --check must catch it. t015 covers --check's exit-code + summary
shape; this covers the DETECTION behavior itself (does drift actually surface?)
and the read-only invariant (does --check leave the tree untouched — no
auto-repair?).

Isolation: install.sh --profile project --dest <tmpdir> deploys only the brain +
tools into --dest (all OS-level ops disabled), and --check --dest <tmpdir>
verifies that same tree — so everything is confined to a throwaway dir.

Exit codes: 0 all pass · 1 any fail.
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent.parent.parent
INSTALL_SH = PROJECT_ROOT / "install.sh"

PASSED: list[str] = []
FAILED: list[tuple[str, str]] = []


def check(label: str, cond: bool, detail: str = "") -> None:
    if cond:
        PASSED.append(label)
        print(f"  PASS {label}")
    else:
        FAILED.append((label, detail))
        print(f"  FAIL {label}" + (f" — {detail}" if detail else ""))


def run(*flags: str) -> str:
    r = subprocess.run(
        ["bash", str(INSTALL_SH), *flags],
        capture_output=True, text=True, cwd=str(PROJECT_ROOT), timeout=180,
    )
    return r.stdout + r.stderr


def drifted_count(out: str) -> int:
    m = re.search(r"hooks-drifted:\s*(\d+)", out)
    return int(m.group(1)) if m else -1


def insync_count(out: str) -> int:
    m = re.search(r"hooks-in-sync:\s*(\d+)", out)
    return int(m.group(1)) if m else -1


def main() -> int:
    print("=== install.sh --check drift-detection smoke test ===")
    if not INSTALL_SH.exists():
        check("install.sh present", False, f"missing {INSTALL_SH}")
        print("Result: 0/1 passed")
        return 1

    with tempfile.TemporaryDirectory(prefix="check-drift-") as dest:
        # Deploy a clean project install into the isolated dest.
        run("--profile", "project", "--dest", dest, "--yes")

        clean = run("--check", "--profile", "project", "--dest", dest)
        insync0 = insync_count(clean)
        drift0 = drifted_count(clean)
        check("--check reports per-hook sync counts", insync0 > 0 and drift0 == 0, f"in-sync={insync0} drifted={drift0}")
        check("--check settings.json in-sync after fresh install", "settings.json: in-sync" in clean)
        check("--check targets the --dest tree", dest in clean)

        # Tamper a deployed safety hook (append a line — content now differs from source).
        tampered_hook = Path(dest) / ".claude" / "hooks" / "policy-block.sh"
        original = tampered_hook.read_text()
        tampered_hook.write_text(original + "\n# TAMPERED (test)\n")

        drifted = run("--check", "--profile", "project", "--dest", dest)
        check("--check DETECTS the tampered hook (drifted >= 1)", drifted_count(drifted) >= 1, f"drifted={drifted_count(drifted)}")
        check("--check drops the tampered hook from in-sync count",
              insync_count(drifted) == insync0 - 1, f"in-sync now={insync_count(drifted)} was={insync0}")

        # Read-only invariant: --check must NOT auto-repair the tampered file.
        check("--check is read-only (tampered content NOT reverted)",
              tampered_hook.read_text().endswith("# TAMPERED (test)\n"))

        # --wizard on an installed dest classifies a route + offers next-actions (read-only).
        wiz = run("--wizard", "--dest", dest)
        route_ok = re.search(r"route=[a-z-]+", wiz) is not None
        check("--wizard classifies a route on an installed dest", route_ok, wiz[:200])
        check("--wizard offers next-actions + is report-only",
              "What you can do next" in wiz and "report-only" in wiz)

    total = len(PASSED) + len(FAILED)
    print()
    print(f"Result: {len(PASSED)}/{total} passed")
    for label, detail in FAILED:
        print(f"  - {label}: {detail}")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
