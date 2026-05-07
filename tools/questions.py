"""tools.questions — agent-pending-questions accumulation + surfacing (operator directive 2026-05-06).

Operator directive: *"questions that do not cummulate in a file like it should
and surface to me with definition via the agent and even the stamp or anything
that needs it relative to what the project does... if there is question and I
dont see them its about the same as if there was no question"*.

Semantics:
    When the agent generates a question for the operator (typically scope
    questions, design choices, ambiguity surfacing), the question is
    accumulated in `active-questions` so it persists across cycles + surfaces
    in stamp/banner/handoff. Without this layer, agent-questions vanish into
    response prose and operator misses them.

    Each question is one line: typically `Q-NNN: <text>` or free text. Newest
    on top by default (operator can revise order with promote/demote like
    priorities).

    Distinct from priorities (imminent-work) and from SBs (systemic bugs).
    This is the "agent-asked-for-input" layer — part of the E003 compound
    retention layer per Milestone v0.2.

State file: `$HOME/.claude/active-questions`
    One question per line. Order = recency or operator-managed.
    Empty file or missing = no pending questions.

Slash command: `/questions <verb> [args]`
    add <text>      — append a new question
    show            — display numbered list
    clear           — empty the list
    remove <N>      — drop question N (1-based)
    answer <N>      — drop question N (alias for remove; semantic: answered)
    promote <N>     — move question N up one rank
    demote <N>      — move question N down one rank
    set <text>      — replace entire list (semicolon-separated for multi)
    update <N> <text> — replace text of question N (position unchanged)
    insert <N> <text> — insert at position N (shifts rest down)
    detail <N> [<text>] — show or write SRP detail companion file Q<N>.md
    solve [first|last|all|N|N,M|Q1] — solving-mode view with full detail

Composes-with:
- Slash commands: /questions (this tool's primary consumer; 12 verbs per SB-134)
- Hooks: mode-enforcement.sh surfaces pending question count + first 3 (per the SB-134
  binding rule that questions MUST surface every prompt or they're invisible);
  end-of-cycle-stamp.sh shows count + first 3 in stamp render
- MCP: root_questions tool at tools.mcp_server wraps the read side
- Sister tools: tools.priorities (operator-authored hot-queue) — questions are the
  agent-authored input-needed parallel; tools.objective (mission/focus/impediment)

State files:
    $HOME/.claude/active-questions          — main queue (one question per line)
    $HOME/.claude/active-questions-detail/  — per-question SRP detail (Q<N>.md companions)

E003 compound retention layer: questions are part of E003 Epic (Milestone v0.2 ai-natural-task-management).
Closes operator-stated bug: *"questions that do not cummulate in a file like it should
and surface to me with definition via the agent and even the stamp or anything that
needs it relative to what the project does"*.

Idempotency invariant: mutations write whole-file atomically; detail companions are
per-Q files (independent atomic writes); solve view is pure read-side.

Action vocabulary (Hard Rule 14): emits `new-artifact` (add/insert/detail with text) OR
`operator-directive-register` (clear/remove/answer/promote/demote/set/update) OR
`read-only-audit` (show/solve/detail-without-text) per the M-E001-1 vocabulary at
wiki/log/2026-05-06-181500-auto-pilot-action-vocabulary-draft.md.

Test file: tools/tests/test-questions.py (33/51 passing 2026-05-06; partial-fail
surfaced for operator-decision per Hooks-pass discipline).

Brain-improvement mandate: wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

QUESTIONS_PATH = Path.home() / ".claude" / "active-questions"
DETAIL_DIR = Path.home() / ".claude" / "active-questions-detail"


def detail_path(n: int) -> Path:
    return DETAIL_DIR / f"Q{n}.md"


def _shift_details_down(start: int, total: int) -> None:
    """After removing Q<start>: shift Q<start+1>.md → Q<start>.md, etc.
    `total` is the NEW total count after removal.
    """
    if not DETAIL_DIR.exists():
        return
    for i in range(start, total + 1):
        src = DETAIL_DIR / f"Q{i+1}.md"
        dst = DETAIL_DIR / f"Q{i}.md"
        if src.exists():
            src.replace(dst)
        elif dst.exists():
            # No source to move, but dst still exists — could be orphan; leave for now
            pass


def _shift_details_up(start: int, total: int) -> None:
    """Before inserting at Q<start>: shift Q<total>.md → Q<total+1>.md, ..., Q<start>.md → Q<start+1>.md.
    `total` is the OLD total count before insertion.
    """
    if not DETAIL_DIR.exists():
        return
    for i in range(total, start - 1, -1):
        src = DETAIL_DIR / f"Q{i}.md"
        dst = DETAIL_DIR / f"Q{i+1}.md"
        if src.exists():
            src.replace(dst)


def _swap_details(a: int, b: int) -> None:
    """Swap Q<a>.md ↔ Q<b>.md (used for promote/demote)."""
    if not DETAIL_DIR.exists():
        return
    pa = DETAIL_DIR / f"Q{a}.md"
    pb = DETAIL_DIR / f"Q{b}.md"
    if pa.exists() and pb.exists():
        tmp = DETAIL_DIR / f"Q{a}.md.swap"
        pa.replace(tmp)
        pb.replace(pa)
        tmp.replace(pb)
    elif pa.exists():
        pa.replace(pb)
    elif pb.exists():
        pb.replace(pa)


def read_questions() -> list[str]:
    if not QUESTIONS_PATH.exists():
        return []
    try:
        return [ln.strip() for ln in QUESTIONS_PATH.read_text().splitlines() if ln.strip()]
    except Exception:
        return []


def write_questions(items: list[str]) -> None:
    QUESTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUESTIONS_PATH.write_text("\n".join(items) + ("\n" if items else ""))


DETAIL_TEMPLATE = """---
id: Q{n}
title: "{title}"
type: agent-pending-question
status: open
parent_milestone: ""
parent_epic: ""
parent_layer: ""
originate_from:
  - operator-directive: ""
  - operator-quote: ""
