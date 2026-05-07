#!/usr/bin/env python3
# Regression tests for end-of-cycle-stamp.sh diff-suppression (operator directive 2026-05-06).
#
# Verifies:
#   - Cold cache → full stamp emitted (~thousands of chars)
#   - Warm cache same semantic content → pointer message (short, contains "unchanged"
#     and "View on demand")
#   - Volatile-stripping: timestamps changing fire-to-fire don't defeat suppression
#   - Cache file written at /tmp/.end-of-cycle-stamp-last-hash
#   - When stamp changes semantically (e.g. priority added) → full re-render
#
# Run: python3 $HOME/.claude/hooks/tests/test-end-of-cycle-stamp-diff-suppression.py

import json
import os
import subprocess
import time
from pathlib import Path

HOME = Path.home()
HOOK = str(HOME / ".claude" / "hooks" / "end-of-cycle-stamp.sh")
CACHE = "/tmp/.end-of-cycle-stamp-last-hash"
PRIORITIES_FILE = HOME / ".claude" / "active-priorities"

passed = 0
failed = 0
results: list = []


def run_hook() -> tuple[int, dict | None]:
    """Fire the hook with a synthetic Stop-event payload; return (rc, parsed-JSON)."""
    payload = json.dumps({
        "hook_event_name": "Stop",
        "cwd": str(HOME),
        "workspace": {"project_dir": str(HOME), "current_dir": str(HOME)},
    })
    env = os.environ.copy()
    env["CLAUDE_PROJECT_DIR"] = str(HOME)
    r = subprocess.run(
        ["python3", HOOK],
        input=payload,
        capture_output=True, text=True,
        env=env, cwd=str(HOME), timeout=20,
    )
    out = r.stdout.strip()
    parsed = None
    if out:
        try:
            parsed = json.loads(out)
        except Exception:
            pass
    return r.returncode, parsed


def expect(label: str, condition: bool, evidence: str = "") -> None:
    global passed, failed
    if condition:
        passed += 1
        results.append(f"✓ {label}")
    else:
        failed += 1
        results.append(f"✗ {label}{(' — ' + evidence) if evidence else ''}")


# Backup cache + priorities
cache_backup = None
if os.path.exists(CACHE):
    with open(CACHE) as f:
        cache_backup = f.read()
prio_backup = None
if PRIORITIES_FILE.exists():
    prio_backup = PRIORITIES_FILE.read_text()

