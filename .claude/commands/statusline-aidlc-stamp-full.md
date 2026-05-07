---
description: Switch statusline to "aidlc-stamp-full" tier — 4-line review (L1 action + L2 objective + L3 telemetry + L4 env+audit, architecture-grouped v3)
---

# /statusline-aidlc-stamp-full

Activate the `aidlc-stamp-full` profile (t5 review — 4 lines, architecture-grouped v3 with L2 objective layer at prime real-estate). Use case: review/audit mode where ALL state needs visibility — action snapshot + compound objective + telemetry + env + decisions/questions audit.

Run:

```
bash /root/.config/ccstatusline/switch-profile.sh aidlc-stamp-full
```

Briefly confirm the new active profile to the operator.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/statusline-aidlc-stamp-full` is the t5 review/audit tier — top of the ccstatusline 5-tier ladder)
- Narrow-terminal variant: [`/statusline-aidlc-stamp-full-narrow`](statusline-aidlc-stamp-full-narrow.md)
- Companion statusline commands: [`/statusline-focus`](statusline-focus.md) · [`/statusline-base`](statusline-base.md) · [`/statusline-standard`](statusline-standard.md) · [`/statusline-project`](statusline-project.md) · [`/statusline-intermediary`](statusline-intermediary.md) · [`/statusline-full-aidlc`](statusline-full-aidlc.md) · [`/statusline-full-aidlc-narrow`](statusline-full-aidlc-narrow.md)
- Meta commands: [`/statusline-list`](statusline-list.md) · [`/statusline-status`](statusline-status.md) · [`/statusline-switch`](statusline-switch.md)
- Surfaces objective layer (L2): mission/focus/impediment from SB-118 state files + audit-line decisions/questions counts
- Backed by script: `/root/.config/ccstatusline/switch-profile.sh`
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
