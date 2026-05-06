---
title: "T013 — Author network bridge configuration (br0 + ethernet members + management wifi outbound-only)"
type: task
status: in-progress
priority: P0
parent_module: "root-ghostproxy-m003-foundation-hardening"
parent_epic: "sfif-rollout-and-second-brain-integration"
current_stage: design
readiness: 50
sfif_stage: Foundation
created: 2026-05-04
updated: 2026-05-05
sources:
  - id: parent-module
    type: wiki
    file: wiki/backlog/modules/root-ghostproxy-m003-foundation-hardening.md
  - id: architecture-md
    type: wiki
    file: ARCHITECTURE.md
    description: "Network position + interface roles + bridge configuration"
tags: [task, p0, t013, foundation, network, bridge, design, m003]
---

# T013 — Author network bridge configuration

## Description

Configure the host's network as the transparent L2 bridge: two ethernet interfaces as members of `br0`, no IPs on the inspected segment, management wifi as outbound-only client.

## Subtasks (decision points)

| Decision | Options | Notes |
|---|---|---|
| Network configuration tool | `ifupdown` (Debian classic) / `netplan` / `systemd-networkd` | Operator-decision; each has trade-offs in declarativeness vs operational maturity |
| Bridge MTU | 1500 (default) / jumbo if upstream supports | If modules will inspect: must match across both members |
| Hardware offloads | Disabled (GRO, LRO, TSO) | Required for inline inspection; keep disabled even before modules install |
| Wifi client mechanism | `wpa_supplicant` direct / NetworkManager | If host runs NetworkManager elsewhere, integrate; if not, wpa_supplicant is simpler |
| Bridge default policy | nftables FORWARD default-accept / default-drop | Operator's threat model decides |

## Done When

- [ ] Network config tool chosen (operator decision); files authored per tool's syntax.
- [ ] Bridge `br0` config: two ethernet members, no IP, hardware offloads disabled.
- [ ] Management wifi config: client to operator's existing SSID, INPUT chain drops everything except established/related, no inbound services bind.
- [ ] systemd unit (or equivalent) brings bridge UP at boot.
- [ ] Recovery: console-only fallback documented.
- [ ] Verification: `brctl show br0` lists both members; `ip addr` shows only management-wifi IP; nftables INPUT chain confirmed outbound-only on wifi.

## Dependencies

- T011 (foundation-IaC approach) — gates authoring style
- T012 (install.sh) — install.sh deploys this config

## Stage-gate

Per methodology stage `scaffold`: type-definitions / schema / config-files allowed; no implementation. The network config FILES are scaffold-stage outputs; the actual bringing-up of the bridge is implement-stage (T012's install.sh apply).

## Relationships

- PART OF: [[root-ghostproxy-m003-foundation-hardening|M003]]
- BLOCKED BY: T011
- RELATES TO: [[T012-author-install-sh|T012]] (install.sh deploys this config)
- BLOCKS: T015 (post-install verification of bridge state)
