---
description: Enable per-row delta highlighting in stamp render (T067 — `[Δ]`/`[+]` markers on changed rows)
---

# /stamp-deltas-on

Enable per-row delta highlighting in the end-of-cycle stamp render. When state-delta detected (per-row hash mismatch vs prior fire), the stamp emits `[Δ]` (changed) or `[+]` (new) markers on the affected rows. Per T067 (extends SB-136 hash-based diff suppression).

Run:

```
python3 -m tools.stamp configure --highlight-deltas true
```

Briefly confirm the new config to operator. Stamp picks up the change on next render (Stop event).

## Cross-references

- **Companion**: [`/stamp-deltas-off`](stamp-deltas-off.md) (disable)
- T067 task page: `wiki/backlog/tasks/T067-highlight-changed-rows-in-stamp-render-when-state-delta-dete.md`
- SB-136 stamp diff-suppression (parent feature): `wiki/governance/systemic-bugs.md`
- Backed by tool: `python3 -m tools.stamp configure --highlight-deltas <true|false>`
- Config persists at: `~/.claude/stamp-config.json` field `highlight_deltas`
