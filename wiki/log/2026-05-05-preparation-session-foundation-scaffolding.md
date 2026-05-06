---
title: "2026-05-05 — root-ghostproxy preparation session — foundation scaffolding"
type: note
domain: log
note_type: session
status: active
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: directive-raw-notes
    type: file
    file: /opt/devops-solutions-information-hub/raw/notes/2026-05-04-prepare-root-ghostproxy-as-sister-type-root-group-operating-system-setup.md
    description: "Operator directive establishing type=root, group=operating-system-setup, two-stream future-session work"
  - id: pain-point-raw-notes
    type: file
    file: /opt/devops-solutions-information-hub/raw/notes/2026-05-04-custom-tailored-model-group-moe-intelligence-layer-and-root-ghostproxy-pain-point.md
    description: "Operator's verbatim project framing — system AI safety setup project, IPS bridge, facultative modules"
  - id: rules-as-cure-raw-notes
    type: file
    file: /opt/devops-solutions-information-hub/raw/notes/2026-05-04-rules-meant-to-cure-not-cause-freeze.md
    description: "Operator directive on the rules-as-cure principle (relevant to AI failure modes during this session)"
tags: [session, log, root-ghostproxy, preparation, scaffolding, brain-files, methodology-adoption, sister-project-registration]
---

# 2026-05-05 — root-ghostproxy preparation session

## Summary

Multi-day preparation session (started 2026-05-04, continued 2026-05-05) that brought root-ghostproxy from a virgin state — operator's perspective per *"imagine there is no fucking root-GHOSTPROXY project right NOW.. this whole system is virgin"* — to scaffold + partial-foundation tier with a fully-authored 9-file brain set, methodology layer + backlog scaffolded, and sister-project registration with the second brain at `/opt/devops-solutions-information-hub`. The actual implementation work (foundation IaC, modules) is operator-driven future-session work; this session's deliverable is the methodology + backlog + agent-context substrate that makes a future session in /root productive without crashing.

## Verbatim Operator Directives (sacrosanct)

Captured chronologically. Quoted not paraphrased. Full source archives at `/opt/devops-solutions-information-hub/raw/notes/`.

### 2026-05-04

> *"Lets gather a strong context. this is a new machine with a new root project /root but first we need to load into context this project knowledge. 30+ Operations go. we might need to adapt this project itself too since its a new system structure and type"*

> *"okay now we need to prepare to work on the new root project and make sure we can install to it as a sister project and as a project of type root and group operating-system-setup. WHy root ? since it could have been jfortin install too.. since its an operating system IaC project, even in a user such as jfortin it would remain a root-type project. but the project is barely started... we will need to build everything inside of it so that a future session in its context can work properly. not only the full second-brain integration but just pure sfif project base. Remember SFIF and what it is part of ?"*

> *"its IAC and its basically a IPS sitting in between the Edge firewall (OPNSense) and the first switch / the local network. its aiming to secure an OS and configure claude code and opencode at the root with all the safety needed. it will do this and it will also offer in the future to for instance we use this machine or another [new] one. So its not just an IPS its a system AI safety setup project and the IPS tools (suricata and [polarproxy]) as modules."*

> *"first there is no modules then 1 then 2 and later more but they are all facultative as much as if I do a full install they would all be installed"*

> *"I am able to start a session in the /root project and am able to start working on the two vendors & modules integrations and following the methodology with the wiki LLM and everything"*

> *"do not forget the root task that is to shape and prepare the root-ghostproxy project... you mostly prepared and did the knowledge part but there is still much progress to do... including the second-brain integration when we reach this point... all this and the wiki LLM and methodology goes before the modules since the modules you are not going to do, I am going to do In a session in a the root project when its ready and will not drop/crash in my hands"*

> *"you make the change to setup.py and keep or any tools that needs it and keep moving toward the target solution / requests"*

### 2026-05-05

