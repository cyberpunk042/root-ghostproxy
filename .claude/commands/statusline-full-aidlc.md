---
description: Switch statusline to "full-aidlc" tier — 3-line full AIDLC planning (9 widgets L1 + telemetry L2 + git/usage L3)
---

# /statusline-full-aidlc

Activate the `full-aidlc` profile (t4 planning — 3 lines, full 9-widget AIDLC L1 + comprehensive telemetry + git). Use case: planning mode where you want all AIDLC state visible without the L4 objective layer.

Run:

```
bash /root/.config/ccstatusline/switch-profile.sh full-aidlc
```

Briefly confirm the new active profile to the operator.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/statusline-full-aidlc` is the t4 planning-tier trigger in the ccstatusline 5-tier ladder)
- Companion statusline commands: [`/statusline-focus`](statusline-focus.md) · [`/statusline-base`](statusline-base.md) · [`/statusline-standard`](statusline-standard.md) · [`/statusline-project`](statusline-project.md) · [`/statusline-intermediary`](statusline-intermediary.md) · [`/statusline-full-aidlc-narrow`](statusline-full-aidlc-narrow.md) (narrow-terminal variant) · [`/statusline-aidlc-stamp-full`](statusline-aidlc-stamp-full.md)
- Meta commands: [`/statusline-list`](statusline-list.md) · [`/statusline-status`](statusline-status.md) · [`/statusline-switch`](statusline-switch.md)
- Backed by script: `/root/.config/ccstatusline/switch-profile.sh`
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
