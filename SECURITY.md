# SECURITY.md — root-ghostproxy

> Security policy for root-ghostproxy. Threat model, layer-by-layer protections, fail-closed invariants, escalation, audit, and known limitations. Load-bearing for type=root + group=operating-system-setup projects — the project IS a security envelope, so SECURITY.md is not auxiliary documentation but a load-bearing artefact of the project itself.

## Project Security Stance (one paragraph)

root-ghostproxy is a system AI safety setup project. Its security stance is **deny-by-default** at every layer: the endpoint AI agent policy denies tool calls unless they pass deny-set + behavior checks; the bridge denies fall-through traffic if the inspection layer says drop; the integrity layer denies every tool call if safety controls are tampered with. The project assumes adversarial input — both at the network layer (untrusted inbound/outbound traffic) and at the agent layer (adversarial content embedded in tool outputs that can hijack agent reasoning via prompt injection). The protections are designed to fail closed where the cost of a false positive is small (deny a tool call; alert the operator) and fail open only where the cost of a false negative is small AND the cost of a false positive is large (network inspection in degraded mode keeps traffic flowing; alerting the operator that inspection has degraded is the mitigation).

## Threat Model

### Adversaries

| Adversary | Capabilities | What we defend against |
|---|---|---|
| **External attacker (network)** | Can send packets crossing the bridge from the upstream side; can attempt to compromise endpoints on the LAN; can scan for open services on the host's management interface | Inbound exploits aimed at LAN endpoints; lateral movement; persistence on the bridge host itself; scanning of the management network |
| **Adversarial content via tool outputs** | Web pages, file contents, search results, MCP server responses fetched by an agent can contain instructions that subvert the agent's reasoning | Prompt-injection-driven agent actions: deny credential reads, deny suspicious filesystem writes, deny exfil-shaped network calls regardless of how the agent was prompted to perform them |
| **Compromised AI agent on the host** | An agent whose reasoning is subverted (prompt injection, malicious instruction) attempts to read credentials, write persistence, exfiltrate data, install malware, tamper with the safety controls themselves | Tool-call-time policy enforcement that blocks dangerous actions even when the agent itself is no longer trusted; tamper-detection that refuses every subsequent tool call if controls are disabled |
| **Insider with operator credentials** | An operator-equivalent actor who can edit configuration, push to the repo, run installs | Out of scope — operator is trusted by design. The project's audit logs preserve a record so operator actions are traceable, but they are not blocked. |
| **AI provider account compromise** | An attacker who gains the operator's API key for a cloud LLM provider can issue API calls posing as the operator | Out of scope at the network layer (these are the operator's own outbound calls); credential-scoped — the operator's responsibility to rotate keys + monitor billing |
| **Untrusted physical access to the host** | An attacker with physical access can take the host offline, read disks, manipulate firmware | Out of scope — physical security is a different control layer (host placement + physical access control) |
| **Adversarial Suricata rule flooding** | A traffic generator that triggers signature matches at high rate to overwhelm logging or saturate the IPS path | Out of scope by default; mitigation is rate-limiting + alert thresholds in the Suricata module's tuning, not in the core foundation |

### Assets to Protect

In priority order:

1. **Credentials in `$HOME`** — `.env*`, `*.pem`, `*.key`, `id_rsa*`, `.aws/credentials`, `kubeconfig`, `.netrc`, `.git-credentials`, `**/secret*` and similar credential-shaped paths. The endpoint policy's deny-set targets these.
2. **AI provider tokens and API keys** — Anthropic, OpenAI, Google, GitHub, GitLab, Slack, AWS, Stripe, SendGrid, npm, Telegram, JWT. The endpoint policy's leak-detection inspects tool outputs for these patterns and refuses to surface them in agent context.
3. **Private keys and DB connection strings** — same leak-detection layer applies.
4. **Authorization headers in tool outputs** — same.
5. **LAN endpoint traffic content** — when the network inspection modules are deployed, the bridge sees and (optionally) controls the content of traffic crossing it. The TLS-firewall ruleset in PolarProxy decides which destinations get decrypted vs bypassed (e.g. banking, healthcare, cert-pinned apps bypass).
6. **Operator's session transcripts, history files, ssh keys** — the deny-set covers these path patterns.
7. **The safety policy itself** — `~/.claude/` and equivalent policy directories must remain owned by the operator and integrity-verified. Tampering refuses every tool call until restored.