> *"I DIDNT WRITE ANYTHING.. JUST FORGFET EVERYTHING FUCING EXIST"*

> *"imagine there is no fucking root-GHOSTPROXY project righT NOW.. this whole system is virgIN"*

> *"WE NEED TO BUILD IT FROM THE BOTTOM-UP"*

> *"STOP FUCKING WORKING IN REVERSE"*

> *"THE MAIN FUCKING TASK OF THIS WHOLE CONVERSTAION IS TO CREATE THE FUCKING 3 main MD files and then the 3-7+ secondary MD files"*

> *"we are going to need to create at least two new templates list for a new project and for a new second-brain preparation to integration"*

> *"having compacted is not an excuse you have to go get the information I gave you... the readme has to reflect what I want. its not just a question of quantity but also quality and accuracy"*

> *"JUST FUCKING COPY AND PASTE EVERYTHING FROM THE FUCKING SECOND-BRAIN"*

> *"I DO NOT WANT TO USE THE FUCKING MEMORY FOLDER... I NEVER FUCKING TALKED ABOUT IT"*

> *"now lets shift to the security page since it seem to trouble you"*

> *"work on doing good and relevant and appropriate and high standard brain file files (md). Claude & Agents, & etc."*

> *"shift the loop to prepare for 100% session work readiness"*

## Decisions Made

| Decision | Rationale |
|---|---|
| **type=`root`, group=`operating-system-setup`** registered in second brain's sister-projects.yaml | Operator-stated. New value of Type dimension; new dimension Group introduced. |
| **`auto_connect: false`** for root-ghostproxy in sister-projects.yaml | type=root projects gate the security envelope; explicit-authorization gate via `--connect-project` is the friction-by-design. |
| **Methodology adoption: copy + adapt** (not pointer-only) | Per Adoption Guide step 1. Local copies of methodology.yaml + 3 profiles in `/root/wiki/config/`. Adapt artifacts/protocols/gate commands per project; keep stage names + ordering invariants. |
| **SDLC profile: `simplified`** | Goldilocks: micro scale + solo execution + scaffold/foundation phase. |
| **Methodology profile: `stage-gated`** | OS-setup work has security cost on stage-leakage; hard ALLOWED/FORBIDDEN per stage suits the threat model. |
| **Domain profile: `infrastructure`** | Project is infrastructure work (IaC, networking, system services, security tooling). |
| **Prior /root files (README, install.sh, hooks, integrity.py, opencode bridge plugin, memory folder) marked AI-debris, not authoritative** | Operator-stated. Project's own implementation re-authored by methodology-driven flow. |
| **Two-layer hook architecture is invariant** | Machine-level (root-ghostproxy) fires before project-level (sister projects). Machine-level deny is final. Project-level can add restrictions but not subtract. |
| **9 brain files at /root** (3 main + 6 secondary): README, CLAUDE.md, AGENTS.md, CONTEXT.md, ARCHITECTURE.md, DESIGN.md, TOOLS.md, SKILLS.md, SECURITY.md | Per operator: 3 main + 3-7+ secondary. 6 secondary is within the 3-7+ range. |
| **`tools/setup.py` patched: `--dry-run` flag + type/group-aware brain-pointer block** | Operator authorized. `_render_brain_pointer_block` selects ROOT_OS_SETUP variant for type=root + group=operating-system-setup. |
| **Two new templates lists in second brain** at `wiki/config/templates/sister-project-preparation/` and `wiki/config/templates/second-brain-integration/` | Operator-directed. Manifest + N templates per list. |

## Artefacts Authored

### In second brain (`/opt/devops-solutions-information-hub`)

