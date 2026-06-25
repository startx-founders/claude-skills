#!/usr/bin/env python3
"""Tier 2 trigger eval harness — does the right skill fire? (advisory signal)

For each skill that ships an evals.json, run its golden ("positive") and
"antipattern" utterances through a real headless Claude Code call with the whole
local skill family loaded, and observe which skill (if any) auto-invokes. This is
a SIGNAL, not a gate: by default it always exits 0 and writes a report. The
firing is detected deterministically from the stream; only the model's choice is
stochastic, which we absorb by sampling each utterance N times and reporting a
rate.

Why load the whole family: antipattern utterances are most useful when a sibling
skill is present to be confused with, so we load every local skill via repeated
--plugin-dir and check whether *this* skill fired.

Auth: uses whatever Claude Code auth is configured. In CI, set
CLAUDE_CODE_OAUTH_TOKEN (subscription billing). Locally, your claude.ai login is
used; unset any stale ANTHROPIC_API_KEY first.

Env knobs:
  EVAL_SAMPLES   samples per utterance (default 3; use 1 for a quick local pass)
  EVAL_MODEL     model id/alias to pin (default: sonnet)
  EVAL_REPORT    output markdown path (default: eval-report.md)

Run locally:
  EVAL_SAMPLES=1 python3 .github/scripts/run_skill_evals.py [repo_root]

evals.json shape (next to SKILL.md):
  { "triggers": { "positive": ["..."], "antipattern": ["..."] } }
"""

import json
import os
import pathlib
import subprocess
import sys

SAMPLES = int(os.environ.get("EVAL_SAMPLES", "3"))
MODEL = os.environ.get("EVAL_MODEL", "sonnet")


def discover(root):
    """Return {skill_name: {dir, evals}} for every local skill, and the list of
    all skill dirs to load."""
    skills = {}
    dirs = []
    for skill_md in sorted((root / "skills").glob("*/*/SKILL.md")):
        d = skill_md.parent
        dirs.append(d)
        name = d.name
        ev = d / "evals.json"
        evals = None
        if ev.exists():
            try:
                evals = json.loads(ev.read_text())
            except json.JSONDecodeError as e:
                print(f"::warning::{ev.relative_to(root)} is not valid JSON: {e}")
        skills[name] = {"dir": d, "evals": evals}
    return skills, dirs


def fired_skills(stream_text):
    """Extract the set of skill names that fired (namespace stripped) from a
    stream-json transcript."""
    fired = set()
    for line in stream_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") != "assistant":
            continue
        for b in ev.get("message", {}).get("content", []):
            if b.get("type") == "tool_use" and b.get("name") == "Skill":
                skill = (b.get("input") or {}).get("skill", "")
                if skill:
                    fired.add(skill.split(":")[-1])  # "plugin:skill" -> "skill"
    return fired


def run_once(utterance, plugin_dirs):
    cmd = [
        "claude", "-p", utterance,
        "--output-format", "stream-json", "--verbose",
        "--max-turns", "1", "--allowedTools", "Skill",
        "--permission-mode", "bypassPermissions", "--model", MODEL,
        "--no-session-persistence",
    ]
    for d in plugin_dirs:
        cmd += ["--plugin-dir", str(d)]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL,
    )
    # exit code is often nonzero (max-turns after a skill fires) — we read stdout.
    return fired_skills(proc.stdout)


def sample(utterance, plugin_dirs, target):
    """Run an utterance SAMPLES times; return (fired_target_count, other_counts)."""
    hit = 0
    others = {}
    for _ in range(SAMPLES):
        fired = run_once(utterance, plugin_dirs)
        if target in fired:
            hit += 1
        for f in fired:
            if f != target:
                others[f] = others.get(f, 0) + 1
    return hit, others


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    skills, dirs = discover(root)
    tested = {n: s for n, s in skills.items() if s["evals"]}
    if not tested:
        print("no skills ship evals.json — nothing to evaluate")
        # write an empty report so CI has an artifact
        pathlib.Path(os.environ.get("EVAL_REPORT", "eval-report.md")).write_text(
            "# Trigger eval report\n\nNo skills ship `evals.json` yet.\n"
        )
        return

    lines = ["# Trigger eval report", ""]
    lines.append(f"_Samples per utterance: {SAMPLES} · model: {MODEL} · "
                 f"family skills under test: {len(dirs)}_")
    lines.append("")
    summary = []

    for name in sorted(tested):
        ev = tested[name]["evals"].get("triggers", {})
        pos = ev.get("positive", []) or []
        neg = ev.get("antipattern", []) or []
        lines.append(f"## {name}")
        lines.append("")

        recall_hits = 0
        if pos:
            lines.append("**Golden (should fire):**")
            for u in pos:
                hit, others = sample(u, dirs, name)
                ok = hit >= (SAMPLES + 1) // 2  # majority
                recall_hits += 1 if ok else 0
                mark = "✅" if ok else "❌"
                extra = f" · also fired: {others}" if others else ""
                lines.append(f"- {mark} {hit}/{SAMPLES} `{u}`{extra}")
            lines.append("")

        fp = 0
        if neg:
            lines.append("**Antipattern (should stay silent):**")
            for u in neg:
                hit, others = sample(u, dirs, name)
                ok = hit == 0
                fp += 0 if ok else 1
                mark = "✅" if ok else "⚠️"
                extra = f" · correctly routed to: {others}" if (ok and others) else (
                    f" · also fired: {others}" if others else "")
                lines.append(f"- {mark} fired {hit}/{SAMPLES} `{u}`{extra}")
            lines.append("")

        recall = f"{recall_hits}/{len(pos)}" if pos else "n/a"
        summary.append((name, recall, fp, len(neg)))

    head = ["", "## Summary", "", "| skill | golden recall | antipattern misfires |",
            "|---|---|---|"]
    for name, recall, fp, nneg in summary:
        head.append(f"| {name} | {recall} | {fp}/{nneg} |")
    report = "\n".join(lines + head) + "\n"

    out = pathlib.Path(os.environ.get("EVAL_REPORT", "eval-report.md"))
    out.write_text(report)
    print(report)
    print(f"\nreport written to {out}")
    # Advisory: always exit 0. (Promotion to a gate is a future, deliberate step.)


if __name__ == "__main__":
    main()
