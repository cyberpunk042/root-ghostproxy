#!/usr/bin/env python3
# Stop hook — emit end-of-cycle status stamp via additionalContext.
#
# Operator-authored I/O enhancement mode (per directive 2026-05-05,
# wiki/log/2026-05-05-input-output-enhancement-mode-context-stamp-trail-status.md):
# "context status at input and a trail or stamp and status at the end".
#
# This hook fires on Claude Code's Stop event (end of agent turn) and invokes
# tools.cycle --status-block --diff-fence to produce the colored ```diff-fenced
# block. The output is injected via additionalContext so it renders naturally
# at the end of the agent's response.
#
# Self-gates via BOOTSTRAP.md + CLAUDE_PROJECT_DIR so this fires only for
# /root sessions (not /opt second-brain or other sister-project sessions).

import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path.home()


def _trace(tag: str, extra: str = "") -> None:
    try:
        from datetime import datetime as _dt
        with open("/tmp/hook-fire-trace.log", "a") as f:
            f.write(
                f"[{_dt.now().isoformat()}] hook=end-of-cycle-stamp.sh "
                f"path={tag} "
                f"cwd={os.getcwd()} "
                f"home={os.environ.get('HOME', '')} "
                f"claude_proj={os.environ.get('CLAUDE_PROJECT_DIR', '<unset>')} "
                f"{extra}\n"
            )
    except Exception:
        pass


def _resolve_python() -> str:
    """Find a python with tools.* importable (project venv preferred)."""
    sb_venv = Path("/opt/devops-solutions-information-hub/.venv/bin/python")
    if sb_venv.exists():
        return str(sb_venv)
    return "python3"


def main() -> None:
    _trace("entered")

    # Parse stdin to determine event type
    raw = ""
    try:
        raw = sys.stdin.read()
    except Exception:
        pass

    event = ""
    try:
        payload = json.loads(raw) if raw else {}
        event = payload.get("hook_event_name", payload.get("hookEventName", ""))
    except Exception:
        pass

    # Self-gate: only fire for /root sessions
    if not (PROJECT_ROOT / "BOOTSTRAP.md").exists():
        _trace("exit-bootstrap-missing")
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "").strip()
    home_str = str(PROJECT_ROOT).rstrip("/")
    if project_dir:
        # Positive evidence: must be /root or under /root
        if not (project_dir.rstrip("/") == home_str or project_dir.startswith(home_str + "/")):
            _trace(f"exit-suppress-on-mismatch:{project_dir}")
            sys.exit(0)
    # If unset → fail-OPEN (fire), per operator priority: visibility > cross-fire-prevention

    # Invoke tools.cycle --ansi-fence — ```ansi fence with ANSI codes (full
    # palette: red/green/yellow/blue/magenta/cyan/dim/bold). Same pattern as
    # /opt second-brain hook: ```ansi-fenced ANSI content delivered via
    # top-level systemMessage renders visibly with colors.
    py = _resolve_python()
    try:
        result = subprocess.run(
            [py, "-m", "tools.cycle", "--ansi-fence"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=8,
        )
        stamp = (result.stdout or "").strip()
    except Exception as exc:
        _trace("exit-tool-error", f"err={exc!r}")
        sys.exit(0)

    if not stamp:
        _trace("exit-empty-stamp")
        sys.exit(0)

    # systemMessage is the only valid display channel for Stop hook per
    # Claude Code official docs (hookSpecificOutput.additionalContext NOT
    # supported for Stop event, hookSpecificOutput hookEventName-only also
    # rejected by schema validator).
    print(json.dumps({"systemMessage": stamp}))
    _trace("fired-systemMessage", f"stamp_len={len(stamp)}")
    sys.exit(0)


if __name__ == "__main__":
    main()
