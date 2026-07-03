# Operator directive — prepare root-ghostproxy for sovereign-os usage (endpoint mode, no proxy)

> Logged verbatim BEFORE acting, per AGENTS.md Hard Rule (log operator directives to `wiki/log/` before acting).
> Session: remote branch `claude/ghostproxy-sovereign-os-prep-ole9ul` (2026-07-03).

## Operator verbatim (sacrosanct)

> "Lets prepare root-ghostproxy for sovereign-os usage, we will use use the repo without the proxy mode enabled."

## Reading of the directive (agent-flagged, per premise-confirmation gate)

Literal grants:

1. **Prepare root-ghostproxy** — the object being prepared is THIS repo. Work lands here.
2. **for sovereign-os usage** — the consumer is the `cyberpunk042/sovereign-os` arc (the SAIN-01
   sovereign node the sovereign-os repo BUILDS). Per sovereign-os SDD-001 the cross-repo status of
   root-ghostproxy was "dormant"; this directive begins its consumption-side preparation.
3. **"without the proxy mode enabled"** — mapped to the repo's own vocabulary: the proxy/IPS half
   (transparent L2 bridge + management wifi + Suricata/PolarProxy modules) stays OFF. In install.sh
   terms that is **`--mode endpoint`** (per SB-074 mode axis: bridge | endpoint | hybrid | auto).
   Bridge + wifi ops are excluded by `mode_includes()`; the endpoint AI agent safety foundation
   (hooks + brain + tools + integrity + opencode bridge) is what sovereign-os consumes.

Agent-constructed premises NOT acted on: no sovereign-os-side edits (its "dormant" markers are that
repo's own docs to evolve); no proxy/bridge code removal (endpoint mode is a runtime selection —
adding ≠ discarding; the bridge half stays intact and facultative).

## Work executed under this directive

| Artifact | Purpose |
|---|---|
| `docs/sovereign-os-endpoint-usage.md` | Canonical consumption guide: install root-ghostproxy on a sovereign-os node in endpoint mode (proxy disabled) |
| `.claude/hooks/tests/test-sovereign-endpoint-mode.py` | Regression smoke test: endpoint mode excludes bridge+wifi ops, includes the endpoint safety foundation; discovered by `tools.run-tests` |
| CONTEXT.md | Append-only rows: this directive + work-completed entry |
| README.md | Additive pointer from Setup Path to the sovereign-os endpoint usage doc |
| This log | Verbatim primary source |
