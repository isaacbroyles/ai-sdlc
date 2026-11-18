# ai-sdlc

Agent skills for running an AI-driven software development lifecycle, published as a [Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces).

The skills describe generic workflows. Each one reads the consuming repository's own instructions (`CLAUDE.md`, `CONTRIBUTING.md`, PR templates, CI workflows) and follows them over its defaults. Anything irreversible or outward-facing, such as merging, defaults to asking first.

## Install

In Claude Code:

```
/plugin marketplace add isaacbroyles/ai-sdlc
/plugin install <plugin-name>@ai-sdlc
```

## Plugins

| Plugin | What it does |
|---|---|
| [`git-workflow`](plugins/git-workflow/) | Lands changes through GitHub flow: branch, commit, pull request, CI, merge, clean up. |

Each plugin's README lists its skills, the settings a repository can override, and an example `CLAUDE.md` snippet.

## Contributing

See [`CLAUDE.md`](CLAUDE.md) for the repository layout and conventions. Validate manifests before opening a pull request:

```bash
claude plugin validate .
```

## License

[MIT](LICENSE)
