# /stamp-vertical

Set stamp render layout to vertical (stacked sections — JOURNEY / PLAN / BLOCKED / PROGRESS / CURSOR).

Run this command and report the result:

```
python3 -m tools.stamp configure --layout vertical
```

Then briefly confirm to the operator that vertical layout is now active for end-of-turn stamps.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/stamp-vertical` is one of two stamp-layout triggers)
- Companion stamp commands: [`/stamp-horizontal`](stamp-horizontal.md) (alternative layout) · [`/stamp-on`](stamp-on.md) · [`/stamp-off`](stamp-off.md) · [`/stamp-auto`](stamp-auto.md) · [`/stamp-status`](stamp-status.md)
- Backed by tool: [`tools/stamp.py`](../../tools/stamp.py)
- Stamp-rendering hook: [`.claude/hooks/end-of-cycle-stamp.sh`](../hooks/end-of-cycle-stamp.sh)
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