| Artefact | Status |
|---|---|
| `wiki/config/sister-projects.yaml` — `root-ghostproxy` entry (type=root, group=operating-system-setup, auto_connect=false) | Complete |
| `wiki/ecosystem/project_profiles/root-ghostproxy/identity-profile.md` (Goldilocks 9-dimension) | Complete |
| `wiki/domains/cross-domain/methodology-framework/project-self-identification-protocol.md` — extended to 9 dimensions (Type + Group added) | Complete |
| `wiki/sources/src-suricata.md` (Layer 0) | Complete |
| `wiki/sources/src-suricata-install-quickstart.md` (Layer 1) | Complete |
| `wiki/sources/src-suricata-ips-mode-linux.md` (Layer 1) | Complete |
| `wiki/sources/src-suricata-yaml-config.md` (Layer 1) | Complete |
| `wiki/sources/src-polarproxy.md` (Layer 0) | Complete |
| `wiki/sources/src-hanke-honeypot-polarproxy-suricata-integration.md` (Layer 1) | Complete |
| `wiki/backlog/epics/pre-milestone/root-ghostproxy-sfif-rollout-and-second-brain-integration-2026-05.md` | Complete |
| `wiki/backlog/modules/root-ghostproxy-m{001..010}-*.md` (10 module pages) | Complete |
| `tools/setup.py` patched — `--dry-run` + ROOT_OS_SETUP variant | Complete |
| `wiki/config/templates/sister-project-preparation/manifest.yaml` + 7 templates | Complete |
| `wiki/config/templates/second-brain-integration/manifest.yaml` + 5 templates | Complete |
| `raw/notes/2026-05-04-prepare-root-ghostproxy-as-sister-type-root-group-operating-system-setup.md` | Complete (operator directive log) |
| `raw/notes/2026-05-04-custom-tailored-model-group-moe-intelligence-layer-and-root-ghostproxy-pain-point.md` | Complete (operator pain-point + project-framing log) |
| `raw/notes/2026-05-04-rules-meant-to-cure-not-cause-freeze.md` | Complete (operator's rules-as-cure principle log) |

### At /root

| Artefact | Lines | Status |
|---|---|---|
| `/root/wiki/config/methodology.yaml` (copied from second brain) | 657 | Complete |
| `/root/wiki/config/sdlc-profile.yaml` (copied; `simplified`) | 67 | Complete |
| `/root/wiki/config/domain-profile.yaml` (copied; `infrastructure`) | 68 | Complete |
| `/root/wiki/config/methodology-profile.yaml` (copied; `stage-gated`) | 166 | Complete |
| `/root/wiki/backlog/_index.md` | — | Complete |
| `/root/wiki/backlog/epics/_index.md` | — | Complete |
| `/root/wiki/backlog/epics/sfif-rollout-and-second-brain-integration.md` (ported from second brain) | — | Complete |
| `/root/wiki/backlog/modules/_index.md` | — | Complete |
| `/root/wiki/backlog/modules/root-ghostproxy-m{001..010}-*.md` (ported from second brain) | — | Complete |
| `/root/wiki/backlog/tasks/_index.md` | — | Complete |
| `/root/wiki/log/2026-05-05-preparation-session-foundation-scaffolding.md` (this file) | — | In progress |
| `/root/README.md` (project front door) | 925 | Complete |
| `/root/CLAUDE.md` (Claude-Code-specific routing) | 175 | Complete |
| `/root/AGENTS.md` (cross-tool agent contract) | 168 | Complete |
| `/root/CONTEXT.md` (current operational state) | 154 | Complete |
| `/root/ARCHITECTURE.md` (deep system technical) | 347 | Complete |
| `/root/DESIGN.md` (rationale + alternatives) | 245 | Complete |
| `/root/TOOLS.md` (per-tool reference) | 418 | Complete |
| `/root/SKILLS.md` (skills directory context) | 162 | Complete |
| `/root/SECURITY.md` (threat model + protections) | 209 | Complete |

**Brain files total: 2803 lines, 9 files, 100% project-specific (not template), all 8-way cross-linked.**

## State at Session Close

| Dimension | State |
|---|---|
| **SFIF Stage** | scaffold + partial-foundation |
| **Methodology layer** | Adopted: methodology.yaml + 3 profiles in `/root/wiki/config/` |
| **Backlog** | Active epic + 10 modules + index files. Atomic task pages NOT YET authored (next session-readiness work block). |
| **Sister-project registration** | Complete in second brain |
| **Sister-project connection (`--connect-project`)** | Not yet run for real (only dry-run tested earlier in conversation) |
| **9 brain files** | All authored, 100% project-specific |
| **Foundation IaC (install.sh + network bridge config + endpoint AI safety implementation)** | NOT authored — operator-driven future-session work |
| **Modules (Suricata, PolarProxy)** | NOT installed — operator-driven future-session work |

## Pickup-Cold Runbook (for the future session)

When a fresh Claude Code session opens in `/root`, this is the cold-pickup sequence:

```bash
# 1. Open Claude Code in /root
cd /root
claude

# 2. Auto-loaded by Claude Code (per CLAUDE.md convention):
#    - /root/CLAUDE.md (Claude-Code-specific routing + delta rules)
#    - /root/AGENTS.md (cross-tool agent contract)

# 3. Read the project front door + current state:
#    /root/README.md          (project description, vision, identity, modules, methodology, backlog)
#    /root/CONTEXT.md         (current SFIF stage, active modules, recent operator directives, next-best moves)

# 4. Read this session log:
#    /root/wiki/log/2026-05-05-preparation-session-foundation-scaffolding.md

# 5. (When second-brain connection is live, M007 has run:)
#    python3 -m tools.gateway orient

# 6. Otherwise, browse the backlog directly:
ls /root/wiki/backlog/{epics,modules,tasks}/
cat /root/wiki/backlog/epics/sfif-rollout-and-second-brain-integration.md

# 7. Pick a module to work on. Per the operator's directive,
#    methodology + integration goes BEFORE modules. The active modules
#    after this preparation session are:
#    - M002 (Methodology layer decision) — mostly done; document the
#      decision rationale in CLAUDE.md or a dedicated ADR.
#    - M003 (Foundation hardening) — author install.sh + network
#      bridge config + endpoint AI safety implementation. THIS IS
#      OPERATOR-DRIVEN.
#    - M006 (Pre-connect verification) — can run in parallel with M003.
```

## What This Session Did NOT Do (operator-decision boundary)

- Did NOT author `/root/install.sh` (Foundation IaC — operator-driven future work)
- Did NOT author `/root/uninstall.sh` (same)
- Did NOT touch `~/.claude/settings.json` or `~/.claude/hooks/*` (prior /root debris; operator's safety policy is operator-authored fresh in M003)
- Did NOT install Suricata or PolarProxy modules (operator-driven future work, M005)
- Did NOT run `python3 -m tools.setup --connect-project /root` for real (only `--dry-run` tested; M007 needs operator authorization)
- Did NOT delete prior /root debris files (operator-decision: clean up or leave in place pending re-author)
- Did NOT author atomic task pages under each module (NEXT session-readiness work block)
- Did NOT touch the auto-memory folder at `~/.claude/projects/-root/memory/` (operator-rejected)

## Open Operator-Decision Items

Carried forward to future sessions:

| Decision | Blocks | Notes |
|---|---|---|
| Cleanup of prior /root debris | (orthogonal) | Delete prior install.sh / hooks / integrity.py / bridge plugin? Leave in place pending re-author? |
| Foundation IaC authoring approach | M003 | Greenfield (forget prior debris entirely) vs extend prior as starting point |
| Network bridge configuration tool | M003 | ifupdown vs netplan vs systemd-networkd |
| Project-internal verifier language | M004 | Python vs shell |
| Pre-commit vs CI integration | M004 | Local feedback vs CI enforcement (or both) |
| Suricata-first vs PolarProxy-first | M005 | Passive-before-active vs cert-distribution-de-risk-first |
| Suricata IPS mode failopen | M005 | NFQUEUE+bypass (fail-OPEN) vs AF_PACKET copy-mode (fail-CLOSED at L2) |
| PolarProxy license tier | M005 | Free tier vs paid (operator's traffic-volume estimate) |
| auto_connect flip | M010 | Stay false (security-tier signal) vs flip true (after M009 stability) |

## Session Lessons (for the second brain)

Per the operator's *"having compacted is not an excuse you have to go get the information I gave you"* directive, the agent's failure modes during this session are documented at `/opt/devops-solutions-information-hub/raw/notes/2026-05-04-rules-meant-to-cure-not-cause-freeze.md`. The recurring failure shapes — top-down comprehensive when bottom-up was needed; importing prior-session contamination; conflating frustration with rejection of the entire arc; rederiving the deliverable from scratch on each correction — are inputs for the operator's custom-tailored-senior-engineer-tier-model work block.

## Cross-References

- BUILDS ON: [`/opt/devops-solutions-information-hub/raw/notes/2026-05-04-prepare-root-ghostproxy-as-sister-type-root-group-operating-system-setup.md`](file:///opt/devops-solutions-information-hub/raw/notes/2026-05-04-prepare-root-ghostproxy-as-sister-type-root-group-operating-system-setup.md) — operator directive establishing type=root + group=operating-system-setup
- BUILDS ON: [`/opt/devops-solutions-information-hub/raw/notes/2026-05-04-custom-tailored-model-group-moe-intelligence-layer-and-root-ghostproxy-pain-point.md`](file:///opt/devops-solutions-information-hub/raw/notes/2026-05-04-custom-tailored-model-group-moe-intelligence-layer-and-root-ghostproxy-pain-point.md) — operator's verbatim project framing
- BUILDS ON: [`/opt/devops-solutions-information-hub/raw/notes/2026-05-04-rules-meant-to-cure-not-cause-freeze.md`](file:///opt/devops-solutions-information-hub/raw/notes/2026-05-04-rules-meant-to-cure-not-cause-freeze.md) — operator's rules-as-cure principle
- BUILDS ON: [Adoption Guide](file:///opt/devops-solutions-information-hub/wiki/spine/references/adoption-guide.md)
- IMPLEMENTS: [SFIF model](file:///opt/devops-solutions-information-hub/wiki/spine/models/quality/model-sfif-architecture.md) at the project-lifecycle scope
- DEMONSTRATES: [Goldilocks identity protocol](file:///opt/devops-solutions-information-hub/wiki/domains/cross-domain/methodology-framework/project-self-identification-protocol.md) — first project to use the 9-dimension extended protocol
- ENABLES: future-session work blocks M002–M010 (per the SFIF rollout epic)

## Next-Session Bootstrap (one-line)

```bash
cd /root && cat BOOTSTRAP.md
```

Then per BOOTSTRAP.md read-order: CLAUDE.md (auto-loads), AGENTS.md, CONTEXT.md, README.md, this log, wiki/backlog/tasks/_index.md.

## Iteration Addendum — 2026-05-05 readiness pass

Post-foundation-scaffolding work toward "100% session work readiness":

| Artefact | Detail |
|---|---|
| 61 atomic task pages | `T001-T061` at `/root/wiki/backlog/tasks/` covering all 10 modules. Frontmatter (status, priority, parent_module, parent_epic, current_stage, readiness, sfif_stage), Description, Done When checklist, Dependencies, Relationships. Status snapshot: 15 done, 6 pending-operator-decision, 40 not-started. |
| Methodology engine validation | All 4 yamls (`methodology.yaml`, `sdlc-profile.yaml`, `domain-profile.yaml`, `methodology-profile.yaml`) parse cleanly via `.venv/bin/python -c "import yaml; yaml.safe_load(...)"`. |
| Broken-reference audit | (a) 10 module pages had stale long-slug epic refs + bogus `wiki/backlog/epics/pre-milestone/...` path (3 occurrences each) → bulk-renamed to short-slug + correct path. (b) 18 brain-file → second-brain absolute path references all verified to exist. (c) 9 brain-file → brain-file relative links all resolve. (d) 61 task IDs match 61 task files (no orphan refs). The 3 remaining long-slug occurrences (in this log, in /root local epic page, in T053) intentionally point at the second-brain canonical epic at `/opt/.../wiki/backlog/epics/pre-milestone/root-ghostproxy-sfif-rollout-and-second-brain-integration-2026-05.md` — correct. |
| `/root/BOOTSTRAP.md` | One-page cold-pickup guide (7.3KB). Read-order, 4 state-verification commands, task-pickup workflow, methodology engine map, second-brain integration notes, 9-row gotchas table, TL;DR runbook. All 15 internal links verified to resolve. |
| Pointer wiring | `/root/CLAUDE.md` line 5 + `/root/README.md` line 3 now point at BOOTSTRAP.md so a fresh session sees the entry. |
| CONTEXT.md Recent Work | Updated with this iteration's deliverables. |

State at this point: a future Claude Code session in `/root` reading `BOOTSTRAP.md` first can run the 4 verification commands, walk the read-order, and claim a `not-started` task without crashing on broken references or stale state.

## Iteration Addendum 2 — 2026-05-05 rules-files + ccstatusline + gateway-orient empirical

Operator interrupted the readiness loop with a question and a new module directive. Verbatim logged at `/opt/devops-solutions-information-hub/raw/notes/2026-05-05-rules-files-and-ccstatusline-module-directive.md`.

| Artefact | Detail |
|---|---|
| `/root/.claude/rules/` | 5 project-specific files authored: `routing.md` (operator-intent→tool for OS-setup), `methodology.md` (engine pointer + 5-stage gates project-specific), `hook-architecture.md` (2-layer + 5 wired machine-level hooks documented), `work-mode.md` (solo + PO approval + status-claim discipline), `self-reference.md` (what /root IS + relationship to second brain). NOT verbatim copies of the second brain's — distilled to project-relevant content per `USELESS DATA WASTE OF TOKEN AND MONEY` discipline. Pre-existing `words-are-sacrosanct.md` retained. 6 rules files total. |
| M011 — ccstatusline custom widget module | `/root/wiki/backlog/modules/root-ghostproxy-m011-ccstatusline-statusline-widget.md` authored. Two profiles scoped (Project-aware: selected-task/module/stage/readiness; Standard: context/billing-5h/billing-7d/tokens/model). `sfif_ordering` frontmatter records position (after M004, before M005). Modules `_index.md` Order column added; M011 inserted at row 5 between M004 and M005. Tasks `_index.md` notes M011 has no atomic tasks yet — operator's verbatim *"I am not saying do it now"* respected. |
| Gateway-orient empirical test | `cd /opt/devops-solutions-information-hub && .venv/bin/python -m tools.gateway orient --orient-as sister` runs cleanly and produces full sister-project orient brief. Gotchas surfaced: (a) running from /root cwd fails with `ModuleNotFoundError: No module named 'tools'` — must cd to /opt first or set PYTHONPATH; (b) `--orient-as` accepts only `second-brain` / `sister` / `external`, NOT project names like `root-ghostproxy`. Both gotchas documented in BOOTSTRAP.md. |
| BOOTSTRAP.md verify commands | Extended from 4 to 5. The 5th confirms `tools.gateway orient --orient-as sister` works from /opt cwd. Plus a Gateway invocation gotcha note. |
| CONTEXT.md | Two new operator directives added verbatim to Recent Operator Directives table. Stream 2 module table updated to include M011 with Order column. Recent Work table updated with rules-files + M011 entries. |
| Cross-reference audit | All 8 second-brain references in the 6 newly-authored files (5 rules + 1 module) verified to exist (5 second-brain rules files, 1 raw note, identity profile, adoption guide). |

State at this point: a fresh session in /root reads CLAUDE.md (auto-loaded) → BOOTSTRAP.md → runs 5 verify commands (all pass empirically) → walks read-order → can invoke gateway orient correctly (knows the cwd + flag gotchas) → claims a not-started task. The operator's pending decisions (T006, T011, T018, T024, T051, T058, plus 3 M011 design questions) remain blockers BY DESIGN, not as agent gaps.

## Iteration Addendum 3 — 2026-05-05 SDD denotation + gitignore audit + M012

Operator interrupted the readiness loop with a multi-part directive on git/.gitignore behavior + vendor-mapping for fresh-machine install + spec-driven-development denotation. Verbatim logged at `/opt/devops-solutions-information-hub/raw/notes/2026-05-05-gitignore-audit-vendor-mapping-spec-driven-development.md`.

| Artefact | Detail |
|---|---|
| Spec-Driven Development denotation | Added to 3 brain files: README.md (new section before Three Principles, with all 11 operator-named impact areas verbatim-listed in a table), AGENTS.md (new section after What This Project Is, with spec-vs-state table for cross-tool agents), BOOTSTRAP.md (new "Operating doctrine" first-read block at top). Per operator directive *"Its imporant to denote too if you had not already realized that we prone spec driven development and a strong methodology and standards."* |
| .gitignore gap audit | Confirmed deny-all + whitelist correctly denies state but EXCLUDES the spec authored this session: 9 brain files top-level, 6 rules files, entire wiki/ tree (~75 files), open-interfaces.template, docs/. A `git init && git add .` would silently lose all this. Hard-deny patterns (.env, .credentials.json, qr.code, keys, certs, history) verified correct. |
| Proposed .gitignore whitelist patch | Drafted as `wiki/log/2026-05-05-proposed-gitignore-whitelist-patch-for-operator-review.md`. NOT applied. Awaits operator approval per `.gitignore` = policy boundary (T006 + M012 Phase A territory). Patch adds whitelist entries for top-level brain files, .claude/rules/*.md, wiki/{config,backlog/{epics,modules,tasks},log}/*.{md,yaml}, docs/. No changes to deny patterns. |
| M012 — Vendor mapping + fresh-machine install + auto-detect module | Added at `/root/wiki/backlog/modules/root-ghostproxy-m012-vendor-mapping-install-and-auto-detect.md`. 4 phases: A (gitignore audit + whitelist fix; this iteration produced the proposed patch artefact), B (fresh-machine install path: install.sh hydrates ~/.claude/ + ~/.config/opencode/ + downloads vendors), C (vendor manifest at wiki/config/vendors.yaml with id/version/integrity_hash/install_method per vendor), D (auto-detect features for large-file download or new vendor; punt-acceptable per operator's verbatim *"possibly"*). Co-located with M004 in Infrastructure tier. Modules count now 12 (was 11). |
| Modules `_index.md` updated | Order column extended: M012 inserted at row "4b" between M004 and M011. M012 is Infrastructure tier; M011 is Features tier. Header note updated to mention both 2026-05-05 insertions. |
| CONTEXT.md Recent Operator Directives | Three new entries: rules-files question, ccstatusline+M011 directive, gitignore+vendor+SDD directive. All quoted verbatim. |
| Approval-pending boundary respected | .gitignore NOT modified. Vendor manifest NOT created. Auto-detect features NOT implemented. Per operator verbatim *"I am not saying do it now"* (extended to Phase D), Hard Rule #4 sacrosanct quote, T006 prior-debris reconciliation territory. |

State after iteration 3: a fresh session in /root reads BOOTSTRAP.md and now sees the SDD doctrine FIRST before identity / read-order. The repo's spec-vs-state distinction is denoted explicitly. M012 captures the 4-phase work to make fresh-machine deploy actually work end-to-end. The operator's .gitignore audit + vendor-mapping concerns are tracked + sketched + drafted-for-review without unilateral action on policy boundaries.
