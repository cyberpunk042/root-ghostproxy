# /stamp-on

Force stamp to always render at end of every turn (overrides default-hide-when-no-mode).

Run this command and report the result:

```
python3 -m tools.stamp configure --enabled on
```

Then briefly confirm to the operator that stamp is now forced-on regardless of active-mode.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/stamp-on` is one of three stamp-enabled-mode triggers)
- Companion stamp commands: [`/stamp-off`](stamp-off.md) (disable globally) · [`/stamp-auto`](stamp-auto.md) (mode-conditional default) · [`/stamp-horizontal`](stamp-horizontal.md) · [`/stamp-vertical`](stamp-vertical.md) · [`/stamp-status`](stamp-status.md)
- Backed by tool: [`tools/stamp.py`](../../tools/stamp.py) — configure / show subcommands; persists to `$HOME/.claude/stamp-config.json`
- Stamp-rendering hook: [`.claude/hooks/end-of-cycle-stamp.sh`](../hooks/end-of-cycle-stamp.sh) — Stop event; emits via `systemMessage` envelope per SB-115; reads stamp-config.json each fire
- SB-116 UX redesign Epic (DRAFT — stamp config + render layout); SB-114/SB-115 closure
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14 (stamp visibility is operator-config)
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
