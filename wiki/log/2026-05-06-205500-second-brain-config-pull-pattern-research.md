---
title: "Second-brain config-pull pattern — research findings (operator pointer 2026-05-06)"
type: log
subtype: research-findings
domain: cross-domain
status: research-complete-pending-operator-direction
created: 2026-05-06
sources:
  - id: operator-directive-2026-05-06-config-pull
    type: directive
    quote: '"we have multiple config from the parent Wiki LLM / second-brain that normally we download into project when not present if not already done and normally those help to do wiring and dynamic setup and empowerer and augment the ecosystem and harness. like openfleet and openarms are doing."'
  - id: second-brain-tools-setup
    type: code
    file: /opt/devops-solutions-information-hub/tools/setup.py
  - id: methodology-adoption-guide
    type: reference
    file: /opt/devops-solutions-information-hub/wiki/spine/references/methodology-adoption-guide.md
tags: [research-findings, config-pull, second-brain, methodology-adoption, augment-pattern]
---

# Second-brain config-pull pattern — research findings

## Operator's pointer

> *"we have multiple config from the parent Wiki LLM / second-brain that normally we download into project when not present if not already done and normally those help to do wiring and dynamic setup and empowerer and augment the ecosystem and harness. like openfleet and openarms are doing. not that I want to deroute you but you might wanna read about that too"*

## What second-brain has vs what root-ghostproxy has

### Already in `/root/wiki/config/` (4 configs — minimal subset, copied per Adoption Guide)

| Config | Purpose |
|---|---|
| `methodology.yaml` | 9 models, 5 stages, ALLOWED/FORBIDDEN per stage |
| `sdlc-profile.yaml` | `simplified` profile (right-sized for solo/micro) |
| `domain-profile.yaml` | `infrastructure` profile |
| `methodology-profile.yaml` | `stage-gated` profile |

### Missing in root, present in second-brain (14 configs)

Located at `/opt/devops-solutions-information-hub/wiki/config/`:

| Config | Description | Augment-value for root-ghostproxy |
|---|---|---|
| `artifact-types.yaml` | Defines every document/artifact type in methodology (concept/reference/source-synthesis/etc.) — categories, thresholds, styling, verification methods | **HIGH** — root's wiki/log/ + wiki/governance/ + wiki/backlog/ all use artifact types implicitly; explicit registry helps validate frontmatter |
| `quality-standards.yaml` | Lint thresholds: min summary words, min deep_analysis words, min_relationships, stale_threshold_days, etc. | **HIGH** — root has rich wiki/log/ + governance/; lint thresholds enable automated quality checks (links to F-future linter task) |
| `wiki-schema.yaml` | Schema for wiki-page frontmatter (required fields, enums, required_sections) | **MEDIUM** — root's brain files + log files all have frontmatter; schema enables validate-frontmatter tooling |
| `domains.yaml` | Domain registry (ai-agents / ai-models / infrastructure / devops / security / knowledge-systems / automation / tools-and-platforms) | **MEDIUM** — root maps to `infrastructure` + `automation` + `security`; explicit registry standardizes domain field |
| `domain-profiles/` directory | Per-domain config files | **MEDIUM** — root currently has only `domain-profile.yaml` (singular); the dir form is the canonical pattern |
| `methodology-profiles/` directory | Per-methodology config files | **MEDIUM** — same pattern |
| `sdlc-profiles/` directory | Per-SDLC config files | **MEDIUM** — same pattern |
| `templates/` directory | Templates for new docs | **MEDIUM** — root could use task-page / module-page templates |
| `contribution-policy.yaml` | Contribution rules | **LOW** — second-brain-internal; root contributes via `gateway contribute` after M007 connect |
| `export-profiles.yaml` | Export rules | **LOW** — second-brain-internal export pipeline |
| `mcp-runtime-values.yaml` | MCP runtime values | **LOW** — second-brain-internal MCP server config |
| `provider-pricing-cache.json` | Provider pricing cache | **LOW** — second-brain-internal pricing data |
| `sister-projects.yaml` | Sister project registry | **N/A** — root is a sister; second-brain is the registry-owner |
| `README.md` | Config dir docs | **LOW** — second-brain-internal docs |

