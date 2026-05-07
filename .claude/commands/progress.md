Show the journey view — current position + planning + path traveled.

> Slash-invoked. Operator types `/progress` literally. Read-only — does not modify state.

## On `/progress`

1. Read `$HOME/wiki/governance/progress.md` in full.
2. Re-verify the "Current position" callout is current — check:
   - SFIF stage matches CONTEXT.md
   - Module status counts match `_index.md` realities
   - Task status counts match (15 done / 6 pending / 40 not-started — re-derive from frontmatter scan)
   - git state line accurate (`cd $HOME && git status --short` for live state)
   - Active milestone reflects current epic
3. If drift found between `progress.md` and live reality: flag the discrepancy + offer to refresh `progress.md`. Do NOT silently update.
4. Present:
   - The "Current position" callout (block-quoted faithfully)
   - The planning view (where we're headed; next concrete moves)
   - The path traveled (compressed; refer to `decisions.md` + `wiki/log/` for details)
   - One-line summary of risk + recent commits
5. Stand by.

## When `/progress` is most useful

- Operator asks "where are we" / "what's the state" — answer from `progress.md`, not improvised
- Beginning of a session (after `/orient`) to know the journey position
- Within `/cycle` if active mode is `pm-scrum-master` or `dual-expert` — backlog-status step composes from this
- When orienting a new participant (sub-agent, future operator session, audit reviewer)

## What `/progress` is NOT

- Not the blockers register (use `/blockers`)
- Not the decisions audit (use `/decisions`)
- Not a real-time dashboard — it's a markdown doc that needs refresh discipline
- Not a substitute for reading wiki/log/<date>-*.md when full session context needed

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 governance — `/progress` is the journey-view surface)
- Companion governance commands: [`/blockers`](blockers.md) (decision queue) · [`/decisions`](decisions.md) (audit trail) · [`/sync-progress`](sync-progress.md) (drift refresh) · [`/log`](log.md) (verbatim primary source)
- Backed by tool: [`tools/progress.py`](../../tools/progress.py) — `--callout` mode for live-derived snapshot
- Register file: [`wiki/governance/progress.md`](../../wiki/governance/progress.md)
- Companion `/sync-progress` applies operator-confirmed refresh when drift surfaces
- Composes into: [`/cycle`](cycle.md) — both PM and Architect cycle sequences invoke `/progress` step
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`read-only-audit`** action type per Hard Rule 14 (drift surfacing only — no mutation; mutation routes through `/sync-progress`)
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
