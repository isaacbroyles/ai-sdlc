# Security policy

Skills in this repository are instructions that an AI agent follows with the permissions of the person who installed them. A malicious or careless change can therefore run commands, expose secrets, or weaken safeguards. We treat that as a security issue.

## Reporting a vulnerability

Please report privately through [GitHub's private vulnerability reporting](https://github.com/isaacbroyles/ai-sdlc/security/advisories/new). Do not open a public issue.

Examples worth reporting:

- A skill that can be made to run unintended commands, leak credentials, or bypass its own guardrails.
- Hidden or obfuscated content in a skill, manifest, or workflow.
- A way to alter what installs from the marketplace without review.
- A look-alike repository impersonating this one.

You can expect an acknowledgement within 7 days. Please allow reasonable time to fix the issue before disclosing it.

## Supported versions

Only the latest release of each plugin is supported. Install from a release tag or commit SHA rather than a moving branch.

## Verifying you have the real thing

The only official source is `github.com/isaacbroyles/ai-sdlc`. Check the owner and spelling before running `/plugin marketplace add`.
