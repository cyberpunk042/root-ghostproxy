#!/usr/bin/env python3
# premise-guard.sh — ARCHIVE (per operator directive 2026-05-06: "label them as archive
# if they are not usefull anymore. dont necessarily delete them").
#
# Status: DISABLED 2026-05-06; reduced to no-op stub. Unwired from settings.json.
# Successor: .claude/hooks/output-discipline-guard.sh (subsumes the premise-detector
#            via the SB-090 + SB-094 + SB-120 detection triple — see SB-108 closure).
# Reason for archival: operator-empirical caused stamp output at start of prompt
#            instead of end of response (Claude Code labeled UserPromptSubmit
#            content as "UserPromptSubmit says..."); UserPromptSubmit-position
#            conflict with end-of-cycle-stamp.sh on Stop event drove the unwiring.
# Retention rationale: per operator directive 2026-05-06 — archived hooks retained
#            on disk for reference; cached session config invoking this stub is
#            harmless (drain stdin + exit 0 = official no-op per Claude Code).
# Cross-refs: .claude/hooks/README.md (DRAFT v1 — WIRED-vs-ARCHIVE labels) ·
#             .claude/hooks/output-discipline-guard.sh (active successor) ·
#             wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md
#
# To re-enable: restore prior content from git or .claude/hooks/.bak versions.

import sys
sys.stdin.read()  # drain stdin to avoid SIGPIPE
sys.exit(0)  # exit 0 with no stdout = official no-op signal per Claude Code hook docs
