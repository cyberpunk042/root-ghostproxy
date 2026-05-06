#!/usr/bin/env python3
# SessionStart hook: print a one-line confirmation that policy protection
# is active, so the user has visible evidence on every session start.

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