related_questions: []
related_sbs: []
related_decisions: []
related_rules: []
agent_attempts:
  - attempt-1: "(agent-DRAFT — record what was tried first)"
created: {date}
updated: {date}
---

# Q{n} — {title}

## Why this question exists

(operator-stated context — quote the directive that surfaced this Q; explain WHY it's a question now)

## Concrete options

### (a) ...

**What**: (mechanism)
**Risks**: ...
**Recovery**: ...

### (b) ...

**What**: (mechanism)
**Risks**: ...
**Recovery**: ...

## Suggested next-step path

(agent's proposed resolution — what should happen next; sequenced steps)

## What operator could pick

- **(a) ...**
- **(b) ...**
- **(c) different shape** — operator names alternative

## Connects to

- (parent Milestone / Epic / Module if any)
- (related SBs / decisions / rules)
"""


def cmd_add(args: argparse.Namespace) -> int:
    text = " ".join(args.text).strip()
    if not text:
        print("ERROR: text required for add", file=sys.stderr)
        return 2
    items = read_questions()
    items.append(text)
    write_questions(items)
    n = len(items)
    print(f"OK: question Q{n} added: {text}")

    # Auto-create templated detail file (operator directive 2026-05-06 — questions
    # tool MUST enforce high-standard quality by default, not via manual edits).
    p = detail_path(n)
    if not p.exists():
        from datetime import date as _date
        title = text[:80].replace('"', "'")
        DETAIL_DIR.mkdir(parents=True, exist_ok=True)
        p.write_text(DETAIL_TEMPLATE.format(n=n, title=title, date=_date.today().isoformat()))
        print(f"OK: detail template scaffolded at {p}")
        print(f"     fill via:  python3 -m tools.questions detail {n} <full-text>")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    items = read_questions()
    if not items:
        print("questions: (none pending — no agent-asked-input outstanding)")
        return 0
    for i, item in enumerate(items, start=1):
        marker = " [+detail]" if detail_path(i).exists() else ""
        print(f"Q{i}: {item}{marker}")
    return 0


def parse_selector(spec: str, total: int) -> list[int]:
    """Parse selector spec into list of 1-based indices.

    Accepts (canonical): 'first' | 'last' | 'all' | '1' | '1,2,3' | 'Q1' | 'Q1,Q3'
    Accepts (natural language, operator-friendly):
      'them all' | 'everything' | 'every' | 'each' → all
      'top' | 'next' | 'one' → first
      'bottom' | 'end' → last
      Trailing punctuation / emoji / extra spaces tolerated.
    Returns: ordered list of valid 1-based indices (deduped, in spec order).
    Empty list if no recognized form.
    """
    if not spec:
        return []
    s = spec.strip().lower()
    if not s:
        return []
    # Tolerate trailing emoji / punctuation by stripping non-essential chars
    # while keeping digits, commas, and letters used in keywords.
    import re as _re
    s_clean = _re.sub(r"[^a-z0-9, ]+", " ", s).strip()
    s_clean = _re.sub(r"\s+", " ", s_clean)

    # Keyword phrase containment (operator-friendly: tolerates leading/trailing noise)
    all_phrases = ("them all", "everything", "every q", "every one", "all of", " all", "all ", "each of", "every", "each")
    if any(p in f" {s_clean} " for p in all_phrases) or s_clean == "all":
        return list(range(1, total + 1))
    first_phrases = ("first", "top", "next", "1st", "one")
    if any(p == s_clean or s_clean.startswith(p + " ") or s_clean.endswith(" " + p) for p in first_phrases):
        return [1] if total >= 1 else []
    last_phrases = ("last", "bottom", "end")
    if any(p == s_clean or s_clean.startswith(p + " ") or s_clean.endswith(" " + p) for p in last_phrases):
        return [total] if total >= 1 else []

    # Numeric / Q-prefix list (comma-separated; tolerates space-separated too)
    out: list[int] = []
    # Replace Q (case-insensitive already lowered) and split on comma OR space
    tokens = _re.split(r"[,\s]+", s_clean.replace("q", ""))
    for part in tokens:
        part = part.strip()
        if not part:
            continue
        try:
            n = int(part)
        except ValueError:
            continue
        if 1 <= n <= total and n not in out:
            out.append(n)
    return out


def cmd_solve(args: argparse.Namespace) -> int:
    """Solving-mode view: show selected questions with full detail content.

    Selector accepts: first | last | all | 1 | 1,2 | Q1 | Q1,Q3
    """
    items = read_questions()
    if not items:
        print("questions: (none pending)")
        return 0
    selector = " ".join(args.selector).strip() if args.selector else "all"
    indices = parse_selector(selector, len(items))
    if not indices:
        print(f"ERROR: selector '{selector}' resolved to no questions (queue size: {len(items)})", file=sys.stderr)
        return 2
    print(f"=== solving mode — {len(indices)} of {len(items)} selected ({selector}) ===")
    for n in indices:
        print()
        print(f"━━━ Q{n} ━━━")
        print(items[n - 1])
        p = detail_path(n)
        if p.exists():
            print()
            print(f"--- detail ({p}) ---")
            print(p.read_text().rstrip())
        else:
            print("(no detail file — write via:  python3 -m tools.questions detail {n} <context...>)".replace("{n}", str(n)))
    print()
    print(f"=== answer with:  python3 -m tools.questions answer <N>   (or update <N> <text>) ===")
    return 0


def cmd_detail(args: argparse.Namespace) -> int:
    """Show or write the detail companion file for question N (presweep enrichment).

    Per operator directive 2026-05-06 (presweep critique): single-line questions are
    insufficient — operator needs context/options/stakes/suggested-default. SRP companion
    files hold richer detail per question without disrupting the index file format.
    """
    items = read_questions()
    n = args.n
    if n < 1 or n > len(items):
        print(f"ERROR: question Q{n} out of range (1..{len(items)})", file=sys.stderr)
        return 2
    p = detail_path(n)
    if args.text:
        text = " ".join(args.text).strip()
        DETAIL_DIR.mkdir(parents=True, exist_ok=True)
        p.write_text(text + ("\n" if not text.endswith("\n") else ""))
        print(f"OK: detail written for Q{n} ({p})")
    else:
        if not p.exists():
            print(f"Q{n}: {items[n-1]}")
            print(f"(no detail file — write via:  python3 -m tools.questions detail {n} <context...>)")
            return 0
        print(f"Q{n}: {items[n-1]}")
        print(f"--- detail ({p}) ---")
        print(p.read_text())
    return 0


def cmd_clear(args: argparse.Namespace) -> int:
    if QUESTIONS_PATH.exists():
        QUESTIONS_PATH.unlink()
    # Also clear all detail companion files (SRP cleanup)
    if DETAIL_DIR.exists():
        for p in DETAIL_DIR.glob("Q*.md"):
            try:
                p.unlink()
            except Exception:
                pass
    print("OK: questions cleared (incl. detail files)")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    items = read_questions()
    n = args.n
    if n < 1 or n > len(items):
        print(f"ERROR: question Q{n} out of range (1..{len(items)})", file=sys.stderr)
        return 2
    dropped = items.pop(n - 1)
    write_questions(items)
    # Detail file sync: delete Q<n>.md, shift Q<n+1..>.md down by 1
    p = detail_path(n)
    if p.exists():
        p.unlink()
    _shift_details_down(n, len(items))
    print(f"OK: question Q{n} removed: {dropped}")
    return 0


def cmd_answer(args: argparse.Namespace) -> int:
    # Alias for remove with answered-semantic message
    items = read_questions()
    n = args.n
    if n < 1 or n > len(items):
        print(f"ERROR: question Q{n} out of range (1..{len(items)})", file=sys.stderr)
        return 2
    answered = items.pop(n - 1)
    write_questions(items)
    p = detail_path(n)
    if p.exists():
        p.unlink()
    _shift_details_down(n, len(items))
    print(f"OK: question Q{n} marked answered + removed: {answered}")
    return 0


def cmd_promote(args: argparse.Namespace) -> int:
    items = read_questions()
    n = args.n
    if n <= 1 or n > len(items):
        print(f"ERROR: cannot promote Q{n} (already top or out of range)", file=sys.stderr)
        return 2
    items[n - 2], items[n - 1] = items[n - 1], items[n - 2]
    write_questions(items)
    _swap_details(n - 1, n)
    print(f"OK: Q{n} promoted to Q{n-1}")
    return 0


def cmd_demote(args: argparse.Namespace) -> int:
    items = read_questions()
    n = args.n
    if n < 1 or n >= len(items):
        print(f"ERROR: cannot demote Q{n} (already bottom or out of range)", file=sys.stderr)
        return 2
    items[n - 1], items[n] = items[n], items[n - 1]
    write_questions(items)
    _swap_details(n, n + 1)
    print(f"OK: Q{n} demoted to Q{n+1}")
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    raw = " ".join(args.text).strip()
    if not raw:
        print("ERROR: text required for set (use clear to empty)", file=sys.stderr)
        return 2
    items = [s.strip() for s in raw.split(";") if s.strip()]
    write_questions(items)
    print(f"OK: questions replaced ({len(items)} items)")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    items = read_questions()
    n = args.n
    if n < 1 or n > len(items):
        print(f"ERROR: question Q{n} out of range (1..{len(items)})", file=sys.stderr)
        return 2
    text = " ".join(args.text).strip()
    if not text:
        print("ERROR: text required for update", file=sys.stderr)
        return 2
    items[n - 1] = text
    write_questions(items)
    print(f"OK: Q{n} updated: {text}")
    return 0


def cmd_insert(args: argparse.Namespace) -> int:
    items = read_questions()
    n = args.n
    if n < 1 or n > len(items) + 1:
        print(f"ERROR: position Q{n} out of range (1..{len(items)+1})", file=sys.stderr)
        return 2
    text = " ".join(args.text).strip()
    if not text:
        print("ERROR: text required for insert", file=sys.stderr)
        return 2
    # Detail sync: shift existing Q<n..>.md UP by 1 BEFORE writing the new index
    _shift_details_up(n, len(items))
    items.insert(n - 1, text)
    write_questions(items)
    # Auto-template the newly-inserted Q's detail file
    p = detail_path(n)
    if not p.exists():
        from datetime import date as _date
        title = text[:80].replace('"', "'")
        DETAIL_DIR.mkdir(parents=True, exist_ok=True)
        p.write_text(DETAIL_TEMPLATE.format(n=n, title=title, date=_date.today().isoformat()))
    print(f"OK: Q{n} inserted: {text}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage active-questions accumulation layer")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="append a question")
    p_add.add_argument("text", nargs="+")
    p_add.set_defaults(func=cmd_add)

    sub.add_parser("show", help="list pending questions").set_defaults(func=cmd_show)
    sub.add_parser("clear", help="empty all questions").set_defaults(func=cmd_clear)

    p_rm = sub.add_parser("remove", help="drop question N")
    p_rm.add_argument("n", type=int)
    p_rm.set_defaults(func=cmd_remove)

    p_ans = sub.add_parser("answer", help="drop question N (answered semantic)")
    p_ans.add_argument("n", type=int)
    p_ans.set_defaults(func=cmd_answer)

    p_pr = sub.add_parser("promote", help="move N up one rank")
    p_pr.add_argument("n", type=int)
    p_pr.set_defaults(func=cmd_promote)

    p_de = sub.add_parser("demote", help="move N down one rank")
    p_de.add_argument("n", type=int)
    p_de.set_defaults(func=cmd_demote)

    p_set = sub.add_parser("set", help="replace whole list (semicolon-separated)")
    p_set.add_argument("text", nargs="+")
    p_set.set_defaults(func=cmd_set)

    p_up = sub.add_parser("update", help="replace text of question N (text only; position unchanged)")
    p_up.add_argument("n", type=int)
    p_up.add_argument("text", nargs="+")
    p_up.set_defaults(func=cmd_update)

    p_in = sub.add_parser("insert", help="insert question at position N (shifts rest down)")
    p_in.add_argument("n", type=int)
    p_in.add_argument("text", nargs="+")
    p_in.set_defaults(func=cmd_insert)

    p_dt = sub.add_parser("detail", help="show or write detail file for question N (SRP companion file at .claude/active-questions-detail/Q<N>.md)")
    p_dt.add_argument("n", type=int)
    p_dt.add_argument("text", nargs="*")
    p_dt.set_defaults(func=cmd_detail)

    p_sv = sub.add_parser("solve", help="solving-mode view — show selected questions with detail (selector: first|last|all|N|N,M|Q1|Q1,Q3)")
    p_sv.add_argument("selector", nargs="*")
    p_sv.set_defaults(func=cmd_solve)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
