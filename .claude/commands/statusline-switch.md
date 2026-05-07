---
description: Switch active statusline profile to the named tier (e.g. focus / base / standard / project / intermediary / full-aidlc / aidlc-stamp-full)
argument-hint: <profile-name>
---

# /statusline-switch

Switch the active ccstatusline profile to `$ARGUMENTS`. Writes the new active-profile state file at `~/.config/ccstatusline/active-profile`; the wrapper picks up the change on next statusline render (no Claude Code restart required).

Run this command and report the result:

```
bash /root/.config/ccstatusline/switch-profile.sh $ARGUMENTS
```

Available profiles (run `/statusline-list` to confirm):
- `focus` — minified 1-line (deep-coding)
- `base` / `standard` — telemetry-focused 2-line
- `project` — project-aware 2-line
- `intermediary` — mid-tier AIDLC work 3-line
- `full-aidlc` — full AIDLC planning 3-line
- `aidlc-stamp-full` — full + objective + audit 4-line review

After switching, briefly confirm the new active profile to the operator. If the named profile doesn't exist, the underlying script prints an error + lists available profiles — relay that to the operator.
