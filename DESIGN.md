# DESIGN.md — root-ghostproxy design pattern rationale

> **Why this shape.** For each major architectural choice in root-ghostproxy, the rationale: alternatives considered, why this choice was made, what it costs, what it gains. Distinct from [ARCHITECTURE.md](ARCHITECTURE.md) (the *what + how*) and [SECURITY.md](SECURITY.md) (specific threat protections). DESIGN.md is the *why this and not something else*.

This file is canonical reference material. When operator or future-session agent asks "why is X this way," the answer should be derivable from this file. When making changes that contradict a documented design choice, the change requires re-deriving the rationale here — not silently overriding it.

## Design Principles in Force

The project commits to four cross-cutting design principles. Each is the lens through which the architecture's specific choices are evaluated.

### 1. Deny-by-default at every layer

Where safety is uncertain, refuse. Refusal is recoverable; an undetected dangerous action may not be.

**What it commits to:**
- Endpoint AI agent policy: tool calls that don't pass deny-set + behavior-pattern check refuse, not allow.
- Network bridge: nftables FORWARD chain default-decision is operator-set per threat model (default-accept for inspection-not-firewall, default-drop for firewall posture). Operator-decided.
- Tamper detection: when integrity check is uncertain, refuse every tool call.
- New AI tools: when added to the host, they default-comply with the existing policy (via adapter); they don't get a free pass to opt out.

**What it costs:** false positives — legitimate operations occasionally blocked, requiring operator confirmation or hook adjustment. The cost is borne in operator friction. The benefit is silent dangerous-action prevention.

**Alternatives rejected:** allow-by-default with explicit deny rules (the inverse). Rejected because in an AI-safety context the cost of an undetected dangerous action is asymmetric: a single credential exfiltration costs more than every legitimate-but-blocked operation combined.

### 2. Fail-closed where stakes are high; fail-open where stakes are low

Different failures have different costs. The architecture matches failure mode to cost asymmetry per layer.

**Fail-closed components:**
- Tamper detection (Layer 1) — when safety controls are tampered, refuse every tool call. The cost of allowing tool calls under tampered policy is asymmetrically high.
- Foundation install integrity check — when post-install verification fails, the install is not declared complete. The cost of a half-installed safety envelope is asymmetrically high.

**Fail-open components (configurable per operator's threat model):**
- Suricata IPS NFQUEUE with `bypass` option — when Suricata is down, traffic continues uninspected. The cost of network downtime in an inspection-not-firewall posture is asymmetrically high vs the cost of uninspected traffic during the recovery window.
- PolarProxy free-tier cap — when the cap is reached, decryption stops; forwarding continues. Inspection silently degrades; network keeps working. Operator monitors the divergence rate and provisions paid tier when needed.

**The choice point:** for the Suricata IPS module, operator picks NFQUEUE+bypass (fail-OPEN) vs AF_PACKET copy-mode (fail-CLOSED at L2). The decision is M005 module-design work. Both are valid; the choice depends on the specific threat model + uptime requirements.

**Alternatives rejected:** uniform fail-CLOSED across all layers (would make the project unusable as an inspection-not-firewall appliance because every Suricata crash takes the LAN offline); uniform fail-OPEN across all layers (would make tamper detection toothless because compromise of a hook script would be silently tolerated).

### 3. Markdown-as-IaC

Configuration is markdown files. Methodology, identity, backlog state, hook policy intent, design decisions — all in markdown, all version-controlled, all readable by operator + AI tools without specialized tooling.

**What it commits to:**
- The methodology engine is `wiki/config/methodology.yaml` (YAML, but human-readable + machine-parseable).
- The agent context is `*.md` files at the repo root (this file, AGENTS.md, CLAUDE.md, etc.) — operator and AI tools both read them via standard file I/O.
- Operator directives are `wiki/log/YYYY-MM-DD-*.md` (verbatim, sacrosanct).
- Backlog is hierarchical markdown: epics + modules + tasks at `wiki/backlog/{epics,modules,tasks}/`.
- Architectural decisions are inlined in this file (DESIGN.md) and (when authored) in `wiki/decisions/`.

**What it costs:** loss of structured-database affordances. There's no SQL query for "all tasks where readiness > 50 and parent_module = M005." Searching means grepping. The compensating mechanism is `pipeline post` (in the second brain) which builds indexes + manifest from frontmatter; the project as it exists at /root has not yet adopted that mechanism (it's available via the second-brain forwarders after M007 connect).

