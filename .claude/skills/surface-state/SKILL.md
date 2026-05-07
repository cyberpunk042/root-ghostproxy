---
name: surface-state
description: Use this skill when the user asks about the project's current STATE / position / situation in NATURAL prose (not slash commands). Triggers on phrases like "where are we", "what's the state", "what's the current situation", "give me a status update", "where do we stand", "current position", "how are we doing", "what's our progress". Do NOT trigger on /progress, /orient, or /mode-status (those are explicit slash commands the user already invoked deterministically). Do NOT trigger on questions about specific topics like "where is the install.sh" — that's lookup, not state.
disable-model-invocation: false
---

# Surface state — natural-prose progress query

## When to use

User asked about the project's overall state in natural prose. Examples that should fire this:
- "where are we?"
- "what's the state?"
- "give me a status"
- "current situation"
- "how is it going"
- "where do we stand"

Examples that should NOT fire this (use the slash command directly):
- "/progress" → use `/progress` slash command
- "/orient" → use `/orient` slash command  
- "/mode-status" → use `/mode-status` slash command
- "where is the install.sh" → file lookup, not state
- "what does T011 say" → specific task lookup, not state

## What to do

When triggered:

1. Run `/orient` (deterministic 21-step intel-gathering chain) — this loads the brain + emits the structured ORIENT REPORT.
2. If the user wants more specifically the journey view (where + headed + how got here), follow up by reading `$HOME/wiki/governance/progress.md` (or invoking `/progress` slash command).
3. If active mode is set (per `/orient` step 19-21), reflect that in the response — "you're in PM Scrum Master mode; here's the cycle's view of state."
4. End the response with a one-line "what's next" that's grounded in the 6 pending operator decisions OR the active mode's cycle-next-action — NOT a generic "what would you like to work on?" question.

## Discipline

- Don't fabricate state. Run the tools.
- Don't ask "what specifically did you mean?" — the user said "where are we"; the answer is a project state report.
- Don't repeat content the user can read in BOOTSTRAP.md — answer the question.
- The tools needed are already invoked by `/orient` — don't redo the chain manually.

## Composition

This skill primarily INVOKES `/orient` then layers the prose-friendly answer on top. The slash command is the deterministic load; this skill is the natural-language shim.

## Cross-references

- **Canonical skills index**: [`.claude/skills/README.md`](../README.md) (DRAFT v1, agent-authored 2026-05-06; 2 skills committed in this project)
- **Trigger mechanism**: description-match auto-trigger (~70-95% determinism per [`.claude/rules/trigger-model.md`](../../rules/trigger-model.md)); harness analyzes operator prose, selects this skill when description-match wins, invokes the body via the Skill tool dispatch
- **Routes to deterministic**: this skill INVOKES [`/orient`](../../commands/orient.md) (100% deterministic 21-step intel-gathering chain); skill provides the auto-trigger layer atop the deterministic command
- **Conflation lesson** (sacrosanct discipline): bare prose `continue` / `resume` / `where are we` is conversational language; the deterministic chain at the end of /orient should NOT be re-run on bare prose if /orient already loaded fresh recently — use the prose-friendly summary from already-loaded context. See `<second-brain>/raw/notes/2026-05-04-rename-continue-conflation-bug-and-similar-conflations.md`.
- **Companion skill**: [`surface-blockers`](../surface-blockers/SKILL.md) (auto-trigger on "what's blocking" / "what needs my input" prose; routes to [`/blockers`](../../commands/blockers.md))
- **Description-match contract**: the description field is LOAD-BEARING per Claude Code's description-match dispatch — vague descriptions produce false-positives (auto-fires too often) or false-negatives (never fires). The 8 example trigger phrases + the explicit Do-NOT-trigger list are the contract; modify only with operator approval.
- **Companion modes** (parallel mechanism for state-surfacing): [`/.claude/modes/pm-scrum-master.md`](../../modes/pm-scrum-master.md) — mode-set-durable persona shifts the agent's lens; this skill is ephemeral auto-trigger
- **`/install-agent-brain` propagation**: this skill deploys to sister projects via [`/install-agent-brain`](../../commands/install-agent-brain.md) per operator-opt-in
- **M-E001-1 productive-cycle action vocabulary**: this skill's downstream `/orient` emits **`read-only-audit`** action type per Hard Rule 14
- **Brain-improvement mandate**: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
