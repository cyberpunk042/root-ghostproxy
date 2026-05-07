# /stamp-horizontal

Set stamp render layout to horizontal (compact 6-line format with sections inline).

Run this command and report the result:

```
python3 -m tools.stamp configure --layout horizontal
```

Then briefly confirm to the operator that horizontal layout is now active for end-of-turn stamps.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/stamp-horizontal` is one of two stamp-layout triggers)
- Companion stamp commands: [`/stamp-vertical`](stamp-vertical.md) (alternative layout) · [`/stamp-on`](stamp-on.md) · [`/stamp-off`](stamp-off.md) · [`/stamp-auto`](stamp-auto.md) · [`/stamp-status`](stamp-status.md)
- Backed by tool: [`tools/stamp.py`](../../tools/stamp.py)
- Stamp-rendering hook: [`.claude/hooks/end-of-cycle-stamp.sh`](../hooks/end-of-cycle-stamp.sh)
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
