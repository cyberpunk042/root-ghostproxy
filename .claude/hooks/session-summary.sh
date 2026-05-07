#!/usr/bin/env python3
# session-summary.sh — SessionEnd hook: print one-line summary of denies + detected
# leaks during this session, so the user has visible feedback that the protection
# is doing something (or that it caught something they should look at).
#
# Wired event: SessionEnd · matcher: (any)
# Strictness tier (per .claude/rules/hook-architecture.md): **Advisory** observability —
#   informational close-of-session counts; no block/deny
# Cross-refs: .claude/hooks/README.md (DRAFT v1) · .claude/hooks/policy-block.sh
#             + malware-block.sh + leak-detector.sh (the layers this summary counts) ·
#             wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md
#             (sacrosanct verbatim directive governing this comment refresh)

import json
import os
import sys

DENY_LOG = os.path.expanduser("~/.claude/hooks/deny.log")
LEAK_LOG = os.path.expanduser("~/.claude/hooks/leaks.log")


def count_session_lines(path, session_id):
    if not session_id or not os.path.exists(path):
        return 0
    n = 0
    try:
        with open(path) as f:
            for line in f:
                # Log line shape: "<ts>\t<session_id>\t<KIND>\t..."
                fields = line.split("\t", 2)
                if len(fields) >= 2 and fields[1] == session_id:
                    n += 1
    except Exception:
        pass
    return n


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    sid = data.get("session_id", "")[:12]
    if not sid:
        sys.exit(0)
    denies = count_session_lines(DENY_LOG, sid)
    leaks = count_session_lines(LEAK_LOG, sid)
    if denies == 0 and leaks == 0:
        sys.exit(0)
    msg_parts = []
    if denies:
        msg_parts.append(f"{denies} secret-file access attempt{'s' if denies != 1 else ''} blocked")
    if leaks:
        msg_parts.append(f"⚠ {leaks} credential value{'s' if leaks != 1 else ''} DETECTED in tool output (rotate + clear recommended)")
    summary = "policy hook session report — " + "; ".join(msg_parts) + ". Logs: ~/.claude/hooks/{deny,leaks}.log"
    print(json.dumps({"systemMessage": summary}))
    sys.exit(0)


if __name__ == "__main__":
    main()
