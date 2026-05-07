Show the active mode (or report none) + summarize.

> Slash-invoked. Operator types `/mode-status` literally.

## On `/mode-status`

1. Read `$HOME/.claude/active-mode` (single-line file containing the active mode name, or absent/empty if no mode set).
   ```bash
   cat $HOME/.claude/active-mode 2>/dev/null || echo "(none)"
   ```
2. If the file is absent or empty:
   - Report: "No mode active. Modes available: `/mode-pm` (PM Scrum Master), `/mode-architect` (DevOps Architect), `/mode-dual` (both lenses)."
   - Mention briefly: each mode enables a `/cycle` chain; combined with `/loop <interval> /cycle` the agent runs as autopilot in the chosen mode.
   - Do NOT auto-enable a mode. Mode-entry is operator-choice (per directive 2026-05-05).
3. If the file contains a mode name (`pm-scrum-master`, `devops-architect`, or `dual-expert`):
   - Read `$HOME/.claude/modes/<name>.md` and summarize: persona, in-scope, out-of-scope, /cycle sequence.
   - Mention how to switch (`/mode-<other>`) or clear (`/mode-clear`).
4. If the file contains an unknown name: report the discrepancy and offer to clear it.

## Cross-references

- **Canonical command index**: [`.claude/commands/README.md`](README.md) (Tier 1 — `/mode-status` is the read-only mode reporter)
- Companion mode commands: [`/mode-pm`](mode-pm.md) · [`/mode-architect`](mode-architect.md) · [`/mode-dual`](mode-dual.md) · [`/mode-clear`](mode-clear.md)
- State file read: `$HOME/.claude/active-mode`
- Mode files: [`.claude/modes/pm-scrum-master.md`](../modes/pm-scrum-master.md) · [`.claude/modes/devops-architect.md`](../modes/devops-architect.md) · [`.claude/modes/dual-expert.md`](../modes/dual-expert.md)
- Auto-enable forbidden: per directive 2026-05-05 mode-entry is operator-choice; this command surfaces options but does NOT pick one
- **M-E001-1 productive-cycle action vocabulary**: this command emits **`read-only-audit`** action type per Hard Rule 14
- Brain-improvement mandate: [`wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md`](../../wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md)
