#!/usr/bin/env python3
"""Regression tests for tools/stamp.py — persistent stamp-render config (SB-115).

stamp.py owns $HOME/.claude/stamp-config.json, which end-of-cycle-stamp.sh reads
on every Stop event to decide layout / enabled / density. The load-bearing logic
is load_config()'s DEFENSIVE SANITIZATION: an invalid or corrupt value in the
JSON must be coerced back to a safe default rather than propagated to the render
hook (a bad `enabled` value that slipped through would make the stamp render or
hide incorrectly every turn). A refactor that dropped a validation branch would
fail silently — these tests pin it. Zero coverage until now.

Isolation: config path is HOME-derived. load_config/save_config run in-process
with the module global CONFIG_PATH repointed at a temp file; the configure/clear
CLI runs as a subprocess with HOME at a temp dir.

Emits the canonical `Result: N/M passed` line consumed by tools.run-tests.
Exit 0 iff all pass.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

import tools.stamp as stamp  # noqa: E402

PASSED: list[str] = []
FAILED: list[tuple[str, str]] = []


def check(label: str, cond: bool, detail: str = "") -> None:
    if cond:
        PASSED.append(label)
        print(f"  PASS {label}")
    else:
        FAILED.append((label, detail))
        print(f"  FAIL {label}" + (f" — {detail}" if detail else ""))


def cfg_file(content: str | None) -> Path:
    d = Path(tempfile.mkdtemp(prefix="stamp-test-"))
    p = d / "stamp-config.json"
    if content is not None:
        p.write_text(content)
    return p


def use(path: Path) -> None:
    stamp.CONFIG_PATH = path  # module global read at call time


def test_defaults_when_absent() -> None:
    use(cfg_file(None))  # no file
    check("absent config → DEFAULT_CONFIG", stamp.load_config() == stamp.DEFAULT_CONFIG)


def test_valid_config_merges() -> None:
    use(cfg_file(json.dumps({"layout": "horizontal", "enabled": "on", "density": "minified"})))
    c = stamp.load_config()
    check("valid values load through", c["layout"] == "horizontal" and c["enabled"] == "on" and c["density"] == "minified")
    # A partial config keeps defaults for the missing keys.
    use(cfg_file(json.dumps({"layout": "horizontal"})))
    c2 = stamp.load_config()
    check("partial config keeps defaults for missing keys", c2["layout"] == "horizontal" and c2["enabled"] == "auto" and c2["density"] == "standard")


def test_invalid_values_sanitized() -> None:
    use(cfg_file(json.dumps({"layout": "diagonal", "enabled": "maybe", "density": "huge"})))
    c = stamp.load_config()
    check("invalid layout → default (vertical)", c["layout"] == "vertical")
    check("invalid enabled → default (auto)", c["enabled"] == "auto")
    check("invalid density → default (standard)", c["density"] == "standard")


def test_corrupt_and_wrongtype() -> None:
    use(cfg_file("{ this is not json"))
    check("non-JSON garbage → DEFAULT_CONFIG", stamp.load_config() == stamp.DEFAULT_CONFIG)
    use(cfg_file(json.dumps([1, 2, 3])))  # valid JSON, wrong type
    check("non-dict JSON → DEFAULT_CONFIG", stamp.load_config() == stamp.DEFAULT_CONFIG)


def test_save_roundtrip() -> None:
    p = cfg_file(None)
    use(p)
    stamp.save_config({"layout": "horizontal", "enabled": "off", "density": "extended", "highlight_deltas": True})
    check("save writes parseable JSON", json.loads(p.read_text())["layout"] == "horizontal")
    check("save→load round-trips values", stamp.load_config()["enabled"] == "off")


# --- CLI (subprocess, HOME-isolated) ---
def _cli(home: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "tools.stamp", *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
        env={"HOME": str(home), "PATH": os.environ.get("PATH", "")},
    )


def _read_cfg(home: Path) -> dict:
    f = home / ".claude" / "stamp-config.json"
    return json.loads(f.read_text()) if f.exists() else {}


def test_cli_configure() -> None:
    h = Path(tempfile.mkdtemp(prefix="stamp-home-"))
    r = _cli(h, "configure", "--layout", "horizontal")
    check("configure --layout persists", r.returncode == 0 and _read_cfg(h).get("layout") == "horizontal")
    # highlight-deltas string coerces to a bool in the saved config.
    _cli(h, "configure", "--highlight-deltas", "true")
    check("configure --highlight-deltas true → bool True", _read_cfg(h).get("highlight_deltas") is True)
    _cli(h, "configure", "--highlight-deltas", "false")
    check("configure --highlight-deltas false → bool False", _read_cfg(h).get("highlight_deltas") is False)
    # invalid value rejected by argparse choices.
    r2 = _cli(h, "configure", "--enabled", "sometimes")
    check("configure invalid --enabled → exit 2", r2.returncode == 2)
    # re-setting the same value reports unchanged.
    _cli(h, "configure", "--layout", "vertical")
    r3 = _cli(h, "configure", "--layout", "vertical")
    check("configure same value → 'unchanged'", "unchanged" in r3.stdout)


def test_cli_clear() -> None:
    h = Path(tempfile.mkdtemp(prefix="stamp-home-"))
    _cli(h, "configure", "--layout", "horizontal")
    check("config exists before clear", (h / ".claude" / "stamp-config.json").exists())
    r = _cli(h, "clear")
    check("clear removes config (defaults reapply)", r.returncode == 0 and not (h / ".claude" / "stamp-config.json").exists())
    check("clear on absent → rc 0", _cli(h, "clear").returncode == 0)


def main() -> int:
    print("=== tools.stamp regression tests ===")
    for t in (
        test_defaults_when_absent, test_valid_config_merges, test_invalid_values_sanitized,
        test_corrupt_and_wrongtype, test_save_roundtrip, test_cli_configure, test_cli_clear,
    ):
        t()
    total = len(PASSED) + len(FAILED)
    print()
    print(f"Result: {len(PASSED)}/{total} passed")
    for label, detail in FAILED:
        print(f"  - {label}: {detail}")
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
