---
title: "Q1 step-1 — second-brain research findings: chain/group/tree canonical pattern"
type: log
subtype: research-findings
domain: cross-domain
status: research-complete
created: 2026-05-06
sources:
  - id: second-brain-research-pipeline-orchestration
    type: concept
    file: /opt/devops-solutions-information-hub/wiki/domains/automation/research-pipeline-orchestration.md
  - id: operator-clarification-2026-05-06
    type: directive
    file: wiki/log/2026-05-06-185000-srp-retention-and-chain-group-tree-model.md
  - id: operator-original-vision-2026-04-08
    type: directive
    file: /opt/devops-solutions-information-hub/raw/notes/2026-04-08-user-directive-ecosystem-connections.md
tags: [research-findings, second-brain, chain-operations, group-operations, tree-operations, q1-research, e003-multi-group]
---

# Q1 step-1 — Second-brain research findings: chain/group/tree canonical pattern

> Per Q1 resolution path step 1 (research-first per principle #5 elevated). Operator pointer 2026-05-06: *"the second-brain must have knowledge about all this we have other project that do those things to higher levels"*. Confirmed empirically — second-brain has THE canonical reference.

## Canonical reference found

**File**: `/opt/devops-solutions-information-hub/wiki/domains/automation/research-pipeline-orchestration.md`

**Status**: concept · maturity=growing · confidence=medium · 2026-04-08 (predates this session by ~30 days)

**Origin**: operator's own directive 2026-04-08 captured at `raw/notes/2026-04-08-user-directive-ecosystem-connections.md` — *"I should be able to add a list of things to research online and/or local in order to automate my needs, however many pipelines or pipelines options we need. And we need to automate what can be automated and group them and make sequence / chain and group call / trees operations in order to always move toward the targets and offload as much as possible the repetitive task."*

The chain/group/tree taxonomy operator named for root-ghostproxy 2026-05-06 IS the same vision operator stated 2026-04-08 for second-brain pipelines. Same vocabulary. Same architectural intent.

## Three operation modes (canonical taxonomy)

| Mode | How it works | When to use |
|---|---|---|
| **Chain / Sequence** | A → B → C, each step feeds the next | Dependent steps (extract before analyze) |
| **Group / Parallel** | A + B + C simultaneously, results merged | Independent inputs (12 URLs at once) |
| **Tree** | Branch into parallel paths, merge at synthesis | Topic → 3 sources → merge into synthesis |

Maps 1:1 to operator's 2026-05-06 operator-quote: *"chain calls is just a way to create a tree of operations... group call is that we have multiple chain inter-dependant or not"*.

## Five pipeline types from canonical (second-brain context)

For reference (these are second-brain's pipelines — root-ghostproxy will have its OWN pipelines; the TAXONOMY is what transfers, not the specific pipelines):

1. ONLINE RESEARCH: web_search → fetch → save_raw → extract → synthesize → integrate
2. LOCAL INGESTION: scan_project → extract_docs → classify → create_pages → integrate
3. CROSS-REFERENCE: load_manifest → gap_analysis → relationship_discovery → integrate
4. DEEPENING: lint_report → identify_thin → research_gaps → enrich → integrate
5. ECOSYSTEM SYNC: detect_changes → diff → update_or_create → cross_reference → integrate

## Execution modes (canonical)

- **Sequential**: dependent steps (extract must finish before analyze)
- **Parallel**: independent inputs (ingest 12 URLs simultaneously)
- **Tree**: branching research (topic → 3 sources → merge into synthesis)

## What this means for root-ghostproxy E003 multi-group component

Per Q1 step-2 (DRAFT v1 spec for chain/group/tree primitive):

### Borrow the taxonomy

Root-ghostproxy uses the SAME 3-mode taxonomy (chain/group/tree) — same vocabulary as operator's directive + second-brain canonical. No reinvention.

### Root-ghostproxy's pipeline types (DRAFT — agent-proposed, operator-revisable)

Operator's example: *"updating tasks and such where we know that the task should imply than more than just one operation, its a chain"* + *"like passing through the stage of one document for specs"*. Concrete pipelines for THIS project:

| Pipeline | Stages | Mode |
|---|---|---|
| **task-complete-cascade** | mark-done → update-readiness → propagate-to-parent-module → cursor-advance → handoff-snapshot → log | Chain |
| **stage-transition** | verify-allowed → run-gate-check → write-stage-log → update-frontmatter → notify-deps | Chain |
| **sb-closure-batch** | tracker-row-update → decisions-D-append → progress.md-callout-refresh → log-author | Chain |
| **multi-file-coherent-edit** | edit-A + edit-B + edit-C (operator-named ≥2 files) → run-tests → commit | Group (parallel edits) → Chain (verify) |
| **research-then-build** | second-brain-query → spec-draft → operator-review → tool-impl → test-impl | Tree (sources merge) |

### Layer A primitive (`tools/group.py` per Q1 decision)

Following second-brain's pattern, the primitive should expose:

- `chain(steps: list[Callable])` — sequential, each step's return feeds next
- `group(callables: list[Callable])` — parallel, results merged into list
- `tree(root: Callable, branches: dict, merge: Callable)` — root invokes branches in parallel, merge synthesizes
- Logic + dependency surface (operator-stated: *"there can be logic and dependency"*)

Pseudo-shape (DRAFT, agent-proposed):

```python
# tools/group.py — DRAFT
def chain(*steps):
    """Sequential: A → B → C; return last step's result."""
    result = None
    for s in steps:
        result = s(result) if result is not None else s()
    return result

def group(*callables):
    """Parallel: A + B + C; return list of all results (preserving order)."""
    return [c() for c in callables]  # MVP synchronous; could async later

def tree(root, branches, merge):
    """root → branches in parallel → merge synthesizes."""
    seed = root()
    parallel = group(*[lambda b=b: b(seed) for b in branches])
    return merge(parallel)
```

### Risks captured from second-brain pattern

- Maturity=growing (second-brain's own implementation is in progress) — root-ghostproxy can't fully borrow code, but the taxonomy + naming + mental model is stable
- Confidence=medium — operator's directive is clear, but concrete edge cases need empirical validation
- Multi-pass principle: operator-stated *"ingestion is multi-pass, not one-shot"* — root-ghostproxy's chains should ALSO be multi-pass-capable (re-run safe)

## Q1 path status

| Step | Status |
|---|---|
| 1. Query second-brain for sister-project chain/group/tree patterns | ✓ DONE this fire — found canonical at `wiki/domains/automation/research-pipeline-orchestration.md` |
| 2. Author DRAFT v1 spec at `wiki/log/<ts>-chain-group-tree-spec-draft.md` for Layer A primitive | next fire (small follow-on; pseudo-shape above is the seed) |
| 3. Operator review of spec | pending operator |
| 4. Implementation: Layer A primitive first; B + C after | pending operator-greenlight |

## Cross-references

- `/opt/devops-solutions-information-hub/wiki/domains/automation/research-pipeline-orchestration.md` (canonical)
- `wiki/backlog/epics/epic-e003-compound-retention-and-multi-group.md` (parent Epic)
- `wiki/log/2026-05-06-180000-task-creation-focus-update-multigroup-compound-milestone-directive.md` (operator's E003 directive)
- `.claude/rules/compound-and-waterfall.md` (chain/group/tree triggers section — already landed last fire)
- `.claude/rules/operating-principles.md` principle #5 (research-first elevation 2026-05-06 — this fire's ACT-OUT of that principle)
