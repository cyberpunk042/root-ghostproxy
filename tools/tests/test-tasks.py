#!/usr/bin/env python3
"""Regression tests for tools/tasks.py — backlog task parsing + active cursor.

tasks.py parses task .md pages (frontmatter, Done-When checklist, BLOCKED-BY
dependencies), filters/derives claimable tasks, and manages the SB-124d
active-task cursor. It backs the /task command, pre-compact.sh's snapshot, and
tools.cycle. Its regex parsers are fiddly (checkbox counting, dependency
extraction, quoted-frontmatter stripping) — exactly where a silent parse
regression would mis-report task readiness or hide a blocker. It had zero
coverage.

Two isolation styles:
  - parsers / filters run IN-PROCESS against fixture .md files + hand-built dict
    lists (no repo backlog touched);
  - the active-task cursor runs as a subprocess with HOME at a temp dir
    (ACTIVE_TASK_FILE is HOME-derived), so the cursor file is sandboxed. `set`
    validates against the real backlog, so it's only exercised with a bogus ID
    (deterministically refused regardless of backlog contents).

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
sys.path.insert(0, str(REPO_ROOT))

import tools.tasks as tk  # noqa: E402

PASSED: list[str] = []
FAILED: list[tuple[str, str]] = []


def check(label: str, cond: bool, detail: str = "") -> None:
    if cond:
        PASSED.append(label)
        print(f"  PASS {label}")
    else:
        FAILED.append((label, detail))
        print(f"  FAIL {label}" + (f" — {detail}" if detail else ""))


FIXTURE = """---
title: "Author the thing"
status: not-started
priority: P1
parent_module: M003
current_stage: scaffold
readiness: 40
sfif_stage: Foundation
---

# Author the thing

## Done When
- [x] first done
- [X] second done uppercase
- [ ] third pending

## Dependencies
BLOCKED BY: T001, T002

## Notes
irrelevant
"""


def write_task(name: str, content: str) -> str:
    d = Path(tempfile.mkdtemp(prefix="tasks-test-"))
    p = d / name
    p.write_text(content)
    return str(p)


def test_parse_frontmatter() -> None:
    fm = tk.parse_frontmatter(write_task("T042-thing.md", FIXTURE))
    check("frontmatter extracts status", fm.get("status") == "not-started")
    check("frontmatter strips quotes from title", fm.get("title") == "Author the thing")
    check("frontmatter extracts priority + module", fm.get("priority") == "P1" and fm.get("parent_module") == "M003")
    check("non-frontmatter file → {}", tk.parse_frontmatter(write_task("x.md", "# no fm\n")) == {})
    check("missing file → {}", tk.parse_frontmatter("/no/such/path.md") == {})


def test_parse_done_when() -> None:
    dw = tk.parse_done_when(write_task("T1-a.md", FIXTURE))
    check("done-when counts checked (incl. uppercase [X])", dw["checked"] == 2)
    check("done-when counts unchecked", dw["unchecked"] == 1)
    check("done-when total = checked + unchecked", dw["total"] == 3)
    empty = tk.parse_done_when(write_task("T2-b.md", "# no section\n"))
    check("no Done-When section → all zero", empty == {"total": 0, "checked": 0, "unchecked": 0})


def test_parse_blocked_by() -> None:
    check("blocked-by extracts both ids", tk.parse_blocked_by(write_task("T1-a.md", FIXTURE)) == ["T001", "T002"])
    none = tk.parse_blocked_by(write_task("T2-b.md", "# no deps\n"))
    check("no Dependencies section → []", none == [])


def test_collect_task() -> None:
    t = tk.collect_task(write_task("T042-author-the-thing.md", FIXTURE))
    check("collect derives id from filename stem", t["id"] == "T042")
    check("collect takes title from '# Heading'", t["title"] == "Author the thing")
    check("collect surfaces status + readiness", t["status"] == "not-started" and t["readiness"] == "40")
    check("collect nests done_when + blocked_by", t["done_when"]["checked"] == 2 and t["blocked_by"] == ["T001", "T002"])


def _t(id_, status, module="M003", priority="P1", blocked=None):
    return {"id": id_, "status": status, "parent_module": module, "priority": priority,
            "blocked_by": blocked or []}


def test_filter_tasks() -> None:
    tasks = [_t("T1", "not-started"), _t("T2", "done", module="M004"), _t("T3", "not-started", priority="P2")]
    check("filter by status", [t["id"] for t in tk.filter_tasks(tasks, status="not-started")] == ["T1", "T3"])
    check("filter by module is case-insensitive substring", [t["id"] for t in tk.filter_tasks(tasks, module="m004")] == ["T2"])
    check("filter by priority", [t["id"] for t in tk.filter_tasks(tasks, priority="P2")] == ["T3"])
    check("no filters → all", len(tk.filter_tasks(tasks)) == 3)


def test_claimable_tasks() -> None:
    tasks = [
        _t("T1", "not-started"),                    # claimable
        _t("T2", "not-started", blocked=["T1"]),    # blocked → not claimable
        _t("T3", "in-progress"),                    # wrong status
        _t("T4", "not-started"),                    # claimable
    ]
    check("claimable = not-started AND no blocked_by", [t["id"] for t in tk.claimable_tasks(tasks)] == ["T1", "T4"])


# --- active-task cursor (subprocess, HOME-isolated) ---
def _cli(home: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "tools.tasks", *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
        env={"HOME": str(home), "PATH": os.environ.get("PATH", "")},
    )


def test_active_cursor() -> None:
    h = Path(tempfile.mkdtemp(prefix="tasks-home-"))
    r = _cli(h, "active", "show")
    check("active show unset → (none), rc 0", r.returncode == 0 and "(none)" in r.stdout)
    r2 = _cli(h, "active", "set", "BOGUS999")
    check("active set bogus id → refused, rc 1", r2.returncode == 1 and "refused" in r2.stderr)
    check("active set bogus does not write cursor", not (h / ".claude" / "active-task").exists()
          or not (h / ".claude" / "active-task").read_text().strip())
    # A stale cursor (id not in backlog) is reported, not crashed.
    (h / ".claude").mkdir(parents=True, exist_ok=True)
    (h / ".claude" / "active-task").write_text("T99999\n")
    r3 = _cli(h, "active", "show")
    check("active show stale cursor → reported, rc 0", r3.returncode == 0 and "stale cursor" in r3.stdout)
    r4 = _cli(h, "active", "clear")
    check("active clear → rc 0", r4.returncode == 0 and "cleared" in r4.stdout)


def main() -> int:
    print("=== tools.tasks regression tests ===")
    for t in (
        test_parse_frontmatter, test_parse_done_when, test_parse_blocked_by,
        test_collect_task, test_filter_tasks, test_claimable_tasks, test_active_cursor,
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
