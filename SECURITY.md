# Security policy

## Scope

This catalog ships **metadata** that points users at skills. Each skill is a separate codebase with its own security posture. The split:

| Issue | Where to report |
|---|---|
| Bug or vulnerability in a specific skill's code | The skill author's own repo (see the skill's README) |
| Malicious skill listed in this catalog | This repo — see "Reporting" below |
| Typosquat / impersonation of a real skill | This repo |
| Catalog-level vulnerability (CI workflow, marketplace.json poisoning, supply chain) | This repo |
| Vulnerability in Claude Code itself | [anthropics/claude-code security advisories](https://github.com/anthropics/claude-code/security) |

## Reporting

For anything in the "report to this repo" rows above:

1. **Do not open a public issue** if the bug allows malicious code execution.
2. Email a curator directly — handles listed in `.github/CODEOWNERS`. Each curator should have a contact email on their GitHub profile.
3. Expect an initial response within 7 days. Curators are volunteers; the SLA is best-effort, not enterprise-grade.

## What curators will do

- Verify the report.
- If a listed skill is malicious or compromised: remove the marketplace.json entry, archive or delete the offending `/skills/<author>/` dir, revoke the author's org membership if warranted, and publish a notice in the next release tag.
- If the catalog itself is compromised (e.g., a curator's account was taken over): rotate credentials, audit recent merges, re-tag.

## Trust model recap

This catalog is curated by humans who verify each contributor is a member of the StartX founder community before granting write access. We do **not** security-audit submitted code. Installing any plugin — from this catalog or any other — runs arbitrary code with your user privileges. Treat every skill as if it were a script someone handed you on a USB drive.
