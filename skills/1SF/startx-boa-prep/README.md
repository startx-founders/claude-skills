# startx-boa-prep

A Claude Code skill that helps a StartX founder prepare for a Board of Advisors meeting, a CEO or board review, or a formal advisor review. It walks six StartX forcing questions across the whole company, demands evidence behind each claim, and produces an advisor-ready pre-read (one-page summary, state of the business, 2-3 challenges, explicit open risks, consolidated asks, and a "Where StartX can help next" section that routes each gap to the right StartX mentor, workshop, peer, or resource) suitable to send 48 hours ahead.

Design intent: sharpen the founder's thinking and surface real risk, do not replace judgment. The skill asks the questions a sharp board would ask. It does not decide for the founder or invent evidence. It is the higher-stakes companion to `startx-office-hours-prep`.

## Usage

In Claude Code, from your working repo or notes directory:

```
/startx-boa-prep
```

Then answer the questions one at a time. The skill writes `boa-prep-YYYY-MM-DD.md` to the current directory and offers a short cover note you can send advisors with the pre-read.

## Requirements

- Runs on macOS or Linux. No sudo required.
- No special mount or API access. Writes one markdown file to the current directory.

## Status

v1.0, initial public release for the StartX summer cohort, alongside `startx-office-hours-prep`. Calibrated against a real BoA #1 dry-run: reads the founder's existing deck first and probes only the gaps; handles the live-but-pre-revenue stage (routes as "has users" plus a forced contract-status check); reconciles each traction claim (signed, verbal, in-pipeline, or interested); flags demand concentration explicitly. Full scope in the SKILL.md CHANGELOG.

## Guardrails

- **Sharpen, do not replace.** No decisions made for the founder, no fabricated evidence, quotes, metrics, or traction. Missing evidence is named, not invented.
- **Non-endorsement.** Community-contributed; not endorsed, validated, or audited by StartX or Anthropic.
- **Not advice.** An operations and planning aid, not legal, regulatory, medical, or financial advice.

## Author

Created by [Adam McGinty](https://github.com/1SF), StartX mentor. Part of a StartX founder-support skill suite built around the Board of Advisors prep-to-debrief loop.

## License

MIT, see [LICENSE](LICENSE). Free for the StartX community and anyone else to use, modify, and share. The only condition is that the copyright and license notice travel with it.
