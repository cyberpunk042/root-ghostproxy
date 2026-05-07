#!/usr/bin/env python3
# leak-detector.sh — PostToolUse hook: scan tool OUTPUTS for credential-shaped values.
#
# Wired event: PostToolUse · matcher: Read|Bash|WebFetch|Grep
# Strictness tier (per .claude/rules/hook-architecture.md): **Enforced** observability —
#   detection + logging + alert; cannot redact (fires after tool output captured)
# Tests: NO formal regression suite (manual test cases only — future M003 T-M003-7
#        territory per refinement queue)
# Cross-refs: .claude/hooks/README.md (DRAFT v1 — flags no-formal-regression-suite) ·
#             .claude/rules/hook-architecture.md (Enforced-tier observability —
#               surfaces detection without state mutation) ·
#             AGENTS.md Hard Rule 1 (deny-by-default) — leak-detector is the
#               post-fact equivalent (loud alert when something slipped through) ·
#             wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md
#               (sacrosanct verbatim directive governing this comment refresh)
#
# Fires AFTER a tool ran, so cannot redact — but surfaces leaks loudly so
# the user can clear the conversation and rotate before more damage happens.
#
# Logs every detection to ~/.claude/hooks/leaks.log
# Emits a systemMessage alert that's visible in the terminal.
# Injects additionalContext telling the model not to echo the value back.

import json
import os
import re
import sys
from datetime import datetime, timezone

LOG_PATH = os.path.expanduser("~/.claude/hooks/leaks.log")

# Same value patterns as policy-block.sh — kept duplicated rather than imported
# to keep each hook script standalone and crash-isolated.
SECRET_VALUE_PATTERNS = [
    (r'sk-ant-[a-zA-Z0-9_\-]{20,}',                            "Anthropic API key"),
    (r'sk-or-v1-[a-zA-Z0-9]{20,}',                              "OpenRouter API key"),
    (r'sk-[a-zA-Z0-9]{32,}',                                    "OpenAI-shaped API key"),
    (r'\bhf_[a-zA-Z0-9]{20,}\b',                                "HuggingFace token"),
    (r'\bgh[pousr]_[A-Za-z0-9]{30,}\b',                         "GitHub PAT"),
    (r'\bglpat-[A-Za-z0-9_\-]{20,}\b',                          "GitLab PAT"),
    (r'\bxox[abprs]-[A-Za-z0-9-]{10,}',                         "Slack token"),
    (r'https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+', "Slack webhook URL"),
    (r'AKIA[0-9A-Z]{16}',                                        "AWS access key id"),
    (r'-----BEGIN ((RSA|EC|DSA|OPENSSH|PGP) )?PRIVATE KEY',     "Private key (PEM)"),
    (r'\bAIza[0-9A-Za-z\-_]{35}\b',                             "Google API key"),
    (r'\bya29\.[0-9A-Za-z\-_]+\b',                              "Google OAuth token"),
    (r'\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b', "JWT"),
    (r'\b(sk|rk|pk)_(live|test)_[A-Za-z0-9]{20,}\b',            "Stripe API key"),
    (r'\bSG\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{30,}\b',        "SendGrid API key"),
    (r'\bkey-[a-f0-9]{32}\b',                                   "Mailgun API key"),
    (r'\bnpm_[A-Za-z0-9]{30,}\b',                               "npm token"),
    (r'\b\d{8,12}:[A-Za-z0-9_\-]{30,}\b',                       "Telegram bot token"),
    (r'\b(postgres(ql)?|mysql|mongodb(\+srv)?|redis|amqp|amqps)://[^\s:/@]+:[^\s@/]+@[^\s/]+', "DB conn-string with creds"),
    (r'Authorization:\s*Bearer\s+[A-Za-z0-9._\-]{20,}',         "HTTP Bearer header"),
    (r'Authorization:\s*Basic\s+[A-Za-z0-9+/=]{16,}',           "HTTP Basic header"),
]
COMPILED = [(re.compile(p), label) for p, label in SECRET_VALUE_PATTERNS]


CURRENT_SESSION = "?"  # populated in main() from hook input


def log_leak(tool, label, sample_redacted):
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a") as f:
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            f.write(f"{ts}\t{CURRENT_SESSION}\tLEAK\t{tool}\t{label}\t{sample_redacted}\n")
    except Exception:
        pass


def redact(s, m):
    """Show prefix only so the leak record doesn't propagate the value."""
    start, end = m.span()
    show = s[start:start + 6] if (end - start) > 8 else "***"
    return f"{show}…[REDACTED {end - start}ch]"


def scan(text):
    """Return list of (label, redacted_sample) for every match found."""
    found = []
    if not text:
        return found
    for c, label in COMPILED:
        for m in c.finditer(text):
            found.append((label, redact(text, m)))
    return found


def main():
    global CURRENT_SESSION
    raw = ""
    try:
        raw = sys.stdin.read()
    except Exception:
        pass
    # Diagnostic trace — UNCONDITIONAL, captures every fire to confirm machine
    # hooks reach this session. Cycle 97 hook-visibility-regression iteration.
    try:
        from datetime import datetime as _dt
        with open("/tmp/hook-fire-trace.log", "a") as _f:
            _f.write(
                f"[{_dt.now().isoformat()}] hook=leak-detector.sh "
                f"cwd={os.getcwd()} "
                f"home={os.environ.get('HOME', '')} "
                f"claude_proj={os.environ.get('CLAUDE_PROJECT_DIR', '<unset>')} "
                f"stdin_len={len(raw)}\n"
            )
    except Exception:
        pass
    try:
        data = json.loads(raw) if raw else {}
    except Exception:
        sys.exit(0)

    CURRENT_SESSION = data.get("session_id", "?")[:12]
    tool = data.get("tool_name", "")
    response = data.get("tool_response", {})

    # Stringify the whole response so we don't need to know the exact field
    # name for each tool. Covers Read / Bash / WebFetch / Grep / etc. uniformly.
    try:
        haystack = json.dumps(response, ensure_ascii=False)
    except Exception:
        haystack = str(response)

    leaks = scan(haystack)
    if not leaks:
        sys.exit(0)

    # Deduplicate by (label, redacted) pair.
    seen = set()
    uniq = []
    for entry in leaks:
        if entry not in seen:
            seen.add(entry)
            uniq.append(entry)

    summary_lines = [f"  - {label}: {sample}" for label, sample in uniq]
    summary = "\n".join(summary_lines)

    for label, sample in uniq:
        log_leak(tool, label, sample)

    alert_msg = (
        f"⚠ CREDENTIAL LEAK DETECTED in {tool} output ({len(uniq)} match"
        f"{'es' if len(uniq) != 1 else ''}):\n{summary}\n"
        f"The value(s) are now in this conversation's context and on disk in the "
        f"transcript. Recommended: rotate the credential immediately, then /clear "
        f"or end this session. Logged to ~/.claude/hooks/leaks.log."
    )
    inject = (
        f"⚠ A credential value was detected in the previous tool output: "
        f"{', '.join(label for label, _ in uniq)}. Do NOT echo, paraphrase, or "
        f"reference any value from that output in your response. Treat it as "
        f"already-burned data; advise the user to rotate and clear."
    )

    print(json.dumps({
        "systemMessage": alert_msg,
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": inject
        }
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
