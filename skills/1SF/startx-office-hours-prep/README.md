# startx-office-hours-prep

A Claude Code skill that helps a StartX founder prepare for a mentor session (StartX Office Hours, a mentor 1:1, or a Lead Mentor 1:1). It walks six StartX forcing questions one at a time, routes by session type, company stage, and BoA cycle phase, flags weak spots, and produces an office-hours prep doc in the StartX Board of Advisors challenge format (challenge, options, pros and cons, lean, ask) that can also seed a BoA pre-read.

Design intent: sharpen the founder's thinking, do not replace it. The skill asks the questions a great mentor would ask. It does not make decisions for the founder, write code, or invent evidence.

## Usage

In Claude Code, from your working repo or notes directory:

```
/startx-office-hours-prep
```

The skill opens by telling you what you'll get and what it needs, usually 2 to 4 questions after it reads your materials. Hand it whatever holds your company context (a deck, a wiki or Notion export, a memo); it reads that first and asks only the gaps. The draft builds as you go, so you can stop anytime and resume later by handing it the draft. It writes `office-hours-prep-YYYY-MM-DD.md` to the current directory, and every output is labeled SEND AHEAD, BRING TO SESSION, or KEEP INTERNAL so you know what goes to your mentor and what stays with you.

## Requirements

- Runs on any Claude surface. No sudo, no special mount, no API access.
- In Claude Code or Cowork, the prep doc is written to your working directory and persists. In the claude.ai app, download or copy the draft before closing the conversation (the workspace there does not persist). In chat-only sessions the draft lives in the conversation; copy it to keep it. Resume any time by giving the skill your draft, as a file or a paste.

## Status

v1.1 (2026-06-12). Stable; used in live StartX sessions. Full history in the SKILL.md CHANGELOG.

## Guardrails

- **Sharpen, do not replace.** No decisions made for the founder, no fabricated evidence, quotes, or metrics. If the founder lacks evidence, say so and recommend how to get it.
- **Non-endorsement.** Community-contributed; not endorsed, validated, or audited by StartX or Anthropic.
- **Not advice.** An operations and planning aid, not legal, regulatory, medical, or financial advice.

## Author

Created by [Adam McGinty](https://github.com/1SF), StartX mentor. Part of a StartX founder-support skill suite built around the Board of Advisors prep-to-debrief loop.

## License

MIT, see [LICENSE](LICENSE). Free for the StartX community and anyone else to use, modify, and share. The only condition is that the copyright and license notice travel with it.