**What it gains:** every artefact is human-readable + AI-readable + diff-able + version-controlled with no special tooling. The operator can edit any file with a text editor. The AI tools see the same data the operator sees. There is no opaque database where state can drift from the operator's view.

**Alternatives rejected:** structured-database-backed configuration (TOML, SQLite, dedicated config service). Rejected because the cost of opacity vs the gain in queryability is asymmetric for this project's micro-scale + solo-operator + scaffold-tier maturity.

### 4. Same policy, different runtimes (no-policy-duplication invariant)

Cross-AI-tool consistency is structural, not coincidental. The agent-safety policy is defined once at the OS-root level; every AI tool obeys it through its own extension mechanism via thin adapters.

**What it commits to:**
- Single source of truth for the deny-set, the behavior-pattern check, the leak-detection patterns, and the hook scripts.
- Per-AI-tool adapters are thin — they map the tool's native envelope to the canonical envelope and dispatch to the same hook scripts.
- Adding a new AI tool means writing the adapter; it does NOT mean re-authoring the policy.

**What it costs:** the canonical envelope shape is constrained — it has to support every AI tool's hook event semantics in a single envelope. This may be lowest-common-denominator in some cases.

**What it gains:** policy drift across AI tools is structurally prevented. There is no "Claude Code says X but opencode says Y" failure mode. Operator's threat model is encoded once, enforced everywhere.

**Alternatives rejected:** per-tool policy with pairwise reconciliation. Rejected because policy drift is the highest-cost failure mode in a multi-AI-tool environment — an attacker exploits the most-permissive tool, and the operator may not realize which tool is most-permissive at any given moment.

## Specific Design Choices

### Stealth bridge (transparent L2) vs routing firewall

**Choice:** transparent L2 bridge — the box is L3-invisible to endpoints on the inspected segment.

**Alternatives considered:** L3 router/firewall (the box has IPs on both sides + does L3 NAT/forwarding); transparent proxy at L7 only (no L2/L3 control, just proxies HTTP-like protocols); span-port mirroring (passive; cannot block, only observe).

**Why stealth bridge:**
- Endpoints don't see "an extra hop" — networks behave as if root-ghostproxy weren't there. Reduces operator-side configuration ripple (no DHCP changes, no gateway changes, no L3 route changes).
- Provides inline control (drop/reject) in addition to inline observation. Span-port mirroring gives observation but not control.
- L3 routing/firewall would require IPs on both sides + would announce the box's presence. The "ghost" half of the project name commits to the L3-invisibility property.

**What it costs:** more complex bridge configuration; specific Linux network configuration required (kernel bridge, hardware offload disabling for inline inspection).

### Modules-as-facultative vs modules-as-required

**Choice:** Suricata + PolarProxy + future modules are **facultative**. The foundation runs without them.

**Alternatives considered:** modules required for the project to be functional (e.g. Suricata mandatory at install time); modules tightly coupled (PolarProxy presupposes Suricata).

**Why facultative:**
- Operator-stated: *"first there is no modules then 1 then 2 and later more but they are all facultative as much as if I do a full install they would all be installed."* Operator's design intent is explicit incrementalism.
- The endpoint AI agent safety + the bridge are useful standalone (a transparent bridge appliance with Claude+opencode hardening is a coherent setup even with zero modules).
- Module work is operator-driven future-session work. Foundation should not gate on module completion.
- License-tier considerations (PolarProxy free-tier cap) make some modules optional anyway — making them facultative architecturally avoids a forced upgrade path.

