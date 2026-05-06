---
title: "T015 — Author post-install verification (integrity check + bridge state + opencode bridge + git audit)"
type: task
status: not-started
priority: P0
parent_module: "root-ghostproxy-m003-foundation-hardening"
parent_epic: "sfif-rollout-and-second-brain-integration"
current_stage: design
readiness: 25
sfif_stage: Foundation
created: 2026-05-04
updated: 2026-05-05
sources:
  - id: parent-module
    type: wiki
    file: wiki/backlog/modules/root-ghostproxy-m003-foundation-hardening.md
tags: [task, p0, t015, foundation, verification, smoke-test, m003]
---

# T015 — Author post-install verification

## Description

After install.sh runs, verify the host reached the expected foundation-tier state. Verification is a script (or set of scripts) that runs the gate checks: integrity check OK, bridge UP with expected members, opencode bridge resolves, git audit shows only whitelisted files tracked.

## Done When

- [ ] Verification script exists (could be `install.sh --check`, or a separate `verify-foundation.sh`, or the `tools/verify-policy.py` from M004 — operator-decision).
- [ ] Integrity check sub-step: integrity sentinel returns OK; output captured.
- [ ] Bridge state sub-step: `brctl show br0` lists both ethernet members; `ip addr` shows only management-wifi IP (no IPs on bridge interface or members).
- [ ] opencode bridge sub-step: `opencode debug config | grep claude-bridge` non-empty.
- [ ] Git audit sub-step: `cd /root && git status` clean; `git ls-files` matches the whitelist (only project-curated files visible to git).
- [ ] All sub-steps pass = verification exit 0; any sub-step fails = verification exit non-zero with specific failure reason.

## Stage-gate (Test stage)

Per methodology: test stage allows test-implementation + test-results; FORBIDS new features. The verification script IS test-stage output for M003. Foundation gate (T017) checks that verification passes.

## Dependencies

- T012 (install.sh) — verification is meaningful only after install runs
- T013 (network bridge config) — verification checks bridge state
- T014 (endpoint AI safety) — verification checks integrity + opencode bridge

## Relationships

- PART OF: [[root-ghostproxy-m003-foundation-hardening|M003]]
- BLOCKED BY: T012, T013, T014
- BLOCKS: T017 (foundation gate)
