Clear the active mode — return to the no-mode default.

> Slash-invoked. Operator types `/mode-clear` literally.

## On `/mode-clear`

1. Remove `$HOME/.claude/active-mode` (or empty it).
   ```bash
   rm -f $HOME/.claude/active-mode
   ```
2. Acknowledge to the operator: mode cleared; agent now operates per the no-mode default (generic CLAUDE.md / BOOTSTRAP.md baseline; no persona overlay; `/cycle` will report no mode active and prompt to pick one).
3. Mention modes available for re-entry whenever desired.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/mode-clear` is the no-mode-default-return)
- Companion mode commands: [`/mode-pm`](mode-pm.md) · [`/mode-architect`](mode-architect.md) · [`/mode-dual`](mode-dual.md) · [`/mode-status`](mode-status.md)
- State file mutated: `$HOME/.claude/active-mode` (removed/emptied)
- Composes with: [`/cycle`](cycle.md) — with no mode active, `/cycle` reports "No mode active" and stands by per directive 2026-05-05 (mode-entry is operator-choice; agent does not auto-pick)
- Side-effect on banner: mode-enforcement hook is silent when no active-mode set (per SB-088 cross-fire-suppress) — banner stops rendering until next mode entry
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`operator-directive-register`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
