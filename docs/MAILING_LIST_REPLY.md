# Reply to the StartX founder mailing list thread

Subject: keep the thread subject (`Re: [StartX AnythingG.] Building ads w/ Claude Design`).

---

Happy to set this up — and actually, just did. The repo is live:

**https://github.com/startx-founders/claude-skills**

Install in Claude Code:

```
/plugin marketplace add startx-founders/claude-skills
```

It returns 0 plugins right now, which is correct — catalog is empty until the first contributor PR lands.

**The model, briefly.** Public repo (anyone reads), write gated to the `@startx-founders` GitHub org. Each contributor gets a `/skills/<github-handle>/` directory routed to them via CODEOWNERS — you control your own skill, you can't touch anyone else's. Branch protection on `main` requires a code-owner approval before anything merges. The "are you really StartX?" check is just "post your handle here and I'll invite you." Same out-of-band pattern Homebrew and Apache use.

It's **curated, not audited** — same disclaimer Anthropic uses for their own plugin marketplace. Installing a skill runs arbitrary code with your user privileges; verifying that the contributor is a StartX founder is what we do, code review is on you.

**A few asks while it's still empty:**

- **Matt** — happy to make `ivy-invest/claude-design-for-ads` the first listing. Your repo would need a small Claude Code plugin manifest (`.claude-plugin/plugin.json` + a one-page SKILL.md teaching Claude Code when to use the toolkit) so `/plugin install` resolves. I can send you a draft of both — ~5 min for you to add and re-tag. OK to proceed?
- **Curators wanted.** I'd like 2–3 people who'll help me review the first PRs. Reply with your GitHub handle.
- **On the name:** I went with `startx-founders` because the existing `github.com/StartX` org has been dormant since 2018 with zero public repos. If anyone has the keys to the old one and wants to consolidate, holler.

CONTRIBUTING.md walks through the 5-step onboarding. Code is at the URL above, no signup needed to read.

Rob

---

## Notes (don't send — for Robert)

- Reply lands on the thread that has Matt, Danny, Ruth Ann, Ivan, Jonathan, Kenneth, Kuanysh — i.e. exactly the right audience already gathered.
- The "Matt — your repo needs a manifest" framing is honest and gives him an easy yes/no: yes, I'll draft the manifest and send it.
- The "Curators wanted" line does double duty: filters for who actually wants to be involved long-term.
- After you send, save the email's permalink (Google Groups URL) — durable record of "we asked the community, here's who replied."
