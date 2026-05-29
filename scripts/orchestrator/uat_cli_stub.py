#!/usr/bin/env python3
"""Stdlib stub for ``configs/execution.yaml`` UAT of ``route --execute``.

Reads the orchestrator context bundle from stdin and writes a short, deterministic
response to stdout. Used to verify CliAdapter plumbing without API keys or network.
Replace ``cli.command`` with your agent CLI (e.g. ``claude -p``) when ready.
"""
from __future__ import annotations

import sys


def main() -> int:
    bundle = sys.stdin.read()
    lines = [ln for ln in bundle.splitlines() if ln.strip()]
    preview = lines[0][:80] if lines else "(empty bundle)"
    print("orchestrator-uat-stub: ok")
    print(f"bundle_chars={len(bundle)}")
    print(f"bundle_preview={preview!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
