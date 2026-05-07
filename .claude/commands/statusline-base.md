---
description: Switch statusline to "base" tier — 2-line telemetry-focused (model + ctx + speed + usage timers)
---

# /statusline-base

Activate the `base` profile (t2 — 2 lines, telemetry-only, no project state). Use case: minimal AI-dev info without AIDLC noise.

Run:

```
bash /root/.config/ccstatusline/switch-profile.sh base
```

Briefly confirm the new active profile to the operator.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/statusline-base` is one of 7 profile-switch triggers in the ccstatusline 5-tier ladder)
- Companion statusline commands: [`/statusline-focus`](statusline-focus.md) (t1) · [`/statusline-standard`](statusline-standard.md) (t2-lean) · [`/statusline-project`](statusline-project.md) (t3) · [`/statusline-intermediary`](statusline-intermediary.md) (t3-work) · [`/statusline-full-aidlc`](statusline-full-aidlc.md) (t4) · [`/statusline-aidlc-stamp-full`](statusline-aidlc-stamp-full.md) (t5)
- Meta commands: [`/statusline-list`](statusline-list.md) (enumerate) · [`/statusline-status`](statusline-status.md) (read active) · [`/statusline-switch`](statusline-switch.md) (named-tier dispatch)
- Backed by script: `/root/.config/ccstatusline/switch-profile.sh`
- Active-profile state file: `~/.config/ccstatusline/active-profile`
- ccstatusline integration: external dependency (Node/JSON-config statusline renderer)
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
