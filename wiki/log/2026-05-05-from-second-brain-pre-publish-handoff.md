---
title: "Pre-publish handoff — scripts + lessons + adoption status (from /opt 2026-05-05)"
type: handoff
from: second-brain
for: root-ghostproxy
created: 2026-05-05
updated: 2026-05-05
status: active
tags: [from-second-brain, cross-project, handoff, root-ghostproxy]
---

# Pre-publish handoff — scripts + lessons + adoption status (from /opt 2026-05-05)

## Metadata

- **From**: /opt second-brain (devops-solutions-information-hub)
- **For**: root-ghostproxy
- **Type**: handoff
- **Date**: 2026-05-05
- **For-action**: review companion task; run publish + checkout scripts at /tmp/ when ready

## Content

## Summary

The /opt second-brain agent has prepared the cross-project channel + publish tooling for root-ghostproxy. Operator is about to publish (gh repo create + push). After publish, operator will checkout the repo on a different machine.

This NOTE is the narrative side of the handoff. The companion TASK lists the actionable items for /root agent (next session).

## What landed in /opt this session arc (relevant to /root)

| Artifact | Path (in /opt) | Purpose |
|---|---|---|
| Handoff log (full) | `wiki/log/2026-05-05-handoff-to-root-session.md` | Detailed table of 19 mature lessons + 1 principle + 2 patterns distilled from /root's session |
| Cross-project channel tools | `tools/cross_project_note.py`, `tools/cross_project_task.py` | Operator-granted write channel (this very note delivered via these) |
| Adoption Guide patterns | `wiki/patterns/03_validated/architecture/{agent-modes-three-mode-pattern,session-orientation-pair-*}.md` | Transcendable agent-behavior infrastructure with full opt-in guides |
| Lessons distilled from /root | 19 in `wiki/lessons/03_validated/`, 1 principle in `wiki/lessons/04_principles/hypothesis/` | Cross-applicable patterns from /root's recent operator directives |
| Orient pair adoption decision | `wiki/log/2026-05-05-orient-pair-adoption-decision.md` | /opt second-brain opted in to /root's session-orientation pair pattern |

## Scripts (correct locations)

The publish script is one-shot ephemeral (operator-tool, not project-deliverable) — stays at `/tmp`. The checkout + curl-bootstrap scripts ARE project deliverables and ship with the repo at `/root/scripts/` (whitelisted in `.gitignore` 2026-05-05 per operator directive).

| Script | Location | Where to run | Purpose |
|---|---|---|---|
| `publish-root-ghostproxy.sh` | `/tmp/` (ephemeral) | /root cwd, /root machine | Initial commit + LICENSE + .gitignore patches + branch rename + gh repo create + push. One-shot operator tool. |
| `install-from-curl.sh` | `/root/scripts/` (committed) | target machine via `curl … \| bash` | One-shot bootstrap. Naturally does the right thing: TTY detected → asks MODE upfront (B safe-default / A advanced). MODE=B → clone to subdir, $HOME UNTOUCHED, done. MODE=A → backup conflict points + checkout -f + AUTO-RUNS `merge-from-backup.sh --apply` (per-change surgical reconciliation) + validates JSON, all in one invocation. No TTY → MODE=B safe default, no prompts. Flags: `--interactive`, `--auto`. Env: REPO_URL, BRANCH, MODE, TARGET, ASSUME_YES. |
| `checkout-a-init-remote.sh` | `/root/scripts/` (committed) | $HOME on target machine | Path A: git init in $HOME + remote add + fetch + checkout -f. Backs up conflict points to `.pre-ghostproxy.bak/` first. |
| `checkout-b-clone-subdir.sh` | `/root/scripts/` (committed) | anywhere on target machine | Path B: clone to subdir (default: `$HOME/root-ghostproxy/`). $HOME untouched. install.sh handles deployment. |
| `merge-from-backup.sh` | `/root/scripts/` (committed) | $HOME on target machine, AFTER Path A checkout | **SURGICAL** post-checkout reconciliation. Default = diff mode (NO changes). `--apply` requires per-change confirmation — there is no `--auto` bypass. Only purely additive changes (permissions.allow/deny/ask union; operator-unique opencode.json keys) are offered as merge candidates. Custom hooks, custom rules, hooks-block changes, and `.gitignore` additions are surfaced ONLY (never auto-applied) — operator decides manually. Stages writes to `.merged` files, validates JSON, atomically swaps with `.pre-merge.bak` preservation. Backup directory NEVER auto-deleted. Recovery procedure printed at end. |