**What it costs:** the architectural integration interfaces (NFQUEUE slot, dummy-interface slot, eve.json output sink) must exist whether modules are installed or not, so that adding a module is a clean composition rather than an architectural retrofit.

**What it gains:** modular incremental rollout per operator's intent; lower-friction first-time install; clean failure isolation between layers.

### Two-layer hook architecture (machine-level + project-level)

**Choice:** safety policy lives at the OS-root level (machine-level), not at any individual project's `.claude/` level. Project-level layers can ADD restrictions but not subtract from machine-level.

**Alternatives considered:** project-level only (each project owns its safety policy); machine-level only (no project-level overrides); single-level with per-project namespace.

**Why two-layer:**
- The operator's safety policy is **about the host**, not about any one project. Endpoints on the LAN are protected regardless of which project a Claude Code session is opened in. A project-only safety policy would only protect that project's sessions.
- Sister projects on the same host inherit root-ghostproxy's machine-level policy uniformly. This is *the point* of root-ghostproxy as a system-AI-safety setup — the host's policy posture is consistent across all AI agent sessions.
- Project-level layers can ADD restrictions (a project can say "in addition to machine-level, also deny X for sessions in this project"). They cannot WEAKEN the machine-level set. This preserves operator's safety-floor while giving projects flexibility to be stricter.

**What it costs:** a session in any sister project is constrained by root-ghostproxy's deny-set. If the operator works in another project on the same host and a tool call is denied by root-ghostproxy's machine-level rules, that sister project's work is constrained.

**What it gains:** uniform safety floor across the host. The threat model is enforced regardless of which project the operator is currently working in.

### Methodology adoption (copy + adapt vs pointer)

**Choice:** copy + adapt. The methodology engine + 3 chosen profiles are local copies in `$HOME/wiki/config/`.

