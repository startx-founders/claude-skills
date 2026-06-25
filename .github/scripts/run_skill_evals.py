#!/usr/bin/env python3
"""Tier 2 trigger eval harness — does the right skill fire? (advisory signal)

For each skill that ships an evals.json, run its golden ("positive") and
"antipattern" utterances through a real headless Claude Code call with the whole
local skill family loaded, and observe which skill (if any) auto-invokes. This is
a SIGNAL, not a gate: it always exits 0. Firing is detected deterministically
from the stream; only the model's choice is stochastic, which we absorb by
sampling each utterance N times and reporting a rate.

Outputs (paths via env, all optional):
  EVAL_REPORT  human markdown report (default eval-report.md) — used as the PR
               comment body; carries a marker so the comment can be upserted.
  EVAL_JSON    structured results (default eval-results.json).
  EVAL_BOARD   if set, write the catalog health board here (nightly full runs).
  EVAL_BADGES  if set (a dir), write shields.io endpoint JSON per skill there.

Scope:
  EVAL_ONLY    comma-separated skill names to evaluate (PR runs pass only the
               changed skills). The whole family is still loaded for realistic
               cross-skill context; only these skills' utterances are run.

Other knobs:
  EVAL_SAMPLES samples per utterance (default 3; use 1 for a quick local pass)
  EVAL_MODEL   model id/alias to pin (default sonnet)

Auth: uses whatever Claude Code auth is configured. CI sets
CLAUDE_CODE_OAUTH_TOKEN (subscription, no metered spend). Locally, your claude.ai
login is used; unset any stale ANTHROPIC_API_KEY first.

Run locally:  EVAL_SAMPLES=1 EVAL_ONLY=startx-boa-prep python3 .github/scripts/run_skill_evals.py .
"""

import datetime
import json
import os
import pathlib
import subprocess
import sys

SAMPLES = int(os.environ.get("EVAL_SAMPLES", "3"))
MODEL = os.environ.get("EVAL_MODEL", "sonnet")
ONLY = [s.strip() for s in os.environ.get("EVAL_ONLY", "").split(",") if s.strip()]
MARKER = "<!-- skill-trigger-evals -->"


def discover(root):
    skills, dirs = {}, []
    for skill_md in sorted((root / "skills").glob("*/*/SKILL.md")):
        d = skill_md.parent
        dirs.append(d)
        ev = d / "evals.json"
        evals = None
        if ev.exists():
            try:
                evals = json.loads(ev.read_text())
            except json.JSONDecodeError as e:
                print(f"::warning::{ev.relative_to(root)} is not valid JSON: {e}")
        skills[d.name] = {"dir": d, "evals": evals}
    return skills, dirs


def fired_skills(stream_text):
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
    proc = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    return fired_skills(proc.stdout)  # exit code is unreliable; read the stream


def sample(utterance, plugin_dirs, target):
    hit, others = 0, {}
    for _ in range(SAMPLES):
        fired = run_once(utterance, plugin_dirs)
        if target in fired:
            hit += 1
        for f in fired:
            if f != target:
                others[f] = others.get(f, 0) + 1
    return hit, others


