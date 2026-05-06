#!/usr/bin/env python3
# agent-discipline-gate (file: output-discipline-guard.sh — name kept for stability).
#
# UserPromptSubmit hook for runtime SB-090 + SB-094 detection. Combines:
#   - PREMISE-RISK detection (SB-090): operator words enumerate observations or
#     ask questions without imperative verbs → agent should not infer action.
#   - ESCALATION detection (SB-094): operator-frustration / shouting markers →
#     agent should shorten response, drop tables, action-first.
#
# Design constraint per Phase B step 2:
#   - Single-line additionalContext banner (high-confidence triggers only).
#   - Silent on routine prompts (no banner = no UI noise).
#   - Compatible with end-of-cycle-stamp.sh on Stop event (different mechanism).
#
# Self-gates via BOOTSTRAP.md presence + CLAUDE_PROJECT_DIR or cwd match.

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path.home()


def is_project_context() -> bool:
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "").strip()
    home = str(PROJECT_ROOT)
    if project_dir:
        return project_dir == home or project_dir.startswith(home + "/")
    cwd = os.getcwd()
    return cwd == home or cwd.startswith(home + "/")


_IMPERATIVE_VERBS = re.compile(
    r"\b(fix|do|make|build|implement|add|remove|delete|update|run|test|verify|"
    r"author|write|edit|stop|start|continue|pick|finish|commit|revert|"
    r"restore|apply|use|wire|enable|disable|configure|patch|create|change)\b",
    re.IGNORECASE,
)

_FRUSTRATION_WORDS = re.compile(
    r"\b(wtf|fuck|fucking|trash|retard|retarded|useless|stupid|"
    r"hopeless|pathetic|incompetent|broken|catastrophic)\b",
    re.IGNORECASE,
)

_CAPS_RE = re.compile(r"\b[A-Z]{4,}\b")
_REPEATED_PUNCT = re.compile(r"[?!]{3,}")

_BENIGN_CAPS = {
    "AIDLC", "IPS", "SFIF", "HOME", "ROOT", "OPT", "JSON", "YAML", "MCP",
    "SDLC", "URL", "API", "HTTP", "HTTPS", "TODO", "ASAP", "OS",
}


def detect_premise_risk(prompt: str) -> str | None:
    """High-confidence premise-construction trigger detection.

    Returns reason string if detected, else None. Conservative — only fires when
    operator words are clearly observation/question without imperative.
    """
    text = (prompt or "").strip()
    if not text:
        return None
    if text.lstrip().startswith("/"):
        return None  # slash command = explicit imperative

    if _IMPERATIVE_VERBS.search(text):
        return None  # imperative present → not premise risk

    lower = text.lower()

    # STRONG signal: enumerative observation ("everything ... doesn't seem")
    if re.search(r"\b(everything|every|all)\b.+?\b(don'?t|doesn'?t|seems?|looks?|appears?|isn'?t)\b", lower):
        return "enumerative observation without imperative"

    # STRONG signal: observational adjective (no imperative) — "weird X happens"
    if re.search(r"\b(weird|strange|odd|funny|interesting|broken)\b", lower):
        return "observational adjective without imperative"

    # STRONG signal: short reaction word (≤4 words)
    words = lower.split()
    if len(words) <= 4 and words and words[0] in {"wtf", "weird", "huh", "really", "strange", "odd"}:
        return "short reaction without imperative"

    # STRONG signal: unclear-reference start — pronoun + state-adjective forces
    # agent to guess WHAT "it/this/that" refers to → premise construction risk.
    # Pattern: [optional "now"] + pronoun (with optional contraction-s OR
    # explicit copula) + state-adjective.
    # Examples caught: "it's broken", "this is wrong", "now it's worse",
    #                  "that's missing", "everything's off"
    if re.match(
        r"^\s*(?:now\s+)?"
        r"(?:it|this|that|what|everything|nothing|something)"
        r"(?:'s|\s+(?:is|isn'?t|was|wasn'?t|seems?|looks?|appears?|feels?))?\s+"
        r"(?:gone|broken|missing|wrong|weird|different|bad|worse|better|"
        r"off|stuck|odd|wrong|broken)\b",
        lower,
    ):
        return "unclear-reference start (it/this/that + state, no explicit subject)"

    # NOTE: bare "?" without imperative was REMOVED — too many false positives on
    # legitimate information questions. Operator's prior complaint about premise-guard
    # was the same trigger firing too often.

    return None


def detect_escalation(prompt: str) -> str | None:
    """High-confidence operator-escalation detection (≥2 markers required)."""
    text = (prompt or "").strip()
    if not text:
        return None
    if text.lstrip().startswith("/"):
        return None

    score = 0
    parts = []

    caps = [w for w in _CAPS_RE.findall(text) if w not in _BENIGN_CAPS and not w.startswith("SB")]
    if len(caps) >= 2:
        score += 1
        parts.append(f"{len(caps)} ALL-CAPS")

    frust = _FRUSTRATION_WORDS.findall(text)
    if frust:
        score += 1
        parts.append(f"{len(frust)} frustration markers")

    if _REPEATED_PUNCT.search(text):
        score += 1
        parts.append("repeated punctuation")

    if score >= 2:
        return "; ".join(parts)
    return None


def _trace(tag: str, extra: str = "") -> None:
    try:
        from datetime import datetime as _dt
        with open("/tmp/hook-fire-trace.log", "a") as f:
            f.write(
                f"[{_dt.now().isoformat()}] hook=output-discipline-guard.sh "
                f"path={tag} cwd={os.getcwd()} home={os.environ.get('HOME', '')} "
                f"claude_proj={os.environ.get('CLAUDE_PROJECT_DIR', '<unset>')} {extra}\n"
            )
    except Exception:
        pass


def main() -> None:
    _trace("entered")

    if not (PROJECT_ROOT / "BOOTSTRAP.md").exists():
        _trace("exit-bootstrap-missing")
        sys.exit(0)
    if not is_project_context():
        _trace("exit-not-project-context")
        sys.exit(0)

    try:
        payload = json.load(sys.stdin)
    except Exception:
        _trace("exit-json-error")
        sys.exit(0)

    prompt = payload.get("prompt", "") or payload.get("user_prompt", "")
    if not isinstance(prompt, str):
        _trace("exit-bad-prompt-type")
        sys.exit(0)

    premise = detect_premise_risk(prompt)
    escalation = detect_escalation(prompt)

    if not (premise or escalation):
        _trace("exit-silent-routine")
        sys.exit(0)  # silent on routine prompts

    flags = []
    if premise:
        flags.append(f"PREMISE-RISK ({premise}) — don't infer action; confirm or refrain")
    if escalation:
        flags.append(f"ESCALATION ({escalation}) — shorten · drop tables · action-first")

    additional_context = "AGENT-DISCIPLINE: " + " | ".join(flags)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional_context,
        }
    }
    print(json.dumps(output))
    fired_kinds = []
    if premise:
        fired_kinds.append("premise")
    if escalation:
        fired_kinds.append("escalation")
    _trace(f"fired-{'+'.join(fired_kinds)}", f"banner_len={len(additional_context)}")
    sys.exit(0)


if __name__ == "__main__":
    main()
