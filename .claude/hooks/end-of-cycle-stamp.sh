#!/usr/bin/env python3
# end-of-cycle-stamp.sh — Stop hook: emit end-of-cycle status stamp via systemMessage.
#
# Wired event: Stop · matcher: (any)
# Strictness tier (per .claude/rules/hook-architecture.md): **Advisory** observability —
#   informational status stamp; no block/deny; reads stamp-config.json for layout
# Self-gate (per SB-088): CLAUDE_PROJECT_DIR / cwd self-gate + BOOTSTRAP.md presence
# Tests: .claude/hooks/tests/test-end-of-cycle-stamp-diff-suppression.py
#        — **PARTIAL FAIL SURFACED** 2026-05-06 evening: 21/22 (1 failing test)
#        per tools.run-tests output. Surfaced for operator-decision per the
#        brain-improvement Hooks pass option A protocol (NOT unilateral fix).
#        Likely SB-138 stamp diff-suppression territory (D038 — emit short
#        pointer when stamp content unchanged since last fire).
# SB closures: SB-114 (horizontal mode + per-prompt opt-out + default-hide-when-no-mode-active) ·
#              SB-115 (slash-command + persistent JSON config redesign — prompt-marker
#                mechanism failed real-session, replaced) ·
#              SB-133 (envelope fix — top-level systemMessage required for Stop hook)
# SB pending: SB-116 (stamp UX redesign Epic placeholder — DRAFT-tier per operator
#               flagging design quality not at high-standards bar) ·
#             SB-138 (stamp diff-suppression — emit short pointer when content
#               unchanged since last fire; D038 directive — partial test failure
#               likely tracking)
# Cross-refs: .claude/hooks/README.md (DRAFT v1) · tools/stamp.py (config persistence
#             layer; reads/writes .claude/stamp-config.json) ·
#             .claude/commands/stamp-{horizontal,vertical,on,off,auto,status}.md
#             (6 slash commands — operator UX surface) ·
#             tools/cycle.py (the rendering engine — emit_status_block_ansi_*
#             functions produce the stamp content) ·
#             wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md
#             (sacrosanct verbatim directive governing this comment refresh)
#
# Operator-authored I/O enhancement mode (per directive 2026-05-05, sacrosanct verbatim
# at wiki/log/2026-05-05-input-output-enhancement-mode-context-stamp-trail-status.md):
# "context status at input and a trail or stamp and status at the end".
#
# This hook fires on Claude Code's Stop event (end of agent turn) and invokes
# tools.cycle --status-block --diff-fence to produce the colored ```diff-fenced
# block. The output is injected via additionalContext so it renders naturally
# at the end of the agent's response.
#
# Self-gates via BOOTSTRAP.md + CLAUDE_PROJECT_DIR so this fires only for
# $HOME sessions (not /opt second-brain or other sister-project sessions).

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
    session_id = "default"
    try:
        payload = json.loads(raw) if raw else {}
        event = payload.get("hook_event_name", payload.get("hookEventName", ""))
        session_id = (payload.get("session_id", "default") or "default")[:32]
    except Exception:
        pass

    # Self-gate: only fire for $HOME sessions
    if not (PROJECT_ROOT / "BOOTSTRAP.md").exists():
        _trace("exit-bootstrap-missing")
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "").strip()
    home_str = str(PROJECT_ROOT).rstrip("/")
    if project_dir:
        # Positive evidence: must be $HOME or under $HOME
        if not (project_dir.rstrip("/") == home_str or project_dir.startswith(home_str + "/")):
            _trace(f"exit-suppress-on-mismatch:{project_dir}")
            sys.exit(0)
    # If unset → fail-OPEN (fire), per operator priority: visibility > cross-fire-prevention

    # SB-115 redesign: read persistent stamp config (slash-command-driven via
    # tools/stamp.py). Replaces failed prompt-marker mechanism (SB-114 v1).
    # Schema: {"layout": "horizontal"|"vertical", "enabled": "on"|"off"|"auto"}
    stamp_cfg = {"layout": "vertical", "enabled": "auto"}
    cfg_file = PROJECT_ROOT / ".claude" / "stamp-config.json"
    if cfg_file.exists():
        try:
            loaded = json.loads(cfg_file.read_text())
            if isinstance(loaded, dict):
                stamp_cfg.update(loaded)
        except Exception:
            pass

    # enabled=off → suppress
    if stamp_cfg.get("enabled") == "off":
        _trace("exit-config-off")
        sys.exit(0)

    # enabled=auto → mode-conditional (SB-114 sub-req c)
    if stamp_cfg.get("enabled") == "auto":
        active_mode = ""
        try:
            mode_file = PROJECT_ROOT / ".claude" / "active-mode"
            if mode_file.exists():
                active_mode = mode_file.read_text().strip()
        except Exception:
            pass
        if not active_mode:
            _trace("exit-auto-no-mode")
            sys.exit(0)

    # enabled=on falls through to render unconditionally

    # Layout determines cycle.py flag
    render_mode = stamp_cfg.get("layout", "vertical")

    # Invoke tools.cycle with mode-appropriate flag.
    # vertical = --ansi-fence (default, stacked sections)
    # horizontal = --ansi-horizontal (compact, single-line-per-section)
    py = _resolve_python()
    flag = "--ansi-horizontal" if render_mode == "horizontal" else "--ansi-fence"
    try:
        result = subprocess.run(
            [py, "-m", "tools.cycle", flag],
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

    # Diff-suppression (operator directive 2026-05-06): if stamp SEMANTIC
    # content is unchanged since last fire, suppress full render + emit short
    # pointer. Hash is computed AFTER stripping volatile fields (current-time
    # timestamps like HH:MM:SS) so the timestamp differing every fire doesn't
    # defeat the suppression. Normal flowing projects have state-deltas in
    # tracker/SB-counts/cursor/priorities/questions so the stamp renders
    # naturally; static-state fires get a 1-line pointer. Pattern parallels
    # mode-enforcement.sh frequency-control (SB-117).
    import hashlib as _hashlib
    import json as _json
    import re as _re
    cache_path = "/tmp/.end-of-cycle-stamp-last-hash"
    rows_cache_path = "/tmp/.end-of-cycle-stamp-row-hashes.json"  # T067 substrate

    def _strip_volatile(s: str) -> str:
        s = _re.sub(r"\x1b\[[0-9;]*m", "", s)  # ANSI
        s = _re.sub(r"\b\d{2}:\d{2}:\d{2}\b", "TIME", s)  # HH:MM:SS
        s = _re.sub(r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\b", "ISO", s)
        return s

    semantic = _strip_volatile(stamp)
    stamp_hash = _hashlib.sha256(semantic.encode()).hexdigest()

    # T067 (Done When #1): per-row hash cache substrate. Each line that begins
    # with a known label keyword gets its own hash entry. Future T067 work
    # (Done When #2-6) consumes this cache to emit per-row delta markers.
    # This fire only WRITES the cache; consumers will be added in subsequent
    # T067 fires.
    row_label_re = _re.compile(r"^[\s·@@\W]*([A-Z][a-zA-Z]+)[\s·:]+", _re.MULTILINE)
    row_hashes: dict = {}
    current_label: str | None = None
    current_buf: list = []
    for line in semantic.splitlines():
        m = row_label_re.match(line)
        if m and m.group(1) in ("Status", "Journey", "Plan", "Priorities", "Questions",
                                "Tracker", "Progress", "Cursor", "Mission", "Focus",
                                "Impediment", "Blocked"):
            if current_label is not None:
                row_hashes[current_label] = _hashlib.sha256("\n".join(current_buf).encode()).hexdigest()
            current_label = m.group(1)
            current_buf = [line]
        elif current_label is not None:
            current_buf.append(line)
    if current_label is not None:
        row_hashes[current_label] = _hashlib.sha256("\n".join(current_buf).encode()).hexdigest()

    suppress = False
    try:
        if os.path.exists(cache_path):
            with open(cache_path) as _f:
                prev = _f.read().strip()
            if prev == stamp_hash:
                suppress = True
        with open(cache_path, "w") as _f:
            _f.write(stamp_hash)
        # T067 row-cache write (separate from suppress decision; consumers TBD)
        with open(rows_cache_path, "w") as _f:
            _json.dump(row_hashes, _f, indent=2)
    except Exception as exc:
        _trace("diff-cache-error", f"err={exc!r}")

    if suppress:
        pointer = (
            "stamp unchanged since last fire — full render suppressed. "
            "View on demand:  python3 -m tools.cycle --ansi-horizontal  "
            "(or --ansi-fence for vertical layout)."
        )
        print(json.dumps({"systemMessage": pointer}))
        _trace("fired-pointer-suppressed", f"hash={stamp_hash[:12]}")
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
