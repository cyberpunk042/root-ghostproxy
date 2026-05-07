"""tools.objective — mission + focus + impediment state-file management (SB-118 build).

Operator directives 2026-05-06:
  - *"this make me think if we dont also need a current mission and a current
    focus. so that we can keep track of everything and not only the current
    task and its states"*
  - *"we can even add impediment.. this is another sub-level from a focus that
    is blocked for example"*

State-file layers in this project (top → bottom granularity):
    $HOME/.claude/active-mode       — Persona overlay (PM / Architect / Dual). Durable.
    $HOME/.claude/active-mission    — Multi-cycle objective. Durable. (NEW)
    $HOME/.claude/active-focus      — Sub-objective within the mission. Durable. (NEW)
    $HOME/.claude/active-impediment — Sub-level when focus is blocked. Durable. (NEW)
    wiki/backlog/tasks/             — Atomic task cursor.

Layer semantics:
    Mission    = multi-cycle objective the agent drives toward across many
                 cycles ("ship M003 Foundation implement-stage"; "close SB audit").
    Focus      = current sub-objective inside the mission ("install.sh
                 real-execute on sandbox host"; "drift-fix doc layer").
    Impediment = the specific block on the current focus, when focus is stuck
                 (e.g. focus="install.sh real-execute" + impediment="awaiting
                 D024 operator turn-on"; OR focus="ship hook X" + impediment=
                 "policy-block false-positive on `.jsonl` extension"). Empty
                 = focus is unblocked. NOT a permanent layer; comes and goes.

This tool writes single-line text values to each state file. Slash commands
`/mission`, `/focus`, `/impediment` accept free-form text + dispatch verbs
(set / clear / show). The mode-enforcement.sh hook reads all three + surfaces
them in the LIVE STATE additionalContext (parallel to active-mode + open-SBs
+ recent-logs + task-cursor).

Schema: each file is a single-line text value (no JSON). Empty file = unset.

Composes-with:
- Slash commands: /mission, /focus, /impediment (3 thin wrappers per state-file layer)
- Hooks: mode-enforcement.sh reads all 3 state files + surfaces in LIVE STATE additionalContext
  (per-prompt banner); end-of-cycle-stamp.sh reads them for stamp render
- MCP: root_objective tool at tools.mcp_server wraps the read side for sub-agents
- Sister tools: tools.priorities (imminent-work hot-queue ABOVE this layer per SB-127);
  tools.questions (E003 retention layer for agent-pending questions)

State-file layer hierarchy (top → bottom granularity):
    active-mode → active-priorities → active-mission → active-focus → active-impediment
                                                                      → active-task (cursor)

Idempotency invariant: set/clear write atomic single-line files; show is read-only;
empty file = unset (treated as "no value" by mode-enforcement banner).

Action vocabulary (Hard Rule 14): emits `operator-directive-register` (set/clear paths)
OR `read-only-audit` (show path) per the M-E001-1 vocabulary at
wiki/log/2026-05-06-181500-auto-pilot-action-vocabulary-draft.md.

Test file: tools/tests/test-objective.py (run via `python3 -m tools.run-tests`).

Brain-improvement mandate: wiki/log/2026-05-06-194730-brain-improvement-mandate-readme-first.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
MISSION_PATH = CLAUDE_DIR / "active-mission"
FOCUS_PATH = CLAUDE_DIR / "active-focus"
IMPEDIMENT_PATH = CLAUDE_DIR / "active-impediment"

LAYER_PATHS = {
    "mission": MISSION_PATH,
    "focus": FOCUS_PATH,
    "impediment": IMPEDIMENT_PATH,
}
LAYER_NAMES = ("mission", "focus", "impediment")


def _path(layer: str) -> Path:
    if layer not in LAYER_PATHS:
        raise ValueError(f"layer must be one of {LAYER_NAMES}, got {layer!r}")
    return LAYER_PATHS[layer]


def read_layer(layer: str) -> str:
    p = _path(layer)
    if not p.exists():
        return ""
    try:
        return p.read_text().strip()
    except Exception:
        return ""


def write_layer(layer: str, text: str) -> None:
    p = _path(layer)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n")


def clear_layer(layer: str) -> bool:
    p = _path(layer)
    if p.exists():
        p.unlink()
        return True
    return False


def cmd_set(args: argparse.Namespace) -> int:
    text = " ".join(args.text).strip()
    if not text:
        print(f"ERROR: text required for {args.layer} set", file=sys.stderr)
        return 2
    write_layer(args.layer, text)
    print(f"OK: {args.layer} set: {text}")
    print(f"  ({_path(args.layer)})")
    return 0


def cmd_clear(args: argparse.Namespace) -> int:
    if clear_layer(args.layer):
        print(f"OK: {args.layer} cleared ({_path(args.layer)})")
    else:
        print(f"OK: {args.layer} already absent ({_path(args.layer)})")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    if args.layer:
        layers = [args.layer]
    else:
        layers = list(LAYER_NAMES)
    for layer in layers:
        val = read_layer(layer)
        if val:
            print(f"{layer}: {val}")
        else:
            print(f"{layer}: (unset)")
        if args.verbose:
            print(f"  path: {_path(layer)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage active-mission + active-focus state files")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_set = sub.add_parser("set", help="set mission|focus|impediment text")
    p_set.add_argument("layer", choices=list(LAYER_NAMES))
    p_set.add_argument("text", nargs="+", help="text value (multi-word OK)")
    p_set.set_defaults(func=cmd_set)

    p_clear = sub.add_parser("clear", help="clear mission|focus|impediment state file")
    p_clear.add_argument("layer", choices=list(LAYER_NAMES))
    p_clear.set_defaults(func=cmd_clear)

    p_show = sub.add_parser("show", help="show mission and/or focus and/or impediment")
    p_show.add_argument("layer", nargs="?", choices=list(LAYER_NAMES))
    p_show.add_argument("-v", "--verbose", action="store_true")
    p_show.set_defaults(func=cmd_show)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
