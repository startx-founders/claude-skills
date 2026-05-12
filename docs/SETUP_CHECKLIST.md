# GitHub setup checklist

One-time configuration. ~25 minutes start to finish. Do these in order.

## Prerequisites

- A GitHub account with 2FA enabled (yours — you'll be the org owner).
- A second trusted person who will also be an org owner (continuity / bus-factor).
- `gh` CLI installed and authenticated: `gh auth status` should show your account.

## 1. Create the GitHub organization

Browser only — the GitHub API does not allow programmatic org creation for personal accounts.

1. Visit https://github.com/organizations/plan
2. Pick the **Free** plan.
3. Organization account name: `startx-founders`
4. Contact email: your email.
5. Belongs to: "My personal account" (you can change ownership later).
6. Verify the org was created: `gh api /orgs/startx-founders | jq .login` should print `startx-founders`.

## 2. Add a second owner immediately

Don't run sole-owner. Even one extra owner is dramatically safer.

1. https://github.com/orgs/startx-founders/people
2. Invite a second person → set role to **Owner**.
3. Confirm they accept.

## 3. Enable required 2FA org-wide

https://github.com/organizations/startx-founders/settings/security

- Check "Require two-factor authentication for everyone in the startx-founders organization"
- Save. (Any future member without 2FA can't be added; you can't be removed because you already have it.)

## 4. Create the `curators` team

1. https://github.com/orgs/startx-founders/new-team
2. Team name: `curators`
3. Description: "Curators with merge rights on startx-founders/claude-skills."
4. Visibility: **Visible** (public). This makes the @startx-founders/curators mention work in CODEOWNERS.
5. Add yourself and your co-owner as members.

## 5. Create the public repo

```bash
gh repo create startx-founders/claude-skills \
  --public \
  --description "Community-curated catalog of Claude Code skills built by StartX founders." \
  --homepage "https://github.com/startx-founders/claude-skills" \
  --disable-wiki
```

## 6. Push the scaffold

```bash
cd ~/Projects/startx-founders-claude-skills
git remote add origin git@github.com:startx-founders/claude-skills.git
git push -u origin main
```

If `git push` fails because the remote already has a default README, run:

```bash
git push -u origin main --force-with-lease
```

(Safe because the remote is empty — we just created it.)

## 7. Grant the curators team write access

```bash
gh api -X PUT /orgs/startx-founders/teams/curators/repos/startx-founders/claude-skills \
  -f permission=push
```

## 8. Branch protection on `main`

Go to https://github.com/startx-founders/claude-skills/settings/branches

Click **Add branch protection rule**:

- Branch name pattern: `main`
- ✅ Require a pull request before merging
  - ✅ Require approvals: **1**
  - ✅ Dismiss stale pull request approvals when new commits are pushed
  - ✅ Require review from Code Owners
- ✅ Require status checks to pass before merging
  - ✅ Require branches to be up to date before merging
  - Add status checks once CI has run once and registers them:
    - `Validate marketplace.json`
    - `Check for typosquat-like author dirs`
    - `Warn if PR touches multiple author dirs`
- ✅ Require conversation resolution before merging
- ✅ Restrict who can push to matching branches → leave empty (nobody bypasses)
- ❌ Allow force pushes
- ❌ Allow deletions

Save.

## 9. (Recommended) Require hardware-key 2FA for curators

If your co-owner has a hardware key (Yubikey / Titan / phone passkey), have them register it. The `curators` team is the highest-privilege role in the org; account takeover here = catalog compromise.

## 10. Tag v0.1.0 once the catalog exists

Wait until the first contributor PR lands. Then:

```bash
git tag -a v0.1.0 -m "First listing"
git push origin v0.1.0
```

Users install via `/plugin marketplace add startx-founders/claude-skills@v0.1.0`.

## 11. Smoke test the catalog locally

```
# In Claude Code:
/plugin marketplace add startx-founders/claude-skills
/plugin marketplace list
```

Should show: `startx-founders` marketplace with 0 plugins (until first PR lands).

## What this leaves you with

- A public, read-by-anyone repo.
- Write access gated to `@startx-founders/curators` (you + co-owner at first).
- Anyone in the world can fork and open PRs.
- No PR can merge to `main` without (a) at least one approval from a code owner and (b) passing CI.
- Outside contributors cannot grant themselves code-owner status — fork PRs evaluate the upstream's CODEOWNERS.

## Optional follow-ups (do later)

- Add a GitHub topic `claude-code-marketplace` to improve discoverability.
- Submit the marketplace to https://clau.de/plugin-directory-submission if you want it listed in Anthropic's directory.
- Wire up GitHub Discussions for catalog-level Q&A.
- Once you have ≥3 active contributors, rotate a third curator in (Homebrew's pattern).
