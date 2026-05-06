#!/usr/bin/env python3
# Regression tests for <project>/.claude/hooks/policy-block.sh
#
# Authored cycle 52 to verify SB-083 fix: BASH_EXFIL_PATTERNS regex
# `\$\(\s*cat\s+[^)]*\)` was too greedy and false-positived on benign
# shell flow control like `cat /file 2>/dev/null || echo fallback`.
# Tightened to `\$\(\s*cat\s+[^\s|&;)]+\s*\)` (single-token argument only).
#
# Run: <second-brain>/.venv/bin/python <project>/.claude/hooks/tests/test-policy-block.py
# Expected: 4/4 PASS (formerly-FP allow + real exfil deny + benign multi-token allow)

import json
import subprocess
from pathlib import Path

# Portable resolution: project root = $HOME for type=root install (matches
# operator's pre-compact.sh / post-compact.sh portability pattern).
HOOK = str(Path.home() / ".claude" / "hooks" / "policy-block.sh")
ACTIVE_MODE = str(Path.home() / ".claude" / "active-mode")

# Construct test cases without literal shell-substitution syntax in this source
# (else this script's own source would trip the hook when read by editors that
# scan content for review, and the regex test would be polluted).
DOLLAR = chr(36)
BACKTICK = chr(96)

tests = [
    ("formerly-FP, should allow",
     f"cat {ACTIVE_MODE} 2>/dev/null " + chr(124) + chr(124) + " echo none"),
    ("real exfil cmd-sub, should DENY",
     "echo X" + DOLLAR + "(cat /etc/sec" + "rets)Y"),
    ("real exfil backtick, should DENY",
     "echo X" + BACKTICK + "cat /etc/sec" + "rets" + BACKTICK + "Y"),
    ("benign cmd-sub with multi-token",
     DOLLAR + "(cat /tmp/foo 2>/dev/null " + chr(124) + chr(124) + " echo none)"),
    # SB-115-adjacent set-regex refinement (2026-05-06): `set` as bash builtin
    # for env dump should DENY; `set` as subcommand arg should ALLOW.
    ("bare set env-dump, should DENY",
     "set"),
    ("set piped to grep, should DENY",
     "set " + chr(124) + " grep PATH"),
    ("set in command chain, should DENY",
     ";" + "set" + ";echo done"),
    ("subcommand set arg, should allow",
     "python3 -m tools.stamp set --layout horizontal"),
    ("bash set option flag, should allow",
     "set -o vi"),
    ("compound name set-url, should allow",
     "git remote set-url origin foo"),
]

passed = 0
total = len(tests)

for label, cmd in tests:
    payload = {"session_id": "test", "tool_name": "Bash", "tool_input": {"command": cmd}}
    r = subprocess.run(
        [HOOK],
        input=json.dumps(payload),
        capture_output=True, text=True,
    )
    out = r.stdout.strip() or "(no output → allow)"
    short_out = out[:200].replace("\n", " ")
    expected_deny = "DENY" in label
    actually_denied = '"deny"' in out
    ok = expected_deny == actually_denied
    if ok:
        passed += 1
    marker = "✓" if ok else "✗"
    print(f"{marker} {label:50s} -> {short_out}")

print()
print(f"Result: {passed}/{total}")
exit(0 if passed == total else 1)
