---
title: "2026-05-05 — Proposed /root/.claude/settings.json patch: wire SessionStart orientation + PostCompact hooks (FOR OPERATOR REVIEW)"
type: log
domain: cross-domain
status: draft
confidence: high
maturity: seed
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-broken-and-idle-test
    type: directive
  - id: test-session-transcript
    type: file
    file: /root/.claude/projects/-root/471cef22-638f-4e3e-a4a9-3ebe7a80a8bc.jsonl
    description: "Fresh session that opened, said Hi, agent said 'What would you like to work on?', sat idle"
tags: [log, settings-json, hook-wiring, session-orient, post-compact, operator-review, awaiting-approval, broken-and-idle-fix]
---

# Proposed `/root/.claude/settings.json` patch — orientation hook wiring

> Status: **DRAFT. NOT APPLIED. Awaiting operator approval.** settings.json is policy territory; modifications to hook wiring need explicit approval per `.claude/rules/work-mode.md` PO Approval Boundary.

## Why

Operator's verbatim 2026-05-05: *"I just tested.... it started like crap somehow... hard to explain... maybe its missing a hook. maybe all session should always have a default hook or maybe this one needs its own personalized one"*. And: *"in the brain we have a start hook and an after compact hook I think right ? with command execution and directives even if I am not wrong ?"*.

Confirmed by transcript inspection of `/root/.claude/projects/-root/471cef22-638f-4e3e-a4a9-3ebe7a80a8bc.jsonl`:

- Fresh session opened at 2026-05-05 14:59
- SessionStart hook fired → printed only `🔒 secret-protection hooks active: policy-block, leak-detector. Logs: ~/.claude/hooks/{deny,leaks}.log`
- User said "Hi"
- Agent responded "Hi. What would you like to work on?" — **generic greeter, no project orientation**
- Subsequent turns: agent stayed inert, didn't proactively load CONTEXT.md / BOOTSTRAP.md / wiki/log/ / raw/notes/

Diagnosis: CLAUDE.md and AGENTS.md auto-load as TEXT, but nothing actively orients the agent. The second brain solves this with a SessionStart hook that prints a structured "RESEARCH WIKI — SESSION-START REMINDER" block — see `/opt/devops-solutions-information-hub/.claude/hooks/session-start.sh`. /root has no equivalent.

## What's authored (this iteration)

Two new hook scripts at `/root/.claude/hooks/`:

| File | Purpose |
|---|---|
| `session-orient.sh` | Prints "ROOT-GHOSTPROXY — SESSION-START REMINDER": project framing, BOOTSTRAP.md instruction, critical context (SDD, operator-supervised, 6 pending decisions, draft hooks, sacrosanct quoting), 12-row loaded-knowledge-layers map. Self-gates via `[ -f /root/BOOTSTRAP.md ] || exit 0`. |
| `post-compact.sh` | Prints "ROOT-GHOSTPROXY — POST-COMPACT REMINDER" + chain-execs `session-orient.sh` for full re-orientation. Tells the agent compaction degraded behavioral state; lists what to re-check (CONTEXT.md, latest log, latest raw notes, relevant rules file); lists what NOT to do (recreate from scratch, re-author existing files, apologize for compaction). |

Both syntax-clean (`bash -n`), executable (`chmod +x`), test-fired produces the expected output. Pattern adapted from `/opt/devops-solutions-information-hub/.claude/hooks/session-start.sh` and `/opt/.../post-compact.sh`.

## Proposed settings.json change

Current `/root/.claude/settings.json` `hooks` block (relevant excerpt):

```json
"SessionStart": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "/root/.claude/hooks/session-start.sh",
        "timeout": 5
      }
    ]
  }
],
"SessionEnd": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "/root/.claude/hooks/session-summary.sh",
        "timeout": 5
      }
    ]
  }
]
```

**Proposed (add session-orient.sh to SessionStart; add new PostCompact entry):**

```json
"SessionStart": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "/root/.claude/hooks/session-start.sh",
        "timeout": 5
      },
      {
        "type": "command",
        "command": "/root/.claude/hooks/session-orient.sh",
        "timeout": 10
      }
    ]
  }
],
"PostCompact": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "/root/.claude/hooks/post-compact.sh",
        "timeout": 10
      }
    ]
  }
],
"SessionEnd": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "/root/.claude/hooks/session-summary.sh",
        "timeout": 5
      }
    ]
  }
]
```

