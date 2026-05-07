#!/usr/bin/env python3
# post-compact.sh — PostCompact hook: restore project orientation after compaction.
#
# Wired event: PostCompact · matcher: (any) · companion: pre-compact.sh
# Strictness tier (per .claude/rules/hook-architecture.md): **Advisory** —
#   directive injected via additionalContext (~85% generative compliance)
# Self-gate (per SB-088): CLAUDE_PROJECT_DIR / cwd self-gate + BOOTSTRAP.md presence
# **CRITICAL ENVELOPE FIX (SB-133, 2026-05-06)**: emits TOP-LEVEL `systemMessage`
#   per Claude Code schema for PostCompact (NOT `hookSpecificOutput` envelope).
#   Was silently failing every compaction since SB-079 introduction. The fix
#   restores the SB-078 → SB-079 reliability chain (PreCompact writes handoff
#   doc → PostCompact directs agent to /orient + reads the handoff).
# SB closures: SB-079 (post-compact directive reliability) ·
#              SB-133 (envelope schema fix — top-level systemMessage)
# Cross-refs: .claude/hooks/README.md (DRAFT v1) · .claude/hooks/pre-compact.sh
#             (the OTHER end of the loop — writes handoff doc before compaction) ·
#             .claude/commands/orient.md (the deterministic chain this hook directs to) ·
#             wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md
#               (sacrosanct verbatim directive governing this comment refresh)
#
# Why: Compaction summarizes earlier turns and replaces them with a compact summary.
# Behavioral state degrades — operator directives, sacrosanct quotes, in-progress
# task state can all erode in summarization. Without this hook, the agent
# re-reads CLAUDE.md / AGENTS.md but doesn't re-prime on project state.
#
# Output via additionalContext JSON (~85% determinism vs plain stdout ~70%).
# Self-gates via BOOTSTRAP.md presence.
#
# Strategy: tell the agent to re-invoke /orient, AND reference the most-recent
# pre-compact handoff doc (written by pre-compact.sh per SB-078 fix). Closes
# the loop between SB-078 (pre-compact handoff) + SB-079 (post-compact reliability).

import glob
import json
import os
import sys
from pathlib import Path

# Portable path resolution: project root is $HOME for type=root install.
PROJECT_ROOT = Path.home()


def is_project_context() -> bool:
    """True if calling agent is operating from THIS project's context.

    Machine-level hooks fire for ALL sessions on the host — including
    second-brain (/opt) sessions. Without cwd-gating, this hook would
    cross-fire and pollute /opt agent sessions with $HOME project-priming
    directives. SB-010 pattern.

    Detection (priority order):
      1. CLAUDE_PROJECT_DIR env var (set by Claude Code per session)
      2. cwd
    Match: == PROJECT_ROOT or starts with PROJECT_ROOT + "/"
    """
    project_root_str = str(PROJECT_ROOT)
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "").strip()
    if project_dir:
        return project_dir == project_root_str or project_dir.startswith(project_root_str + "/")
    cwd = os.getcwd()
    return cwd == project_root_str or cwd.startswith(project_root_str + "/")


def find_most_recent_handoff() -> str | None:
    """Return path to most recent pre-compact-handoff log, or None."""
    pattern = str(PROJECT_ROOT / "wiki" / "log" / "*-pre-compact-handoff.md")
    matches = glob.glob(pattern)
    if not matches:
        return None
    matches.sort(key=os.path.getmtime, reverse=True)
    return matches[0]


def main() -> None:
    if not (PROJECT_ROOT / "BOOTSTRAP.md").exists():
        sys.exit(0)
    # Cross-firing prevention: only enforce in this project's context.
    # Other sister-project sessions (e.g. /opt second-brain) must pass through.
    if not is_project_context():
        sys.exit(0)

    try:
        json.load(sys.stdin)
    except Exception:
        pass

    handoff = find_most_recent_handoff()
    handoff_block = ""
    if handoff:
        handoff_block = f"""

CRITICAL — read the pre-compact handoff to recover in-flight state:

  {handoff}

That file was written by pre-compact.sh just BEFORE this compaction event. It
contains: active mode, active task, **objective layer** (mission · focus · impediment
per SB-118), **priorities** (imminent-work queue per SB-127), cycle state JSON,
blockers JSON, recent logs by mtime, git state. The summarizer will have erased
nuance from those — this handoff is the deterministic snapshot. Read it AFTER
/orient completes."""

    additional_context = f"""═══════════════════════════════════════════════════════════════════════════
ROOT-GHOSTPROXY — POST-COMPACT REMINDER
═══════════════════════════════════════════════════════════════════════════

Conversation was just compacted. Behavioral state may have degraded:
  - Operator directives quoted verbatim earlier may have been summarized.
  - Sacrosanct quotes ("the operator said X") risk paraphrase-after-compact.
  - In-progress task state, decisions made, file paths discussed — all
    summarized, not preserved.

INVOKE /orient NOW.

  /orient is the deterministic 21-step intel-gathering chain at
  $HOME/.claude/commands/orient.md. Re-running it after compaction
  restores the brain (BOOTSTRAP, CONTEXT, 6 rules files, latest log,
  latest operator-verbatim raw notes) and re-emits the structured ORIENT
  REPORT — so post-compact you have the same project awareness as a
  fresh session.{handoff_block}

DO NOT after compaction:
  - Recreate from scratch what the compacted-out portion already produced.
  - Re-author files that already exist (read first; check git status).
  - Apologize for the compaction or re-introduce yourself.

If unclear what was in flight pre-compact, ASK the operator after /orient
+ handoff-read complete: "Pre-compact we were doing X (per <log file>);
the handoff at <handoff path> shows we were at <task> in <mode>. Continue
or shift?"

═══════════════════════════════════════════════════════════════════════════"""

    # Schema: PostCompact does NOT accept hookSpecificOutput.additionalContext.
    # Use top-level systemMessage (the only operator-visible channel for
    # PostCompact per Claude Code hook schema). The earlier hookSpecificOutput
    # envelope made this hook silently fail every compaction — defeating the
    # whole SB-079 post-compact reliability fix.
    output = {"systemMessage": additional_context}
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
