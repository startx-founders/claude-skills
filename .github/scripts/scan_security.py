#!/usr/bin/env python3
"""Conservative hardcoded-credential scan for the skills catalog (Tier 1 gate).

Stdlib only, deterministic, no network. Designed for ~0 false positives so it can
safely block a merge:

  - HIGH-CONFIDENCE credential shapes (private keys, provider token formats) are
    ERRORS that fail the build.
  - A generic `secret = "..."` heuristic is only a WARNING (it is the FP-prone
    one, so it never blocks).
  - Both honor .github/skill-lint/secret-allowlist.txt — one substring per line;
    any match on that line is ignored. Use it for documented example keys.
  - Obvious placeholders (example, your-, xxxx, <...>, ${VAR}, redacted) are
    skipped so teaching material does not trip the scan.

Run locally:  python3 .github/scripts/scan_security.py [repo_root]
"""

import os
import pathlib
import re
import sys

ERRORS = []
WARNINGS = []

# High-confidence: distinctive enough that a real match is almost certainly a
# leaked credential, not prose. These ERROR (block the build).
HIGH_CONFIDENCE = {
    "private key block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
    "AWS access key id": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Anthropic API key": re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}"),
    "OpenAI API key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9]{32,}"),
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "Stripe secret key": re.compile(r"\bsk_live_[A-Za-z0-9]{20,}\b"),
}

# Lower-confidence: a literal assigned to a secret-ish name. WARN only.
GENERIC_ASSIGN = re.compile(
    r"""(?ix)
    \b(?:api[_-]?key|secret|token|password|passwd|client[_-]?secret|access[_-]?key)
    \b \s* [:=] \s* ["']([^"']{12,})["']
    """
)

PLACEHOLDER = re.compile(
    r"(?i)(example|your[-_ ]|xxxx|<[^>]+>|\$\{?[A-Z_]+\}?|redacted|changeme|placeholder|dummy|todo|\.\.\.)"
)

TEXT_EXTS = {".md", ".json", ".jsonc", ".txt", ".sh", ".py", ".js", ".ts", ".yml", ".yaml", ".toml"}


def load_allowlist(root):
    p = root / ".github" / "skill-lint" / "secret-allowlist.txt"
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    allow = load_allowlist(root)

    scan_roots = [root / "skills"]
    mp = root / ".claude-plugin" / "marketplace.json"
    files = []
    for sr in scan_roots:
        if sr.is_dir():
            files += [p for p in sr.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_EXTS]
    if mp.exists():
        files.append(mp)

    for f in sorted(files):
        rel = f.relative_to(root).as_posix()
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if any(a in line for a in allow):
                continue
            for label, rx in HIGH_CONFIDENCE.items():
                if rx.search(line):
                    ERRORS.append(f"{rel}:{i}: possible {label} committed")
            m = GENERIC_ASSIGN.search(line)
            if m and not PLACEHOLDER.search(m.group(1)):
                WARNINGS.append(f"{rel}:{i}: secret-like assignment (verify it is not a real credential)")

    for w in WARNINGS:
        print(f"::warning::{w}")
    if ERRORS:
        for e in ERRORS:
            print(f"::error::{e}")
        print(f"\nsecurity scan FAILED: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        sys.exit(1)
    print(f"security scan OK ({len(WARNINGS)} warning(s))")
    sys.exit(0)


if __name__ == "__main__":
    main()
