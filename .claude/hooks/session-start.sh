#!/usr/bin/env python3
# session-start.sh — SessionStart hook: print one-line confirmation that policy
# protection is active, so the user has visible evidence on every session start.
#
# Wired event: SessionStart · matcher: (any) · companion: session-orient.sh
# Strictness tier (per .claude/rules/hook-architecture.md): **Advisory** observability —
#   informational message; no block/deny; pure session-start banner
# Cross-refs: .claude/hooks/README.md (DRAFT v1) · .claude/hooks/session-orient.sh
#             (companion SessionStart hook — directs agent to invoke /orient) ·
#             .claude/hooks/policy-block.sh + leak-detector.sh (the protection
#               layers this banner confirms are active) ·
#             wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md
#             (sacrosanct verbatim directive governing this comment refresh)

import json
import os
import sys

POLICY = os.path.expanduser("~/.claude/hooks/policy-block.sh")
DETECT = os.path.expanduser("~/.claude/hooks/leak-detector.sh")


def main():
    # Read stdin (hook input) but don't actually need any of it.
    try:
        json.load(sys.stdin)
    except Exception:
        pass

    parts = []
    parts.append("policy-block" if os.access(POLICY, os.X_OK) else "policy-block MISSING")
    parts.append("leak-detector" if os.access(DETECT, os.X_OK) else "leak-detector MISSING")

    msg = (
        f"🔒 secret-protection hooks active: {', '.join(parts)}. "
        f"Logs: ~/.claude/hooks/{{deny,leaks}}.log"
    )
    print(json.dumps({"systemMessage": msg}))
    sys.exit(0)


if __name__ == "__main__":
    main()
