# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repo is an open-source (MIT) collection of AI agent skills for running an AI-driven software development lifecycle (SDLC). It is published as a **Claude Code plugin marketplace**, so other repos (the author's and anyone else's) can install the skills instead of copying them.

Today it targets Claude Code only. Support for other agents may come later, so skill content should describe the *workflow*. Avoid relying on Claude-specific tool names or harness behavior unless the skill really needs them.

Skills must stay generic and stand on their own. Anything specific to one consumer belongs in that consumer's `CLAUDE.md`, not here. That includes task-ID formats, roadmap files, build commands, and merge policy. Each skill should:
- name the settings a repo can override, with a sensible default for each, and tell the agent to read the repo's instructions first;
- default to the safer choice for anything irreversible or outward-facing (e.g. ask before merging).

Each plugin's `README.md` documents those settings for humans, with an example `CLAUDE.md` snippet.

## Layout

The repo follows Claude Code's plugin marketplace layout:

```
.claude-plugin/marketplace.json   # marketplace catalog: lists each plugin and its source path
plugins/<plugin-name>/
  .claude-plugin/plugin.json      # plugin manifest (name, description, version, author)
  skills/<skill-name>/SKILL.md    # one directory per skill
  skills/<skill-name>/...         # optional supporting files the skill references (scripts, templates, references)
```

- A **plugin** groups related skills that a consumer installs together, for example by SDLC phase. A **skill** is one focused capability.
- Each `SKILL.md` starts with YAML frontmatter that has `name` (kebab-case, matching the directory name) and `description`. The `description` decides when the agent loads the skill, so it should state what the skill does and when to trigger it.
- Put long reference material in separate files inside the skill directory, and have `SKILL.md` point to them. That keeps `SKILL.md` short, because it is loaded into context.
- When you add a plugin, add its entry to `.claude-plugin/marketplace.json`. When you change a plugin's behavior, bump its `version` in `plugin.json`.

## Validating and testing locally

```bash
claude plugin validate .                      # validate the marketplace and plugin manifests
```

To try the skills end-to-end, open Claude Code in another repo and run:

```
/plugin marketplace add /path/to/ai-sdlc      # or isaacbroyles/ai-sdlc from GitHub
/plugin install <plugin-name>@ai-sdlc
```