def color(recall_ok, misfires):
    if misfires > 0:
        return "red"
    return "brightgreen" if recall_ok else "yellow"


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    skills, dirs = discover(root)
    tested = {n: s for n, s in skills.items() if s["evals"]}
    if ONLY:
        tested = {n: s for n, s in tested.items() if n in ONLY}

    report = [MARKER, "# Trigger eval report", "",
              f"_samples/utterance: {SAMPLES} · model: {MODEL} · "
              f"family loaded: {len(dirs)} · evaluated: {len(tested)}_", ""]
    results = []

    if not tested:
        report.append("_No skills in scope ship an `evals.json`._")
        pathlib.Path(os.environ.get("EVAL_REPORT", "eval-report.md")).write_text(
            "\n".join(report) + "\n")
        pathlib.Path(os.environ.get("EVAL_JSON", "eval-results.json")).write_text("[]\n")
        print("no skills in scope ship evals.json — nothing to evaluate")
        return

    for name in sorted(tested):
        trig = tested[name]["evals"].get("triggers", {})
        pos = trig.get("positive", []) or []
        neg = trig.get("antipattern", []) or []
        report += [f"## {name}", ""]

        recall_hits = 0
        if pos:
            report.append("**Golden (should fire):**")
            for u in pos:
                hit, others = sample(u, dirs, name)
                ok = hit >= (SAMPLES + 1) // 2
                recall_hits += 1 if ok else 0
                extra = f" · also fired: {others}" if others else ""
                report.append(f"- {'✅' if ok else '❌'} {hit}/{SAMPLES} `{u}`{extra}")
            report.append("")

        misfires = 0
        if neg:
            report.append("**Antipattern (should stay silent):**")
            for u in neg:
                hit, others = sample(u, dirs, name)
                ok = hit == 0
                misfires += 0 if ok else 1
                extra = (f" · correctly routed to: {others}" if (ok and others)
                         else (f" · also fired: {others}" if others else ""))
                report.append(f"- {'✅' if ok else '⚠️'} fired {hit}/{SAMPLES} `{u}`{extra}")
            report.append("")

        recall_ok = bool(pos) and recall_hits == len(pos)
        results.append({
            "skill": name,
            "recall_hits": recall_hits, "recall_total": len(pos),
            "misfires": misfires, "antipattern_total": len(neg),
            "samples": SAMPLES,
        })

    # Summary table in the report.
    report += ["## Summary", "", "| skill | golden recall | antipattern misfires |",
               "|---|---|---|"]
    for r in results:
        report.append(f"| {r['skill']} | {r['recall_hits']}/{r['recall_total']} "
                      f"| {r['misfires']}/{r['antipattern_total']} |")
    report_text = "\n".join(report) + "\n"

    pathlib.Path(os.environ.get("EVAL_REPORT", "eval-report.md")).write_text(report_text)
    pathlib.Path(os.environ.get("EVAL_JSON", "eval-results.json")).write_text(
        json.dumps(results, indent=2) + "\n")
    print(report_text)

    # Catalog health board (nightly full runs only).
    board_path = os.environ.get("EVAL_BOARD")
    if board_path:
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        board = ["# Skill health", "",
                 f"_Trigger evals, regenerated {now}. Advisory signal — see "
                 f"`docs/CI-ARCHITECTURE.md`. History: the git log of this file._", "",
                 "| skill | golden recall | antipattern misfires | status |",
                 "|---|---|---|---|"]
        for r in results:
            recall_ok = r["recall_total"] and r["recall_hits"] == r["recall_total"]
            status = "🔴" if r["misfires"] else ("🟢" if recall_ok else "🟡")
            board.append(f"| {r['skill']} | {r['recall_hits']}/{r['recall_total']} "
                         f"| {r['misfires']}/{r['antipattern_total']} | {status} |")
        pathlib.Path(board_path).write_text("\n".join(board) + "\n")
        print(f"board written to {board_path}")

    # shields.io endpoint badges (one JSON per skill).
    badges_dir = os.environ.get("EVAL_BADGES")
    if badges_dir:
        bd = pathlib.Path(badges_dir)
        bd.mkdir(parents=True, exist_ok=True)
        for r in results:
            recall_ok = r["recall_total"] and r["recall_hits"] == r["recall_total"]
            msg = f"{r['recall_hits']}/{r['recall_total']}"
            if r["misfires"]:
                msg += f", {r['misfires']} misfire"
            (bd / f"{r['skill']}.json").write_text(json.dumps({
                "schemaVersion": 1, "label": "trigger evals", "message": msg,
                "color": color(recall_ok, r["misfires"]),
            }) + "\n")
        print(f"badges written to {bd}/")

    # Advisory: always exit 0. Promotion to a gate is a future, deliberate step.


if __name__ == "__main__":
    main()
