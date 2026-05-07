---
description: Switch statusline to "intermediary" tier — 3-line mid-tier AIDLC work (mode/task/stage/readiness/blockers + telemetry + git)
---

# /statusline-intermediary

Activate the `intermediary` profile (t3-work — 3 lines, mid-tier AIDLC). Use case: active SFIF work with project + telemetry + git all visible.

Run:

```
bash /root/.config/ccstatusline/switch-profile.sh intermediary
```

Briefly confirm the new active profile to the operator.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/statusline-intermediary` is the t3-work mid-tier-AIDLC trigger in the ccstatusline 5-tier ladder)
- Companion statusline commands: [`/statusline-focus`](statusline-focus.md) · [`/statusline-base`](statusline-base.md) · [`/statusline-standard`](statusline-standard.md) · [`/statusline-project`](statusline-project.md) · [`/statusline-full-aidlc`](statusline-full-aidlc.md) · [`/statusline-aidlc-stamp-full`](statusline-aidlc-stamp-full.md)
- Meta commands: [`/statusline-list`](statusline-list.md) · [`/statusline-status`](statusline-status.md) · [`/statusline-switch`](statusline-switch.md)
- Backed by script: `/root/.config/ccstatusline/switch-profile.sh`
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
