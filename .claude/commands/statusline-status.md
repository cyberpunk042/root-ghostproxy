---
description: Show currently active statusline profile + resolved config path
---

# /statusline-status

Display the active statusline profile (read from `~/.config/ccstatusline/active-profile`) plus the resolved config-file path.

Run this command and report the result:

```
bash /root/.config/ccstatusline/switch-profile.sh
```

Briefly confirm to the operator the active profile name + config path.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/statusline-status` is the read-only active-profile reporter)
- Companion meta commands: [`/statusline-list`](statusline-list.md) (enumerate profiles) · [`/statusline-switch`](statusline-switch.md) (named-tier dispatch)
- Profile-switch commands: 7 per tier ladder (focus/base/standard/project/intermediary/full-aidlc/aidlc-stamp-full) + 2 narrow variants
- State file read: `~/.config/ccstatusline/active-profile`
- Backed by script: `/root/.config/ccstatusline/switch-profile.sh`
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`read-only-audit`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
