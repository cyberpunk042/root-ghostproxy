---
title: "2026-05-05 — Operator directive: first real Epics will be ccstatusline + custom profiles + possibly luckyPipewrench/pipelock scaffolding (PRELIMINARY ONLY — not development)"
type: note
domain: cross-domain
status: raw
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-first-real-epics-preliminary-only
    type: directive
tags: [note, operator-directive, sacrosanct, verbatim, ccstatusline, m011, luckypipewrench, pipelock, github, preliminary-only, no-development, informed-decision, comments-not-deroute]
---

# Operator directive — 2026-05-05 first real Epics + comments-don't-deroute meta

## Verbatim

> "it should be implyed in case like this that when I add a comment like I am doing right now its not to deroute you. but I wanted to add that the first real task or Epics were gonna be the ccstatusline and custom profiles and even possibly the skaffolding of the luckyPipewrench/pipelock on github and yeah this time I specificaly ask not for development but only for doing the preliminary part so we can better discuss it and make informed decision and do the proper integration."

## Decomposition

### A — Comments-don't-deroute (META rule, IMPLICIT)
- "it should be implyed in case like this that when I add a comment like I am doing right now its not to deroute you"
- The agent SHOULD assume operator's mid-flight comments are CONTEXT-ADDITIVE, not interruptions.
- Continue current iteration; integrate the comment.

### B — First real Epics named (forward planning)
- "the first real task or Epics were gonna be"
  1. **ccstatusline + custom profiles** (this is M011 — already on backlog, deferred-pending-go-ahead)
  2. **possibly the skaffolding of the luckyPipewrench/pipelock on github** (NEW — not yet on backlog)

### C — Scoped to PRELIMINARY only (CRITICAL)
- "I specifically ask not for development but only for doing the preliminary part"
- Forbidden: development, implementation, feature work
- Allowed: scoping, defining, module-page authoring, decision surfacing, source-research, design framing

### D — Goal: better discussion + informed decision + proper integration
- "so we can better discuss it and make informed decision and do the proper integration"
- The preliminary work GENERATES material for operator-discussion → operator-decision → integration-when-ready.

### E — luckyPipewrench/pipelock specifics
- A github project ("luckyPipewrench/pipelock"). Likely operator's own.
- Agent does NOT know this project's content. Preliminary work must avoid fabrication: research first (via second-brain `pipeline fetch` / `wiki_fetch` MCP after M007 lands, OR operator-supplied context), THEN scope.
- Until then: register the gap, surface a decision request (operator clarification needed on pipelock's purpose + scope + integration shape).

## Action plan (integrate with active iteration loop)

1. Log this directive verbatim — done (this file).
2. Add backlog task pages for M011 PRELIMINARY work:
   - T-M011-1: scope ccstatusline widget set (selected-task / progress / stage / context / billing-5h / billing-7d / tokens)
   - T-M011-2: scope custom profile mechanism (which profiles, profile-switching UX)
   - T-M011-3: identify ccstatusline project (vendor) + integration approach
   - T-M011-4: surface pre-implementation decisions for operator
   (NOTE: NO dev. Authoring task pages = scaffolding-stage allowed artefact.)
3. Add a NEW module M014 — luckyPipewrench/pipelock preliminary scaffolding:
   - Module page at /root/wiki/backlog/modules/root-ghostproxy-m014-luckypipewrench-pipelock-preliminary-scaffolding.md
   - Frontmatter: `status: pending-clarification`, `current_stage: document`
   - Atomic tasks: clarify with operator (what is pipelock + relationship to root + integration shape) → research via second-brain → scope → surface decisions
4. Update modules `_index.md` to register M014.
5. Continue dual-mode iteration loop — these directives extend (not replace) the self-eval/self-test/self-improve workstream.

## No-conflate guard

- "first real task or Epics were gonna be" = forward-planning intent, NOT a directive to start implementation now ("this time I specifically ask not for development").
- "preliminary part" = scoping + decision-surfacing, NOT implementation. Honor the boundary even if temptation grows during cycles.
- "possibly the skaffolding" — the word "possibly" is doing work. Pipelock module is conditional on operator deciding to include it. Author the module page in `pending-clarification` status, NOT `not-started`.
- "for doing the preliminary part" applies to BOTH ccstatusline and pipelock. Don't development-creep on the ccstatusline side just because it's already on the backlog.
- "comments... not to deroute" = don't break flow on operator's clarifications; integrate them. Doesn't mean ignore them — integrate.