Notes:
- session-start.sh stays as the FIRST SessionStart hook (security-envelope confirmation prints first, then orientation).
- session-orient.sh has a 10s timeout (more output than the 5s security check; conservative budget).
- PostCompact is net-new for /root (not currently wired). Pattern parallels second brain's `/opt/.../wiki/.claude/settings.json` PostCompact entry.

## Scope question (operator's verbatim): "is that possible? cause in the brain we have a start hook... and a way not to apply to all project globally but only when starting from there?"

Yes. Claude Code hook configuration is per-`settings.json`, scoped per-cwd:

- `/root/.claude/settings.json` fires when cwd is `/root` or any subdir
- `/opt/devops-solutions-information-hub/.claude/settings.json` fires when cwd is /opt/.../ or subdir
- Sessions in `~/openarms/` fire that project's hooks, NOT /root's

The edge case for /root: it IS the home dir of the root user, so any session as root in /root will fire these hooks. For root-ghostproxy specifically that's correct (the project IS at /root). Both new hook scripts self-gate via `[ -f /root/BOOTSTRAP.md ] || exit 0` — so if BOOTSTRAP.md is missing (= this isn't a root-ghostproxy session), they exit silently.

## Verification (post-patch, if applied)

After operator approval + patch applied:

1. Start a fresh Claude Code session in /root.
2. Confirm session-start.sh fires (security-envelope confirmation appears first).
3. Confirm session-orient.sh fires (orientation block appears second).
4. Send a generic prompt like "Hi" — agent should now reference BOOTSTRAP.md / project state / pending decisions, not "What would you like to work on?".
5. Trigger compaction (long session forces it; or manual via `/compact`). Confirm post-compact.sh fires + agent re-orients.

## Risks / considerations

1. **Two SessionStart hooks fire sequentially.** Sequential output: security-envelope first, then orientation. Some risk of the orientation getting truncated if the agent's context window is tight at startup. Mitigation: orientation is structured + factual; agent should be able to skim. If problematic, merge into one hook later.
2. **Hook output is verbose** (~70 lines for orientation). Trade-off: brevity vs orientation completeness. The 70 lines surface the actual gap that broke the test session. Tunable.
3. **Self-gate via BOOTSTRAP.md** means if BOOTSTRAP is removed/renamed the orientation silently disappears. Acceptable — BOOTSTRAP IS the project's entry; if it's gone, orientation is meaningless anyway.
4. **PostCompact + SessionStart both call session-orient.sh content** = some duplication. Acceptable for now; could DRY later by having session-orient.sh be the canonical and post-compact.sh a thin wrapper (which is what was done).

## What this patch does NOT do

- Does NOT modify the existing `session-start.sh` (security-envelope handler).
- Does NOT change deny rules or PreToolUse / PostToolUse hooks.
- Does NOT change SessionEnd handling.
- Does NOT auto-fix the false-positive patterns in policy-block.sh / malware-block.sh (T-M003-7 still queued).

## Operator action requested

1. Review the two new hook scripts (`/root/.claude/hooks/session-orient.sh` + `post-compact.sh`).
2. Review the proposed settings.json change above.
3. Approve / modify / reject.
4. If approved: apply the settings.json change; test by starting a fresh /root session; confirm orientation fires correctly.

## Cross-references

- Test transcript that surfaced the gap: `/root/.claude/projects/-root/471cef22-638f-4e3e-a4a9-3ebe7a80a8bc.jsonl` (16 lines)
- New scripts: `/root/.claude/hooks/session-orient.sh` (5.2KB) + `/root/.claude/hooks/post-compact.sh` (1.6KB)
- Pattern source: `/opt/devops-solutions-information-hub/.claude/hooks/session-start.sh` (second brain's reminder hook)
- Hook architecture rule: `/root/.claude/rules/hook-architecture.md` (2-layer: machine + project)
- M003 T-M003-7: queued refinement of policy-block + malware-block false positives
