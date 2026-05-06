---
date: 2026-05-05
slug: statusline-cross-project-leak-type-root-path-a-collision
type: cross-project-lesson
for: second-brain
tags: [type-root, path-a-install, settings-json, statusline, scope-collision, lesson, cross-project]
---

# type=root Path A install — `$HOME == project-root` settings.json collision

## Operator's verbatim trigger (2026-05-05)

> "weird my second-brain statusline is in the root context somehow... really weird..."

(Followed by: *"just fucking fix this new bug lol.. wtf...."*)

## Context

Type=root projects installed via Path A (operator's chosen install path: `git init` in `$HOME` so `$HOME == repo root`) have an unintended scope-collision: `~/.claude/settings.json` IS `<project>/.claude/settings.json` — the same physical file. Confirmed via `readlink -f`:

```
$ readlink -f ~/.claude/settings.json
/root/.claude/settings.json
$ readlink -f /root/.claude/settings.json
/root/.claude/settings.json
```

Claude Code's settings precedence treats `~/.claude/settings.json` as **user-level** (applies to all projects this user opens) and `<project>/.claude/settings.json` as **project-level** (applies only to that project). For Path A type=root, those collapse to one file.

## The leak pattern

When the operator opens a sister project (e.g. /opt second-brain) in a separate Claude Code session:

1. Claude Code reads project-level: `/opt/.../.claude/settings.json` — has no `statusLine` field
2. Falls through to user-level: `~/.claude/settings.json` (= `/root/.claude/settings.json`) — HAS `statusLine.command` pointing at root-ghostproxy's wrapper
3. Wrapper reads `~/.config/ccstatusline/active-profile` (= /root/.config/...) and renders root-ghostproxy's state (Mode/Blockers/Bugs/Tasks/Readiness)
4. **Sister project shows root-ghostproxy's statusline** with root-ghostproxy's state values

Same pattern would fire for `permissions`, `env`, `model`, any other settings field set in the user-level file.

## Why this is a Path A specific bug

Path B install (clone to `<project>/projects/root-ghostproxy/` or similar) keeps `~/.claude/` and `<project>/.claude/` as physically distinct files. Project-level vs user-level scopes work as Claude Code intends.

Path A is convenient for operators who want their type=root project AT $HOME, but leaks any settings field set in `<project>/.claude/settings.json` to all sister projects on the same user account.

## Fix applied (root-ghostproxy side)

`/root/templates/ccstatusline-config/claude-code-statusline-wrapper.sh` now has a project-scope guard at the top:

```bash
readonly RGP_PROJECT_ROOT="${ROOT_GHOSTPROXY_PROJECT_ROOT:-${HOME}}"
if [[ -n "${CLAUDE_PROJECT_DIR:-}" && "${CLAUDE_PROJECT_DIR}" != "${RGP_PROJECT_ROOT}" ]]; then
    exit 0
fi
```

When `$CLAUDE_PROJECT_DIR` (set by Claude Code per session) doesn't match `$RGP_PROJECT_ROOT` (= `$HOME` by default), wrapper exits empty — sister project's own `statusLine` (if any) renders normally. When `$CLAUDE_PROJECT_DIR` is unset (legacy / non-Claude-Code runners), wrapper proceeds — preserves working behavior.

4-scope regression test passed (`/tmp/test-wrapper-scopes.sh`).

## Generalized lesson (for any settings field, not just statusLine)

For type=root Path A projects, the install is responsible for either:

| Strategy | When |
|---|---|
| **Scope-aware command wrappers** | When a settings field invokes a command (`statusLine`, `hooks`) — wrapper checks `$CLAUDE_PROJECT_DIR` and no-ops outside the project. Pattern: project-scope guard at top of script. |
| **Sister projects author their own override** | When sister project wants a different value — author project-level setting in their own `<sister>/.claude/settings.json`. Overrides user-level fallback per Claude Code precedence. |
| **Document the leak as known Path A gotcha** | When the leak is acceptable or out of scope — operator decides per-field whether they care. |

For sister projects on the same user account: **assume any user-level setting authored by a type=root Path A project may leak in.** Author project-level overrides defensively for fields you care about (statusLine, model, hooks, permissions).

## Recommended cross-project actions

1. **Second-brain side** (operator-owned per binding rule):
   - Author project-level `statusLine` in `/opt/.../.claude/settings.json` to override the leak cleanly. Could be its own ccstatusline wrapper showing /opt state, or simply set to a no-op string to render nothing.
   - Optional: register Path A collision as a generalized lesson in `/opt/.../wiki/lessons/` — applies to ANY type=root project on a single-user account.

2. **Future type=root install scripts**:
   - Auto-detect install path (Path A vs Path B) and emit a warning if Path A: "Settings written to `<project>/.claude/settings.json` will leak to all projects on this user account. Sister projects should author project-level overrides for fields they care about."
   - Default all command wrappers (statusLine, hooks, status-line-equivalents) to scope-aware guards.

3. **Documentation update** (root-ghostproxy):
   - BOOTSTRAP.md gotchas table — add Path A settings.json collision row.
   - SECURITY.md or scripts/README.md — note the cross-project leak vector for any future settings-field additions.

## Cross-project channel

This lesson belongs in `/opt/.../wiki/lessons/01_drafts/` once the cross-project channel is connected (M007). Until then, this log file is the staging ground.

Suggested /opt path: `wiki/lessons/01_drafts/type-root-path-a-settings-json-scope-collision.md`.

## Related

- SB-087 (this bug, registered in `/root/wiki/governance/systemic-bugs.md`)
- SB-086 (related collision: hook command paths in user-level settings.json — same Path A class of bug)
- BOOTSTRAP.md gotcha "type=root scope-not-path" (anticipated identity scope, missed file-collision instance)
- Path A vs Path B install paths (in `<project>/scripts/checkout-a-init-remote.sh` and `checkout-b-clone-subdir.sh`)
