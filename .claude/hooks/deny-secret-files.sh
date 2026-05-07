#!/usr/bin/env python3
# ============================================================================
# ARCHIVED — UNWIRED 2026-05-06 — superseded by policy-block.sh
# ----------------------------------------------------------------------------
# This is the predecessor credential-exposure hook. The currently-wired hook
# (.claude/hooks/policy-block.sh) covers the same defense-in-depth patterns
# and is referenced by settings.json PreToolUse. This file is kept for
# reference only.
#
# Kept per operator directive 2026-05-06:
# "label them as archive if they are not usefull anymore. dont necessarily
#  delete them. they remind me of something."
#
# Cross-refs: .claude/hooks/README.md (DRAFT v1 — WIRED-vs-ARCHIVE labels) ·
#             .claude/hooks/policy-block.sh (active successor with broader matcher) ·
#             .claude/hooks/tests/test-policy-block.py (10/10 regression tests) ·
#             wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md
#
# Original purpose preserved below for historical reference.
# ============================================================================
#
# Pre-tool-use hook: hard-block credential exposure across the full tool ecosystem.
# Defense-in-depth on top of permissions.deny rules in settings.json.
# False positives are acceptable; false negatives are not.
#
# Covers tools:  Read, Bash, Edit, Write, Glob, Grep, WebFetch, NotebookEdit
# Covers leaks via:
#   - Reading credential files (direct path or via shell readers)
#   - Editing/writing TO credential-shaped paths (could exfiltrate)
#   - Writing secret-shaped CONTENT to arbitrary destinations
#   - Globbing/grepping FOR credential paths (enumeration / content scrape)
#   - Web-fetching URLs that carry credentials or upload local files
#   - Shell exfiltration: env/printenv dumps, curl --data-binary @secret, etc.

import json
import re
import sys

