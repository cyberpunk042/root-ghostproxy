---
description: Switch statusline to "focus" tier — minified 1-line for deep-coding mode (mode + task + ctxpct + blockers, ~50 chars)
---

# /statusline-focus

Activate the `focus` profile (t1 minified — single line, 4 widgets: Mode + Task + Ctx Used + Blockers). Use case: deep-coding when statusline must not distract.

Run:

```
bash /root/.config/ccstatusline/switch-profile.sh focus
```

Briefly confirm the new active profile to the operator. Statusline picks up the change on next render (no Claude Code restart needed).

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/statusline-focus` is the t1 minified-line trigger in the ccstatusline 5-tier ladder)
- Companion statusline commands: [`/statusline-base`](statusline-base.md) (t2) · [`/statusline-standard`](statusline-standard.md) (t2-lean) · [`/statusline-project`](statusline-project.md) (t3) · [`/statusline-intermediary`](statusline-intermediary.md) (t3-work) · [`/statusline-full-aidlc`](statusline-full-aidlc.md) (t4) · [`/statusline-aidlc-stamp-full`](statusline-aidlc-stamp-full.md) (t5)
- Meta commands: [`/statusline-list`](statusline-list.md) · [`/statusline-status`](statusline-status.md) · [`/statusline-switch`](statusline-switch.md)
- Backed by script: `/root/.config/ccstatusline/switch-profile.sh`
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
