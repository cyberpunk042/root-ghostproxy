# /stamp-status

Show current stamp render config (layout, enabled mode).

Run this command and report the result:

```
python3 -m tools.stamp show
```

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/stamp-status` is the read-only stamp-config reporter)
- Companion stamp commands: [`/stamp-on`](stamp-on.md) · [`/stamp-off`](stamp-off.md) · [`/stamp-auto`](stamp-auto.md) · [`/stamp-horizontal`](stamp-horizontal.md) · [`/stamp-vertical`](stamp-vertical.md)
- Backed by tool: [`tools/stamp.py`](../../tools/stamp.py)
- Config file inspected: `$HOME/.claude/stamp-config.json`
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`read-only-audit`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
