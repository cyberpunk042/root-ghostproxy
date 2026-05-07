---
description: Switch statusline to "full-aidlc-narrow" tier — 3-line planning variant for narrow terminals (~90 chars; drops session/thinking/vim/weekly/sescost)
---

# /statusline-full-aidlc-narrow

Activate the `full-aidlc-narrow` profile (t4-narrow planning variant for narrow terminals ~90 chars). Use case: planning mode on narrow terminal — full AIDLC visibility without overflow.

Drops vs full-aidlc: L1-model (redundant with L2-model) · L1-stage (SFIF carries phase) · L2-session-name · L2-thinking · L2-vim · L3-weeklyusage · L3-sescost.

Run:

```
bash /root/.config/ccstatusline/switch-profile.sh full-aidlc-narrow
```

Briefly confirm the new active profile to the operator.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/statusline-full-aidlc-narrow` is the t4-narrow planning variant for narrow terminals ~90 chars)
- Wide-terminal variant: [`/statusline-full-aidlc`](statusline-full-aidlc.md)
- Companion statusline commands: [`/statusline-focus`](statusline-focus.md) · [`/statusline-base`](statusline-base.md) · [`/statusline-standard`](statusline-standard.md) · [`/statusline-project`](statusline-project.md) · [`/statusline-intermediary`](statusline-intermediary.md) · [`/statusline-aidlc-stamp-full`](statusline-aidlc-stamp-full.md) · [`/statusline-aidlc-stamp-full-narrow`](statusline-aidlc-stamp-full-narrow.md)
- Meta commands: [`/statusline-list`](statusline-list.md) · [`/statusline-status`](statusline-status.md) · [`/statusline-switch`](statusline-switch.md)
- Backed by script: `/root/.config/ccstatusline/switch-profile.sh`
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
