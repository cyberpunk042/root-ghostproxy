#!/usr/bin/env python3
# Regression tests for $HOME/.claude/hooks/agent-output-scan.sh
#
# Per SB-140 forward-fix (Stop hook scanning agent's last assistant turn for
# self-blocking phrases). Verifies: silent on clean output · emits systemMessage
# warning when self-blocking phrase detected · phrase-list extensible via state file.
#
# Run: python3 $HOME/.claude/hooks/tests/test-agent-output-scan.py

import json
import os
import subprocess
import tempfile
from pathlib import Path

HOOK = str(Path.home() / ".claude" / "hooks" / "agent-output-scan.sh")
HOME = Path.home()

passed = 0
failed = 0
results: list = []


def run_hook(stdin_json: str, env_overrides: dict | None = None) -> tuple[int, str]:
    env = os.environ.copy()
    env["CLAUDE_PROJECT_DIR"] = str(HOME)
    if env_overrides:
        env.update(env_overrides)
    r = subprocess.run(
        ["python3", HOOK],
        input=stdin_json,
        env=env,
        capture_output=True, text=True,
        cwd=str(HOME),
    )
    return r.returncode, r.stdout


def expect(label: str, condition: bool, evidence: str = "") -> None:
    global passed, failed
    if condition:
        passed += 1
        results.append(f"✓ {label}")
    else:
        failed += 1
        results.append(f"✗ {label}{(' — ' + evidence) if evidence else ''}")


def make_transcript(messages: list[dict]) -> str:
    """Write transcript JSONL to a tempfile; return path."""
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False)
    for msg in messages:
        f.write(json.dumps(msg) + "\n")
    f.close()
    return f.name


# Ensure executable
if not os.access(HOOK, os.X_OK):
    Path(HOOK).chmod(0o755)


# Test 1: empty stdin → silent exit
rc, out = run_hook("")
expect("T1 empty stdin → silent exit 0", rc == 0 and out == "", f"rc={rc} out='{out}'")


# Test 2: missing transcript_path → silent
rc, out = run_hook(json.dumps({}))
expect("T2 missing transcript_path → silent", rc == 0 and out == "", f"rc={rc} out='{out}'")


# Test 3: nonexistent transcript path → silent
rc, out = run_hook(json.dumps({"transcript_path": "/tmp/nonexistent-xyz.jsonl"}))
expect("T3 nonexistent transcript → silent", rc == 0 and out == "", f"rc={rc} out='{out}'")


# Test 4: clean transcript (no self-blocking phrases) → silent
clean_path = make_transcript([
    {"role": "user", "content": "hi"},
    {"role": "assistant", "content": "Running install.sh real per D024 greenlit. Closes 3 of 4 FAILs."},
])
rc, out = run_hook(json.dumps({"transcript_path": clean_path}))
expect("T4 clean output → silent", rc == 0 and out == "", f"rc={rc} out='{out}'")
os.unlink(clean_path)


# Test 5: transcript with self-blocking phrase → systemMessage warning
flagged_path = make_transcript([
    {"role": "user", "content": "what's next"},
    {"role": "assistant", "content": "T012 install.sh real-execute is operator-driven future-session work; agent can't unilaterally."},
])
rc, out = run_hook(json.dumps({"transcript_path": flagged_path}))
expect("T5 flagged phrase → exit 0", rc == 0, f"rc={rc}")
expect("T5 emits non-empty stdout", bool(out.strip()), "empty")
if out.strip():
    try:
        parsed = json.loads(out)
        expect("T5 stdout valid JSON", True)
        sysmsg = parsed.get("systemMessage", "")
        expect("T5 has systemMessage field", bool(sysmsg))
        expect("T5 systemMessage mentions SB-140", "SB-140" in sysmsg)
        expect("T5 systemMessage names matched phrase", '"operator-driven future-session"' in sysmsg)
    except Exception as e:
        expect("T5 stdout valid JSON", False, str(e))
os.unlink(flagged_path)


