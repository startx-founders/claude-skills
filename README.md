# StartX Founders — Claude Code skills

A community-curated catalog of [Claude Code](https://code.claude.com) skills and plugins built by StartX founders, for StartX founders.

## Install

```
/plugin marketplace add startx-founders/claude-skills
/plugin install <plugin-name>@startx-founders
```

Pin to a tagged release for safer, reproducible installs:

```
/plugin marketplace add startx-founders/claude-skills@v0.1.0
```

After installing, run `/plugin marketplace update` to pull catalog changes; run `/plugin install <plugin>@startx-founders` to add a specific skill.

## ⚠️  Trust model — read before installing

This catalog is **curated, not audited**. StartX Founders curators perform a basic review of each PR for fit and obvious problems. We do **not** perform a security review of submitted code.

**Plugins run arbitrary code on your machine with your user privileges.** This is true of every Claude Code plugin marketplace, not just this one. Anthropic itself states the same thing about plugins listed in its official marketplace. Treat each skill in this catalog the same way you'd treat a script from a friend: read it before you run it, and only install ones from people you have reason to trust.

- StartX (the accelerator) does not run, endorse, or audit this catalog.
- StartX Founders curators verify that contributors are members of the StartX community before granting write access — that is the trust gate. The content of each skill is the contributor's responsibility.
- Each skill in `/skills/<author>/` retains its own license; check before redistribution.

## Listed skills

The catalog starts empty — first contributor PR is pending.

Once skills are listed, they will be auto-rendered here. For now, the source of truth is [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).

## Who can contribute

Current and alumni StartX founders. Verification happens out-of-band: post your GitHub handle in the StartX founder mailing list (or our Slack), and a curator will invite you to the [`@startx-founders`](https://github.com/startx-founders) GitHub organization.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full flow.

## Maintainers

This catalog is community-organized. Curators (with merge rights) are listed in [`.github/CODEOWNERS`](.github/CODEOWNERS) under the `@startx-founders/curators` team.

Started by [@robertnowell](https://github.com/robertnowell) (Kopi, StartX founder community). Curator additions made by existing curators after a contributor has shipped a few well-received PRs — same model Homebrew uses.

## Reporting issues

- **Bug in a specific skill** → file an issue in the skill's own repo, or open an issue in this repo and we'll route it.
- **Bug in the catalog itself (marketplace.json, CI, docs)** → open an issue in this repo.
- **Suspected malicious skill or security concern** → see [SECURITY.md](SECURITY.md).

## License

Catalog metadata (this README, marketplace.json, CODEOWNERS, CI workflows, docs) is MIT. Each contributed skill retains its own license.
