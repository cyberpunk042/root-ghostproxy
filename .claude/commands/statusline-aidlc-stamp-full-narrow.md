---
description: Switch statusline to "aidlc-stamp-full-narrow" tier — 4-line review variant for narrow terminals (~110 chars)
---

# /statusline-aidlc-stamp-full-narrow

Activate the `aidlc-stamp-full-narrow` profile (t5-narrow review variant for narrow terminals ~110 chars). Use case: review/audit on narrow terminal — full AIDLC + objective + audit visibility without overflow.

Drops vs aidlc-stamp-full: L1-model · L1-stage · L3-session-name · L3-thinking · L3-vim · L4-weeklyusage · L4-sescost.

Run:

```
bash /root/.config/ccstatusline/switch-profile.sh aidlc-stamp-full-narrow
```

Briefly confirm the new active profile to the operator.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/statusline-aidlc-stamp-full-narrow` is the t5-narrow review variant for narrow terminals ~110 chars)
- Wide-terminal variant: [`/statusline-aidlc-stamp-full`](statusline-aidlc-stamp-full.md)
- Companion statusline commands: [`/statusline-focus`](statusline-focus.md) · [`/statusline-base`](statusline-base.md) · [`/statusline-standard`](statusline-standard.md) · [`/statusline-project`](statusline-project.md) · [`/statusline-intermediary`](statusline-intermediary.md) · [`/statusline-full-aidlc`](statusline-full-aidlc.md) · [`/statusline-full-aidlc-narrow`](statusline-full-aidlc-narrow.md)
- Meta commands: [`/statusline-list`](statusline-list.md) · [`/statusline-status`](statusline-status.md) · [`/statusline-switch`](statusline-switch.md)
- Backed by script: `/root/.config/ccstatusline/switch-profile.sh`
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