**Alternatives considered:** pointer-only (root-ghostproxy references the second brain's methodology config without copying); per-project local engine with no second-brain link.

**Why copy + adapt:**
- The Adoption Guide step 1 prescribes copy + adapt: artifacts, gate commands, commit scope, directory paths are project-specific variables; stage names + ordering + readiness ranges + hierarchy are ecosystem-wide invariants. Copying enables adaptation; pointer-only freezes the project to the second brain's exact gate commands.
- Operator-stated build order: *"all this and the wiki LLM and methodology goes before the modules."* The methodology layer needs to be in place + adaptable per project before module work begins. Pointer-only would require ongoing second-brain availability for every methodology operation.
- root-ghostproxy is type=root + group=operating-system-setup; some methodology gates (e.g. "lint passes" as a stage gate) need translation into infrastructure-specific equivalents (e.g. `./install.sh --dry-run` returns `unchanged` per file). Copy + adapt enables these translations.

**What it costs:** drift risk — the local methodology may fall behind the second brain's evolution. Mitigation: re-copy the engine + profiles when the second brain publishes a methodology update; only adaptations remain project-local.

**What it gains:** the project owns its methodology layer + adapts gates per-domain; doesn't require live connection to the second brain for stage-gate operations.

### Sister-project registration with `auto_connect: false`

**Choice:** root-ghostproxy is registered in the second brain's `sister-projects.yaml` with `auto_connect: false`. Connection requires explicit `--connect-project /root` invocation by the operator.

**Alternatives considered:** `auto_connect: true` (auto-hookup on `tools.setup` runs); not registered at all (no integration, no methodology-driven cross-project flow).

**Why `auto_connect: false`:**
- type=root projects gate the security envelope of the host. Auto-connect would bypass the operator's explicit-authorization step.
- The friction-by-design of `auto_connect: false` is intentional: integration requires a deliberate operator command. This is appropriate for a project that owns the machine-level safety policy.
- M010 (the auto_connect flip decision module) provides the operator-decision point to revisit this default after M009 stability is proven.

**What it costs:** operator must run `--connect-project` explicitly per host. Multi-host deployments require N explicit runs (one per host). This is acceptable given root-ghostproxy is currently single-host.

**What it gains:** explicit-authorization gate; consistent with the project's deny-by-default principle (the connection is a state change to /root, so it requires explicit operator input).

### Wifi as outbound-only management

**Choice:** the management wifi interface is configured as outbound-only — wifi client to operator's existing secure SSID, no inbound services bind.

**Alternatives considered:** wifi as inbound management (SSH on the wifi); wifi as access point (root-ghostproxy serves a wireless network alongside the inspection bridge); no management interface (console-only).

**Why outbound-only:**
- The bridge is L3-invisible to inspected-segment endpoints. The wifi gives the box itself internet access (apt updates, threat-intel feeds, AI APIs, outbound web) without exposing services on the inspected segment.
- Inbound management would expose attack surface on a security-sensitive appliance. The operator's threat model values minimal attack surface on the host itself.
- Console-only would lose operator's ability to update the host without physical access. The wifi gives outbound updates while preserving console-only-recovery for the worst case.
- AP mode (offering a wireless network) was operator-deferred per the prior session memory: typical wifi cards (e.g. RTL8821CE on rtw88) lack stable AP support; out-of-tree drivers are flaky. Deferred until AP-capable hardware is in place.

**What it costs:** operator has only a one-way diagnostic channel (logs + status reports out via wifi); inbound debugging is console-only.

**What it gains:** minimal attack surface on the appliance itself; outbound updates work normally; recovery story preserves console as the always-available fallback.

### `git init` at $HOME (deny-all + whitelist .gitignore)

**Choice:** the repo is structured to be `git init`'d at `$HOME` itself. The `.gitignore` is deny-all + whitelist — only curated config files visible to git; everything else in $HOME stays local.

**Alternatives considered:** repo at `$HOME/<projectname>` (conventional sub-directory); repo at `/etc/root-ghostproxy` (system-level, not user-level).

**Why git init at $HOME:**
- Files installed by the project live in `$HOME/.claude/` and `$HOME/.config/opencode/` — these are SUB-PATHS of `$HOME`. A repo at `$HOME/<projectname>` would not naturally contain them; the install would have to copy from one location to another.
- A repo at `$HOME` directly contains the install destinations as part of the tree. The `.gitignore` deny-all + whitelist means only the curated files are tracked; the rest of `$HOME` (sessions, transcripts, history, ssh, env, credentials) stays local.
- This is the type=root scope-not-path property in concrete form: the repo IS the home directory; the home directory IS the operating-system-setup target.

**What it costs:** unusual repo layout — operators familiar with `cd ~/projectname && git status` would expect that pattern. This pattern is `cd ~ && git status`.

**What it gains:** install + repo are the same tree; no copy-from-repo-to-install indirection; `.gitignore` whitelist is the security gate that prevents accidental publishing of secrets.

## Anti-Patterns Deliberately Avoided

| Anti-pattern | Why we avoid | What we do instead |
|---|---|---|
| **Per-tool deny lists** | Drift across AI tools; an attacker exploits the most-permissive tool. | One source of truth, multiple adapters (no-policy-duplication invariant). |
| **Allow-by-default with deny rules** | Asymmetric cost — undetected dangerous action vs blocked legitimate operation. | Deny-by-default at every layer. |
| **Silent fail (refuse without telling the operator)** | Operator can't recover what they don't know failed. | Every refusal logs reason + (where useful) bypass mechanism. The hook architecture pattern requires reason + remediation + bypass. |
| **Tamper detection without integrity verification of the sentinel itself** | An attacker who compromises the sentinel can simulate "all OK." | The sentinel is integrity-protected (its size + checksum is part of the verification). Editing the sentinel itself triggers a check failure on next run. |
| **Modules tightly coupled to foundation** | Module installation gates on foundation hooks; module uninstall would break foundation. | Modules are facultative; foundation runs standalone; module integration interfaces are explicit slots, not implicit dependencies. |
| **Pointer-only methodology (no local copy)** | Project gates on second-brain availability for every methodology operation. | Copy + adapt per Adoption Guide step 1. |
| **Single-tier safety policy (no machine-level / project-level distinction)** | Project-level only doesn't cover sister-project sessions; machine-level only is too rigid for project-specific additions. | Two-layer architecture; machine-level fires first; project-level adds restrictions. |
| **Auto-connect for type=root projects** | Bypasses operator's explicit-authorization gate for projects that gate the security envelope. | `auto_connect: false`; explicit `--connect-project` invocation. |
| **Hardcoded interface device names** | Hosts vary; `enp2s0` on one host is `eth0` on another. | Configuration uses role-based names (upstream-eth, lan-eth, management-wifi); device names are install-time mappings. |
| **AI tools authored their own per-tool policy files** | Drift; multiple sources of truth. | The bridge plugin pattern: one canonical envelope, adapters per AI tool. |
| **Modules required at install time** | Forces operator into full install; loses incrementalism. | Facultative; first-install can have zero modules. |

### Unified trigger model (signal → action → recovery)

Per `.claude/rules/trigger-model.md` (cycle 49). Insight: hooks, slash commands, skills, modes, tools, MCP, scheduled tasks, and sub-agents all share the same shape — `SIGNAL → ACTION → RECOVERY`. They differ in WHO fires the signal, HOW deterministic the action is, and WHAT the recovery loop looks like.

Three signal-source categories: **harness-deterministic** (hooks fire on lifecycle; tools fire when agent invokes), **operator-explicit** (slash commands), **semantic-match** (skills auto-trigger on prose).

Three action-determinism tiers: **programmatic** (tools/MCP — same input → same output), **scripted** (hooks/commands — 100% reliable when harness executes), **generative** (skills/modes/sub-agents — ~70-95% generative compliance).

Picking the right mechanism is per cost-of-false-positive vs cost-of-false-negative. Hard security gates → hooks (logical) or `permissions.deny` (deterministic). Persona shifts across turns → modes. Delegated research without context bloat → sub-agents. Recurring autopilot → scheduled task wrapping a slash command.

### Verbosity calibration discipline (anti-pendulum)

Per cycles 41-43 statusline UX iterations + SB-082 (extremes pendulum recurring). When correcting an over-A behavior, agent default is over-correct to over-B. Counter-pattern: **render-and-measure-both-extremes-and-pick-middle** before shipping any calibration. Settled rule of thumb for this project: full-word labels, compact ratio values (e.g. `Bugs: 13/7` not `SB:13/6` and not `SystemicBugs: 13 open · 6 recurring`). Every future calibration re-reads this section first to verify intent.

## Trade-offs Taken (vs Alternatives)

| Choice | Alternative considered | Why this one wins for root-ghostproxy |
|---|---|---|
| Deny-by-default | Allow-by-default | AI safety context: cost of undetected dangerous action >> cost of false-positive friction |
| Fail-closed (tamper) + Fail-open (Suricata bypass option) | Uniform fail-mode | Different layers have different cost asymmetries; matched per-layer is correct |
| Markdown-as-IaC | Structured-database config | Human + AI readability + diff-ability outweighs query expressiveness at this project's micro scale |
| No-policy-duplication | Per-tool policies | Cross-AI-tool drift is the worst failure mode in multi-AI environments |
| Stealth L2 bridge | L3 router | Reduces operator-side L3 reconfiguration; the "ghost" property is project intent |
| Facultative modules | Required modules | Operator-stated incrementalism + license-tier flexibility |
| Two-layer hooks | Single-tier | Sister-project sessions on the same host inherit safety policy uniformly |
| Methodology copy + adapt | Pointer-only | Project owns gates per domain; doesn't gate on live second-brain availability |
| `auto_connect: false` for type=root | `auto_connect: true` | Friction-by-design appropriate for security-envelope projects |
| Wifi as outbound-only management | Inbound SSH on wifi | Minimal attack surface on a security-sensitive appliance |
| `git init` at $HOME | Repo at `$HOME/<projectname>` | Install destinations are sub-paths of $HOME; repo IS the home directory |

## Open Design Questions

These are unresolved and require operator decision (or future-session investigation):

| Question | Blocks | Notes |
|---|---|---|
| Suricata IPS mode failopen choice | M005 (Suricata-first path) | NFQUEUE+bypass (fail-OPEN) vs AF_PACKET copy-mode (fail-CLOSED at L2). Different threat models support different choices. |
| Foundation IaC authoring approach | M003 | Author install.sh from scratch (operator-driven greenfield) vs extend the prior $HOME/install.sh as a starting point. |
| Network bridge configuration tool | M003 | `ifupdown` (Debian classic) vs `netplan` vs `systemd-networkd`. Each has trade-offs in declarativeness vs operational maturity. |
| Project-internal verifier language | M004 | Python (aligns with `integrity.py` if extended) vs shell (aligns with install.sh + hooks). |
| Pre-commit vs CI integration | M004 | Pre-commit catches local-only drift; CI catches drift on every git push. Both possible, both have setup cost. |
| First module choice | M005 | Suricata-first ("passive before active") vs PolarProxy-first ("de-risk cert distribution first"). Operator decides per priority. |
| PolarProxy bypass list policy | M005 (PolarProxy path) | Default chrome-bypass list + operator additions vs operator-curated from scratch. |
| eBPF integration | Phase-2 | If/when AF_PACKET multi-thread + eBPF load balancing is needed for throughput beyond ~Gigabit. |
| Active response capability | Phase-3 | Operator-decision: should root-ghostproxy be able to actively respond (rewrite flows, inject responses, honeypot specific destinations)? |
| Multi-host deployment shape | Phase-2 | How many hosts? Each independent or coordinated? Configuration-management mechanism (Ansible / Salt / NixOS / direct git pull)? |

## Cross-References

| For… | Read |
|---|---|
| What the project is + identity + modules + status | [README.md](README.md) |
| System topology + components + data flow + module integration interfaces | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Threat model + protections + fail-closed invariants | [SECURITY.md](SECURITY.md) |
| Tool reference (when scripts exist) | [TOOLS.md](TOOLS.md) |
| Cross-tool agent contract | [AGENTS.md](AGENTS.md) |
| Claude Code-specific routing | [CLAUDE.md](CLAUDE.md) |
| Current operational state | [CONTEXT.md](CONTEXT.md) |
| Skills directory context (skill-vs-command-vs-hook decision matrix) | [SKILLS.md](SKILLS.md) |
| Methodology engine (canonical) | [wiki/config/methodology.yaml](wiki/config/methodology.yaml) |
| Second brain Adoption Guide (the strictly-defined sister-project adoption process) | `<second-brain>/wiki/spine/references/adoption-guide.md` |
| SFIF model (canonical, in second brain) | `<second-brain>/wiki/spine/models/quality/model-sfif-architecture.md` |
| Markdown-as-IaC model (canonical, in second brain) | `<second-brain>/wiki/spine/models/agent-config/model-markdown-as-iac.md` |
| Operator-verbatim project framing | `<second-brain>/raw/notes/2026-05-04-prepare-root-ghostproxy-as-sister-type-root-group-operating-system-setup.md`, `2026-05-04-custom-tailored-model-group-moe-intelligence-layer-and-root-ghostproxy-pain-point.md` |
