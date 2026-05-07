---
title: "T067 — Highlight changed rows in stamp render when state-delta detected (extends SB-136 hash-based diff suppression)"
type: task
status: in-progress
priority: P3
parent_blocker: "SB-116"
current_stage: implement
readiness: 83
created: 2026-05-06
updated: 2026-05-07
tags: [agent-drafted, m-e002-1-create-verb]
---

# T067 — Highlight changed rows in stamp render when state-delta detected (extends SB-136 hash-based diff suppression)

> Agent-DRAFT created via `tools.tasks create from-blocker` (M-E002-1, 2026-05-06). Operator-revisable.

## Description

Extension to SB-136 stamp diff-suppression: when a stamp DOES change since last fire (hash-mismatch), highlight WHICH row(s) changed instead of just rendering the new full stamp. Operator-stated 2026-05-06: *"when there is an actual diff in the stamp we could even find a way to highly it properly"*.

### Compound-fit rationale

- SB-136 already computes per-fire SHA-256 of stamp content (with volatile-strip for ANSI/HH:MM:SS/ISO). When unchanged → pointer; when changed → full render.
- This extension adds **per-row diff awareness**: cache prior stamp's row-keyed hashes (e.g. one hash per Status/Plan/Priorities/Tracker/Cursor/Mission/Focus/Impediment/Questions row) instead of one whole-stamp hash.
- On render, compare each row's hash to last fire's; if changed → emit the row with a delta marker (e.g. ANSI bold/yellow underline, or `▶` prefix, or "CHANGED" suffix).

### 3 concrete shapes (DRAFT, agent-proposed)

- **(a) Per-row hash cache**: `/tmp/.end-of-cycle-stamp-row-hashes.json` keyed by row-name; each entry = sha256 of row's content. On render, diff per-row + emit delta-marker on changed rows.
- **(b) Diff-mode flag**: `tools.cycle --ansi-horizontal --highlight-deltas` reads cache + emits per-row markers. Default off; enable via stamp config or per-mode default.
- **(c) Categorical highlight**: distinguish "added" / "modified" / "removed" rows (e.g. green for added, yellow for modified, dim-strikethrough for removed). Higher fidelity but more complex.

Suggested default: **(a) + (b)** — per-row hash cache + opt-in flag. (c) is a future enhancement after (a)+(b) prove out empirically.

### Compound layers this extends

- Stamp render (cycle.py horizontal + vertical layouts)
- SB-136 diff-suppression (volatile-strip pattern reusable)
- Mindfulness clause #6 (substance-per-fire — visible deltas reinforce real work)

## Done When

- [x] Per-row hash cache wired in `end-of-cycle-stamp.sh` (extends `/tmp/.end-of-cycle-stamp-last-hash` to JSON-keyed) — landed prior session
- [x] `tools.cycle --highlight-deltas` flag added; reads cache + emits per-row delta markers — landed prior session
- [x] Stamp config schema extended: `highlight_deltas` field (bool, default false) — **landed 2026-05-07 (autopilot fire 28)**: `~/.claude/stamp-config.json` gained `"highlight_deltas": false` + `tools/stamp.py` extended with `--highlight-deltas {true,false}` flag in `configure` verb; round-trip smoke-test PASS
- [x] `/stamp-deltas-on` / `/stamp-deltas-off` slash commands (parallel to existing /stamp-* pattern) — **landed 2026-05-07 (autopilot fire 29)**: both .md command files authored at `.claude/commands/`; both visible in Claude Code skill discovery
- [x] Regression tests added to `test-end-of-cycle-stamp-diff-suppression.py`: cache write + per-row diff detection + delta-marker render — landed prior session (22/22 PASS)
- [ ] Operator-empirical: real session run shows changed rows visibly highlighted on next-fire after state mutation

## Dependencies

- **Hard**: SB-136 stamp diff-suppression (already structurally-fixed)
- **Soft**: SB-116 stamp UX Epic — this task fits inside that operator-pending Epic; advancing T067 would advance SB-116 partially

## Connects to

- SB-116 (parent_blocker — stamp UX Epic-pending)
- SB-136 (extends — same hash-based delta primitive)
- compound-and-waterfall.md (stamp is compound layer; visible deltas enrich it)
- Mindfulness clause #6 (visible deltas counter thin-output regression)
- M-E001-1 vocabulary (likely emits as `verified-edit` action when row-content state-mutates)

