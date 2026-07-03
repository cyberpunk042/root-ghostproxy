#!/usr/bin/env python3
"""Sovereign-OS endpoint-mode smoke test — source-path-independent.

Verifies the consumption contract documented at docs/sovereign-os-endpoint-usage.md
(per operator directive 2026-07-03, verbatim: "Lets prepare root-ghostproxy for
sovereign-os usage, we will use use the repo without the proxy mode enabled."):

  install.sh with --mode endpoint MUST exclude the proxy/IPS half (network
  bridge + management wifi) and MUST retain the endpoint AI agent safety
  foundation (agent brain + tools + integrity + opencode bridge), for both
  the base and full profiles.

Pattern follows test-t014-endpoint-safety-smoke.py: runs against the
ROOT-GHOSTPROXY SOURCE tree, not the deployed ~/.claude/. Dry-run only —
no filesystem mutation beyond a scratch --dest directory that dry-run
never writes into.

Test classes:
  - T1-T5: endpoint mode × base profile — plan excludes bridge+wifi, includes foundation
  - T6-T7: endpoint mode × full profile — bridge+wifi still excluded (mode gate wins)
  - T8:    explicit-mode logging — endpoint mode acknowledged, not auto-promoted
  - T9:    dry-run exit code 0
  - T10:   docs/sovereign-os-endpoint-usage.md exists + names the canonical invocation

Exit codes:
  0 — all tests pass
  1 — one or more tests fail (verification gate fails)
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

# Locate the source root: this script lives at .claude/hooks/tests/, so
# go up 3 levels to reach the project root.
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent.parent.parent
INSTALL_SH = PROJECT_ROOT / "install.sh"
USAGE_DOC = PROJECT_ROOT / "docs" / "sovereign-os-endpoint-usage.md"

PASSED: list[str] = []
FAILED: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        PASSED.append(name)
        print(f"  PASS {name}")
    else:
        FAILED.append(name)
        print(f"  FAIL {name}{' — ' + detail if detail else ''}")


def dry_run(profile: str, dest: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(INSTALL_SH), "--dry-run", "--profile", profile,
         "--mode", "endpoint", "--dest", dest],
        capture_output=True, text=True, cwd=str(PROJECT_ROOT), timeout=120,
    )


def main() -> int:
    tests = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10"]

    with tempfile.TemporaryDirectory(prefix="ghostproxy-endpoint-smoke-") as dest:
        base = dry_run("base", dest)
        out_base = base.stdout + base.stderr

        # T1-T2 — the proxy half is excluded by the mode gate (base profile)
        check("T1 endpoint/base skips network bridge",
              "skip: network bridge" in out_base, "no 'skip: network bridge' line")
        check("T2 endpoint/base skips management wifi",
              "skip: management wifi" in out_base, "no 'skip: management wifi' line")

        # T3-T5 — the endpoint safety foundation is retained
        check("T3 endpoint/base plans agent-brain deploy (settings/hooks)",
              "policy-block.sh" in out_base and "settings.json" in out_base,
              "agent-brain artefacts missing from plan")
        check("T4 endpoint/base plans tools deploy",
              "tools/run-tests.py" in out_base or "tools/state.py" in out_base,
              "tools/*.py missing from plan")
        check("T5 endpoint/base plans integrity sentinel",
              "integrity" in out_base and "baseline" in out_base,
              "integrity baselines missing from plan")

        full = dry_run("full", dest)
        out_full = full.stdout + full.stderr

        # T6-T7 — mode gate wins over the full profile too (composition invariant:
        # installed iff (profile says yes) AND (mode_includes(op)))
        check("T6 endpoint/full skips network bridge",
              "skip: network bridge" in out_full, "no 'skip: network bridge' line")
        check("T7 endpoint/full skips management wifi",
              "skip: management wifi" in out_full, "no 'skip: management wifi' line")

        # T8 — explicit mode is acknowledged (not auto-promoted to bridge)
        check("T8 explicit endpoint mode acknowledged",
              "mode explicit: endpoint" in out_base, "no 'mode explicit: endpoint' log line")

        # T9 — dry-run exits 0 in endpoint mode
        check("T9 endpoint dry-run exit code 0 (base+full)",
              base.returncode == 0 and full.returncode == 0,
              f"rc base={base.returncode} full={full.returncode}")

    # T10 — the consumption doc exists and names the canonical invocation
    doc_ok = USAGE_DOC.is_file()
    doc_text = USAGE_DOC.read_text(encoding="utf-8") if doc_ok else ""
    check("T10 sovereign-os usage doc names canonical invocation",
          doc_ok and "--profile base --mode endpoint" in doc_text,
          "docs/sovereign-os-endpoint-usage.md missing or lacks canonical invocation")

    print(f"Result: {len(PASSED)}/{len(tests)} passed")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
