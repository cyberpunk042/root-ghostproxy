---
title: "Epic E005 — Big-Picture Vision Tool — composed-state surface for agent decision-point grounding"
type: epic
status: document-stage
priority: P2
parent_milestone: v0.2-ai-natural-task-management
current_stage: document
readiness: 5
created: 2026-05-07
sources:
  - id: operator-directive-2026-05-07-big-picture-vision
    type: directive
    quote: '"Is there not tool that give big picture visions are you not supposed to used them ? are you not dirrected to use the proper information ? are not even piece injected ? maybe that is still missing. that should probably be at least one new Epic with tasks.."'
tags: [epic, draft, big-picture, vision, decision-grounding, composed-state-surface, sb-140-prevention]
---

# Epic E005 — Big-Picture Vision Tool

> **Agent-DRAFT v1 per SB-095** — operator-directed Epic-level scope. Operator-revisable.

## Summary

Existing tools each surface PARTIAL views of project state — `/orient` (intel chain) · `/progress` (journey) · `/blockers` (operator-input register) · `/decisions` (audit trail) · mode-enforcement banner (priorities + mission + live state) · mindfulness banner (discipline) · stamp (end-of-turn snapshot) · `tools.cycle --json` (cycle state). **None compose into a single big-picture digest the agent consults at decision points.** Result: agent makes per-fire decisions on partial context → falls into SB-140 (self-imposes false gates because it can't see all available work simultaneously) → freezes / drifts to meta-layer / claims "exhausted" when project-layer items are visible to operator. This Epic builds the composed-state surface AND wires it into the agent's decision-points.

## Mission

Make it **structurally impossible** for agent to claim "agent-actionable work exhausted" when project-layer items are visible-to-operator. The big-picture tool must surface ALL agent-actionable items per fire decision-point, with explicit cross-layer scan (project-IaC + meta-substrate + governance + tracker + recurring patterns + active priorities).

## Operator directive (verbatim, sacrosanct)

> *"Is there not tool that give big picture visions are you not supposed to used them ? are you not dirrected to use the proper information ? are not even piece injected ? maybe that is still missing. that should probably be at least one new Epic with tasks.."*

## Suggested module decomposition (DRAFT — operator-revisable)

### M-E005-1 — Inventory existing partial-view tools [document-stage]

Catalog what's there + what each surfaces + what each MISSES. Gap-map.

| Existing tool | What it surfaces | What it MISSES from big picture |
|---|---|---|
| `/orient` | brain load + state-files + recent logs | doesn't compose blockers + decisions + recurring-SBs into one digest |
| `/progress` | journey + milestones + planning | doesn't surface SBs + recurring patterns |
| `/blockers` | operator-input-register | doesn't show recurring-SBs nor agent-actionable work |
| `/decisions` | audit trail | doesn't link to current-priority-relevance |
| Mode-enforcement banner | priorities + mission + live state | already-truncated; doesn't list ALL agent-actionable items |
| Mindfulness banner | clauses-discipline | proactive-reminder, not big-picture |
| Stamp | end-of-turn snapshot | post-hoc, not at decision-point |
| `tools.cycle --json` | cycle state JSON | structured but agent doesn't consult per fire |

### M-E005-2 — Big-picture composed-digest design [design-stage; gated on M-E005-1]

Design the ONE digest that composes: ALL agent-actionable items grouped by layer (project-IaC / meta-substrate / governance / tracker open-SBs / recurring-SBs / active-priorities literal text) + decision-tree per layer-priority + verification-appropriateness reminder per edit-type (clause #9). Explicit gate-verification per clause #8 (each item: tracker-row literal text quoted; not agent-construction).

### M-E005-3 — `/big-picture` slash command [scaffold-stage; gated on M-E005-2]

Operator-invoked: composes M-E005-2 design output in real-time. Reads tracker + decisions + active-priorities + tools.progress + tools.blockers + tools.cycle + tools.questions; emits structured digest.

### M-E005-4 — `tools/big_picture.py` Python tool [scaffold-stage]

Programmatic access for hooks/skills/MCP consumers. JSON output for composability; ANSI-rendered stdout for direct invocation.

### M-E005-5 — Hook injection at decision-points [scaffold-stage; gated on M-E005-4]

Per pathway D8 + clause-architecture: inject big-picture digest at strategic moments — every N prompts? every cycle? on cycle.md step 4 (PM lens scan)? Operator-decides cadence; pathway D9 mode-alternance considerations.

Possible mechanisms:
- Compound with mode-enforcement.sh (extend banner with big-picture excerpt per cycle)
- New UserPromptSubmit hook every N=N prompts (e.g., every 5th)
- Auto-fire on `/cycle` invocation as step 0 (pre-orient grounding)
- PreToolUse on Edit/Write — gate before each substantive edit (verify item is in big-picture-actionable list)

### M-E005-6 — SB-140 prevention integration [test-stage; gated on M-E005-3/4/5]

Empirical: re-run a meta-treadmill scenario (like fires F1-F18 of the loop run) WITH big-picture tool wired. Verify agent picks project-IaC over meta-substrate when big picture surfaces both.

### M-E005-7 — Tests + operator-empirical [test-stage]

Regression + behavioral.

## Open structural questions (operator scope-direction)

| Q | Question | Default per pathway |
|---|---|---|
| Q1 | Per-prompt injection vs per-cycle vs operator-pull? | Hybrid: per-cycle (auto-inject in /cycle skill) + operator-pull (`/big-picture` command) |
| Q2 | Compound with existing mode-enforcement banner OR separate banner? | Separate — mode-enforcement is persona; big-picture is state |
| Q3 | What constitutes "agent-actionable" per layer? Hard-coded checks vs heuristic? | Hard-coded per pathway D8 layer-table (project-IaC = install.sh + bridge + IPS modules · meta = rules + hooks + tracker · governance = decisions + progress + journey) |
| Q4 | How does big-picture interact with SB-140 agent-output-scan hook? | Compound — big-picture is proactive (decision-grounding); agent-output-scan is reactive (post-output) |
| Q5 | Should big-picture digest be operator-readable OR agent-only? | Both — operator can also `/big-picture` to see what agent sees |

## Composition with existing layers

- **SB-140 mitigation stack** (clause #8 + agent-output-scan hook + 16/16 test) — REACTIVE detection of self-blocking phrases
- **Big-picture tool (THIS Epic)** — PROACTIVE surfacing of ALL actionable items so agent doesn't NEED to hallucinate gates
- **Mode-enforcement banner** — persona overlay
- **Mindfulness banner** — discipline reminders
- **Stamp** — end-of-turn snapshot
- **Iterative-evolution-pathway D8 SDD/SFIF/methodology integration** — references the layers big-picture must compose

The big-picture is the MISSING decision-point grounding tool. Compounds, doesn't replace.

## Verification gate (when this Epic is "done")

- `/big-picture` returns composed digest: project-IaC layer (install.sh status + remaining FAILs) + meta layer (open SBs + recurring patterns) + governance (decisions + journey) + active-priorities literal text + verification-appropriateness reminder
- Auto-injected at chosen cadence per Q1
- SB-140 prevention test: simulated meta-treadmill scenario picks project-IaC item from big-picture > agent does not freeze/drift to meta
- Operator-empirical confirmation across 2-3 work blocks

## Cross-references

- SB-140 (the bug this Epic structurally PREVENTS): `wiki/governance/systemic-bugs.md`
- E004 AI Modes Assistant / doctor (cousin): `wiki/backlog/epics/epic-e004-ai-modes-assistant-doctor.md` (E004 = reactive watchdog; E005 = proactive grounding — both compose)
- Iterative-evolution-pathway D8 (layers big-picture composes): `.claude/rules/iterative-evolution-pathway.md`
- Mindfulness clauses 8+9 (rule-layer mitigation): `.claude/hooks/mindfulness.sh`
- Active milestone v0.2: `wiki/backlog/milestones/v0.2-ai-natural-task-management.md` — E005 joins E001/E002/E003/E004
- Existing tools cataloged in M-E005-1 to be inventoried
