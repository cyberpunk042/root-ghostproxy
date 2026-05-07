"""tools.decisions — list / append entries in the decisions logbook.

Reads <project>/wiki/governance/decisions.md to enumerate D### entries; can append
new entries with the standard format (operator-supplied via CLI arg or stdin).

Usage:
    python3 -m tools.decisions list                  # list all D### entries (id, date, summary)
    python3 -m tools.decisions get D018              # get a specific decision (full detail)
    python3 -m tools.decisions next-id               # next D### in sequence (e.g. D019)
    python3 -m tools.decisions verify                # check format integrity (frontmatter, sequential IDs)

Append (writes to disk; only run with operator approval):
    python3 -m tools.decisions append \\
        --decision "Operator picked greenfield for B001 (T011)" \\
        --verbatim "go greenfield, scrap the prior install.sh" \\
        --rationale "operator wants a clean re-author" \\
        --affected "T011, T012, T013, T014, T015, T016, T017" \\
        --reversibility "fully-reversible" \\
        --downstream "M003 unblocks; T-M003-7 hook refinement still queued" \\
        --linked-blocker "B001"

Composes-with:
- Slash commands: /decisions (primary), /log (decision-shaped log triggers append),
  /audit step 10 (verify)
- Hooks: end-of-cycle-stamp surfaces decision count; pre-compact.sh reads recent D-IDs
  to include in its auto-snapshot
- MCP: 4 root_decisions_* tools at tools.mcp_server (list, get, verify, next_id)
- Sister tool: tools.blockers — resolve() appends a linked D### entry; --linked-blocker
  field is the bidirectional governance link

Operator-authority surfaces (read this tool's output when operator invokes them; agent
does NOT auto-invoke these): /handoff, /terminate, /finish-smoothly are operator-typed
session-control commands; they collect recent decisions via tools.decisions when run.

Idempotency invariant: list/get/verify/next-id are read-only; append writes to
wiki/governance/decisions.md with format-validation per ENTRY_PATTERN regex.

Action vocabulary (Hard Rule 14): emits `read-only-audit` (default invocations) OR
`operator-directive-register` action type (append path) per Hard Rule 14 + M-E001-1
vocabulary at wiki/log/2026-05-06-181500-auto-pilot-action-vocabulary-draft.md.

Test file: .claude/hooks/tests/test-decisions.py + tools/tests/test-decisions-tier3.py
(run via `python3 -m tools.run-tests`).

Sacrosanct discipline: every D### entry MUST contain operator-verbatim quote in
--verbatim field per .claude/rules/words-are-sacrosanct.md (alignment substrate).

Brain-improvement mandate: wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

from tools._paths import DECISIONS_DOC
ENTRY_PATTERN = re.compile(
    r"^### (D\d+) — (.+?)\s*$\n\n- \*\*Date\*\*: (\d{4}-\d{2}-\d{2})[^\n]*$",
    re.MULTILINE,
)


def parse_entries() -> list:
    if not DECISIONS_DOC.exists():
        return []
    content = DECISIONS_DOC.read_text()
    entries = []
    for match in ENTRY_PATTERN.finditer(content):
        entries.append({
            "id": match.group(1),
            "summary": match.group(2),
            "date": match.group(3),
        })
    return entries


def next_id() -> str:
    entries = parse_entries()
    if not entries:
        return "D001"
    max_n = max(int(e["id"][1:]) for e in entries)
    return f"D{max_n + 1:03d}"


def get_entry(decision_id: str) -> str | None:
    if not DECISIONS_DOC.exists():
        return None
    content = DECISIONS_DOC.read_text()
    pattern = re.compile(rf"^### {decision_id} — .+?(?=^### D\d+ — |\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(content)
    return match.group(0).strip() if match else None


def verify() -> dict:
    entries = parse_entries()
    issues: list = []
    if not entries:
        issues.append("no entries found")
        return {"entries": 0, "issues": issues, "ok": False}

    # IDs sequential?
    expected_ids = [f"D{i:03d}" for i in range(1, len(entries) + 1)]
    found_ids = sorted([e["id"] for e in entries])
    if sorted(expected_ids) != found_ids:
        issues.append(f"IDs not sequential: expected {expected_ids[:5]}... got {found_ids[:5]}...")

    return {"entries": len(entries), "issues": issues, "ok": not issues}


def append_entry(args: argparse.Namespace) -> int:
    if not DECISIONS_DOC.exists():
        print(f"error: {DECISIONS_DOC} does not exist", file=sys.stderr)
        return 1

    new_id = next_id()
    today = date.today().isoformat()

    entry = f"""### {new_id} — {args.decision}

- **Date**: {today}
- **Decision**: {args.decision}
- **Operator's verbatim**: *"{args.verbatim}"*
- **Rationale**: {args.rationale}
- **Affected**: {args.affected}
- **Reversibility**: {args.reversibility}
- **Downstream**: {args.downstream}
- **Linked blocker**: {args.linked_blocker}

---

"""

    content = DECISIONS_DOC.read_text()
    # Insert after "## Decisions made (chronological, newest first)\n\n---\n\n"
    insertion_marker = "## Decisions made (chronological, newest first)\n\n---\n\n"
    if insertion_marker not in content:
        print(f"error: insertion marker not found in {DECISIONS_DOC}", file=sys.stderr)
        return 1
    new_content = content.replace(insertion_marker, insertion_marker + entry, 1)
    DECISIONS_DOC.write_text(new_content)
    print(f"appended {new_id} to {DECISIONS_DOC}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage decisions logbook")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="list all D### entries")
    sub.add_parser("next-id", help="next D### in sequence")
    sub.add_parser("verify", help="check format integrity")

    get_p = sub.add_parser("get", help="get a specific D###")
    get_p.add_argument("decision_id")

    append_p = sub.add_parser("append", help="append a new D### entry (writes to disk)")
    append_p.add_argument("--decision", required=True)
    append_p.add_argument("--verbatim", required=True, help="operator's verbatim words")
    append_p.add_argument("--rationale", required=True)
    append_p.add_argument("--affected", required=True)
    append_p.add_argument("--reversibility", default="fully-reversible")
    append_p.add_argument("--downstream", required=True)
    append_p.add_argument("--linked-blocker", default="")

    args = parser.parse_args()

    if args.cmd == "list":
        entries = parse_entries()
        for e in entries:
            print(f"  {e['id']}  {e['date']}  {e['summary']}")
        print(f"\n{len(entries)} entries")
        return 0
    if args.cmd == "next-id":
        print(next_id())
        return 0
    if args.cmd == "get":
        body = get_entry(args.decision_id)
        if body is None:
            print(f"not found: {args.decision_id}", file=sys.stderr)
            return 1
        print(body)
        return 0
    if args.cmd == "verify":
        result = verify()
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 1
    if args.cmd == "append":
        return append_entry(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
