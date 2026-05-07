# /stamp-auto

Set stamp to auto mode (default) — renders only when an active-mode is set; silent otherwise.

Run this command and report the result:

```
python3 -m tools.stamp configure --enabled auto
```

Then briefly confirm to the operator that stamp is now in auto mode (mode-conditional).

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/stamp-auto` is the default mode-conditional trigger)
- Companion stamp commands: [`/stamp-on`](stamp-on.md) (force-on) · [`/stamp-off`](stamp-off.md) (disable globally) · [`/stamp-horizontal`](stamp-horizontal.md) · [`/stamp-vertical`](stamp-vertical.md) · [`/stamp-status`](stamp-status.md)
- Backed by tool: [`tools/stamp.py`](../../tools/stamp.py)
- Stamp-rendering hook: [`.claude/hooks/end-of-cycle-stamp.sh`](../hooks/end-of-cycle-stamp.sh) — auto mode renders only when `$HOME/.claude/active-mode` is set; silent otherwise (default behavior)
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
