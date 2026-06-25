#!/usr/bin/env python3
"""Deterministic content lint for the StartX skills catalog.

Codifies the checks a curator would otherwise run by hand on every skill PR.
Stdlib only (no pip install in CI), no network, no model calls: same inputs
always produce the same verdict. This is an advisory check (it is not a
required status check), so a red run flags problems for curators without
hard-blocking a merge.

Two layers:
  1. Repo-wide structural integrity (applies to every local skill):
       - marketplace.json and the on-disk skills/ tree agree (no skill is
         registered-but-missing, none is on-disk-but-unregistered).
       - each SKILL.md has valid frontmatter; name matches its directory and
         its marketplace entry; name is kebab-case; description is non-empty.
  2. Opt-in per-author rules (.github/skill-lint/<author>.json):
       - shared_blocks: named "## sections" that must be byte-identical across
         every skill that author ships (catches silent drift in a shared layer).
       - forbid_em_dash / banned_words: a house style an author commits to, so
         the SKILL.md files practice what they preach.

Run locally:  python3 .github/scripts/validate_skills.py [repo_root]
"""

import json
import os
import pathlib
import re
import sys

ERRORS = []
WARNINGS = []


def err(msg):
    ERRORS.append(msg)


def warn(msg):
    WARNINGS.append(msg)


def parse_frontmatter(text):
    """Parse a leading `--- ... ---` YAML-ish frontmatter block into a dict.

    Only flat `key: value` pairs are supported (with naive line continuation),
    which is all a SKILL.md frontmatter uses. Returns None if absent/malformed.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip("\n")
    fm = {}
    key = None
    for line in block.split("\n"):
        m = re.match(r"^([A-Za-z0-9_-]+):\s?(.*)$", line)
        if m:
            key = m.group(1)
            fm[key] = m.group(2).strip()
        elif key is not None and line.strip():
            fm[key] = (fm[key] + " " + line.strip()).strip()
    return fm


def body_after_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            nl = text.find("\n", end + 1)
            return text[nl + 1:] if nl != -1 else ""
    return text


def section(text, header):
    """Return the body of a `## <header>` section, trimmed, or None."""
    m = re.search(
        r"(?m)^##\s+" + re.escape(header) + r"\s*$\n(.*?)(?=^##\s|\Z)",
        text,
        re.S,
    )
    return m.group(1).strip() if m else None


def local_source_path(entry):
    """Return the repo-relative dir a marketplace entry points to, if local.

    Local skills use a string `source` like "./skills/1SF/foo"; remote skills
    use an object source ({"source": "github", ...}) and are not in this repo.
    """
    src = entry.get("source")
    if isinstance(src, str):
        return src.lstrip("./").rstrip("/")
    return None


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    mp_path = root / ".claude-plugin" / "marketplace.json"
    if not mp_path.exists():
        err(".claude-plugin/marketplace.json is missing")
        return finish()
    try:
        mp = json.loads(mp_path.read_text())
    except json.JSONDecodeError as e:
        err(f"marketplace.json is not valid JSON: {e}")
        return finish()

    plugins = mp.get("plugins", []) or []

    # Map local marketplace entries by the dir they claim.
    entry_by_path = {}
    for entry in plugins:
        rel = local_source_path(entry)
        if rel is None:
            continue  # remote-sourced plugin, lives in another repo
        entry_by_path[rel] = entry
        skill_dir = root / rel
        if not (skill_dir / "SKILL.md").exists():
            err(f"marketplace entry '{entry.get('name')}' points to "
                f"'{rel}' but {rel}/SKILL.md does not exist")

    # Walk every skill on disk: skills/<author>/<skill>/SKILL.md
    skills_root = root / "skills"
    by_author = {}
    for skill_md in sorted(skills_root.glob("*/*/SKILL.md")):
        skill_dir = skill_md.parent
        rel = skill_dir.relative_to(root).as_posix()
        author = skill_dir.parent.name
        dir_name = skill_dir.name
        by_author.setdefault(author, []).append(skill_md)

        text = skill_md.read_text()
        fm = parse_frontmatter(text)
        if fm is None:
            err(f"{rel}/SKILL.md: missing or malformed frontmatter")
            continue
        name = fm.get("name", "").strip()
        desc = fm.get("description", "").strip()
        if not name:
            err(f"{rel}/SKILL.md: frontmatter has no 'name'")
        if not desc:
            err(f"{rel}/SKILL.md: frontmatter has no 'description'")
        if name and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
            err(f"{rel}/SKILL.md: name '{name}' is not kebab-case")
        if name and name != dir_name:
            err(f"{rel}/SKILL.md: name '{name}' does not match directory "
                f"'{dir_name}'")

        entry = entry_by_path.get(rel)
        if entry is None:
            err(f"{rel} has a SKILL.md but no marketplace.json entry "
                f"(skill is unregistered and will not install)")
        elif name and entry.get("name") != name:
            err(f"{rel}: marketplace name '{entry.get('name')}' != SKILL.md "
                f"name '{name}'")

    # Opt-in per-author rules.
    lint_dir = root / ".github" / "skill-lint"
    for author, skill_mds in sorted(by_author.items()):
        cfg_path = lint_dir / f"{author}.json"
        if not cfg_path.exists():
            continue
        try:
            cfg = json.loads(cfg_path.read_text())
        except json.JSONDecodeError as e:
            err(f".github/skill-lint/{author}.json is not valid JSON: {e}")
            continue
        texts = {p.parent.name: p.read_text() for p in skill_mds}

        # Shared blocks must be byte-identical wherever they appear.
        for header in cfg.get("shared_blocks", []):
            present = {n: section(t, header) for n, t in texts.items()}
            present = {n: b for n, b in present.items() if b is not None}
            distinct = set(present.values())
            if len(distinct) > 1:
                names = ", ".join(sorted(present))
                err(f"[{author}] shared block '## {header}' has drifted: "
                    f"not identical across {names}")

        # Em dashes only. We deliberately do NOT lint banned vocabulary here:
        # these are teaching docs that quote the banned words as bad examples
        # ("people say it is interesting" as a demand red flag), so a word scan
        # cannot tell a real style slip from a quoted warning. The skills
        # already self-enforce banned vocabulary on their *generated output*.
        if cfg.get("forbid_em_dash", False):
            for skill_name, text in texts.items():
                rel = f"skills/{author}/{skill_name}/SKILL.md"
                for i, line in enumerate(text.split("\n"), 1):
                    if "—" in line:
                        err(f"{rel}:{i}: em dash (—) is banned by "
                            f"{author}'s house style")

    return finish()


def finish():
    for w in WARNINGS:
        print(f"::warning::{w}")
    if ERRORS:
        for e in ERRORS:
            print(f"::error::{e}")
        print(f"\nskill content lint FAILED: {len(ERRORS)} error(s), "
              f"{len(WARNINGS)} warning(s)")
        sys.exit(1)
    print(f"skill content lint OK ({len(WARNINGS)} warning(s))")
    sys.exit(0)


if __name__ == "__main__":
    main()
