#!/usr/bin/env python3
# output-discipline-guard.sh — UserPromptSubmit hook for runtime SB-094 enforcement.
#
# Detects operator-frustration / escalation patterns in input and injects a
# reminder to apply output-discipline-under-pressure: shorter response, no
# tables-of-options, action-first, no new frameworks.
#
# Self-gates via BOOTSTRAP.md presence + cwd-aware (only fires for /root sessions).
# Generative-compliance ~85%; runtime nudge for the rule layer in
# /root/.claude/rules/work-mode.md "Output discipline under pressure" subsection.

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path


HOME = Path.home()
PROJECT_ROOT = HOME


def is_project_context() -> bool:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "").strip()
    home = str(PROJECT_ROOT)
    if project_dir:
        return project_dir == home or project_dir.startswith(home + "/")
    cwd = os.getcwd()
    return cwd == home or cwd.startswith(home + "/")


# Frustration / escalation markers. Order: cheapest first.
_FRUSTRATION_WORDS = re.compile(
    r"\b(wtf|fucking|fuck|trash|retard|useless|stupid|"
    r"lazy|cheap|broken|pathetic|incompetent)\b",
    re.IGNORECASE,
)

_PROFANITY_OR_ALL_CAPS_RE = re.compile(r"[A-Z]{4,}")


def detect_escalation(prompt: str) -> tuple[bool, str]:
    """Heuristic: classify input as showing operator-escalation/frustration.

    Returns (is_escalation, reason).
    """
    text = (prompt or "").strip()
    if not text:
        return (False, "")

    # Skip slash commands (operator-explicit, not emotional)
    if text.lstrip().startswith("/"):
        return (False, "")

    matches = []

    # ALL-CAPS words of length >= 4 (typed shouting)
    caps = _PROFANITY_OR_ALL_CAPS_RE.findall(text)
    # Filter out common acronyms / project tokens we don't want to flag
    benign = {"AIDLC", "IPS", "SFIF", "HOME", "ROOT", "OPT", "JSON", "YAML", "MCP", "SDLC", "PR", "URL"}
    caps = [c for c in caps if c not in benign and not c.startswith("SB")]
    if len(caps) >= 2:
        matches.append(f"{len(caps)} ALL-CAPS words")

    # Frustration vocabulary
    frust = _FRUSTRATION_WORDS.findall(text)
    if frust:
        matches.append(f"{len(frust)} frustration markers ({', '.join(set(m.lower() for m in frust))})")

    # Repeated "?" or "!" (high-emphasis punctuation)
    if re.search(r"[?!]{3,}", text):
        matches.append("repeated punctuation (??? or !!!)")

    if matches:
        return (True, "; ".join(matches))
    return (False, "")


def main() -> None:
    if not (PROJECT_ROOT / "BOOTSTRAP.md").exists():
        sys.exit(0)
    if not is_project_context():
        sys.exit(0)

    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    prompt = payload.get("prompt", "") or payload.get("user_prompt", "")
    if not isinstance(prompt, str):
        sys.exit(0)

    is_esc, reason = detect_escalation(prompt)
    if not is_esc:
        sys.exit(0)

    additional_context = (
        "═══════════════════════════════════════════════════════════════════════════\n"
        "OUTPUT DISCIPLINE GUARD — operator escalation detected\n"
        "═══════════════════════════════════════════════════════════════════════════\n"
        f"\n"
        f"Detected: {reason}\n"
        f"\n"
        f"Per SB-094 (output-discipline-under-pressure, work-mode.md):\n"
        f"\n"
        f"  - Shorten the response (don't lengthen)\n"
        f"  - Drop tables and option-trees (operator wants resolution, not choices)\n"
        f"  - State the next concrete action and TAKE IT (or one-sentence blocker)\n"
        f"  - No new principles, frameworks, or analyses unless explicitly requested\n"
        f"\n"
        f"Per SB-099 (abdication-as-freeze): 'holding here / your move / I'm not going\n"
        f"to act on a guess' is FREEZING IN DISGUISE. Build forward by addressing\n"
        f"the actual workload.\n"
        f"\n"
        f"Per SB-093 (anti-extremes pre-flight): if your last move swung opposite to\n"
        f"the prior correction, don't ship — adjust by ONE notch only.\n"
        f"\n"
        f"This is a nudge. If operator literally requested analysis ('HARD ANALYSIS\n"
        f"REQUIRED'), structured response is appropriate.\n"
        f"═══════════════════════════════════════════════════════════════════════════"
    )

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional_context,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
