# /stamp-off

Disable stamp rendering globally — no stamp will appear at end of turns until re-enabled.

Run this command and report the result:

```
python3 -m tools.stamp configure --enabled off
```

Then briefly confirm to the operator that stamp is now disabled (use /stamp-on or /stamp-auto to re-enable).

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/stamp-off` is the global-disable stamp trigger)
- Companion stamp commands: [`/stamp-on`](stamp-on.md) (force-on) · [`/stamp-auto`](stamp-auto.md) (mode-conditional default) · [`/stamp-horizontal`](stamp-horizontal.md) · [`/stamp-vertical`](stamp-vertical.md) · [`/stamp-status`](stamp-status.md)
- Backed by tool: [`tools/stamp.py`](../../tools/stamp.py)
- Stamp-rendering hook: [`.claude/hooks/end-of-cycle-stamp.sh`](../hooks/end-of-cycle-stamp.sh) (silent when disabled)
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