# Test 6: multiple matches → all listed
multi_path = make_transcript([
    {"role": "assistant", "content": "T012 is operator-pending decision and SB-117 is operator-Epic-scope"},
])
rc, out = run_hook(json.dumps({"transcript_path": multi_path}))
expect("T6 multiple matches → exit 0", rc == 0)
if out.strip():
    parsed = json.loads(out)
    sysmsg = parsed.get("systemMessage", "")
    expect("T6 first match listed", '"operator-pending decision"' in sysmsg)
    expect("T6 second match listed", '"operator-epic-scope"' in sysmsg.lower())
os.unlink(multi_path)


# Test 7: assistant-content-as-list format (Claude Code transcript shape)
list_path = make_transcript([
    {"role": "assistant", "content": [{"type": "text", "text": "this is operator-pending - but is it really?"}]},
])
rc, out = run_hook(json.dumps({"transcript_path": list_path}))
expect("T7 list-content format → detected", rc == 0 and out.strip() != "")
os.unlink(list_path)


# Test 8: Claude Code session-jsonl shape (.message.role / .message.content)
session_path = make_transcript([
    {"message": {"role": "assistant", "content": "operator-driven future-session per my read"}},
])
rc, out = run_hook(json.dumps({"transcript_path": session_path}))
expect("T8 .message wrapped format → detected", rc == 0 and out.strip() != "")
os.unlink(session_path)


# Test 9-Phase2: extended phrase list (fire-26 self-blocking emits)
phase2_path = make_transcript([
    {"role": "assistant", "content": "agent-actionable substantive work-block exhausted within current authority"},
])
rc, out = run_hook(json.dumps({"transcript_path": phase2_path}))
expect("T9P2 Phase 2 phrase 'exhausted within current authority' detected", rc == 0 and out.strip() != "")
if out.strip():
    sysmsg = json.loads(out).get("systemMessage", "")
    expect("T9P2 phrase listed in warning", "exhausted within current authority" in sysmsg)
os.unlink(phase2_path)

phase2b_path = make_transcript([
    {"role": "assistant", "content": "P4 SB-117 sub-items operator-Epic-scope-pending per literal"},
])
rc, out = run_hook(json.dumps({"transcript_path": phase2b_path}))
expect("T9P2b 'operator-Epic-scope-pending' detected", rc == 0 and out.strip() != "")
os.unlink(phase2b_path)

# Test 9-Phase3: SB-099 abdication-as-freeze phrases (cousin pattern, Phase 3)
phase3_path = make_transcript([
    {"role": "assistant", "content": "Holding here, your move. I'll wait for your call."},
])
rc, out = run_hook(json.dumps({"transcript_path": phase3_path}))
expect("T9P3 SB-099 abdication-phrase 'Holding here, your move' detected",
       rc == 0 and out.strip() != "")
if out.strip():
    sysmsg = json.loads(out).get("systemMessage", "")
    # Hook lowercases matched phrases in warning text
    expect("T9P3 warning lists 'holding here, your move' (case-insensitive)",
           "holding here, your move" in sysmsg.lower())
    expect("T9P3 warning lists 'i'll wait for your call' (case-insensitive)",
           "i'll wait for your call" in sysmsg.lower())
os.unlink(phase3_path)

phase3b_path = make_transcript([
    {"role": "assistant", "content": "I'm not going to act on a guess. Standing by until you direct."},
])
rc, out = run_hook(json.dumps({"transcript_path": phase3b_path}))
expect("T9P3b SB-099 'Standing by until you direct' detected",
       rc == 0 and out.strip() != "")
os.unlink(phase3b_path)

# Test 10: only LAST assistant turn scanned (older clean turns not flagged twice)
multi_turn_path = make_transcript([
    {"role": "assistant", "content": "operator-driven future-session"},  # OLDER turn (would flag)
    {"role": "user", "content": "ok continue"},
    {"role": "assistant", "content": "fixing it now"},  # LATEST turn (clean)
])
rc, out = run_hook(json.dumps({"transcript_path": multi_turn_path}))
expect("T10 only last turn scanned (older flag ignored)", rc == 0 and out == "", f"out='{out}'")
os.unlink(multi_turn_path)


# Summary
print()
for r in results:
    print(r)
print(f"\nResult: {passed}/{passed + failed}")

import sys
sys.exit(0 if failed == 0 else 1)
