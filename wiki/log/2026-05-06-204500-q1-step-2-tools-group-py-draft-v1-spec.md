---
title: "Q1 step-2 — DRAFT v1 spec for tools/group.py (chain/group/tree primitive)"
type: log
subtype: design-draft-spec
domain: cross-domain
status: draft-spec-pending-operator-review
created: 2026-05-06
sources:
  - id: q1-research-findings-step-1
    type: log
    file: wiki/log/2026-05-06-203000-q1-research-second-brain-chain-group-tree-canonical.md
  - id: second-brain-research-pipeline-orchestration
    type: concept
    file: /opt/devops-solutions-information-hub/wiki/domains/automation/research-pipeline-orchestration.md
  - id: operator-original-vision-2026-04-08
    type: directive
    file: /opt/devops-solutions-information-hub/raw/notes/2026-04-08-user-directive-ecosystem-connections.md
tags: [draft-spec, q1-step-2, tools-group-py, chain-group-tree, e003-multi-group, layer-a-primitive]
---

# DRAFT v1 spec — `tools/group.py` chain / group / tree primitive

> **Agent-DRAFT v1 per SB-095** — this is a SPEC, not implementation. Operator-revisable. Authored 2026-05-06 per Q1 resolution path step-2 (research-first per principle #5 elevated; canonical taxonomy borrowed from second-brain `wiki/domains/automation/research-pipeline-orchestration.md`).

## Purpose

Provide root-ghostproxy with a chain/group/tree primitive for batched operations. Operator directives (2026-05-06):

- *"a group call and chain calls is just a way to create a tree of operations"*
- *"updating tasks and such where we know that the task should imply than more than just one operation, its a chain"*
- *"NOT binary, build ALL three layers"* (Q1 resolution: tool + commands + rules; this spec is Layer A)

## Module location

`/root/tools/group.py` (sibling to existing `tools/cycle.py`, `tools/tasks.py`, etc.)

## Public API (3 functions + 1 type alias)

### Type alias: `Step`

```python
Step = Callable[..., Any]
```

A step is any zero-or-one-arg callable that returns Any. Chain passes prior result; group passes nothing; tree passes seed.

### `chain(*steps, initial=None) -> Any`

**Semantics**: sequential composition. Each step receives previous step's return value (or `initial` for first step). Returns final step's return value.

```python
def chain(*steps: Step, initial: Any = None) -> Any:
    """Run steps sequentially; thread result through.

    Example:
        result = chain(
            lambda: read_active_task(),
            lambda task: mark_done(task),
            lambda task: propagate_to_module(task),
            lambda task: log_completion(task),
        )

    Returns: final step's return value.
    Raises: any exception from any step (chain stops at first failure; partial-state caveat).
    """
```

**Failure semantics**: if step N raises, chain stops. Steps 1..N-1 already ran (state mutations persist). Caller decides recovery (retry / rollback / continue from N+1).

### `group(*callables) -> list`

**Semantics**: parallel composition (synchronous in MVP — could be async later). All callables receive no args. Returns list of results in input order.

```python
def group(*callables: Step) -> list:
    """Run callables 'in parallel' (MVP synchronous, results in input order).

    Example:
        results = group(
            lambda: read_active_task(),
            lambda: read_active_focus(),
            lambda: read_active_priorities(),
        )
        task, focus, prios = results

    Returns: list of all results in input order.
    Raises: collects all results+exceptions; raises GroupError aggregating failures.
    """
```

**Failure semantics**: all callables run regardless of individual failures. Failures aggregated into `GroupError` raised after all complete.

### `tree(root, branches, merge) -> Any`

**Semantics**: root produces seed; branches receive seed + run in parallel; merge synthesizes branch outputs.

```python
def tree(root: Step, branches: list[Step], merge: Step) -> Any:
    """Tree composition: root → parallel branches → merge.

    Example:
        synthesis = tree(
            root=lambda: collect_pending_state(),
            branches=[
                lambda state: extract_blockers(state),
                lambda state: extract_decisions(state),
                lambda state: extract_questions(state),
            ],
            merge=lambda parts: synthesize_handoff_doc(parts),
        )

    Returns: merge's return value.
    """
```

## Failure mode + recovery design

Per second-brain canonical (multi-pass principle): chains should be RE-RUN-SAFE. Idempotency at the step level is the contract — each step must be safe to re-invoke if a partial chain failed mid-way.

For non-idempotent steps (file-write at specific line, network call), wrap in retry-or-skip helper. NOT in scope for v1 spec; future v2.

## Tests required (v1 acceptance)

- `chain` 3-step sequential: each step's input is prior output ✓
- `chain` empty steps list: returns `initial` ✓
- `chain` step raises: subsequent steps NOT called, exception propagates ✓
- `group` 3 callables: returns list in input order ✓
- `group` one callable raises: GroupError aggregates; other callables completed ✓
- `tree` root→2 branches→merge: branches receive root's seed; merge gets branch list ✓
- Roundtrip example: task-complete-cascade chain (mark-done → propagate → log) ✓

## What v1 does NOT include (forward-anchors)

- **Async / parallel concurrency** — group is sync MVP; v2 could add `asyncio.gather`-style parallel
- **Step dependencies (DAG)** — v1 is linear-chain or independent-group only; v2 could add explicit DAG
- **Logic conditionals** — v1 has no `if-step-N-fails-then-step-N'` branching; v2 could add
- **Cycle integration** — v1 is library-only; consumers (cycle skill, command wrappers, hooks) come in Layer B + C per Q1 resolution

## Connection to root-ghostproxy ops

5 named pipeline candidates (DRAFT, agent-proposed):

| Pipeline | Mode | Concrete chain |
|---|---|---|
| task-complete-cascade | chain | mark-done → readiness → parent_module → cursor → handoff → log |
| stage-transition | chain | verify-allowed → gate-check → write-stage-log → frontmatter → notify |
| sb-closure-batch | chain | tracker-row → decisions-D → progress.md → log |
| multi-file-coherent-edit | group→chain | (edit-A + edit-B + edit-C) → run-tests → commit |
| research-then-build | tree | second-brain-query → [spec-draft, prior-art, risks] → synthesize-spec |

These are agent-suggested candidates — operator may pick / revise / add others.

## Q1 path status (updated)

| Step | Status |
|---|---|
| 1. Research-first second-brain query | ✓ DONE (research log 2026-05-06 20:30) |
| 2. DRAFT v1 spec (this file) | ✓ DONE (this fire) |
| 3. Operator review of spec | next: operator picks (a) greenlight implementation / (b) revise spec / (c) wait |
| 4. Implementation: Layer A `tools/group.py` | gated on operator step-3 |
| 5. Layer B + C (commands + rules) | gated on Layer A landing empirically |

## Cross-references

- Q1 research findings: `wiki/log/2026-05-06-203000-q1-research-second-brain-chain-group-tree-canonical.md`
- Self-elevation report (Q1-Q4 resolved): `wiki/log/2026-05-06-200000-q1-q4-self-elevated-decisions-report.md`
- Parent Epic E003: `wiki/backlog/epics/epic-e003-compound-retention-and-multi-group.md`
- Compound+waterfall trigger (b) rule extension (already landed): `.claude/rules/compound-and-waterfall.md`
- SB-131 chain-batched ops pattern (rule-layer precedent): `wiki/governance/systemic-bugs.md`
