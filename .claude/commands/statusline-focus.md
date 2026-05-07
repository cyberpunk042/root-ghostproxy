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
