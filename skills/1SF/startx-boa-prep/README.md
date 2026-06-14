# startx-boa-prep

A Claude Code skill that helps a StartX founder prepare for a Board of Advisors meeting, a CEO or board review, or a formal advisor review. It walks six StartX forcing questions across the whole company, demands evidence behind each claim, and produces an advisor-ready pre-read (one-page summary, state of the business, 2-3 challenges, explicit open risks, consolidated asks, and a "Where StartX can help next" section that routes each gap to the right StartX mentor, workshop, peer, or resource) suitable to send 48 hours ahead.

Design intent: sharpen the founder's thinking and surface real risk, do not replace judgment. The skill asks the questions a sharp board would ask. It does not decide for the founder, write code, or invent evidence. It is the higher-stakes companion to `startx-office-hours-prep`.

## Usage

In Claude Code, from your working repo or notes directory:

```
/startx-boa-prep
```

The skill opens by telling you what you'll get and what it needs: six questions across the company for a first review, fewer for follow-ups, after it reads your materials. Hand it whatever holds your company context (a deck, a wiki or Notion export, a memo); it reads that first and asks only the gaps. The draft builds as you go, so you can stop anytime and resume later by handing it the draft. It writes `boa-prep-YYYY-MM-DD.md` to the current directory with a cover note for advisors, every output is labeled SEND AHEAD or KEEP INTERNAL, and a send-safety pass runs before anything goes to your board.

## Requirements

- Runs on any Claude surface. No sudo, no special mount, no API access.
- In Claude Code or Cowork, the pre-read is written to your working directory and persists. In the claude.ai app, download or copy the draft before closing the conversation (the workspace there does not persist). In chat-only sessions the draft lives in the conversation; copy it to keep it. Resume any time by giving the skill your draft, as a file or a paste.

## Status

v1.1 (2026-06-12). Stable; companion to `startx-office-hours-prep`. Full history in the SKILL.md CHANGELOG.

## Guardrails

- **Sharpen, do not replace.** No decisions made for the founder, no fabricated evidence, quotes, metrics, or traction. Missing evidence is named, not invented.
- **Non-endorsement.** Community-contributed; not endorsed, validated, or audited by StartX or Anthropic.
- **Not advice.** An operations and planning aid, not legal, regulatory, medical, or financial advice.

## Author

Created by [Adam McGinty](https://github.com/1SF), StartX mentor. Part of a StartX founder-support skill suite built around the Board of Advisors prep-to-debrief loop.

## License

MIT, see [LICENSE](LICENSE). Free for the StartX community and anyone else to use, modify, and share. The only condition is that the copyright and license notice travel with it.
