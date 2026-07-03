#!/usr/bin/env python3
"""T016 idempotency smoke test — install.sh is a no-op on re-run.

The methodology test-stage gate for IaC (per CLAUDE.md "5 Universal Stages")
is: *"idempotent re-run is no-op"*. T016 documents the idempotency invariants;
this test EXERCISES the core one end-to-end against the real installer — the
first behavioral (not just documentary) coverage of it.

Approach (safe + isolated): run `install.sh --profile project --dest <tmpdir>`
twice into a throwaway directory. The `project` profile deploys only the agent
brain + tools (settings/hooks/rules/commands/agents/modes/skills/tools) into
--dest and disables ALL OS-level ops (bridge / wifi / integrity / ccstatusline /
opencode), so nothing touches the host — the whole effect is confined to the
temp dir.

The invariant:
  - Run 1 (fresh):  every deployed file is reported `installed:` ; zero `unchanged:`.
  - Run 2 (re-run): zero `installed:` ; every previously-installed file is now
                    `unchanged:` (count matches run 1). Skip count is stable.
A regression that made install_file() re-write or re-back-up identical content
would surface as `installed:` / `updated:` / `backed up` lines on run 2.

Note: the installer's post-install op_verify exits non-zero under the `project`
profile (it checks OS-level artefacts that project-mode intentionally does not
deploy), so this test asserts on the ACTION lines, not the process exit code —
op_verify's project-mode behavior is a separate concern (covered by T015).

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


def run_install(dest: str) -> str:
    r = subprocess.run(
        ["bash", str(INSTALL_SH), "--profile", "project", "--dest", dest, "--yes"],
        capture_output=True, text=True, cwd=str(PROJECT_ROOT), timeout=180,
    )
    return r.stdout + r.stderr


def count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text))


def main() -> int:
    print("=== T016 install.sh idempotency smoke test ===")

    if not INSTALL_SH.exists():
        check("install.sh present", False, f"missing {INSTALL_SH}")
        print("Result: 0/1 passed")
        return 1

    with tempfile.TemporaryDirectory(prefix="t016-idempotency-") as dest:
        out1 = run_install(dest)
        installed1 = count(r"\] installed:", out1)
        unchanged1 = count(r"\] unchanged:", out1)
        skip1 = count(r"\] skip:", out1)

        # Run 1: a fresh install must actually install files, none pre-existing.
        check("run 1 installs files (installed: > 0)", installed1 > 0, f"installed1={installed1}")
        check("run 1 has no unchanged files (fresh dest)", unchanged1 == 0, f"unchanged1={unchanged1}")

        out2 = run_install(dest)
        installed2 = count(r"\] installed:", out2)
        unchanged2 = count(r"\] unchanged:", out2)
        skip2 = count(r"\] skip:", out2)
        updated2 = count(r"\] updated:", out2)
        backedup2 = count(r"backed up|backup:", out2)

        # Run 2: the idempotency invariant.
        check("run 2 re-installs NOTHING (installed: == 0)", installed2 == 0, f"installed2={installed2}")
        check("run 2 writes no updates (updated: == 0)", updated2 == 0, f"updated2={updated2}")
        check("run 2 backs up nothing (identical content)", backedup2 == 0, f"backedup2={backedup2}")
        check("run 2 reports every prior file unchanged (count matches run 1)",
              unchanged2 == installed1, f"unchanged2={unchanged2} vs installed1={installed1}")
        check("skip count is stable across runs", skip1 == skip2, f"skip1={skip1} skip2={skip2}")

        # Structural: the brain + tools actually landed in the isolated dest.
        check("agent brain deployed to dest (.claude/)", (Path(dest) / ".claude").is_dir())
        check("tools deployed to dest (tools/)", (Path(dest) / "tools").is_dir())

    total = len(PASSED) + len(FAILED)
    print()
    print(f"Result: {len(PASSED)}/{total} passed")
    for label, detail in FAILED:
        print(f"  - {label}: {detail}")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
