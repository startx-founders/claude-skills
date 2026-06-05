# startx-office-hours-prep

A Claude Code skill that helps a StartX founder prepare for a mentor session (StartX Office Hours, a mentor 1:1, or a Lead Mentor 1:1). It walks six StartX forcing questions one at a time, routes by session type, company stage, and BoA cycle phase, flags weak spots, and produces an office-hours prep doc in the StartX Board of Advisors challenge format (challenge, options, pros and cons, lean, ask) that can also seed a BoA pre-read.

Design intent: sharpen the founder's thinking, do not replace it. The skill asks the questions a great mentor would ask. It does not make decisions for the founder, write code, or invent evidence.

## Usage

In Claude Code, from your working repo or notes directory:

```
/startx-office-hours-prep
```

Then answer the questions as they come, one at a time. The skill writes `office-hours-prep-YYYY-MM-DD.md` to the current directory and offers a short summary you can paste into a message to your mentor.

## Requirements

- Runs on macOS or Linux. No sudo required.
- No special mount or API access. Writes one markdown file to the current directory.

## Status

v1.0, initial public release for the StartX summer cohort. Calibrated against a real pre-BoA-1 dry-run: reads the founder's existing deck first and probes only the gaps; handles the live-but-pre-revenue stage; reconciles each traction claim (signed, verbal, in-pipeline, or interested) so "paying customer" language matches what is contracted. Full scope in the SKILL.md CHANGELOG.

## Guardrails

- **Sharpen, do not replace.** No decisions made for the founder, no fabricated evidence, quotes, or metrics. If the founder lacks evidence, say so and recommend how to get it.
- **Non-endorsement.** Community-contributed; not endorsed, validated, or audited by StartX or Anthropic.
- **Not advice.** An operations and planning aid, not legal, regulatory, medical, or financial advice.

## Author

Created by [Adam McGinty](https://github.com/1SF), StartX mentor. Part of a StartX founder-support skill suite built around the Board of Advisors prep-to-debrief loop.

## License

MIT, see [LICENSE](LICENSE). Free for the StartX community and anyone else to use, modify, and share. The only condition is that the copyright and license notice travel with it.
