# Contributing to startx-founders/claude-skills

## Who can contribute

Current and alumni StartX founders. We verify membership socially, not via email domain — see "First-time contributor flow" below.

## Skill quality bar (kept deliberately low at v0.1)

- Has a `README.md` explaining what the skill does and one usage example.
- Runs on macOS or Linux (Windows is a bonus, not required).
- Doesn't require root / sudo to install or run.
- Has a permissive license (MIT, Apache-2.0, BSD, or similar) — or is clearly marked otherwise.

We'll raise the bar over time. For now, getting more StartX founders to share working tools matters more than polish.

> **Coming soon — trigger evals.** A future change will let you ship an optional
> `evals.json` next to your `SKILL.md` (utterances that should and should not
> invoke your skill) so CI can track how reliably your `description` triggers.
> It is not wired up yet; see `docs/CI-ARCHITECTURE.md` for the plan.

## Two ways to contribute a skill

### Option A — Point us at your own repo (zero friction)

If your skill already lives in a public GitHub repo (like [`ivy-invest/claude-design-for-ads`](https://github.com/ivy-invest/claude-design-for-ads)), keep it there. The catalog will reference it by repo URL and a pinned tag/SHA.

**Pros:** you keep full control, releases happen on your timeline, no migration. **Cons:** every catalog version pin update requires a small PR here.

### Option B — Vendor your skill into this repo

Put your skill code in `/skills/<your-github-handle>/<skill-name>/`. Catalog uses a relative path.

**Pros:** single source of truth, easier for users to audit, one PR ships a new version. **Cons:** changes to your skill require opening a PR here every time.

Either is fine. New contributors tend to start with Option A (less friction) and graduate to B if they want tighter review.

## First-time contributor flow (5 steps)

1. **Verify membership.** Post your GitHub handle in the StartX founder mailing list:
   > "I'm @your-github-handle, StartX [batch], adding a Claude Code skill called X."
2. **Wait for org invite.** A curator confirms you're in the StartX channel and invites your GitHub username to the [`@startx-founders`](https://github.com/startx-founders) org. Accept it.
3. **Open your first PR.** Make these changes in one PR:
   - Add `.github/CODEOWNERS` line: `/skills/<your-github-handle>/    @<your-github-handle>`
   - If vendoring (Option B): add `/skills/<your-github-handle>/<skill-name>/` with your skill files + a README.
   - Add one entry to `.claude-plugin/marketplace.json` under `plugins`. See examples below.
4. **Get a curator review.** A curator (anyone in `@startx-founders/curators`) verifies the CODEOWNERS line matches your handle, sanity-checks the skill README, and approves. CI runs schema validation and a typosquat check.
5. **Merge.** Your skill is listed. Future updates to your own `/skills/<your-handle>/` directory can be self-approved (CODEOWNERS routes back to you) — though we recommend asking another StartX member to take a look.

## marketplace.json entry examples

**Option A (external repo, pinned tag):**

```json
{
  "name": "claude-design-for-ads",
  "description": "Build ad creatives (image + video) with Claude Design.",
  "source": {
    "source": "github",
    "repo": "ivy-invest/claude-design-for-ads",
    "ref": "v1.0.0"
  },
  "author": {
    "name": "Matt Pauker",
    "url": "https://github.com/mattpauker"
  },
  "category": "design",
  "tags": ["ads", "design", "video"],
  "license": "MIT"
}
```

**Option B (vendored, relative path):**

```json
{
  "name": "my-skill",
  "description": "What it does in one sentence.",
  "source": "./skills/your-handle/my-skill",
  "author": {
    "name": "Your Name",
    "url": "https://github.com/your-handle"
  },
  "category": "productivity",
  "tags": ["..."],
  "license": "MIT"
}
```

## Updating an existing skill

If you authored a skill in this catalog and want to update it:

- **Option A (external):** publish a new tag in your own repo, then open a PR here that bumps the `ref` in your marketplace.json entry. Curator review = sanity-check the tag exists.
- **Option B (vendored):** open a PR with the changes inside your `/skills/<handle>/` dir. Because you're the CODEOWNER of that dir, you can self-approve (assuming branch protection allows it) — but for non-trivial changes please ping another StartX member for a look.

## Alumni policy

Alumni keep ownership of skills they already shipped. We don't auto-remove. If you're no longer active and a maintenance update is needed, a curator can take over a folder after 6 months of no response.

## Revocation

If a contributor acts in bad faith (publishes malware, harasses other contributors, etc.):

1. A curator removes them from the `@startx-founders` org. Write access is revoked immediately.
2. A curator opens a PR removing their CODEOWNERS line and archiving or removing their `/skills/<handle>/` dir.
3. The marketplace.json entry is removed in the same PR; catalog is re-tagged.

## Naming rules

- Skill directory: `/skills/<your-github-handle>/` (lowercase, hyphen-separated GitHub username).
- Skill name (in marketplace.json): kebab-case, descriptive, not impersonating Anthropic-reserved names.
- Per-skill subdir if you ship multiple: `/skills/<handle>/<skill-name>/`.

## Questions

Open an issue or ask on the mailing list. Curators monitor both.
