/**
 * claude-bridge — opencode plugin that delegates security policy to
 * Claude Code's settings.json + hook scripts.
 *
 * Single source of truth: ~/.claude/settings.json
 *   - permissions.deny  → enforced before each tool call
 *   - hooks.PreToolUse  → spawned with Claude Code stdin contract
 *   - hooks.PostToolUse → spawned after tool completes
 *   - hooks.SessionStart / SessionEnd → fired on opencode session events
 *
 * This bridge does NOT reproduce policy. It loads it from disk and runs
 * the same scripts Claude Code runs, with the same JSON-on-stdin contract,
 * and parses the same JSON-on-stdout response.
 */

import type { Plugin } from "@opencode-ai/plugin"
import { spawn } from "node:child_process"
import { readFileSync, existsSync } from "node:fs"
import { homedir } from "node:os"
import { join } from "node:path"

// ---------------------------------------------------------------------------
// Types matching Claude Code's settings.json shape
// ---------------------------------------------------------------------------

type ClaudeHookEntry = {
  matcher: string
  hooks: Array<{
    type: "command"
    command: string
    timeout?: number
  }>
}

type ClaudeSettings = {
  permissions?: {
    deny?: string[]
    allow?: string[]
    ask?: string[]
    disableBypassPermissionsMode?: string
  }
  hooks?: {
    PreToolUse?: ClaudeHookEntry[]
    PostToolUse?: ClaudeHookEntry[]
    SessionStart?: ClaudeHookEntry[]
    SessionEnd?: ClaudeHookEntry[]
  }
  disableAllHooks?: boolean
}

type HookStdoutDecision = {
  hookSpecificOutput?: {
    hookEventName?: string
    permissionDecision?: "allow" | "deny" | "ask"
    permissionDecisionReason?: string
    additionalContext?: string
  }
  systemMessage?: string
}

// ---------------------------------------------------------------------------
// Tool name mapping: opencode → Claude Code
// Hooks key off the Claude Code name. Unknown tools pass through unchanged
// so MCP tools (mcp__server__name) match the mcp__.* matcher untouched.
// ---------------------------------------------------------------------------

const TOOL_MAP: Record<string, string> = {
  bash: "Bash",
  read: "Read",
  write: "Write",
  edit: "Edit",
  multiedit: "Edit",
  patch: "Edit",
  glob: "Glob",
  grep: "Grep",
  webfetch: "WebFetch",
  websearch: "WebSearch",
  task: "Agent",
  todowrite: "TaskUpdate",
  todoread: "TaskList",
}

function mapTool(opencodeName: string): string {
  return TOOL_MAP[opencodeName] ?? opencodeName
}

// ---------------------------------------------------------------------------
// permissions.deny matcher
//
// Claude rule syntax: `Tool(glob)` — e.g. `Read(.env)`, `Bash(cat *.env)`,
// `Read(**/*.pem)`. Glob: `**` = any depth, `*` = single segment-ish
// (we treat it permissively since policy-block.sh has its own deeper scan).
// ---------------------------------------------------------------------------

type DenyRule = { tool: string; pattern: RegExp; raw: string }

function parseDenyRules(rules: string[]): DenyRule[] {
  const out: DenyRule[] = []
  for (const raw of rules) {
    const m = raw.match(/^([A-Za-z_][\w]*(?:__[\w]+)*)\((.*)\)$/)
    if (!m) continue
    const tool = m[1]
    const glob = m[2]
    const re = globToRegex(glob)
    out.push({ tool, pattern: re, raw })
  }
  return out
}

function globToRegex(glob: string): RegExp {
  let re = ""
  for (let i = 0; i < glob.length; i++) {
    const c = glob[i]
    if (c === "*") {
      if (glob[i + 1] === "*") {
        re += ".*"
        i++
      } else {
        re += "[^/]*"
      }
    } else if (/[.+?^${}()|[\]\\]/.test(c)) {
      re += "\\" + c
    } else {
      re += c
    }
  }
  // Anchored: must match the whole argument string. We use a leading .* so
  // path tails like "/etc/foo/.env" still match a rule like ".env".
  return new RegExp("^(?:.*/)?" + re + "$")
}

