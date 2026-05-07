Run one cycle of the active mode's autopilot sequence.

> Slash-invoked. Operator types `/cycle` literally — typically wrapped in `/loop <interval> /cycle` for recurring autopilot. Otherwise one-shot.

## On `/cycle`

1. Read `$HOME/.claude/active-mode` (single-line file with mode name, or absent if no mode set).
   ```bash
   cat $HOME/.claude/active-mode 2>/dev/null || echo ""
   ```

   **Or use the structured tool**: `python3 -m tools.cycle --json` returns the active mode + cycle definition + state + blockers summary + progress summary + lifecycle signals (auto-flagged scenarios per loop-cron-lifecycle.md). Sub-agents/MCP consumers should use this.

2. **Consult methodology engine for stage-gate awareness**:
   ```bash
   <second-brain>/.venv/bin/python -c "
   import yaml
   with open('$HOME/wiki/config/methodology.yaml') as f:
       m = yaml.safe_load(f)
   # Use m['stages'] + m['models'] to know what's ALLOWED/FORBIDDEN at the current SFIF stage
   "
   ```
   The cycle's stage-gate-check step (Architect mode) + risk-blocker-scan step (PM mode) should use this to flag any in-progress work that's outside the stage's allowed outputs.

3. **If no mode is active** (file absent or empty):
   - Do NOT execute any cycle.
   - Report: "No mode active. /cycle requires a mode. Use `/mode-pm`, `/mode-architect`, or `/mode-dual` first. Per operator directive 2026-05-05, mode-entry is operator-choice — agent will not auto-pick."
   - Mention what /cycle would do per mode (one-line each).
   - Stand by.

4. **If mode is `pm-scrum-master`**: execute the PM cycle per `$HOME/.claude/modes/pm-scrum-master.md` "/cycle sequence" section:
   - `/orient` to refresh
   - `/blockers` to surface pending-operator-decision items with full context
   - `/progress` to refresh journey view (current position + planning + path)
   - Risk + blocker drift scan (compare blockers.md vs live state — flag any drift)
   - One-line summary + stand by

5. **If mode is `devops-architect`**: execute the Architect cycle per `$HOME/.claude/modes/devops-architect.md` "/cycle sequence":
   - `/orient` to refresh
   - `/progress` (current position + planning lens — engineering-relevant subset)
   - Architecture review (read ARCHITECTURE.md + DESIGN.md; flag open questions, staleness vs recent commits)
   - Implementation progress scan (in-progress tasks next-action; claimable-in-scope smallest-step; gated tasks flagged for PM)
   - Stage gate check (per methodology.yaml)
   - One-line summary + stand by

6. **If mode is `dual-expert`**: execute the Dual cycle per `$HOME/.claude/modes/dual-expert.md` — both PM and Architect lenses per fire (longer than focused-mode cycles):
   - `/orient` to refresh
   - `/blockers` (PM lens)
   - `/progress` (both lenses)
   - Architecture review + implementation progress (Architect lens)
   - Cross-cutting items
   - One-line summary + stand by

7. **If mode is unknown**: report the discrepancy + recommend `/mode-status` then re-enable.

8. **Loop-cron-lifecycle self-evaluation** (per `.claude/rules/loop-cron-lifecycle.md`):
   - Run `python3 -m tools.cycle --json` and check `lifecycle_signals[]`
   - If any signal applies + cron is firing this cycle: consult the rule's reporting protocol; triggers REFINED 2026-05-05 — default action keeps loop running unless operator-confirmed target + N stable cycles.
   - Always report the action (what + why + evidence + mode + recovery + log path).

