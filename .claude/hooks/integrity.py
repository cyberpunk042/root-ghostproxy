"""Shared integrity check used by policy-block.sh and malware-block.sh.

Both hooks call integrity_check() at the start of main(). If it returns a
non-None reason, the hook denies the current tool call AND emits a loud
systemMessage so the user notices the regression. The check is intentionally
strict — better to deny good calls than to let a tampered config silently
weaken protection.

Status (2026-05-06 evening): not-yet-wired as standalone CLI; imported as
Python module by policy-block.sh + malware-block.sh. Standalone CLI wiring
deferred to T015 post-install verification work (foundation IaC roadmap).
The module IS active runtime — every PreToolUse fire calls integrity_check()
via the wired hooks; this file ITSELF is not directly hook-wired in
.claude/settings.json (which is correct — it's a library, not a hook).

Cross-refs:
- .claude/hooks/README.md (DRAFT v1 — WIRED-vs-ARCHIVE labels mark this
  as not-yet-wired-as-standalone-CLI but actively imported)
- .claude/hooks/policy-block.sh + .claude/hooks/malware-block.sh (importers)
- .claude/rules/hook-architecture.md (Strict-tier 2-layer architecture +
  3-component design pattern; integrity_check() is the foundation safety
  envelope's first layer)
- T015 module page in backlog (planned standalone CLI wiring + manual
  invocation surface for operator audit)
- wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md
  (sacrosanct verbatim directive governing this comment refresh)
"""

import json
import os

SETTINGS_PATH = os.path.expanduser("~/.claude/settings.json")
HOOKS_DIR = os.path.expanduser("~/.claude/hooks/")

# Hooks that MUST be present and wired into PreToolUse. Adding to this list
# makes the integrity check enforce more.
REQUIRED_HOOK_FILES = [
    "policy-block.sh",
    "malware-block.sh",
    "leak-detector.sh",
]
REQUIRED_HOOK_MIN_BYTES = 500
REQUIRED_DENY_RULES_MIN = 100


def integrity_check():
    """Return None if config is intact. Otherwise return a string reason."""
    # Settings file must exist and parse.
    try:
        with open(SETTINGS_PATH) as f:
            s = json.load(f)
    except Exception as e:
        return f"settings.json missing or unparseable ({e})"

    # No global hook disable.
    if s.get("disableAllHooks") is True:
        return "disableAllHooks=true — every hook would be neutered"

    perms = s.get("permissions") or {}

    # Bypass-mode lockout must remain.
    if perms.get("disableBypassPermissionsMode") != "disable":
        return ("permissions.disableBypassPermissionsMode is not 'disable' — "
                "someone could boot Claude with --dangerously-skip-permissions "
                "and skip all hooks")

    # Deny-rule list must not be eroded below threshold.
    deny = perms.get("deny") or []
    if len(deny) < REQUIRED_DENY_RULES_MIN:
        return (f"permissions.deny has only {len(deny)} entries "
                f"(< {REQUIRED_DENY_RULES_MIN}) — protection eroded")

    # Required hook scripts must be wired in PreToolUse.
    pre = (s.get("hooks") or {}).get("PreToolUse") or []
    wired_cmds = []
    for entry in pre:
        for h in entry.get("hooks") or []:
            cmd = h.get("command", "")
            if cmd:
                wired_cmds.append(cmd)
    for fname in REQUIRED_HOOK_FILES:
        # leak-detector.sh is wired under PostToolUse, not PreToolUse — handle below.
        if fname == "leak-detector.sh":
            continue
        if not any(fname in c for c in wired_cmds):
            return f"PreToolUse missing hook: {fname}"

    # leak-detector under PostToolUse
    post = (s.get("hooks") or {}).get("PostToolUse") or []
    post_cmds = []
    for entry in post:
        for h in entry.get("hooks") or []:
            cmd = h.get("command", "")
            if cmd:
                post_cmds.append(cmd)
    if not any("leak-detector.sh" in c for c in post_cmds):
        return "PostToolUse missing hook: leak-detector.sh"

    # Each hook script must exist and be non-trivially sized (catches
    # truncation attacks where someone pipes empty content into the file).
    for fname in REQUIRED_HOOK_FILES:
        path = os.path.join(HOOKS_DIR, fname)
        try:
            sz = os.path.getsize(path)
        except OSError:
            return f"hook script {fname} is missing"
        if sz < REQUIRED_HOOK_MIN_BYTES:
            return (f"hook script {fname} is suspiciously small ({sz} bytes) "
                    f"— likely truncated or replaced with a no-op")
        if not os.access(path, os.X_OK):
            return f"hook script {fname} is not executable — chmod -x suspected"

    return None
