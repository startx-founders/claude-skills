# CI architecture — how this catalog is validated

This explains what CI runs on this repo, why, and what is deliberately left out.
If you're a future maintainer deciding whether to add a check, read the one rule
first.

## The one rule

> **Deterministic checks block the merge. Model-in-the-loop checks inform the
> maintainer. Never the reverse.**

Safety questions ("is this skill broken, unsafe, or will it fail to install?")
have a single correct answer every time, so they gate. Quality questions ("does
it trigger at the right moment and behave well?") are answered by a language
model and are inherently probabilistic, so they only ever inform — never block.

## Status

- **Shipped and gating: Tier 1 (the deterministic gate).** This is what runs
  today on every PR.
- **Designed but NOT shipped: Tier 2 (the trigger eval).** Deliberately deferred
  after a security audit found that running model-in-the-loop evals over
  contributor-authored skill content is unsafe unless carefully sandboxed and
  re-authed. See [Tier 2 — planned](#tier-2--the-signal-planned-not-shipped).

## Tier 1 — The Gate (deterministic, blocks merge) — SHIPPED

Runs on **every PR**, including from forks. Needs **no secrets**. False-positive
rate is ~0 by construction, which is the only reason it is allowed to block.

| Check | What it catches | Blocks? |
|---|---|---|
| `claude plugin validate .` | malformed manifest, duplicate names, path traversal (`..`), wrong field types, unparseable frontmatter | **yes** |
| `claude plugin validate . --strict` | unrecognized / leftover manifest fields | no — **advisory** |
| `validate_skills.py` | marketplace↔disk mismatch (unregistered or missing skill); name ≠ dir ≠ entry; per-author shared-block drift; house-style (em-dash) | **yes** |
| `install_smoke.sh` | the skill does not actually install or exposes no component | **yes** |
| `scan_security.py` | hardcoded credentials / private keys committed to a skill | **yes** (allowlist for examples) |
| `zizmor` | insecure patterns in *our own* workflows (injection, unpinned actions), gated at high severity | **yes** |
| existing guards | typosquat author dirs, cross-author edits, marketplace schema | warn / yes |
| CODEOWNERS + 1 review | a human curator judges intent; authors own their own dir | **yes** (branch protection) |

Two deliberate FP-control choices inside Tier 1:

- **Gate on plain `validate`, keep `--strict` advisory.** Plain `validate` fails
  only on real defects. `--strict` *additionally* nags on unrecognized fields —
  the one place the official validator can flag a harmless PR. So strict runs,
  but as a warning.
- **The secret scan is conservative + allowlisted.** It matches only
  high-confidence credential shapes and honors
  `.github/skill-lint/secret-allowlist.txt`, so it does not cry wolf on teaching
  material.

**`zizmor` is gated at `--min-severity high`** — the supply-chain / injection
class that actually enables compromise. Medium `artipacked` findings are
low-confidence credential-persistence notes and benign here (lint jobs upload
nothing), so gating on them would add false-positive friction without security
value.

Human review stays. No automated check can decide whether a skill's *intent* is
benign; for a multi-author community catalog a curator still eyeballs each
submission. The gate removes mechanical toil from that review — it does not
replace it.

## Tier 2 — The Signal (planned, NOT shipped)

The intended Tier 2 is a **trigger eval**: per skill, golden utterances that
*should* invoke it and antipattern utterances that should *not*, run headlessly
to see which skill the model actually selects — reported as an advisory signal,
never a gate. This is genuinely novel (no Claude Code marketplace, including
Anthropic's, does it today).

**It is not shipped, and must not be enabled as originally drafted.** A June 2026
security audit (archived at `~/Documents/deep-research/2026-06-25-claude-skills-ci-security-audit.md`)
found two real holes in the first implementation:

1. `--permission-mode bypassPermissions` + `--allowedTools Skill` does **not**
   sandbox the skill (`--allowedTools` doesn't restrict tools — only `--tools`
   does; bypass approves everything). A weaponized merged skill could exfiltrate
   the credential.
2. A `SKILL.md` `!`shell`` block executes at **load** time, before the model
   even responds.

When Tier 2 is built, it must:

- Run **sandboxed**: `claude --bare --plugin-dir <skill> --tools "Skill"
  --disallowedTools "mcp__*" --settings '{"disableSkillShellExecution":true}'
  --permission-mode dontAsk`, block subagent spawning, and **detect the trigger
  from the stream without executing the skill body**.
- Authenticate with **API key via Workload Identity Federation** (short-lived,
  keyless) — not a long-lived subscription OAuth token. (`--bare` requires an API
  key anyway.)
- Stay **advisory** and run only in trusted contexts.

**Likely sequencing:** before (or instead of) the trigger eval, adopt an LLM
**read-only security scan** — Anthropic ships a reusable one
(`anthropics/claude-plugins-community/.github/actions/scan-plugins`) that runs
`claude -p --bare --allowed-tools "Read,Glob,Grep"` over each plugin with WIF
auth as a hard gate. For a public multi-author repo that scan matters more for
safety than the trigger eval.

## What we deliberately do NOT do

- No LLM-judge as a merge gate, ever (top false-positive source).
- No model-in-the-loop check that runs untrusted skill content with a credential
  present and without the sandbox above.
- No `pull_request_target` / two-workflow secret juggling (Tier 2, when built,
  uses same-repo gating + WIF instead).
- No snapshot / exact-match tests on skill prose (flaky by design).

## File map

```
.github/
  workflows/
    lint.yml          # Tier 1 — the gate (every PR)
    release.yml       # auto-tag/release on push to main
  scripts/
    validate_skills.py  # Tier 1: structural + house-style lint
    install_smoke.sh    # Tier 1: real install + component check
    scan_security.py    # Tier 1: conservative secret scan
  skill-lint/
    <author>.json        # per-author house-style config (shared_blocks, em-dash)
    secret-allowlist.txt # documented example credentials to ignore
skills/<author>/<skill>/
    SKILL.md
    README.md
```
