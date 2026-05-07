#!/usr/bin/env python3
# agent-output-scan.sh — Stop hook scanning agent's last assistant turn for
# self-blocking phrases (SB-140 forward-fix).
#
# Wired event: Stop · matcher: (any) · per SB-140 row's corrected layer.
# Reads transcript_path from hook stdin JSON, extracts the most-recent
# assistant turn, scans for self-blocking framings agent constructed without
# operator-explicit-statement OR tracker-row-literal text. Emits systemMessage
# warning when detected; silent on clean output.
#
# Compounds with: end-of-cycle-stamp.sh (state visualization at same Stop event).
# Doesn't replace.
#
# Phrase list = the self-blocking framings agent uses to hallucinate gates per
# SB-140 root cause. Operator can extend via .claude/agent-output-scan-phrases
# state file (one phrase per line) — empty/missing means use defaults below.

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path.home()
PHRASES_FILE = PROJECT_ROOT / ".claude" / "agent-output-scan-phrases"
TRACE_LOG = "/tmp/hook-fire-trace.log"

# Default phrase list (lowercased substring match). Each = a self-blocking
# framing agent uses on un-stated gates per SB-140 pattern.
DEFAULT_PHRASES = [
    "operator-driven future-session",
    "operator-pending decision",
    "operator-epic-scope",
    "operator-domain decision",
    "would need operator approval",  # often ungrounded
    "this is operator-pending",
    # Phase 2 additions (caught fire-26 self-blocking emit):
    "operator-stated-pending",
    "operator-epic-scope-pending",
    "operator-catching-territory",
    "exhausted within authority",
    "exhausted within current authority",
    "work-block exhausted",
    "agent-actionable substantive work",  # often paired with "exhausted"
    "operator-scope-pending",
    # Phase 3 additions 2026-05-07 (SB-099 abdication-as-freeze cousin pattern
    # per operating-principles.md extension #10 — freeze-disguised-as-respect;
    # 5 phrases operator literally cited as the failure mode):
    "Holding here, your move",
    "I'm not going to act on a guess",
    "Standing by until you direct",
    "Tell me literally what you see",
    "I'll wait for your call",
]


def is_project_context() -> bool:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "").strip()
    home = str(PROJECT_ROOT)
    if project_dir:
        return project_dir == home or project_dir.startswith(home + "/")
    cwd = os.getcwd()
    return cwd == home or cwd.startswith(home + "/")


def load_phrases() -> list[str]:
    if PHRASES_FILE.exists():
        try:
            lines = [
                line.strip().lower()
                for line in PHRASES_FILE.read_text().splitlines()
                if line.strip() and not line.strip().startswith("#")
            ]
            if lines:
                return lines
        except Exception:
            pass
    return [p.lower() for p in DEFAULT_PHRASES]


def trace(tag: str, extra: str = "") -> None:
    try:
        with open(TRACE_LOG, "a") as f:
            f.write(
                f"[{datetime.now().isoformat()}] hook=agent-output-scan.sh "
                f"path={tag} extra={extra}\n"
            )
    except Exception:
        pass


def extract_last_assistant_turn(transcript_path: str) -> str:
    """Return the text content of the most-recent assistant message in transcript."""
    try:
        path = Path(transcript_path)
        if not path.exists():
            return ""
        last_assistant_text = ""
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                # transcript format: {"role": "assistant", "content": [...]}
                # OR Claude Code's session JSONL with .message.role / .message.content
                msg = obj.get("message", obj)
                role = msg.get("role")
                if role == "assistant":
                    content = msg.get("content", "")
                    if isinstance(content, list):
                        text = " ".join(
                            (item.get("text", "") if isinstance(item, dict) else str(item))
                            for item in content
                        )
                    else:
                        text = str(content)
                    last_assistant_text = text
        return last_assistant_text
    except Exception:
        return ""


def scan_for_self_blocking(text: str, phrases: list[str]) -> list[str]:
    """Return list of matched phrases found in text (case-insensitive substring)."""
    if not text:
        return []
    text_lower = text.lower()
    return [p for p in phrases if p in text_lower]


def main() -> None:
    trace("entered")

    if not (PROJECT_ROOT / "BOOTSTRAP.md").exists():
        trace("exit-bootstrap-missing")
        sys.exit(0)
    if not is_project_context():
        trace("exit-not-project-context")
        sys.exit(0)

    raw = ""
    try:
        raw = sys.stdin.read()
    except Exception:
        trace("exit-stdin-read-error")
        sys.exit(0)

    if not raw:
        trace("exit-no-stdin")
        sys.exit(0)

    try:
        data = json.loads(raw)
    except Exception:
        trace("exit-json-parse-error")
        sys.exit(0)

    transcript_path = data.get("transcript_path", "")
    if not transcript_path:
        trace("exit-no-transcript-path")
        sys.exit(0)

    last_turn = extract_last_assistant_turn(transcript_path)
    if not last_turn:
        trace("exit-no-assistant-turn")
        sys.exit(0)

    phrases = load_phrases()
    matches = scan_for_self_blocking(last_turn, phrases)

    if not matches:
        trace("exit-clean")
        sys.exit(0)

    matches_str = " · ".join(f'"{m}"' for m in matches)
    warning = (
        f"⚠ AGENT-OUTPUT-SCAN (SB-140 fwd-fix): self-blocking phrases detected "
        f"in last assistant turn: {matches_str}. "
        f"VERIFY each against tracker-row OR decision-logbook literal text. "
        f"If un-stated gating, MUST default to PROJECT-LAYER substance "
        f"per Directive 36 + clause #8."
    )

    output = {"systemMessage": warning}
    print(json.dumps(output))
    trace("fired", extra=f"matches={len(matches)}")
    sys.exit(0)


if __name__ == "__main__":
    main()