All three default to dry-run; pass `--execute` to mutate. The `/root/scripts/` ones get committed + published with the repo so they're available after publish to anyone cloning.

Typical user one-liner after publish (Path B equivalent, the safest default):

```bash
curl -fsSL https://raw.githubusercontent.com/<owner>/root-ghostproxy/main/scripts/install-from-curl.sh | bash
```

Or with overrides (Path A — touches $HOME):

```bash
curl -fsSL https://.../install-from-curl.sh | MODE=A bash
```

## Pre-publish state (what publish script handles automatically)

Per /tmp/publish-root-ghostproxy.sh:
- Pre-flight: cwd=/root, gh authenticated, core files present, no pre-staged changes, no existing commits, sensitive files correctly gitignored, repo name available on GitHub.
- Step 1: appends `/tools/` and `/templates/` whitelist to .gitignore (skipped if already present).
- Step 2: fetches LICENSE body via `gh api /licenses/<type>`, stamps year + author into placeholders.
- Step 3: stage + show staged file count + types breakdown + top-level entries.
- Step 4: initial commit with substantive multi-line message.
- Step 5: rename master → main.
- Step 6: gh repo create with --private (default) or --public.
- Step 7: push.

## Post-publish checkout paths

Path A (init + remote into $HOME) — for the operator's own dev work on a different machine where $HOME == repo-root is desired. Conflict points (`.claude/settings.json`, `.config/opencode/opencode.json`, `.gitignore`, etc.) are auto-backed-up to `.pre-ghostproxy.bak/`. Manual merge step needed post-checkout for those paths.

Path B (clone to subdir) — for read/inspect/test scenarios. $HOME untouched. Repo at ~/root-ghostproxy/. install.sh handles deployment (when M003+M004+M012 land).

## Empirical observations from this session

- Hook-cross-firing lesson re-validated: /root's machine-level `policy-block.sh` cross-fired against /opt-cwd Bash command via `.claude/...jsonl` substring (credential pattern). The lesson at `wiki/lessons/03_validated/tools-architecture/hook-scope-machine-vs-project-level-cross-firing-anti-pattern.md` predicts this exactly. The cross-firing did not block actual work — read /root/wiki/log/ instead of jsonl, per the lesson's correct discipline.
- Bash multi-line for-loop variable-expansion bug: registered as unreproduced finding at `raw/notes/2026-05-05-bash-multiline-for-loop-variable-expansion-finding-not-reproduced.md`. Worth knowing in case /root agent encounters something similar.

## What /root agent does NOT need to do

- Edit /opt files (boundary respected — operator runs publish from /root cwd; /opt is read-only from /root's perspective except via contribute channel).
- Worry about LICENSE / .gitignore patches manually — publish script handles.
- Worry about modifying CONTEXT.md or BOOTSTRAP.md to surface this note — /root's existing /orient command (step 11) reads recent wiki/log/ entries, picks this up automatically.

## Channel discipline going forward

The cross-project channel `tools.cross_project_{note,task}` at /opt is the designated write path from /opt to sister projects. /opt agent does NOT modify any other path in /root. /root agent contributes back to /opt via the planned `gateway contribute` channel (M007 — pending) or operator-mediated transfer.

## Pickup mechanism

This file lives at `root-ghostproxy/wiki/log/<date>-from-second-brain-<slug>.md` in the target project's iteration log layer. Target's `/orient` command (or equivalent intel-gathering chain) reads recent `wiki/log/` entries on session start; this note will be among them.

**Channel discipline**: cross-project notes via this channel are advisory — target agent reads, decides, acts within target's own scope. /opt agent does not write outside this designated channel.
