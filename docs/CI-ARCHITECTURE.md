# CI architecture — how this catalog is validated

This document explains *what* CI checks run on this repo, *why* each one exists,
and *what is deliberately left out*. If you are a future maintainer deciding
whether to add a check, read the one rule first.

## The one rule

> **Deterministic checks block the merge. Model-in-the-loop checks inform the
> maintainer. Never the reverse.**

Everything below follows from this. Safety questions ("is this skill broken,
unsafe, or will it fail to install?") have a single correct answer every time, so
they gate. Quality questions ("does it trigger at the right moment and behave
well?") are answered by a language model and are inherently probabilistic — even
a perfect skill is not auto-invoked 100% of the time — so they are recorded as a
signal, never used to block a contributor.

This is the same record-now / gate-later shape used elsewhere in our work; if you
understand one, you understand this.

## The two tiers

### Tier 1 — The Gate (deterministic, blocks merge)

Runs on **every PR**, including from forks. Needs **no secrets**. False-positive
rate is ~0 by construction, which is the only reason it is allowed to block.

| Check | What it catches | Blocks? |
|---|---|---|
| `claude plugin validate .` | malformed manifest, duplicate names, path traversal (`..`), wrong field types, unparseable frontmatter | **yes** |
| `claude plugin validate . --strict` | unrecognized / leftover manifest fields | no — **advisory** |
| `validate_skills.py` | marketplace↔disk mismatch (unregistered or missing skill); name ≠ dir ≠ entry; per-author shared-block drift; house-style (em-dash) | **yes** |
| `install_smoke.sh` | the skill does not actually install or exposes no component | **yes** |
| `scan_security.py` | hardcoded credentials / private keys committed to a skill | **yes** (allowlist for examples) |
| `zizmor` | insecure patterns in *our own* workflows (injection, unpinned actions) | **yes** |
| existing guards | typosquat author dirs, cross-author edits, marketplace schema | warn / yes |
| CODEOWNERS + 1 review | a human curator judges intent; authors own their own dir | **yes** (branch protection) |

Two deliberate FP-control choices inside Tier 1:

- **Gate on plain `validate`, keep `--strict` advisory.** Plain `validate` fails
  only on real defects. `--strict` *additionally* nags on unrecognized fields —
  the one place the official validator can flag a harmless PR. So strict runs,
  but as a warning, not a blocker.
- **The secret scan is conservative + allowlisted.** It matches only
  high-confidence credential shapes and honors `.github/skill-lint/secret-allowlist.txt`
  for documented example keys, so it does not cry wolf on teaching material.

Human review stays. No automated check can decide whether a skill's *intent* is
benign; for a multi-author community catalog a curator still eyeballs each
submission. The gate removes mechanical toil from that review — it does not
replace it.

### Tier 2 — The Signal (model-in-the-loop, never blocks)

Runs **nightly** and **on demand** (`workflow_dispatch`), **not** on the PR
critical path. Posts a report; never a required check.

| Check | What it measures |
|---|---|
| trigger eval (`run_skill_evals.py`) | for each skill's golden utterances, does the right skill fire? For each antipattern utterance, does it correctly stay silent? Reported as fired/precision/recall. |

How it works: for each utterance it runs `claude -p "<utterance>" --output-format
stream-json` with the skill loaded via `--plugin-dir`, then looks for the
built-in `Skill` tool-use event in the stream to see which skill (if any) fired.
The *detection* is deterministic; only the model's choice is stochastic, which we
absorb by sampling each utterance N times and reporting a rate, not a verdict.

Authors opt in by shipping an `evals.json` next to their `SKILL.md` (see
[Authoring evals](#authoring-evals)). Skills without one are simply skipped.

### Tier 3 — Output quality (deferred, may never exist)

LLM-as-judge grading of what a skill actually produces. This is the fuzziest and
most false-positive-prone layer, so it is **not built**. If it is ever added it
stays advisory. Revisit only if the trigger signal proves insufficient.

## Why Tier 2 runs nightly instead of per-PR

This single choice removes three problems at once:

1. **No fork-secret attack surface.** Running secret-using evals on untrusted PR
   code is the root of the `pull_request_target` / two-workflow RCE class
   (CVE-2025-61671). By running only in trusted contexts (schedule, manual,
   push-to-main), that surface and its complex workaround simply do not exist.
2. **No probabilistic check between a contributor and merge.** A flaky model
   decision can never block a good PR.
3. **Bounded cost.** Once a night over changed skills, not once per push. The
   harness authenticates with a subscription `CLAUDE_CODE_OAUTH_TOKEN`
   (see the workflow), so runs do not incur metered API spend.

A maintainer who wants the signal *before* merging something significant runs the
`evals` workflow manually against the branch.

## Promotion path: turning the signal into a gate

Tier 2 stays advisory until its own data earns a gate. Criterion: after ~2 weeks
of nightly runs, if a skill's trigger recall is stable and the check's own
false-positive rate is near zero, a **loose** trigger floor may be promoted to a
required check **on same-repo-branch PRs only** — e.g. "fires for ≥1 golden
utterance across 5 samples", which catches a genuinely broken description without
punishing normal model variance. You flip a grade into a gate only after the
grade has proven it will not false-positive. Behavioral grading (Tier 3) likely
stays advisory permanently.

## What we deliberately do NOT do

- No LLM-judge as a merge gate, ever (top false-positive source).
- No model-in-the-loop check on the PR critical path.
- No `pull_request_target` / two-workflow secret juggling.
- No snapshot / exact-match tests on skill prose (flaky by design; use the
  trigger signal and, if ever, rubric grading).
- No external eval framework (promptfoo/DeepEval) — the trigger harness is ~150
  lines we own and can audit. Reconsider only if Tier 3 is ever built.

## Authoring evals

Drop an `evals.json` beside a skill's `SKILL.md`:

```jsonc
// skills/<author>/<skill>/evals.json
{
  "triggers": {
    "positive": [
      "I have a board meeting next week, help me prep",
      "can you help me get ready for my BoA?"
    ],
    "antipattern": [
      "write me a marketing email",
      "debug this python script"
    ]
  }
}
```

- `positive`: utterances where this skill **should** fire.
- `antipattern`: utterances where it should **stay silent** — include
  out-of-domain prompts and near-misses that belong to a *sibling* skill in the
  same family (these catch over-broad descriptions).

The nightly harness reports, per skill: recall over `positive`, and the
false-positive count over `antipattern`. Tune your `SKILL.md` `description` until
both look right. There is no pass/fail and no merge impact today (see the
promotion path above).

## File map

```
.github/
  workflows/
    lint.yml          # Tier 1 — the gate (every PR)
    evals.yml         # Tier 2 — the signal (nightly + manual)
    release.yml       # auto-tag/release on push to main
  scripts/
    validate_skills.py  # Tier 1: structural + house-style lint
    install_smoke.sh    # Tier 1: real install + component check
    scan_security.py    # Tier 1: conservative secret scan
    run_skill_evals.py  # Tier 2: trigger eval harness
  skill-lint/
    <author>.json       # per-author house-style config (shared_blocks, em-dash)
    secret-allowlist.txt # documented example credentials to ignore
skills/<author>/<skill>/
    SKILL.md
    evals.json          # optional, opt-in trigger eval set
```