try:
    # Test 1: cold cache → full stamp emitted
    if os.path.exists(CACHE):
        os.unlink(CACHE)
    rc, msg = run_hook()
    expect("fire-1 (cold cache) exits 0", rc == 0)
    expect("fire-1 emits systemMessage", msg is not None and "systemMessage" in (msg or {}))
    if msg and "systemMessage" in msg:
        sm = msg["systemMessage"]
        expect("fire-1 stamp is substantial (>500 chars)", len(sm) > 500, f"len={len(sm)}")
        expect("fire-1 cache file written", os.path.exists(CACHE))

    # Test 2: warm cache, same semantic content → pointer
    time.sleep(1)  # ensure HH:MM:SS timestamp differs
    rc, msg = run_hook()
    expect("fire-2 (warm cache, same state) exits 0", rc == 0)
    if msg and "systemMessage" in msg:
        sm = msg["systemMessage"]
        expect("fire-2 emits pointer (contains 'unchanged')", "unchanged" in sm, sm[:80])
        expect("fire-2 emits pointer (contains 'View on demand')", "View on demand" in sm, sm[:80])
        expect("fire-2 stamp is short (<500 chars)", len(sm) < 500, f"len={len(sm)}")

    # Test 3: volatile-stripping — multiple fires across timestamp change still suppress
    time.sleep(1)
    rc, msg = run_hook()
    if msg and "systemMessage" in msg:
        expect("fire-3 still suppressed (volatile-strip works)", "unchanged" in msg["systemMessage"])

    # Test 4: semantic change → full re-render
    # Replace priorities with just our marker (becomes P1, always rendered)
    PRIORITIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    PRIORITIES_FILE.write_text("TEST-DIFF-SUPPRESSION-MARKER-P1\n")
    rc, msg = run_hook()
    if msg and "systemMessage" in msg:
        sm = msg["systemMessage"]
        expect("fire-4 (semantic change) re-renders full stamp", len(sm) > 500, f"len={len(sm)}")

    # Test 5: cache content is sha256 hex (64 chars)
    if os.path.exists(CACHE):
        with open(CACHE) as f:
            cached = f.read().strip()
        expect("cache content is sha256 hex (64 chars)", len(cached) == 64 and all(c in "0123456789abcdef" for c in cached))

    # === T067: per-row hash cache (Done When #1) ===
    ROW_CACHE = "/tmp/.end-of-cycle-stamp-row-hashes.json"
    if os.path.exists(ROW_CACHE):
        os.unlink(ROW_CACHE)

    # Test 12: Stop hook writes row-hash cache
    rc, msg = run_hook()
    expect("T067 Done#1: row-hash cache file written by hook", os.path.exists(ROW_CACHE))
    if os.path.exists(ROW_CACHE):
        import json as _json
        with open(ROW_CACHE) as f:
            row_hashes = _json.load(f)
        expect("T067 Done#1: cache is dict", isinstance(row_hashes, dict))
        expect("T067 Done#1: cache has multiple rows (≥5 expected)", len(row_hashes) >= 5, f"got {len(row_hashes)} rows")
        # Hashes should be sha256 hex (64 chars)
        all_sha256 = all(len(v) == 64 and all(c in "0123456789abcdef" for c in v) for v in row_hashes.values())
        expect("T067 Done#1: all row-hashes are sha256 hex", all_sha256)

    # === T067 Done When #2: --highlight-deltas flag ===
    import subprocess as _sp
    cycle_cmd = ["python3", "-m", "tools.cycle", "--ansi-horizontal", "--highlight-deltas"]
    r = _sp.run(cycle_cmd, capture_output=True, text=True, cwd=str(HOME), timeout=15)
    expect("T067 Done#2: --highlight-deltas flag exits 0", r.returncode == 0, r.stderr[:200])
    out_clean = r.stdout
    # When cache matches current state, expect no marker on most rows. Just verify the flag doesn't break the render.
    expect("T067 Done#2: --highlight-deltas produces non-empty output", len(out_clean) > 100)

    # Test: corrupt the cache to force a delta on every row → expect markers
    with open(ROW_CACHE, "w") as f:
        f.write('{"Status":"deadbeef","Priorities":"deadbeef","Tracker":"deadbeef","Cursor":"deadbeef"}')
    r2 = _sp.run(cycle_cmd, capture_output=True, text=True, cwd=str(HOME), timeout=15)
    expect("T067 Done#2: corrupt cache → at least one ▶ marker emitted",
           "[Δ]" in r2.stdout, r2.stdout[:300].replace("\x1b[", "ESC["))

    # Test: empty cache file (no rows) → treated as "no prior knowledge" → no markers
    with open(ROW_CACHE, "w") as f:
        f.write("{}")
    r3 = _sp.run(cycle_cmd, capture_output=True, text=True, cwd=str(HOME), timeout=15)
    expect("T067 Done#2: empty cache → no markers (no prior knowledge)", "[Δ]" not in r3.stdout and "[+]" not in r3.stdout, r3.stdout[:300].replace("\x1b[", "ESC["))

    # Test: cache with SUBSET of rows → rows in cache but changed get ▶, rows missing from cache get ＋
    with open(ROW_CACHE, "w") as f:
        f.write('{"Cursor":"deadbeef"}')  # only Cursor present, all other rows new
    r3b = _sp.run(cycle_cmd, capture_output=True, text=True, cwd=str(HOME), timeout=15)
    expect("T067 Done#2: subset cache → ＋ for missing rows", "[+]" in r3b.stdout, r3b.stdout[:300].replace("\x1b[", "ESC["))
    expect("T067 Done#2: subset cache → ▶ for changed cached rows", "[Δ]" in r3b.stdout, r3b.stdout[:300].replace("\x1b[", "ESC["))

    # Test: missing cache file → no markers, no crash
    if os.path.exists(ROW_CACHE):
        os.unlink(ROW_CACHE)
    r4 = _sp.run(cycle_cmd, capture_output=True, text=True, cwd=str(HOME), timeout=15)
    expect("T067 Done#2: missing cache → no crash, no markers", r4.returncode == 0 and "[Δ]" not in r4.stdout and "[+]" not in r4.stdout)

finally:
    # Restore cache + priorities
    if cache_backup is not None:
        with open(CACHE, "w") as f:
            f.write(cache_backup)
    elif os.path.exists(CACHE):
        os.unlink(CACHE)
    # Clean up T067 row-cache (test artifact, no backup needed)
    if os.path.exists("/tmp/.end-of-cycle-stamp-row-hashes.json"):
        os.unlink("/tmp/.end-of-cycle-stamp-row-hashes.json")
    if prio_backup is not None:
        PRIORITIES_FILE.write_text(prio_backup)
    elif PRIORITIES_FILE.exists() and "TEST-DIFF-SUPPRESSION-MARKER" in PRIORITIES_FILE.read_text():
        # Strip our test marker if it crept in
        cleaned = "\n".join(
            ln for ln in PRIORITIES_FILE.read_text().splitlines()
            if "TEST-DIFF-SUPPRESSION-MARKER" not in ln
        )
        if cleaned.strip():
            PRIORITIES_FILE.write_text(cleaned + "\n")
        else:
            PRIORITIES_FILE.unlink()

print()
for line in results:
    print(line)
print()
print(f"Result: {passed}/{passed + failed}")
exit(0 if failed == 0 else 1)