# ---------- Credential-file path patterns ----------
# Each entry is a regex matched (case-insensitively) against the path-or-command
# string with leading/trailing whitespace padding. Patterns aim for substring
# match — false positives over false negatives.
SECRET_FILE_PATTERNS = [
    # Generic .env family
    r'(^|/|\s)\.env(\.|/|\s|$)',
    r'(^|/|\s)[^/\s]+\.env($|/|\s)',
    r'(^|/|\s)\.envrc(\.|/|\s|$)',

    # secrets / secret naming
    r'(^|/|\s)secrets?(\.|/|\s|$)',
    r'(^|/|\s)[^/\s]*secrets?[^/\s]*',

    # X.509 / PKI / keys
    r'\.pem($|\s)',
    r'\.key($|\s)',
    r'\.crt($|\s)',
    r'\.cer($|\s)',
    r'\.der($|\s)',
    r'\.p12($|\s)',
    r'\.pfx($|\s)',
    r'\.jks($|\s)',
    r'\.keystore($|\s)',

    # SSH
    r'(^|/|\s)id_(rsa|ed25519|ecdsa|dsa)(\.|$|\s)',
    r'(^|/|\s)\.ssh/id_',
    r'(^|/|\s)authorized_keys2?($|\s)',

    # Generic credentials
    r'(^|/|\s)credentials?(\.|/|\s|$)',
    r'(^|/|\s)[^/\s]*credentials?[^/\s]*',
    r'(^|/|\s)\.git-credentials($|\s)',

    # Common dotrc files holding auth
    r'(^|/|\s)\.netrc($|\s)',
    r'(^|/|\s)\.npmrc($|\s)',
    r'(^|/|\s)\.pypirc($|\s)',
    r'(^|/|\s)\.pgpass($|\s)',
    r'(^|/|\s)\.htpasswd($|\s)',
    r'(^|/|\s)\.htdigest($|\s)',
    r'(^|/|\s)\.my\.cnf($|\s)',
    r'(^|/|\s)\.pg_service\.conf($|\s)',
    r'(^|/|\s)\.fetchmailrc($|\s)',
    r'(^|/|\s)\.mbsyncrc($|\s)',
    r'(^|/|\s)\.git-tokens?($|\s)',

    # Cloud SDK config dirs (AWS / GCP / Azure / etc.)
    r'\.aws/(credentials|config)($|\s)',
    r'\.azure/(accessTokens\.json|tokens\.json|azureProfile\.json)($|\s)',
    r'\.config/gcloud/',
    r'\.gcloud/',
    r'(^|/|\s)application_default_credentials\.json($|\s)',
    r'service[-_]account[^/\s]*\.json($|\s)',
    r'(^|/|\s)gcs-key[^/\s]*\.json($|\s)',

    # Container / orchestration
    r'\.docker/config\.json($|\s)',
    r'(^|/|\s)kubeconfig($|/|\s)',
    r'\.kubeconfig($|\s)',
    r'\.kube/config($|\s)',
    r'(^|/|\s)k8s-secret[^/\s]*\.ya?ml',
    r'(^|/|\s)secret[-_][^/\s]*\.ya?ml',

    # Hashicorp
    r'(^|/|\s)\.vault-token($|\s)',
    r'(^|/|\s)consul-token[^/\s]*',
    r'(^|/|\s)nomad-token[^/\s]*',

    # Terraform / IaC
    r'\.tfstate($|\s)',
    r'\.tfstate\.backup($|\s)',
    r'\.tfvars($|\s)',
    r'(^|/|\s)terraform\.tfvars\.json($|\s)',
    r'(^|/|\s)secrets?\.ya?ml($|\s)',
    r'(^|/|\s)vault[-_][^/\s]*\.ya?ml',
    r'(^|/|\s)ansible[-_]vault[^/\s]*',

    # Helm / sops / age / encrypted secrets
    r'(^|/|\s)values[-_]secret[^/\s]*\.ya?ml',
    r'\.sops\.ya?ml($|\s)',
    r'\.age($|\s)',
    r'\.gpg($|\s)',
    r'\.asc($|\s)',
    r'\.enc($|\s)',

    # Password managers / wallets
    r'\.kdbx($|\s)',
    r'\.kdb($|\s)',
    r'(^|/|\s)1password[-_]export[^/\s]*',
    r'(^|/|\s)bitwarden[-_]export[^/\s]*',
    r'(^|/|\s)wallet\.dat($|\s)',
    r'(^|/|\s)keystore\.json($|\s)',

    # Browser credential stores
    r'(^|/|\s)Login Data($|\s)',
    r'(^|/|\s)logins\.json($|\s)',
    r'(^|/|\s)key[34]\.db($|\s)',
    r'(^|/|\s)signons\.sqlite($|\s)',
    r'(^|/|\s)cookies\.sqlite($|\s)',
    r'(^|/|\s)Cookies($|\s)',

    # WiFi / VPN / network
    r'wpa_supplicant[^\s]*\.conf($|\s)',
    r'\.ovpn($|\s)',
    r'/etc/wireguard/',
    r'\.wgconf($|\s)',
    r'(^|/|\s)ipsec\.secrets($|\s)',
    r'(^|/|\s)chap-secrets($|\s)',
    r'(^|/|\s)pap-secrets($|\s)',

    # Mail / IRC / chat auth
    r'\.irssi/config($|\s)',
    r'\.znc/configs/',
    r'\.mutt/(passwords|muttrc)',
    r'\.s3cfg($|\s)',
    r'\.boto($|\s)',

    # GnuPG private material (public key files .gpg/.asc covered above; this catches private dir)
    r'\.gnupg/(secring|private-keys|trustdb|random_seed)',
    r'(^|/|\s)secring\.(gpg|kbx)($|\s)',

    # GitHub / GitLab / generic dev tokens by name
    r'(^|/|\s)token[^/\s]*\.(json|txt|env)',
    r'(^|/|\s)[^/\s]*api[_-]?key[^/\s]*',
    r'(^|/|\s)[^/\s]*oauth[_-]?token[^/\s]*',
    r'(^|/|\s)[^/\s]*access[_-]?token[^/\s]*',
    r'(^|/|\s)[^/\s]*refresh[_-]?token[^/\s]*',
    r'(^|/|\s)[^/\s]*bearer[_-]?token[^/\s]*',

    # Backup variants of any of the above (.bak / .orig / ~)
    r'\.env(\.|_)?(bak|backup|orig|old)($|\s)',
    r'secrets?(\.|_)?(bak|backup|orig|old)($|\s)',
]

# ---------- Secret VALUE shape patterns (for Write/Edit content) ----------
# If a Write/Edit content arg looks like it carries a real credential, refuse.
SECRET_VALUE_PATTERNS = [
    r'sk-ant-[a-zA-Z0-9_\-]{20,}',         # Anthropic API
    r'sk-or-v1-[a-zA-Z0-9]{20,}',           # OpenRouter
    r'sk-[a-zA-Z0-9]{32,}',                  # OpenAI-shaped
    r'\bhf_[a-zA-Z0-9]{20,}\b',              # HuggingFace
    r'\bgh[pousr]_[A-Za-z0-9]{30,}\b',       # GitHub PATs
    r'\bxox[abprs]-[A-Za-z0-9-]{10,}',       # Slack
    r'AKIA[0-9A-Z]{16}',                      # AWS access key id
    r'-----BEGIN ((RSA|EC|DSA|OPENSSH|PGP) )?PRIVATE KEY',
    r'\bAIza[0-9A-Za-z\-_]{35}\b',           # Google API key
    r'\bya29\.[0-9A-Za-z\-_]+\b',            # Google OAuth access token
    r'\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b',  # JWTs
]

