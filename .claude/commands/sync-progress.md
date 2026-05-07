Re-derive `$HOME/wiki/governance/progress.md` Current-position callout from live state.

> Slash-invoked. Operator types `/sync-progress` literally. Modifies progress.md only with operator-confirmed changes.

## On `/sync-progress`

1. Read current `$HOME/wiki/governance/progress.md` Current-position callout.
2. Run `python3 -m tools.progress --callout` for the live-derived callout.
3. Diff the two; report what changed:
   - SFIF stage change?
   - Module status counts changed?
   - Task status counts changed (15 done / 6 pending / 40 not-started — most likely candidate for drift)?
   - Active milestone change?
   - git state change (commit count, uncommitted file count)?
   - Recent logs / commits added?
4. If drift detected:
   - Show the operator the diff
   - Ask: apply the live callout into progress.md? (y/n)
   - If y: replace the Current-position callout block in progress.md with the live one (preserving the rest of the doc)
5. If no drift: report "in sync" and stand by.

## What `/sync-progress` is NOT

- Not a full progress.md rewrite — it ONLY refreshes the Current-position callout
- Not auto-applied — operator confirms the change
- Not a substitute for editing the milestone planning view (that's manual; lives below the callout)
- Not a substitute for the journey log (that's manually appended after each session)

## Composition with `/cycle`

In any mode, `/cycle` includes `/progress` as a step. If progress.md is stale, the cycle's report flags it; operator can `/sync-progress` to refresh.

## When to invoke

- After a task status changes (e.g., a `pending-operator-decision` resolved → moved to `done`)
- After a module readiness flip
- After a git commit
- After an SFIF stage transition
- Before sharing the journey view with someone (operator's audience or future session)

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 governance — `/sync-progress` is the live-state-refresh surface)
- Companion governance commands: [`/blockers`](blockers.md) · [`/decisions`](decisions.md) · [`/progress`](progress.md) · [`/log`](log.md)
- Backed by tool: [`tools/progress.py`](../../tools/progress.py) — `--callout` mode emits derived snapshot block; consumed here for diff
- Register file: [`wiki/governance/progress.md`](../../wiki/governance/progress.md) — Current-position callout block is the only mutated section
- Composes into: [`/cycle`](cycle.md) — every active mode's `/cycle` includes a `/progress` step that surfaces stale-callout drift; operator runs `/sync-progress` to apply
- Drift-fix discipline: [`.claude/rules/work-mode.md`](../rules/work-mode.md) "Verify status claims" — re-derive from live state, don't trust cached
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`drift-fix-with-empirical`** action type per Hard Rule 14 (when drift detected + applied) OR **`read-only-audit`** action type (when in-sync confirmed)
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
