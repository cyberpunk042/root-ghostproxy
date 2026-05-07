---
description: Switch statusline to "standard" tier — 2-line lean variant of base (model + ctx + usage)
---

# /statusline-standard

Activate the `standard` profile (t2-lean — 2 lines, slimmer than base). Use case: lean session-aware view without project widgets.

Run:

```
bash /root/.config/ccstatusline/switch-profile.sh standard
```

Briefly confirm the new active profile to the operator.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/statusline-standard` is the t2-lean variant trigger in the ccstatusline 5-tier ladder)
- Companion statusline commands: [`/statusline-focus`](statusline-focus.md) · [`/statusline-base`](statusline-base.md) · [`/statusline-project`](statusline-project.md) · [`/statusline-intermediary`](statusline-intermediary.md) · [`/statusline-full-aidlc`](statusline-full-aidlc.md) · [`/statusline-aidlc-stamp-full`](statusline-aidlc-stamp-full.md)
- Meta commands: [`/statusline-list`](statusline-list.md) · [`/statusline-status`](statusline-status.md) · [`/statusline-switch`](statusline-switch.md)
- Backed by script: `/root/.config/ccstatusline/switch-profile.sh`
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
