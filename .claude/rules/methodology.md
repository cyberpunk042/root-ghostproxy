# $HOME/.claude/rules/methodology.md — Methodology engine for root-ghostproxy

> Loaded on demand when stage or model selection comes up. CLAUDE.md has the summary; this file is the project-specific delta.

## Engine location

The methodology engine for this project lives at `$HOME/wiki/config/`:

| File | Profile | Why this profile |
|---|---|---|
| `methodology.yaml` | (engine) | 9 models, 5 stages, ALLOWED/FORBIDDEN per stage, gates. Adapt artifacts/protocols/gate commands per project; keep stage names + ordering + readiness ranges + hierarchy invariants. |
| `sdlc-profile.yaml` | `simplified` | Right-sized for micro scale + solo execution. Avoids ceremony. |
| `domain-profile.yaml` | `infrastructure` | Gate-command + path-pattern overrides for IaC work. |
| `methodology-profile.yaml` | `stage-gated` | Hard ALLOWED/FORBIDDEN per stage. Suits OS-setup where leakage carries security cost. |

All four parse cleanly via `.venv/bin/python -c "import yaml; yaml.safe_load(open('<file>'))"`.

## 5 universal stages (this project's gates)

| Stage | Readiness | ALLOWED | FORBIDDEN | Gate command (project-specific) |
|---|---|---|---|---|
| **document** | 0–25% | wiki page, raw notes | code-file, test-file | Page exists with Summary + gaps identified |
| **design** | 25–50% | design-document, ADR, tech-spec | code-file, test-file | Trade-offs documented; spec reviewed |
| **scaffold** | 50–80% | type-definitions, schema, test-stubs, config-files | implementation, real test assertions | install.sh `--dry-run` runs cleanly without performing real changes; backlog page+module+task structure exists |
| **implement** | 80–95% | implementation, integration-wiring | new test files | install.sh runs end-to-end on a sandbox host; lint passes |
| **test** | 95–100% | test-implementation, test-results | new features | Idempotency invariant holds; integration smoke-test passes |

## Methodology models (selection conditions)

For root-ghostproxy specifically:

| task_type | Model | Selected when |
|---|---|---|
| `epic` / `module` | feature-development | Solution not yet known; design required (most M### work) |
| `bug` | bug-fix | Restoring correct behavior; no new architecture |
| `refactor` | refactor | Restructure existing IaC without behavior change |
| (wire existing) | integration | Bridge pattern — e.g., `tools.setup --connect-project` integration |
| project-level | project-lifecycle (SFIF) | Macro: Scaffold → Foundation → Infrastructure → Features. Other models nest. |

## Stage-boundary discipline

**Do not ship implementation in a Document task. Do not ship tests as features.** The profile name `stage-gated` is enforcement, not advisory. Per second brain learning (OpenArms Bug 5: scaffold produced 135 lines of business logic — boundary now hard).

## Cross-references

- Full engine reference: `<second-brain>/.claude/rules/methodology.md` (canonical, second brain).
- Engine: `$HOME/wiki/config/methodology.yaml` (this project's local copy).
- Adoption Guide: `<second-brain>/wiki/spine/references/adoption-guide.md`.