### Out of Scope

- Physical security of the host
- Console access (it is the recovery path; an attacker with console can override anything)
- Operator's manual edits to configuration (operator is trusted; their edits are subject to integrity verification afterward but are not blocked)
- Cryptographic strength of TLS itself (the project relies on the host's TLS implementation; replacing OpenSSL or hardening cipher suites is a host-config concern, not a project concern)
- Side-channel attacks (timing, power, thermal) on co-located AI accelerators
- Supply chain integrity of upstream packages (Suricata, PolarProxy, Debian packages — the project relies on package signature verification done by the host's package manager)

## Layer-by-Layer Protections

The project defends in depth across three layers. Layer 1 is the foundation and is always required. Layers 2 and 3 are facultative modules — operator decides at install time whether to deploy them.

### Layer 1 — Endpoint AI Agent Safety (foundation)

**What it provides.** A shared policy source at the OS-root level that all installed AI tools (Claude Code, opencode, future tools) obey through their respective extension mechanisms. Protections include:

- **Deny-set on credential-shaped paths.** Tool calls that touch credential-shaped paths are blocked before the AI tool's runtime hands the call to the OS — regardless of which AI tool issued the call.
- **Behavior-pattern check on tool inputs.** Tool inputs are inspected for shell-exfil idioms, malicious payload patterns, and known dangerous-shape inputs. Matches are blocked or asked-for-confirmation depending on severity.
- **Output scanning for sensitive values.** Tool outputs are inspected for credential-shaped values matching patterns for major AI/cloud/SaaS providers. Detected leaks are logged and the operator is alerted; the leak-shaped value is optionally redacted before being surfaced to the agent.
- **Cross-AI-tool consistency via shared policy.** Multi-AI-tool environments share one policy source so deny rules + behavior checks are not duplicated across tool runtimes — defined once at the OS-root level, enforced uniformly. Adding a new AI tool means adding a thin extension that mirrors hooks under the new tool's plugin/extension SDK; the policy itself is not duplicated.
- **Fail-closed tamper detection.** A pre-tool-call sentinel verifies the safety policy is intact: policy source present, hooks not disabled, deny-set above a known-safe threshold, all required enforcement scripts present + executable + non-suspicious size. If any check fails, every subsequent tool call refuses until restored. The sentinel itself is integrity-protected.

**What it does NOT provide at this layer:**
- Network-layer defense — that's Layers 2 and 3
- Agent reasoning correction — the model can still be fooled by prompt injection; what this layer prevents is the ACTIONS that flow from being fooled
- Per-AI-tool runtime sandboxing — the AI tools run as themselves; the policy operates AROUND them, not under them

### Layer 2 — Network IDS/IPS (Suricata module — facultative)

**Status.** Module not yet installed. Foundation runs without it. Documented here for the layered-defense story.

**What it provides when installed.** Inline signature-based detection on the bridge data path. Suricata sees every packet crossing the bridge, matches against rule sets (ET Open, custom AI-safety rules, operator-curated additions), and either alerts (IDS mode) or drops (IPS mode) flows that match malicious or AI-policy-violating patterns. Output is structured eve.json for downstream consumption.

**Failopen behavior.** Per the source-synthesis at `wiki/sources/src-suricata-ips-mode-linux.md`, Suricata's IPS mode has a load-bearing failopen decision:
- **Phase-1 path (recommended for inspection-not-firewall posture):** keep the kernel bridge, use NFQUEUE on the FORWARD chain with the `bypass` option. When Suricata is down, traffic flows uninspected — network keeps working, inspection silently degrades.
- **Phase-2 path (tighter integration, fail-CLOSED at L2):** retire the kernel bridge, use AF_PACKET IPS mode with copy-mode pairing of the two ethernet interfaces. When Suricata is down, the copy stops and packets pile up at the NIC.

The failopen choice is operator's threat-model decision and is part of M005 module-design work.

### Layer 3 — Network TLS Inspection (PolarProxy module — facultative)

**Status.** Module not yet installed. Foundation runs without it.

**What it provides when installed.** Transparent TLS termination on the bridge data path. PolarProxy intercepts TLS streams, decrypts using a per-instance dynamically generated CA, re-encrypts toward the destination, and emits cleartext as PCAP-over-IP for downstream consumers (typically Suricata). Pairs with Suricata via the Hanke-pattern dummy interface + tcpreplay setup (per `wiki/sources/src-hanke-honeypot-polarproxy-suricata-integration.md`).

**Failopen behavior of the free tier.** Per `wiki/sources/src-polarproxy.md`: PolarProxy's free tier caps at 10 GB / 10 000 sessions / 10 000 rule-matches per day. Past the cap, PolarProxy keeps forwarding TLS but stops decrypting. **Inspection silently degrades; network keeps working.** This is fail-OPEN at the inspection layer. Mitigation: monitor the rate of TLS sessions seen vs decrypted; alert on divergence after the cap; consider paid tier when traffic volume sustains above the cap.

**CA distribution requirement.** PolarProxy decryption requires that LAN endpoints trust the proxy's CA. Endpoints without the CA in their trust store see cert errors and self-block. Cert-pinned apps (banking, mobile pinning) reject the proxy's CA regardless of trust-store presence; these destinations must be added to the bypass list (`--bypass <regex-file>` or the TLS-firewall ruleset).

## Network Posture (host-level constraints)

Per operator directive 2026-05-05: *"with the wifi client mode enabled with will not be in dhcp and we will make sure that we are in DNS over TLS and that we are not opening any leak, this is not for not reason I said no to ssh server setup"*.

The $HOME host operates under these network constraints:

| Constraint | What it means | Why |
|---|---|---|
| **WiFi client mode** | The host has a wifi interface in client mode (not AP mode) for management connectivity | Reduces RF surface; host doesn't broadcast its presence; uses an existing trusted network for out-of-band management |
| **NOT in DHCP** | Static IP assignment; addresses configured deterministically | DHCP broadcast solicitation leaks MAC + hostname + DHCP options; static config eliminates the leak vector |
| **DNS over TLS (DoT)** | All DNS resolution over TLS to a trusted resolver | Eliminates plaintext DNS leaks (which expose visited domains to anyone on-path); aligns with the no-leak principle |
| **No leaks** | Broader principle: no unintended outbound flows from the host | Aligns with the leak-detector hook (PostToolUse on Read/Bash/WebFetch/Grep scans tool output for credential patterns); network-stack-level extension of the same principle |
| **No SSH server** | SSH **server** explicitly NOT installed (operator's verbatim decision); SSH client may exist for outbound use | Operator: *"this is not for not reason I said no to ssh server setup"*. SSH server = remote attack surface + auth log + key management surface; conflicts with the no-leak principle. Out-of-band management via wifi client interface or console-only is sufficient |

These constraints inform M003 (Foundation hardening) install.sh authoring: install.sh should configure the wifi client interface with static IP, set DNS over TLS as the system resolver (e.g., systemd-resolved with DoT, or stubby), and explicitly NOT install or enable openssh-server.

## Fail-Closed Invariants

| Invariant | What it means | Enforcement |
|---|---|---|
| **Tamper detection precedes every tool call** | An integrity sentinel runs before every tool call decision. If safety controls are tampered, the call refuses. | Pre-tool-call hook in the AI tool's policy mechanism. |
| **Policy source must be present and not disabled** | If the safety-policy file is missing, or hooks are disabled (`disableAllHooks=true`-equivalent), the integrity check fails. | Tamper detection. |
| **Deny-set must meet a known-safe threshold** | If the deny-set has been eroded below an operator-set threshold (e.g. `< N` patterns), the integrity check fails. The threshold is operator-decided based on how comprehensive the original deny-set was. | Tamper detection. |
| **Required enforcement scripts must be present + executable** | If any required hook script is missing, non-executable, or suspiciously small (size deviation from baseline), the integrity check fails. | Tamper detection. |
| **Stage gates are hard during methodology-driven work** | When operator or agent works on the project under the stage-gate methodology, ALLOWED/FORBIDDEN per stage is enforced — implementation cannot ship in a Document-stage task, code cannot ship in a Design-stage task. | Methodology engine + agent's adherence + (when authored) project-internal verifier (M004). |
| **Tracked git files must match the deny-all + whitelist invariant** | The repo's `.gitignore` is deny-all + whitelist. Only project files are visible to git. Credentials, sessions, transcripts, logs, ssh, env stay local. Verifier checks `git ls-files` against the expected whitelist. | Foundation gate (M003) + Infrastructure tooling (M004). |

## Escalation Paths

| Event | Detection | Response |
|---|---|---|
| Tool call denied by deny-set | Endpoint policy logs the denial with reason | Logged for operator review; agent receives clear failure indicating the policy decision. No silent allow-throughs. |
| Tool call asks-for-confirmation on legitimate-but-risky operation | Behavior pattern matched (apt/pip/sudo/crontab/authorized_keys/etc.) | Operator confirms or denies in real-time. Pattern + decision logged for retrospective. |
| Leak detected in tool output | Output-scanning hook matched a credential-shaped value pattern | Leak logged with provider tag and redacted excerpt; operator alerted via system message; the leak-shaped value optionally redacted before being surfaced to the agent context. |
| Tamper detected | Integrity sentinel returned non-OK | Every subsequent tool call refuses. Operator must restore policy and re-verify integrity before tool calls resume. The sentinel's failure mode is fail-CLOSED. |
| Suricata IPS alert at high severity | Suricata rule with priority=1 (or operator-curated equivalent) matched a flow | When the Suricata module is installed: eve.json event emitted + (optional) downstream sink (Filebeat → Loki / Logstash → Slack / etc. — see Hanke-pattern integration). The default is alert-only; operator decides what becomes a drop. |
| PolarProxy free-tier cap reached | Rate of TLS sessions seen vs decrypted diverges after the daily cap | When the PolarProxy module is installed: monitor the divergence; alert operator; decision: provision a paid license tier or accept inspection degradation. |
| Bridge link flap or unrecoverable foundation error | systemd unit reports failure / kernel logs report bridge issue | Configurable per operator's threat model: fail-OPEN (network keeps working, inspection silently disabled) or fail-CLOSED (network stops; operator notified). The default is operator-decision at Foundation tier. |

## Audit Logging

| Channel | What's logged | Retention |
|---|---|---|
| **Tool-call decisions** | Per-call timestamp + tool + input pattern + decision (allow/deny/ask) + reason | Operator-decided rotation policy at Infrastructure tier (M004) |
| **Leak detections** | Timestamp + provider tag + redacted excerpt + tool + agent session ID | Same rotation policy |
| **Suricata events** (when module installed) | eve.json structured events: alert, anomaly, http, dns, tls, flow, fileinfo, stats. Daily rotation. | logrotate config in M005 install |
| **PolarProxy decryption metadata** (when module installed) | TLS handshake metadata + flow timing + bypass-decision audit. PCAP files of the cleartext (fed to Suricata). | Operator-decided rotation policy |
| **Operator directives + session logs** | `$HOME/wiki/log/YYYY-MM-DD-<slug>.md` — operator's verbatim directives, AI session logs, completion notes | Permanent (git-tracked when whitelisted) |
| **Backlog + work-state evolution** | `$HOME/wiki/backlog/` epic + module + task pages with frontmatter state-machine fields (status, current_stage, readiness, progress, stages_completed) | Permanent (git-tracked) |
| **Memory-layer auto-journals** | NOT used by this project. The `~/.claude/projects/-root/memory/` directory at $HOME from prior session is debris and not part of the project's authoritative state. | (n/a) |

## Hardening Posture by SFIF Stage

The project's security posture intensifies as it climbs SFIF stages:

| SFIF Stage | Security characteristic |
|---|---|
| **Scaffold** | Identity declared; methodology adopted; backlog scaffolded; agent-context files authored. No live security enforcement yet — this is the planning layer. |
| **Foundation** | Endpoint AI agent safety operational. Idempotent install. Integrity check operational. Deny-set in place. Bridge topology configured (passive forwarding). Policy source-of-truth present. Tamper-detection operational. Audit logging enabled. **This is when the project becomes a security envelope.** |
| **Infrastructure** | Project-internal verifier tooling enforces invariants programmatically (deny-set threshold, hook permissions, executable presence, integrity check). Validation pipeline (pre-commit OR CI) runs the verifier on every change. Operator-authorable threshold values in config. |
| **Features** | First inspection module deployed (Suricata or PolarProxy). Network-layer defense becomes operational alongside endpoint-layer. Failopen behavior of the chosen module is the operator's decision per threat model. |

## Operational Hygiene

| Practice | Why |
|---|---|
| Run `./install.sh --dry-run` before any install on a host | Preview what will change. The install backs up existing files but a dry-run is the safety net before any backup ever happens. |
| Verify integrity check passes before AND after any change to the safety policy | The integrity check is what stops a half-installed or tampered state from going live. |
| Audit `git status` and `git ls-files` before publishing | Ensure no unintended file is in the tracked set. The deny-all + whitelist `.gitignore` should leave only project files visible. |
| Run hook regression tests after editing any hook | `python3 .claude/hooks/tests/test-policy-block.py` + `test-malware-block.py` verify that hook regex changes don't introduce false-positives (which silently block the agent's own work) or false-negatives (which silently let attacks through). Both suites must PASS 4/4 before claiming a hook fix done. |
| Rotate AI provider keys regularly | Key compromise is out of scope at the network layer; rotation is operator's responsibility. |
| Review leak-detector logs weekly | Patterns of leak attempts are themselves a signal. |
| Re-verify deny-set count after any settings.json edit | The threshold is what tamper-detection enforces. Editing without re-verifying risks fail-closing every subsequent tool call. |
| Keep `~/.claude/settings.json` in version control (tracked side) | Auditability of the policy source's evolution. |
| Review the operator-pending decisions table in CONTEXT.md regularly | The `auto_connect` flip (M010), failopen mechanism choice for Suricata, license tier for PolarProxy, etc. accumulate. |
| Before initial publish: run `bash /tmp/publish-root-ghostproxy.sh` (dry-run) + Python audit script | Verify which files would actually stage; defense-in-depth against credential paths slipping in via deep-dir whitelist gaps (e.g. SB-085 caught `/scripts/lib/` exclusion that would have shipped broken merge-from-backup.sh). |

## Reporting a Vulnerability

Vulnerability reporting channel is **to be determined** at Foundation tier — likely an email channel (`security@<operator-domain>`) or a GitHub Security Advisory channel once the project is published with a remote. Until then, the operator's direct channel is the reporting path.

**Coordinated disclosure.** When the project is published with a remote, plan to follow standard coordinated-disclosure practice: private report → fix authored → patched release → public advisory after a reasonable embargo (typically 90 days from report).

**Severity tiers.** Adopted from the upstream Suricata SECURITY.md pattern (`wiki/sources/src-suricata.md`):
- **CRITICAL** — disrupts availability or enables traffic-based RCE/crash/evasion. Fix in private; release across all supported branches; immediate.
- **HIGH** — lower-risk than critical, perhaps disabled-by-default features or less likely exploitation. Fix in private up to ~1 month.
- **MODERATE** — Tier-2 / Community features not enabled by default. Roll up into the next release.
- **LOW** — CLI utilities, unlikely configurations. Fix in development versions; backport at discretion.

The same severity classification applies whether the vulnerability is in the foundation IaC, the Suricata module integration, or the PolarProxy module integration.

## Known Limitations

These limitations are inherited (from upstream tooling) or by-design (from the project's posture). They are not bugs; they are documented constraints.

### Inherited from PolarProxy upstream

1. **Free tier fails OPEN past the daily cap** — 10 GB / 10 000 sessions / 10 000 rule-matches per day. Past the cap, decryption stops; forwarding continues. Mitigation: monitor decryption-rate divergence + alert; provision paid tier when sustained above cap.
2. **No support for opportunistic STARTTLS / explicit TLS** — SMTP STARTTLS, FTPS AUTH TLS, etc. are not decryptable. Those flows pass through encrypted regardless of the inspection posture.
3. **No ESNI / ECH support** — Sessions using Encrypted SNI / Encrypted Client Hello are not decryptable. Adoption rate of ESNI/ECH on the LAN's outbound destinations affects how much traffic remains opaque.
4. **CA distribution required for every endpoint** — Endpoints without the proxy's CA in their trust store see cert errors. Pinned apps (banking, mobile pinning) reject the proxy's CA regardless. Cert-pinning bypass for some Android apps is possible via Frida-based scripts but out of project scope.
5. **Not FIPS-compliant** — PolarProxy uses non-FIPS-compliant cryptography. On FIPS-enabled hosts it refuses to start.

### Inherited from Suricata upstream

1. **In IPS mode a Suricata crash takes the inspected segment offline UNLESS bypass is configured** — The bridge layer MUST have a failopen mechanism (NFQUEUE `bypass` option, kernel-level bridge passthrough, or systemd-watchdog). Operator decides at M005 module-design.
2. **Custom rule SIDs must avoid reserved upstream ranges** — Suricata reserves SIDs 2200000–2299999 per protocol/component. Local rules must use 1000000–1999999 (per ET/Snort convention) to avoid update collisions.
3. **Hardware offloads (GRO/LRO/TSO) interfere with inline inspection** — Must be disabled on the bridge interfaces to prevent dropped packets from oversized datagrams.

### By-design (project posture)

1. **The bridge as inline data path means a hardware/software failure of the host stops traffic** unless the bridge layer has explicit failopen. Operator's threat model decides: high-trust environment → fail-closed (acceptable downtime); inspection-not-firewall environment → fail-open (network keeps working when inspection is offline).
2. **The wifi as outbound-only management means in-band recovery is limited.** If the wifi misconfigures or the host is unreachable from operator's network, recovery requires local console access. SSH is not bound to the wifi interface; that is by design.
3. **CA distribution is a separate operational track.** PolarProxy's CA must be deployed to LAN endpoints by some mechanism (manual install, AD GPO, MDM, Linux package). root-ghostproxy provides the proxy + CA; deployment is operator's lift.
4. **Two-layer hook architecture means root-ghostproxy's machine-level policy fires across all sister-project Claude Code sessions on the host.** A LAN endpoint with root-ghostproxy installed has its endpoint AI safety policy enforced uniformly across every AI-agent session, regardless of which project that session is operating in. Operator working in another sister project on the same host inherits root-ghostproxy's policy. This is by-design (it's the point of the machine-level layer); the side-effect is that other-project work is constrained by root-ghostproxy's deny-set.
5. **Multi-host portability is intent, not yet realized.** Operator's framing is that root-ghostproxy will be deployable to a new host when needed (`"this machine or another [new] one"`). The current state is single-host. Cross-host deployment may surface host-specific config items (interface device names, CA trust paths, package manager differences) that are currently abstracted but not validated across hosts.

## Cross-References

| For… | Read |
|---|---|
| Architecture topology + component responsibilities | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Design pattern rationale (why deny-by-default, why fail-closed, why two layers) | [DESIGN.md](DESIGN.md) |
| Tool reference (when install scripts + verifier scripts exist) | [TOOLS.md](TOOLS.md) |
| Universal cross-tool agent rules | [AGENTS.md](AGENTS.md) |
| Claude Code-specific routing | [CLAUDE.md](CLAUDE.md) |
| Project front door | [README.md](README.md) |
| Current operational state | [CONTEXT.md](CONTEXT.md) |
| Skills directory context (incl. hook-vs-command-vs-skill decision for safety enforcement) | [SKILLS.md](SKILLS.md) |
| Methodology engine | [wiki/config/methodology.yaml](wiki/config/methodology.yaml) |
| Active SFIF rollout epic | [wiki/backlog/epics/sfif-rollout-and-second-brain-integration.md](wiki/backlog/epics/sfif-rollout-and-second-brain-integration.md) |
| Suricata source-syntheses (Layer 0 README + Layer 1 install/quickstart, IPS modes for Linux, suricata.yaml master config) | `<second-brain>/wiki/sources/src-suricata*.md` |
| PolarProxy source-syntheses (Layer 0 product page + Layer 1 Hanke integration via dummy interface + tcpreplay) | `<second-brain>/wiki/sources/src-polarproxy.md`, `src-hanke-honeypot-polarproxy-suricata-integration.md` |

## Acknowledgments

This SECURITY.md is informed by:
- The upstream Suricata SECURITY.md (severity-tier framing, coordinated-disclosure pattern)
- The upstream PolarProxy product page (license-tier failure semantics, CA-distribution constraints)
- The Hanke honeypot writeup (the Suricata + PolarProxy integration pattern + audit-log routing)
- The second brain's Principle 1 (Infrastructure Over Instructions) — the deny-set + integrity check + tamper detection are structural enforcement, not prose-rule reliance
- The second brain's Principle 4 (Declarations Aspirational Until Verified) — every protection in this document needs a verification gate (verifier script, test, or operator-confirmed observation) before it is real, not aspirational
- Operator's verbatim project framing: *"secure an OS and configure claude code and opencode at the root with all the safety needed"* + *"its IAC and its basically a IPS sitting in between the Edge firewall (OPNSense) and the first switch / the local network"*
