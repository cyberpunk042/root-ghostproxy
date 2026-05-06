#!/usr/bin/env python3
# premise-guard.sh — DISABLED 2026-05-06.
#
# Was wired as UserPromptSubmit hook. Operator-empirical: caused stamp output
# at start of prompt instead of end of response (Claude Code labeled
# UserPromptSubmit content as "UserPromptSubmit says..."). Unwired from
# settings.json; this no-op preserves the file in case cached session config
# still attempts to invoke it.
#
# To re-enable: restore prior content from git or .claude/hooks/.bak versions.

import sys
sys.stdin.read()  # drain stdin to avoid SIGPIPE
sys.exit(0)  # exit 0 with no stdout = official no-op signal per Claude Code hook docs