## The pull mechanism (canonical)

### `tools/setup.py --connect-project <path>` (from second-brain)

Per `/opt/devops-solutions-information-hub/tools/setup.py:430-435`:

> Usage from any sister project:
>     python3 <second-brain>/tools/setup.py --connect
> Or from the second brain itself targeting a sister:
>     python3 -m tools.setup --connect-project ~/openarms

This is the existing connection wiring (writes `.mcp.json` + sister-projects.yaml entry). It does NOT currently copy methodology configs — those are operator-curated per Adoption Guide.

### Adoption Guide (canonical config-adoption process)

`/opt/devops-solutions-information-hub/wiki/spine/references/methodology-adoption-guide.md` documents the 4-tier adoption:

1. Tier 1 (read) — read second-brain's wiki models, no local config
2. Tier 2 (configure) — copy methodology.yaml + profile yamls into project
3. Tier 3 (validate) — add frontmatter validators using wiki-schema.yaml
4. Tier 4 (enforce) — full infrastructure enforcement (linters, pre-commit hooks)

Root-ghostproxy is at **Tier 2** (the 4 configs already copied). Pulling artifact-types.yaml + quality-standards.yaml + wiki-schema.yaml would advance to **Tier 3**.

## Operator's "openfleet and openarms are doing" pattern

Both sister projects implement Tier 2+ adoption:
- `~/openarms` — auto_connect=true in sister-projects.yaml; full setup connects
- `~/openfleet` — referenced in second-brain's E016 integration-chain proof epic

Need empirical investigation of what configs they each pull. Forward-anchor: examining `~/openarms/wiki/config/` (if accessible) would show exactly what they sync.

## Decision-package for operator (not a question; recommendation set)

Per Q-self-elevation pattern (4-gate pre-check): this is NOT pending a Q because operator explicitly named the action ("you might wanna read about that too"). Recommendation set with defaults:

### High-value pull candidates (root-ghostproxy applicable)

1. **artifact-types.yaml** — adds frontmatter `type:` validation; root's logs/governance/backlog already use these types implicitly; making explicit enables linter
2. **quality-standards.yaml** — page-quality thresholds; useful for future linter task
3. **wiki-schema.yaml** — frontmatter schema; complements artifact-types

Default: pull these 3 into `/root/wiki/config/` as augment.

### Medium-value (consider per current scope)

4. **domains.yaml** — domain registry; root maps to known domains
5. **templates/** directory — page templates; useful for new tasks/modules

Default: pull these 2 if Tier-3 adoption desired.

### Low-value / skip

- contribution-policy.yaml / export-profiles.yaml / mcp-runtime-values.yaml / provider-pricing-cache.json / sister-projects.yaml / README.md — second-brain-internal; not project-applicable

## Suggested next action (agent-DRAFT)

Pull the 3 high-value configs as a chain (per SB-131 chain-batch pattern + the new chain primitive Q1 Layer A — could use `chain()` to do this!):

```
chain(
  copy_config("artifact-types.yaml"),
  copy_config("quality-standards.yaml"),
  copy_config("wiki-schema.yaml"),
  update_progress_md_callout,
  log_decision_D041,
)
```

Each step is idempotent. Can re-run safely. Per "if not present already done" — copy only if local doesn't exist.

## Cross-references

- Q1 Layer A primitive (just landed): `tools/group.py` — could be used for the pull operation itself!
- Adoption Guide: `/opt/devops-solutions-information-hub/wiki/spine/references/methodology-adoption-guide.md`
- Existing root configs: `/root/wiki/config/`
- Setup tool: `/opt/devops-solutions-information-hub/tools/setup.py`
- Sister-projects registry: `/opt/devops-solutions-information-hub/wiki/config/sister-projects.yaml`
