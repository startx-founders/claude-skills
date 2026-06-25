# startx-office-hours-prep

Prepares a StartX founder for a mentor session (office hours, a mentor 1:1, or a Lead Mentor 1:1). Runs the StartX forcing questions, routes by session type, company stage, and BoA cycle phase, and helps you build a prep doc in StartX's challenge format plus a mentor-note outline you write your message from. Helps sharpen the founder's thinking; it does not decide for the founder or invent evidence.

## The StartX BoA AI Skills family

One of three skills in the **StartX BoA AI Skills family** (by [1SF](https://github.com/1SF)). Each helps you think your way through one part of the BoA loop; none does the work or makes the calls for you:

- **startx-office-hours-prep** helps you sharpen a mentor session: the question to bring and how to frame it.
- **startx-boa-prep** helps you get ready for a board meeting: the challenges to put to the board and the evidence behind them.
- **startx-boa-debrief** helps you debrief afterward: think through the board's input and shape your own follow-up and next steps.

Loop: prepare, meet, debrief, and carry it into the next round. Overview: [the family README](../README.md).

## Usage

`/startx-office-hours-prep` in Claude Code, from your working or notes directory. Hand it your deck, wiki, or notes; it reads those first and asks only the gaps (usually 2 to 4 questions), building a resumable draft. It writes `office-hours-prep-YYYY-MM-DD.md` and labels every output BRING TO SESSION or KEEP INTERNAL.

## Requirements

Any Claude surface. No sudo, mount, or API. In Claude Code or Cowork the draft persists in your working directory; in the claude.ai app, download or copy it before closing. Resume any time by handing the skill your draft.

## Status

v1.2 (2026-06-24). Companion to `startx-boa-prep` and `startx-boa-debrief`. History in the SKILL.md CHANGELOG.

## Guardrails

- **Sharpen, do not replace.** No decisions are made for the founder. No fabricated evidence, quotes, metrics, or traction. Missing evidence is named, not invented, and the skill says how to get it.
- **Non-endorsement.** A community-contributed skill, developed and released by Adam McGinty (1SF); not affiliated with, endorsed by, or audited by StartX or Anthropic.
- **Not advice.** An operations and planning aid, not legal, regulatory, medical, or financial advice.

## Disclaimer

This skill, and any document it produces, is for informational purposes only and does not constitute legal, medical, financial, or other professional advice. It is provided "as is", without warranties of any kind, express or implied, including merchantability, fitness for a particular purpose, and non-infringement. To the fullest extent permitted by law, the author and contributors disclaim all liability for any loss or damage arising from its use. Consult a qualified professional before acting on its output.

## License

MIT, see [LICENSE](LICENSE). By [Adam McGinty](https://github.com/1SF), StartX mentor.
