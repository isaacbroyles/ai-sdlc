# AI SDLC skills for Claude Code

Open-source [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) skills for running an **AI-driven software development lifecycle (AI SDLC)**. They ship as a [Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces), so any repository can install them with two commands instead of copying prompts around.

The first plugin, [`git-workflow`](plugins/git-workflow/), includes a **GitHub flow skill**. It takes a change from a fresh branch to a merged pull request: commit, verify locally, open the PR, wait for CI and fix failures, merge, and clean up.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code plugin marketplace](https://img.shields.io/badge/Claude%20Code-plugin%20marketplace-D97757)](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
[![Agent Skills](https://img.shields.io/badge/format-Agent%20Skills%20(SKILL.md)-555)](https://docs.claude.com/en/docs/claude-code/skills)

## Quick start

In Claude Code:

```
/plugin marketplace add isaacbroyles/ai-sdlc
/plugin install git-workflow@ai-sdlc
```

Then ask for a change the way you normally would, e.g. *"start work on fixing the login redirect"*, *"open a PR for this"*, or *"ship it"*. The skill loads on its own and runs the flow.

## Plugins and skills

| Plugin | Skill | SDLC phase | What it does |
|---|---|---|---|
| [`git-workflow`](plugins/git-workflow/) | [`github-flow`](plugins/git-workflow/skills/github-flow/SKILL.md) | Implement, review, release | Runs GitHub flow end to end: branch from the latest default branch, commit, verify, open a pull request, watch CI (fixing failures, up to 3 attempts), merge, clean up, and report any deploy. |

Each plugin's README lists its skills, the settings a repository can override, and an example `CLAUDE.md` snippet.

## How the skills work

- **Your repository's conventions win.** Each skill reads the consuming repository's own instructions (`CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, PR templates, CI workflows, `git log`) and follows them over its defaults: branch names, commit format, task IDs, local checks, merge method.
- **Safe by default.** Anything irreversible or outward-facing, such as merging, defaults to asking first. The skills never force-push, bypass branch protection, skip hooks, or approve their own pull requests.
- **Generic and portable.** Nothing in a skill is tied to one project. Settings that differ per repository are documented with a default for each.

## FAQ

### What is an AI SDLC?

An AI-driven software development lifecycle is one where a coding agent carries out SDLC steps, such as branching, implementing, testing, opening pull requests, responding to CI, and releasing, under rules the team writes down once. This repository packages those rules as reusable agent skills.

### What is a Claude Code skill?

A skill is a folder with a `SKILL.md` file: YAML frontmatter (`name`, `description`) plus instructions. Claude Code loads a skill automatically when a request matches its description. Skills are bundled into plugins, and plugins are distributed through marketplaces like this one. See the [Claude Code skills docs](https://docs.claude.com/en/docs/claude-code/skills).

### Can I use the GitHub flow skill with my existing branch and PR rules?

Yes. Add a short "Git workflow" section to your repository's `CLAUDE.md` with only what differs from the defaults (branch naming, title format, pre-push checks, merge method, whether to merge without asking). The [`git-workflow` README](plugins/git-workflow/README.md#configuring-it-for-your-repository) has a full example.

### Does it work with agents other than Claude Code?

The skills use the plain `SKILL.md` format and describe the workflow rather than Claude-specific tools, but today they are only tested with Claude Code.

## Contributing

Contributions are welcome, especially skills for other SDLC phases. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

[MIT](LICENSE)
