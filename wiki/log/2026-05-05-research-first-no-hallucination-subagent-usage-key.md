---
title: "2026-05-05 — Operator directive: research-first / no-hallucination / sub-agent usage + instructions are KEY"
type: note
domain: cross-domain
status: raw
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-research-first-no-hallucination
    type: directive
tags: [note, operator-directive, sacrosanct, verbatim, research-first, no-hallucination, no-outdated-data, subagent-usage, online-research, local-research, expert-discipline]
---

# Operator directive — 2026-05-05 research-first + no-hallucination + sub-agent usage

## Verbatim

> "oh one things seem to not have been clear but we work like real expert and we do our online and local research properly... especialy for cases like when we need a sub-agent or a strong session about doing a really strong research when needed naturally not to fill the specs and the docs with hallucinated or random data or outdated data... again another input, and yet really important... research and sub-agent usage and instructions is keys"

## Decomposition

### A — Operating standard: real expert
- "we work like real expert"
- Discipline level set: senior practitioner, not novice.

### B — Online + local research, both
- "we do our online and local research properly"
- Sources of truth: BOTH external (online) AND internal (project + second brain)
- "Properly" implies: cite-able, verifiable, not assumption-based.

### C — When sub-agent / strong-research session is needed
- "especialy for cases like when we need a sub-agent or a strong session about doing a really strong research when needed naturally"
- Sub-agent dispatch is a NATURAL move when the question warrants depth.
- Sub-agents available in /root: `general-purpose`, `Explore`, `Plan`, `claude-code-guide`, `statusline-setup`.

### D — No hallucination / no random data / no outdated data
- "not to fill the specs and the docs with hallucinated or random data or outdated data"
- THREE forbidden: hallucinated / random / outdated
- Specs + docs = the artefacts we author. Each fact in them must trace to a source.

### E — Research + sub-agent usage + instructions is KEY
- "research and sub-agent usage and instructions is keys"
- Three pillars: (1) research, (2) sub-agent usage, (3) instructions for sub-agents.
- All three must be solid. Especially the INSTRUCTIONS we give sub-agents (sub-agent quality = instruction quality).

## Action plan (integrate with active iteration)

1. Log this directive verbatim — done (this file).
2. Add F-eval-10 to iteration log: research-first requirement applied to ALL upcoming spec/doc authoring.
3. **Update F-eval-6 (M011 preliminary task pages)**: REQUIRE research-first. Before authoring T-M011-* task pages with widget names / vendor details / config schema, dispatch an Explore-agent or general-purpose agent to research:
   - The ccstatusline project (github vendor, latest release, config schema, available widgets, profile mechanism)
   - Claude Code statusline integration mechanism (how the harness consumes the statusline)
   - Existing custom widget patterns (community examples)
   No widget names / config keys / API surfaces in the task pages without source citation.
4. **Update F-eval-7 (M014 luckyPipewrench/pipelock module)**: HARD-GATED on operator-clarification. Pipelock content is unknown to me. Cannot scope without:
   - Operator-supplied context, OR
   - Authorized github research (WebFetch, but ONLY if operator specifies the URL — not URL-fabrication)
5. **Establish iteration discipline**: every spec/doc artefact authored under this iteration loop carries a source-trace. If a fact has no source, mark it `?` or `[needs-research]`.
6. **Sub-agent instruction quality**: when dispatching sub-agents, follow the prompt-discipline guidance in the Agent tool description — self-contained prompts, explicit goals, files/lines, no "based on X figure it out" punts.

## Forbidden actions (explicit, sacrosanct boundary)

| Forbidden | Why |
|---|---|
| Authoring widget names / config schema for ccstatusline from base-model knowledge | Source-required; potentially outdated |
| Authoring pipelock specs based on guess | Hallucination risk; operator hasn't named it |
| Authoring vendor manifests without WebFetch + operator-approved URL | Source-required; URL-guessing forbidden per CLAUDE.md |
| Filling in "best practice" claims without source | "Random data" pattern |
| Citing pre-2026 patterns as current | Outdated-data pattern |

## No-conflate guard

- "we work like real expert" = OPERATING STANDARD raised, not a one-off. Applies to EVERY spec/doc authoring action under this directive forward.
- "another input" = additive context, not interruption (per the comments-don't-deroute meta-rule from earlier this turn).
- "research and sub-agent usage and instructions is keys" = KEY, meaning critical/load-bearing — not "key" as in "one of many." Treat as top-priority discipline.
- "sub-agent... when needed naturally" = sub-agents are not always needed; the test is whether the depth-of-research warrants them. For ccstatusline / pipelock / new vendor work: yes, warrants. For doc-drift fixes: no, doesn't.