# ---------- Bash exfiltration command patterns ----------
# Match against the full Bash command string. These are common ways to dump
# environment or pipe credentials to a remote endpoint.
BASH_EXFIL_PATTERNS = [
    r'(^|[\s;&|`])(env|printenv)([\s;&|`]|$)',          # env / printenv (whole-env dump)
    r'(^|[\s;&|`])set([\s;&|`]|$)',                       # bash `set` (dumps env vars too)
    r'(^|[\s;&|`])declare(\s+-x)?([\s;&|`]|$)',           # declare -x (env)
    r'curl[^|;]*--data-binary\s+@',                       # curl exfil via @file
    r'curl[^|;]*-T\s+',                                    # curl upload (-T)
    r'curl[^|;]*-F[^|;]*=@',                              # curl multipart with @file
    r'wget[^|;]*--post-file[= ]',                         # wget post-file exfil
    r'nc(\s+-\w+)*\s+\S+\s+\d+\s*<',                      # netcat with redirect
    r'\$\(\s*cat\s+[^)]*\)',                              # $(cat secret) command substitution
    r'`\s*cat\s+[^`]*`',                                  # `cat secret` backticks
]

COMPILED_FILE = [re.compile(p, re.IGNORECASE) for p in SECRET_FILE_PATTERNS]
COMPILED_VALUE = [re.compile(p) for p in SECRET_VALUE_PATTERNS]
COMPILED_EXFIL = [re.compile(p, re.IGNORECASE) for p in BASH_EXFIL_PATTERNS]


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason
        }
    }))
    sys.exit(0)


def check_path_like(s, label):
    if not s:
        return
    padded = " " + s + " "
    for c in COMPILED_FILE:
        m = c.search(padded)
        if m:
            deny(
                f"Blocked by deny-secret-files hook: {label} contains "
                f"'{m.group(0).strip()}' matching credential-file pattern. "
                f"Hard policy on this machine — credentials are not accessed by "
                f"Claude. Edit ~/.claude/hooks/deny-secret-files.sh to bypass."
            )


def check_value_shape(s, label):
    if not s:
        return
    for c in COMPILED_VALUE:
        m = c.search(s)
        if m:
            deny(
                f"Blocked by deny-secret-files hook: {label} appears to contain a "
                f"credential value (matched pattern '{c.pattern[:40]}...'). "
                f"Refusing to relocate or echo a secret. If this is a false positive "
                f"on a non-credential string, edit "
                f"~/.claude/hooks/deny-secret-files.sh."
            )


def check_bash_exfil(cmd):
    if not cmd:
        return
    for c in COMPILED_EXFIL:
        m = c.search(cmd)
        if m:
            deny(
                f"Blocked by deny-secret-files hook: command '{cmd[:80]}' matches "
                f"environment-dump or exfiltration pattern '{m.group(0).strip()}'. "
                f"Hard policy — environment variables and credential files are not "
                f"dumped or piped over the network."
            )


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {}) or {}

    if tool == "Read":
        check_path_like(inp.get("file_path", ""), "Read path")

    elif tool == "Bash":
        cmd = inp.get("command", "")
        check_path_like(cmd, "Bash command")
        check_bash_exfil(cmd)

    elif tool == "Edit":
        check_path_like(inp.get("file_path", ""), "Edit path")
        # Also refuse if a credential VALUE is being written into a file.
        check_value_shape(inp.get("new_string", ""), "Edit new_string")

    elif tool == "Write":
        check_path_like(inp.get("file_path", ""), "Write path")
        check_value_shape(inp.get("content", ""), "Write content")

    elif tool == "NotebookEdit":
        check_path_like(inp.get("notebook_path", ""), "NotebookEdit path")
        check_value_shape(inp.get("new_source", ""), "NotebookEdit new_source")

    elif tool == "Glob":
        check_path_like(inp.get("pattern", ""), "Glob pattern")
        check_path_like(inp.get("path", ""), "Glob root")

    elif tool == "Grep":
        check_path_like(inp.get("path", ""), "Grep path")
        check_path_like(inp.get("glob", ""), "Grep glob")

    elif tool == "WebFetch":
        url = inp.get("url", "")
        check_path_like(url, "WebFetch URL")
        # Also refuse URLs that smell like they're carrying inline credentials.
        if url:
            for c in COMPILED_VALUE:
                if c.search(url):
                    deny(
                        f"Blocked by deny-secret-files hook: WebFetch URL appears "
                        f"to contain a credential value. Refusing to send a secret "
                        f"to a remote endpoint."
                    )

    sys.exit(0)


if __name__ == "__main__":
    main()
