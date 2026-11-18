# Contributing

Thanks for helping improve these AI SDLC skills for Claude Code.

## What makes a good skill here

- It describes a generic workflow that any repository could use.
- Anything specific to one project (task-ID formats, build commands, merge policy) is a setting the consuming repository overrides in its own `CLAUDE.md`, with a sensible default in the skill.
- Irreversible or outward-facing steps default to the safer choice, such as asking before merging.

[`CLAUDE.md`](CLAUDE.md) describes the repository layout and conventions in full.

## Before opening a pull request

1. Validate the marketplace and plugin manifests:

   ```bash
   claude plugin validate .
   ```

2. Try the skill end to end from another repository:

   ```
   /plugin marketplace add /path/to/ai-sdlc
   /plugin install <plugin-name>@ai-sdlc
   ```

3. If you changed a plugin's behavior, bump its `version` in `plugins/<plugin-name>/.claude-plugin/plugin.json`.
4. If you added a plugin, list it in `.claude-plugin/marketplace.json` and in the table in [`README.md`](README.md).

## Security expectations

Skills are instructions an agent runs with the installing user's permissions, so review them like code. The `Validate` workflow enforces the following, and a maintainer must sign off on any exception:

- No hooks, MCP servers, scripts, or executables inside plugins. Plugins hold Markdown, JSON, and PNG files only.
- No HTML comments, invisible or bidirectional Unicode characters, or encoded content.
- No commands in code blocks that pipe downloads into a shell, decode base64, use `--dangerously-*` flags, or bypass protections (`--admin`, `--no-verify`).
- Links only to allowlisted hosts (see `.github/scripts/lint.py`).
- Marketplace entries must use local `./plugins/...` sources, never external repositories.
- Never weaken a guardrail (asking before merging, no force-push) to make a workflow faster.

Run the same check locally with `python3 .github/scripts/lint.py`. Report vulnerabilities privately as described in [`SECURITY.md`](SECURITY.md).
