# startx-boa-debrief

[![trigger evals](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fstartx-founders%2Fclaude-skills%2Feval-results%2Fbadges%2Fstartx-boa-debrief.json)](https://github.com/startx-founders/claude-skills/blob/eval-results/docs/skill-health.md)

Helps a StartX founder debrief a Board of Advisors meeting: think through the board's input, then turn it into a follow-up outline. It works from your own notes and recall, holds a confirmation gate so nothing you have not confirmed carries through, and helps you build a follow-up outline (you write the email in your voice) plus a handoff into your next pre-read. It organizes your thinking; it does not write the email, record the meeting, invent feedback, or replace judgment.

## The StartX BoA AI Skills family

One of three skills in the **StartX BoA AI Skills family** (by [1SF](https://github.com/1SF)). Each helps you think your way through one part of the BoA loop; none does the work or makes the calls for you:

- **startx-office-hours-prep** helps you sharpen a mentor session: the question to bring and how to frame it.
- **startx-boa-prep** helps you get ready for a board meeting: the challenges to put to the board and the evidence behind them.
- **startx-boa-debrief** helps you debrief afterward: think through the board's input and shape your own follow-up and next steps.

Loop: prepare, meet, debrief, and carry it into the next round. Overview: [the family README](../README.md).

## Usage

`/startx-boa-debrief` in Claude Code, from your working or notes directory. Hand it your prep doc and your meeting notes or recall; it helps you reconstruct what the board said, marks anything uncertain "to confirm" for you to confirm or cut, then helps you build a follow-up outline from confirmed content only that you write your email from. A safety pass runs before anything reaches your board.

## Requirements

Any Claude surface. No sudo, mount, or API. In Claude Code or Cowork files persist in your working directory; in the claude.ai app, download or copy before closing.

## Status

v1.0 (2026-06-24). Companion to `startx-boa-prep` and `startx-office-hours-prep`. History in the SKILL.md CHANGELOG.

## Guardrails

- **Sharpen, do not replace.** No decisions are made for the founder. No fabricated evidence, quotes, metrics, or traction. Missing evidence is named, not invented, and the skill says how to get it.
- **Non-endorsement.** A community-contributed skill, developed and released by Adam McGinty (1SF); not affiliated with, endorsed by, or audited by StartX or Anthropic.
- **Not advice.** An operations and planning aid, not legal, regulatory, medical, or financial advice.

## Disclaimer

This skill, and any document it produces, is for informational purposes only and does not constitute legal, medical, financial, or other professional advice. It is provided "as is", without warranties of any kind, express or implied, including merchantability, fitness for a particular purpose, and non-infringement. To the fullest extent permitted by law, the author and contributors disclaim all liability for any loss or damage arising from its use. Consult a qualified professional before acting on its output.

## License

MIT, see [LICENSE](LICENSE). By [Adam McGinty](https://github.com/1SF), StartX mentor.
