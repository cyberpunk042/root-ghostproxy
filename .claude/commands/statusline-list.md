---
description: List all available statusline profiles in ~/.config/ccstatusline/
---

# /statusline-list

List every `profile-<name>.json` available in `~/.config/ccstatusline/` so the operator can see which profiles exist before switching.

Run this command and report the result:

```
bash /root/.config/ccstatusline/switch-profile.sh list
```

The profiles surface as a bulleted list. Each name is operator-pickable via `/statusline-switch <name>` (or `bash ~/.config/ccstatusline/switch-profile.sh <name>` directly).

Tier mapping reference (current naming → use-case):
- `focus` — t1 minified (1 line, deep-coding mode)
- `base` / `standard` — t2 telemetry (2 lines)
- `project` — t3 project-aware basic
- `intermediary` — t3 work tier (3 lines, mid-AIDLC)
- `full-aidlc` — t4 planning tier (3 lines, full AIDLC)
- `aidlc-stamp-full` — t5 review tier (4 lines, full + objective + audit)
