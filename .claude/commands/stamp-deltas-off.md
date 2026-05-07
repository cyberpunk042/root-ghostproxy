---
description: Disable per-row delta highlighting in stamp render (T067 — back to plain stamp)
---

# /stamp-deltas-off

Disable per-row delta highlighting in stamp render. Stamp returns to plain rendering (no `[Δ]`/`[+]` markers). Per T067.

Run:

```
python3 -m tools.stamp configure --highlight-deltas false
```

Briefly confirm the new config to operator.

## Cross-references

- **Companion**: [`/stamp-deltas-on`](stamp-deltas-on.md) (enable)
- T067 task page: `wiki/backlog/tasks/T067-highlight-changed-rows-in-stamp-render-when-state-delta-dete.md`
- SB-136 stamp diff-suppression (parent feature): `wiki/governance/systemic-bugs.md`
- Backed by tool: `python3 -m tools.stamp configure --highlight-deltas <true|false>`
- Config persists at: `~/.claude/stamp-config.json` field `highlight_deltas`
