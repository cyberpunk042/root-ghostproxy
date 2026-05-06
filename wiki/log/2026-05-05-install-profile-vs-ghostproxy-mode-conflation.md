---
title: "2026-05-05 — Operator directive: install-profile vs ghostproxy-mode conflation (orthogonal axes)"
type: log
domain: cross-domain
status: active
confidence: high
created: 2026-05-05
updated: 2026-05-05
sources:
  - id: operator-directive-2026-05-05-install-profile-mode-conflation
    type: directive
tags: [log, operator-directive, sacrosanct, verbatim, conflation, install-profile, ghostproxy-mode, orthogonal-axes, sb-074]
---

# Operator directive — 2026-05-05 install-profile vs ghostproxy-mode conflation

## Verbatim

> "wtf somehow you conflated everything..."

> "you conflated the ghostproxy mode with the install profile..."

## Decomposition

### A — Two orthogonal axes
- **Install profile** (install-time scope choice): base / full / interactive
  - base = foundation install
  - full = base + ALL facultative modules
  - interactive = TUI-prompted choices
- **Ghostproxy mode** (runtime / host-property): bridge / endpoint / hybrid / etc.
  - bridge = host acts as transparent L2 IPS (Suricata + PolarProxy + bridge config relevant)
  - endpoint = host runs Claude Code + opencode locally; no bridge
  - hybrid = both
  - (other modes possible)

### B — The conflation I made
- I tied `profile=base` defaults to `bridge=0, wifi=0`
- That bakes ghostproxy-mode assumptions INTO the install profile
- Wrong: a base install on a bridge-mode host SHOULD include bridge config (bridge is foundation-tier per M003 brain files); a base install on endpoint-mode host should NOT
- The mode determines whether bridge-related ops are applicable; the profile determines the install scope (foundation vs foundation+modules)

### C — Right model

```
operations applicable = ghostproxy mode (host-property: which ops apply at all)
operations to install = install profile (operator-choice: scope of THIS install run)
```

E.g.:
- mode=bridge   + profile=base   → foundation incl. bridge config (because mode applies + profile=base = foundation)
- mode=bridge   + profile=full   → foundation + bridge + ALL modules (Suricata, PolarProxy, etc.)
- mode=endpoint + profile=base   → foundation WITHOUT bridge (mode doesn't apply for bridge ops)
- mode=endpoint + profile=full   → foundation + ALL APPLICABLE modules (skip bridge-related)

### D — Where bridge config lives

Per brain files (M003 + ARCHITECTURE.md), bridge config is FOUNDATION-tier (not module-tier). But foundation operations are conditional on mode applicability. So the model is:

```
For each foundation operation:
  applicable = (operation's mode-precondition satisfied)
  install    = applicable AND (profile says yes OR explicit --with-X)
```

## Action plan

1. Log directive — done.
2. Add SB-074: install-profile/ghostproxy-mode conflation in install.sh.
3. Revise install.sh:
   - Add `--mode <bridge|endpoint|hybrid|auto>` flag (auto-detects from host)
   - Profile decides INSTALL SCOPE (base = foundation; full = foundation+modules)
   - Mode decides WHICH FOUNDATION OPS APPLY (bridge config only if mode includes bridge)
   - Profile + Mode compose; per-op `--with-X` / `--no-X` overrides
4. Surface a decision package on the mode taxonomy (what modes? auto-detection rules?)

## Open questions for operator (decision package format per SB-071)

- Mode taxonomy: bridge / endpoint / hybrid is enough? Or others (proxy / gateway / monitor)?
- Auto-detection: if 2+ ethernet interfaces present + bridge tools installed → mode=bridge? Or always-explicit?
- Default mode: if --mode unspecified, auto-detect or fail-safe to endpoint?

## Cross-references

- T012 (install.sh authoring) — revision pass needed
- SB-073 (install.sh too-narrow assumptions) — this directive specifies the conflation precisely
- SB-072 (auto-research before asking) — should have read M003 brain files more carefully before making the bridge=0 call in profile=base
