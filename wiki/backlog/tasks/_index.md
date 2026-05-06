---
title: "root-ghostproxy tasks"
type: index
status: active
created: 2026-05-04
updated: 2026-05-05
---

# Tasks — atomic work units across all modules

Naming: `T<NNN>-<slug>.md`. Sequence is per-project (T001 onwards). Per Adoption Guide: tasks are the atomic units that go through stages. Readiness flows up to module, module to epic.

Each task page has frontmatter (status, priority, parent_module, parent_epic, current_stage, readiness, sfif_stage, created/updated dates, sources, tags), Description (1+ paragraphs), Done When (atomic checkboxes), Dependencies, Relationships.

## Coverage by module (61 atomic tasks across 10 modules + 1 module pending tasks)

### Stream 2 — Pure SFIF Project Base

| Module | Range | Pages | Description |
|---|---|---|---|
| **M001 — CLAUDE.md + AGENTS.md** | T001-T006 | 6 | AGENTS.md scope + authoring; CLAUDE.md scope + authoring; operator review; prior-debris reconciliation |
| **M002 — Methodology layer decision** | T007-T010 | 4 | Trade-off decision (local copy chosen); CLAUDE.md methodology section; copy yamls; document decision |
| **M003 — Foundation hardening** | T011-T017 | 7 | Foundation IaC approach decision; install.sh; network bridge config; endpoint AI safety policy; post-install verification; idempotency invariants; foundation gate |
| **M004 — Infrastructure tooling** | T018-T023 | 6 | Verifier scope; verify-policy.py authoring; pipeline wiring (pre-commit/CI); smoke-test verifier; document in CLAUDE.md; M003 no-regression check |
| **M011 — ccstatusline custom widget** | (none yet) | 0 | Added 2026-05-05 per operator directive. Ordered before M005. Atomic tasks pending — operator gives go-ahead before tasks T-M011-* are authored. |
| **M005 — First feature module** | T024-T030 | 7 | Operator picks Suricata/PolarProxy first; follow-up source-syntheses (done); test pcap; design doc; install integration; smoke-test; operator end-to-end validation |

### Stream 1 — Second-Brain Integration

| Module | Range | Pages | Description |
|---|---|---|---|
| **M006 — Pre-connect verification** | T031-T037 | 7 | AGENTS.md exists check; clean git state; capture pre-connect state; read setup.py collision behavior; dry-run from second brain; pre-connect snapshot; assemble audit log |
| **M007 — Connect to second brain** | T038-T043 | 6 | Read setup.py impl; verify type=root handling (done — patched); run --connect-project for real; inspect 4 artefacts; commit atomic; rollback policy on failure |
| **M008 — Smoke test from inside** | T044-T050 | 7 | Open fresh session; time-to-orient ≤ 60s; gateway orient; view spine; MCP tool; failure-mode test (brain unreachable); document M008 results |
| **M009 — Worked example** | T051-T056 | 6 | Reframe operator-decision; execute chosen flow demo; verify second brain knows root-ghostproxy (done); MCP sister-project tool; gateway timeline --scope; document proof |
| **M010 — auto_connect flip decision** | T057-T061 | 5 | Cooling-off period (≥1 week); operator decides flip; apply if yes; document if no; close SFIF rollout epic |

## Status snapshot

As of 2026-05-05 end of preparation session:

| Status | Count | Tasks |
|---|---|---|
| `done` | 15 | T001-T005 (M001 except T006), T007-T010 (M002 all), T025 (M005 source-syntheses), T031 + T034 (M006 — AGENTS.md check + setup.py read), T038 + T039 (M007 — code-review + type=root patch), T053 (M009 — second-brain knows root-ghostproxy) |
| `pending-operator-decision` | 6 | T006 (prior-debris reconciliation), T011 (Foundation IaC approach), T018 (verifier scope), T024 (Suricata-first vs PolarProxy-first), T051 (M009 reframe), T058 (auto_connect flip) |
| `not-started` | 40 | All future-session implementation work — install.sh, network bridge, endpoint safety, modules, smoke tests, etc. |
| **Total** | **61** | |

## Workflow

A future Claude Code session in /root picks up work as follows:

1. Read [CONTEXT.md](../../../CONTEXT.md) for current SFIF stage + active modules.
2. List `pending-operator-decision` tasks → if operator is available, surface them for decision.
3. List `not-started` tasks with no `BLOCKED BY` outstanding → claim one to work on.
4. Per task page's `Done When` checklist + methodology stage gate: complete the task; update status to `done` + readiness=100.
5. After multiple tasks complete, parent module's readiness flows up; when all parent module's tasks are done, module status → done.
6. When all modules of an epic are done, run [T061](T061-close-sfif-rollout-epic.md) to close the epic.

## Methodology

Each task respects the methodology engine: [`../../config/methodology.yaml`](../../config/methodology.yaml) + chosen profiles (simplified SDLC, infrastructure domain, stage-gated methodology). Stage boundaries (document → design → scaffold → implement → test) are hard. ALLOWED/FORBIDDEN per stage is enforced.

## Cross-references

- Active epic: [SFIF Rollout + Second-Brain Integration](../epics/sfif-rollout-and-second-brain-integration.md)
- All 10 module pages: [../modules/](../modules/)
- Operator log: [../../log/](../../log/)

## Cross-project tasks

Tasks added by sister projects via the cross-project channel (operator-granted). Triage these as you would any other task; move into module-scoped sections once accepted.

| Task | Title | Source | Added |
|---|---|---|---|
| T066 | Pre-publish readiness review + post-publish checkout workflow verification | from /opt second-brain | 2026-05-05 |