// Pull the path-/command-shaped argument out of an opencode tool's args,
// mirroring policy-block.sh's per-tool field selection.
function extractMatchTargets(claudeTool: string, args: any): string[] {
  if (!args || typeof args !== "object") return []
  const out: string[] = []
  switch (claudeTool) {
    case "Read":
      out.push(args.file_path ?? args.filePath ?? args.path ?? "")
      break
    case "Bash":
      out.push(args.command ?? "")
      break
    case "Edit":
      out.push(args.file_path ?? args.filePath ?? args.path ?? "")
      // multiedit-shaped opencode args
      if (Array.isArray(args.edits)) {
        for (const e of args.edits) out.push(e.file_path ?? e.path ?? "")
      }
      break
    case "Write":
      out.push(args.file_path ?? args.filePath ?? args.path ?? "")
      break
    case "Glob":
      out.push(args.pattern ?? "")
      out.push(args.path ?? "")
      break
    case "Grep":
      out.push(args.path ?? "")
      out.push(args.glob ?? "")
      break
    case "WebFetch":
      out.push(args.url ?? "")
      break
    case "WebSearch":
      out.push(args.query ?? "")
      break
    default:
      // For unknown / mcp__ tools, scan all string values shallowly.
      for (const v of Object.values(args)) {
        if (typeof v === "string") out.push(v)
      }
  }
  return out.filter((s) => typeof s === "string" && s.length > 0)
}

// ---------------------------------------------------------------------------
// Settings loader (re-read on every session start so edits take effect)
// ---------------------------------------------------------------------------

const SETTINGS_PATH = join(homedir(), ".claude", "settings.json")

function loadSettings(): ClaudeSettings {
  try {
    if (!existsSync(SETTINGS_PATH)) {
      console.error(
        `[claude-bridge] ${SETTINGS_PATH} missing — running with NO security policy. Install Claude Code config first.`,
      )
      return {}
    }
    const raw = readFileSync(SETTINGS_PATH, "utf8")
    return JSON.parse(raw) as ClaudeSettings
  } catch (e) {
    console.error(
      `[claude-bridge] failed to parse ${SETTINGS_PATH}: ${(e as Error).message}. Failing closed — every tool call denied.`,
    )
    // Fail closed: synthesize a settings object that denies everything.
    return {
      permissions: { deny: ["Bash(*)", "Read(*)", "Edit(*)", "Write(*)"] },
    }
  }
}

// ---------------------------------------------------------------------------
// Hook spawn — Claude Code stdin/stdout contract
// ---------------------------------------------------------------------------

type HookInputBase = {
  session_id: string
  hook_event_name: string
  tool_name?: string
  tool_input?: any
  tool_response?: any
}

async function runHookCommand(
  command: string,
  timeoutSec: number,
  input: HookInputBase,
): Promise<HookStdoutDecision | null> {
  return new Promise((resolve) => {
    const proc = spawn("/bin/sh", ["-c", command], {
      stdio: ["pipe", "pipe", "pipe"],
    })
    let stdout = ""
    let stderr = ""
    const timeoutMs = Math.max(1000, (timeoutSec || 5) * 1000)
    const timer = setTimeout(() => {
      try {
        proc.kill("SIGKILL")
      } catch {}
    }, timeoutMs)

    proc.stdout.on("data", (b) => (stdout += b.toString("utf8")))
    proc.stderr.on("data", (b) => (stderr += b.toString("utf8")))
    proc.on("close", (code) => {
      clearTimeout(timer)
      if (stderr.trim()) {
        console.error(`[claude-bridge] hook stderr (${command}): ${stderr.trim()}`)
      }
      if (code !== 0 && code !== null) {
        // Non-zero exit. Treat as deny defensively, but only if the hook
        // didn't already emit a structured deny on stdout.
        const parsed = tryParseDecision(stdout)
        if (parsed?.hookSpecificOutput?.permissionDecision) {
          return resolve(parsed)
        }
        return resolve({
          hookSpecificOutput: {
            permissionDecision: "deny",
            permissionDecisionReason: `Hook ${command} exited ${code}: ${stderr.trim() || "(no stderr)"}`,
          },
        })
      }
      resolve(tryParseDecision(stdout))
    })
    proc.on("error", (err) => {
      clearTimeout(timer)
      resolve({
        hookSpecificOutput: {
          permissionDecision: "deny",
          permissionDecisionReason: `Hook ${command} failed to spawn: ${err.message}`,
        },
      })
    })

    try {
      proc.stdin.write(JSON.stringify(input))
      proc.stdin.end()
    } catch {}
  })
}

function tryParseDecision(stdout: string): HookStdoutDecision | null {
  const s = stdout.trim()
  if (!s) return null
  try {
    return JSON.parse(s) as HookStdoutDecision
  } catch {
    // Hook printed non-JSON. Treat as advisory / informational.
    return { systemMessage: s }
  }
}

// ---------------------------------------------------------------------------
// Hook dispatcher: run all entries whose matcher regex matches the tool name.
// First DENY wins. ASK is downgraded to DENY in v1 (TODO: wire to
// opencode's permission.ask prompt in phase 2).
// ---------------------------------------------------------------------------

type Verdict = {
  decision: "allow" | "deny"
  reason?: string
  systemMessages: string[]
  additionalContext: string[]
}

