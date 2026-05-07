---
description: Switch statusline to "project" tier — 2-line project-aware basic (task + stage + progress + git)
---

# /statusline-project

Activate the `project` profile (t3 — 2 lines, project-aware basic widgets). Use case: lightweight project context without full AIDLC.

Run:

```
bash /root/.config/ccstatusline/switch-profile.sh project
```

Briefly confirm the new active profile to the operator.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/statusline-project` is the t3 project-aware-basic trigger in the ccstatusline 5-tier ladder)
- Companion statusline commands: [`/statusline-focus`](statusline-focus.md) · [`/statusline-base`](statusline-base.md) · [`/statusline-standard`](statusline-standard.md) · [`/statusline-intermediary`](statusline-intermediary.md) · [`/statusline-full-aidlc`](statusline-full-aidlc.md) · [`/statusline-aidlc-stamp-full`](statusline-aidlc-stamp-full.md)
- Meta commands: [`/statusline-list`](statusline-list.md) · [`/statusline-status`](statusline-status.md) · [`/statusline-switch`](statusline-switch.md)
- Backed by script: `/root/.config/ccstatusline/switch-profile.sh`
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
