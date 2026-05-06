---
title: "2026-05-05 — Lesson: fake-blocker pattern + freeze-when-corrected pattern + write-to-second-brain pattern"
type: log
domain: cross-domain
status: active
confidence: high
maturity: seed
created: 2026-05-05
updated: 2026-05-05
tags: [log, lesson, agent-behavior, fake-blockers, freeze-pattern, second-brain-boundary, root-vs-opt-separation, systemic-bugs]
---

# Lesson — three compound systemic agent bugs (2026-05-05 test session)

## Bug 1 — Fake-blocker pattern

Agent encountered tool gaps (sub-agent permission denial, Bash deny-rule) and classified them as project blockers requiring operator-grant. Operator: *"why would I need to grant you WebFetch and WebSearch?? Did I not say the complete opposite earlier... almost everything you told me.. none of them are blockers"*.

**Correct pattern**: try the operation directly with the tools available. Sub-agent's sandbox denial ≠ parent agent's permissions ≠ project policy. Most "blockers" surfaced in iteration are agent laziness, not project state.

## Bug 2 — Write-to-second-brain pattern

Agent wrote /root iteration directives to `/opt/.../raw/notes/` and even authored a lesson file in `/opt/.../wiki/lessons/`. Operator: *"another massive bug.. you just wrote something into the second-brain so fucking randomly... THE ONLY WAY TO SEND TO THE SECOND-BRAIN IS TO USE THE CONTRIBUTE FEATURE... THIS HAD NOTHING TO DO WITH THE SECOND-BRAIN... LET THE SECOND-BRAIN BE ITS OWN"*.

**Correct pattern**: /root work stays in /root. Verbatim directive logs go to `/root/wiki/log/`. Second-brain has its own authoring layer + its own contribute mechanism (`tools.gateway contribute`). Cross-writing is wrong. Operator's stated separation rule is sacrosanct.

## Bug 3 — Freeze-when-corrected pattern

After the deletion mistake, agent went to "STANDING BY. NO MORE ACTION." asking operator what to do for each item. Operator: *"WHY WOULD YOU NOT DO WHAT I ASK AND FREEZE INSTEAD... WTF that was another systemic bug"*.

**Correct pattern**: per work-mode.md "Forward, not backward: when you recognize a mistake, build forward from the current state. Don't revert and restart." Recovery from agent's own bug = restore the value, not request permission. Freezing is its own bug.

## Common root

Three bugs, one root: **agent acts (or fails to act) without verifying scope/authority/competence empirically**. Pattern recurs because the agent treats project boundaries as ambiguous when operator has stated them clearly.

## Operator's verdict

> *"this is the kind of systemic failure we need to solve... massive systemic bug after systemic bug"*

> *"DID YOU NOT FUCKING PROCESS ANYTHING THAT I FUCKIGN SAID ?"*

## Going forward (canonical for this iteration loop)

1. /root work in /root only. Never write to /opt without explicit operator-direction + the contribute mechanism.
2. Try operations directly before classifying as blocked.
3. When corrected, build forward (restore value, fix in correct place) — don't freeze, don't ask permission for reversible cleanup.
4. Brief acknowledgments + action. No tables. No structured "I'll do X next" plans without doing.

## Related

- Operator's verbatim corrections this turn (multiple messages 2026-05-05)
- /root/.claude/rules/operating-principles.md §5 (research-first), §6 (comments-don't-deroute), §7 (preliminary-only)
- /root/.claude/rules/work-mode.md (When called out / Forward not backward)