async function runHookEntries(
  entries: ClaudeHookEntry[] | undefined,
  toolName: string | undefined,
  input: HookInputBase,
): Promise<Verdict> {
  const verdict: Verdict = {
    decision: "allow",
    systemMessages: [],
    additionalContext: [],
  }
  if (!entries || entries.length === 0) return verdict
  for (const entry of entries) {
    if (toolName && entry.matcher && entry.matcher !== "") {
      let matcherRe: RegExp
      try {
        matcherRe = new RegExp("^(?:" + entry.matcher + ")$")
      } catch {
        continue
      }
      if (!matcherRe.test(toolName)) continue
    }
    for (const h of entry.hooks ?? []) {
      const decision = await runHookCommand(h.command, h.timeout ?? 5, input)
      if (!decision) continue
      if (decision.systemMessage) verdict.systemMessages.push(decision.systemMessage)
      const hso = decision.hookSpecificOutput
      if (hso?.additionalContext) verdict.additionalContext.push(hso.additionalContext)
      const d = hso?.permissionDecision
      if (d === "deny" || d === "ask") {
        verdict.decision = "deny"
        verdict.reason = hso?.permissionDecisionReason ?? `Blocked by ${h.command}`
        return verdict // first deny wins
      }
    }
  }
  return verdict
}

// ---------------------------------------------------------------------------
// Plugin entrypoint
// ---------------------------------------------------------------------------

const seenSessions = new Set<string>()

const plugin: Plugin = async ({ client }) => {
  let settings = loadSettings()
  let denyRules = parseDenyRules(settings.permissions?.deny ?? [])

  function reload() {
    settings = loadSettings()
    denyRules = parseDenyRules(settings.permissions?.deny ?? [])
  }

  function surface(messages: string[]) {
    for (const m of messages) {
      // stderr always (visible with --print-logs), and best-effort TUI toast.
      console.error(`[claude-bridge] ${m}`)
      try {
        // @ts-ignore — event.publish exists at runtime even if SDK types drift
        client.event?.publish?.({
          body: {
            type: "tui.toast.show",
            properties: { variant: "warning", message: m },
          },
        })
      } catch {}
    }
  }

  return {
    async event({ event }) {
      if (event.type === "session.created") {
        const sid = event.properties.info.id
        if (!seenSessions.has(sid)) {
          seenSessions.add(sid)
          reload() // pick up any settings edits between sessions
          const v = await runHookEntries(settings.hooks?.SessionStart, undefined, {
            session_id: sid,
            hook_event_name: "SessionStart",
          })
          surface(v.systemMessages)
        }
      } else if (event.type === "session.deleted") {
        const sid = event.properties.info.id
        const v = await runHookEntries(settings.hooks?.SessionEnd, undefined, {
          session_id: sid,
          hook_event_name: "SessionEnd",
        })
        surface(v.systemMessages)
        seenSessions.delete(sid)
      }
    },

    async "tool.execute.before"(input, output) {
      if (settings.disableAllHooks === true) return
      const claudeTool = mapTool(input.tool)

      // (1) permissions.deny — same syntax as Claude Code, enforced here so
      // opencode obeys the exact same rule list with no duplication.
      for (const rule of denyRules) {
        if (rule.tool !== claudeTool && rule.tool !== input.tool) continue
        const targets = extractMatchTargets(claudeTool, output.args)
        for (const t of targets) {
          if (rule.pattern.test(t)) {
            const msg = `Blocked by permissions.deny rule '${rule.raw}' (target='${t}'). Source: ~/.claude/settings.json. Tool: ${input.tool}→${claudeTool}.`
            surface([msg])
            throw new Error(msg)
          }
        }
      }

      // (2) PreToolUse hooks — Claude Code stdin contract.
      const v = await runHookEntries(settings.hooks?.PreToolUse, claudeTool, {
        session_id: input.sessionID,
        hook_event_name: "PreToolUse",
        tool_name: claudeTool,
        tool_input: output.args,
      })
      surface(v.systemMessages)
      if (v.decision === "deny") {
        throw new Error(
          `Blocked by Claude PreToolUse hook: ${v.reason ?? "(no reason)"}`,
        )
      }
    },

    async "tool.execute.after"(input, output) {
      if (settings.disableAllHooks === true) return
      const claudeTool = mapTool(input.tool)
      const v = await runHookEntries(settings.hooks?.PostToolUse, claudeTool, {
        session_id: input.sessionID,
        hook_event_name: "PostToolUse",
        tool_name: claudeTool,
        tool_input: input.args,
        tool_response: { output: output.output, metadata: output.metadata },
      })
      surface(v.systemMessages)
      // additionalContext can't be injected into next LLM turn from this hook
      // point; it's already logged by the hook script (e.g. leaks.log) and
      // surfaced to the user as a systemMessage. v2: wire to a chat hook.
      if (v.additionalContext.length) {
        console.error(
          `[claude-bridge] PostToolUse additionalContext (logged-only): ${v.additionalContext.join(" | ")}`,
        )
      }
    },
  }
}

export default { id: "claude-bridge", server: plugin }