9. **Systemic-bugs tracker iteration** (per `wiki/governance/systemic-bugs.md`, operator directive 2026-05-05 *"they must all be addressed seriously into a loop"*):
   - Read `wiki/governance/systemic-bugs.md` — register of agent-behavioral + structural systemic bugs with status (open / in-progress / structurally-fixed / verified / recurring).
   - Pick the next item to drive this cycle:
     - First priority: any `open` bug with available structural fix path → highest-leverage one
     - Else: any `structurally-fixed` bug awaiting verification → propose verification approach
     - Else: any `recurring` bug → flag for operator-attention (rules don't auto-fix runtime; operator's catching is the verification)
   - Apply the structural fix (rule edit, hook script, code change in $HOME) OR surface the verification ask.
   - Update tracker: status field + evidence column entry.
   - Surface in cycle report: "This cycle's SB pick: SB-XXX. Action: <what>. New status: <status>."
   - **This step is the work-doing step.** Per operating-principles.md #11, the cycle does the systemic-fix work between cycles; this is where the work names itself.

## Productive cycle taxonomy (SB-128 — closes thin-output pattern)

Per operator directive 2026-05-06: *"I am talking about the fact it bugs.. that it does a little thing sometimes even noting and do a weird statement and stop"*. Each cycle fire must produce one of the following productive outputs. **Naming which category was produced is mandatory in the cycle report**; if none applies, the cycle is THIN (the bug operator named) — name it as such instead of dressing it up.

| # | Category | What it looks like | Empirical signal |
|---|---|---|---|
| 1 | **SB closure with evidence** | Tracker row status `open|recurring` → `structurally-fixed` or `verified` with fix-evidence + verification-evidence columns populated | tracker diff + test pass output OR operator-empirical confirmation |
| 2 | **Code edit with test verification** | Source file edit + corresponding test file edit/run + test exit 0 | inline test output, exit code 0 |
| 3 | **Drift fix with empirical confirmation** | Re-read shows previously-misaligned state now aligned (tracker says X, code/file/state agrees) | inline `grep`/`Read` output of post-fix state |
| 4 | **Documentation with operator-quoted directive** | Rule/command/mode file edit grounded in verbatim operator quote (sacrosanct) | quoted operator words inline + file diff |
| 5 | **Explicit standby with concrete reason** | Cycle reports "no productive work this fire because: [specific blocker / operator-pending decision X / pause-requested by operator]" | named blocker/decision/pause-source |
| 6 | **Tracker reconciliation** | Tracker entry brought to match current empirical reality (status flip / evidence-column refresh / drift-correction with grep) | inline before/after grep output |

**Anti-patterns** (THIN cycle — name it as the bug):

- "Standing by" / "Awaiting your call" without naming a specific blocker → SB-099 abdication-as-freeze
- "Surveyed N items" without action → SB-128 productive-ceiling
- Wall-of-tables explanation without concrete edit → SB-036 compulsive-structured-tables
- "Made minor edit to file X" with no test/verification → P4 declarations-aspirational-until-verified violation

The cycle report's **last line** must end with: `Productive output: <category> — <one-line specific>`. Example: `Productive output: 1 (SB closure) — SB-132 hook-ln false-positive fixed; 8/8 tests pass.`

**Cross-reference**: see also `$HOME/.claude/hooks/mindfulness.sh` clause #6 (4 operator-canonical action types) + `$HOME/wiki/log/2026-05-06-181500-auto-pilot-action-vocabulary-draft.md` (M-E001-1 DRAFT v2 — 9 types, 4 canonical + 5 agent-proposed). The 6 categories above overlap with those vocabularies; harmonization across all three is operator-decision territory, not agent-unilateral.

## Composition with /loop

`/loop 30m /cycle` (in any mode) = autopilot. Each fire executes the active mode's cycle, which is deterministic per the mode file. Switching modes mid-loop changes the cycle on the next fire (state file is read fresh each time).

## Discipline

`/cycle` surfaces, reports, drives the systemic-bugs tracker, and waits. The mode-specific cycle steps (4-6) survey; step 9 actively does the systemic work. The productive-cycle taxonomy (above) is the cycle's quality gate — every fire names its output category. Forward feature-action remains operator's call (per principle #11).
