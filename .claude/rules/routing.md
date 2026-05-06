# $HOME/.claude/rules/routing.md — Operator intent → tool routing for root-ghostproxy

> Loaded on demand when operator intent is ambiguous. CLAUDE.md has the summary delta; this file has the routing table for THIS project (OS-setup IaC at /root).

## Mechanism Selection (commands vs hooks vs MCP vs CLI)

| Mechanism | Determinism | Trigger | Use when |
|---|---|---|---|
| **Hook** | Logical (block + reason + remediation) | Tool-call lifecycle event | Structural enforcement at $HOME/.claude/hooks/. Currently 7 fires across 5 events: policy-block (PreToolUse — deny secret reads), malware-block (PreToolUse — deny dangerous bash), leak-detector (PostToolUse — exfil scan), session-start (SessionStart — security envelope confirm), session-orient (SessionStart — project priming + /orient direction), post-compact (PostCompact — re-orient after compaction), session-summary (SessionEnd — summary). |
| **Command** (`.claude/commands/`) | 100% deterministic | Operator types `/<name>` | Workflow with predictable scripted steps. NONE built yet for this project — author when a workflow stabilizes. |
| **Skill** (`.claude/skills/`) | ~70% deterministic | Auto-trigger on description match | Auto-trigger workflows. NONE built yet for this project. |
| **MCP tool** | Programmatic | AI invokes during reasoning | Discrete operations. None local; this project consumes the second brain's 28 MCP tools (deferred load via ToolSearch). |
| **CLI** | Programmatic | AI runs via Bash | Shell-mediated ops. install.sh / uninstall.sh are local; tools.* are at <second-brain>/. |

## Operator-intent routing (this project)

| Operator says... | First action | Tool |
|---|---|---|
| `"build the bridge"` / `"set up L2"` | Read SFIF stage in CONTEXT.md → check M003 (Foundation hardening) tasks | wiki/backlog/tasks/_index.md |
| `"install"` / `"run install.sh"` | Confirm dry-run first; SFIF Foundation tasks gate this | install.sh + T013 |
| `"verify state"` | Run BOOTSTRAP.md's 4 verify commands | BOOTSTRAP.md |
| `"status"` / `"where are we"` | Show SFIF stage + active modules + pending-decision tasks | CONTEXT.md + _index.md |
| `"add Suricata"` / `"PolarProxy"` | M005 territory; check ordering against ccstatusline (M011 ordered before M005) | M005 / M011 module pages |
| `"connect to second brain"` | M007 — `tools.setup --connect-project /root --dry-run` first | M007 task pages T038-T043 |
| `"verify second brain knows /root"` | T053 — `gateway query --backlog`, sister-projects.yaml grep | T053 |
| `"ingest a URL"` | NOT this project's role. Route to second brain (`pipeline fetch` / `wiki_fetch` MCP from /opt). | second brain |
| `"the operator said X"` (verbatim) | Log verbatim to `$HOME/wiki/log/<date>-<slug>.md` BEFORE acting. **NOT** `/opt/.../raw/notes/` — that's the second-brain's own layer; /root must not write there. | /root iteration log |
| `"check pending decisions"` | List `pending-operator-decision` tasks | _index.md status table |
| `"claim a task"` | List `not-started` with no `BLOCKED BY` outstanding → operator picks → work it per Done When + stage gate | _index.md → T###*.md |

## Cross-references

- `<second-brain>/.claude/rules/routing.md` — second brain's full 24-row table + 28-tool MCP catalog. This project consumes from there.
- `$HOME/CLAUDE.md` — Claude-Code-specific delta + operator-intent summary.
- `$HOME/AGENTS.md` — universal cross-tool agent contract (canonical envelope, hook firing order).
- `$HOME/BOOTSTRAP.md` — cold-pickup guide (read first).
