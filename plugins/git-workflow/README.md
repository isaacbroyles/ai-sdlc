# git-workflow: GitHub flow skill for Claude Code

A Claude Code plugin from [ai-sdlc](../../README.md) for landing changes through source control. Its `github-flow` skill automates the pull request lifecycle: branch, commit, open the PR, wait for CI, merge, and clean up, following your repository's own conventions.

## Skills

### `github-flow`

Runs [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) from start to finish. It branches from the latest default branch, commits, verifies locally, opens a pull request, waits for CI (fixing failures, up to 3 attempts), merges, and cleans up.

The skill is generic. Anything specific to your repository goes in that repository's `CLAUDE.md`. The skill reads it and follows it over its own defaults.

## Install

```
/plugin marketplace add isaacbroyles/ai-sdlc
/plugin install git-workflow@ai-sdlc
```

## Configuring it for your repository

Add a section like this to the consuming repository's `CLAUDE.md`. Include only what differs from the defaults. With no settings, the skill asks before merging and picks up conventions from `git log`, the PR template, and the CI workflows.

```markdown
## Git workflow

All changes land through the `github-flow` skill. Never commit directly to `master`.

- Branch names: `<task-id>-<summary>`, e.g. `t1-5-useful-404`.
- Commit and PR titles end with the task ID: `Add useful 404 page (T1.5)`.
- Before pushing, run `bundle exec jekyll build` and `npm run lint:md`.
- Tick the task's checkbox in `docs/roadmap.md` in the same PR.
- Merge with merge commits, without asking, once all checks pass.
- Merging deploys the site. Watch the `pages.yml` run and report the live URL.
```

Because this line sits in `CLAUDE.md`, the "never commit directly" rule applies even in sessions where the skill doesn't load.

### Permissions

To keep the flow from pausing at every step, allow the routine commands in the consuming repository's `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(git switch:*)",
      "Bash(git pull --ff-only:*)",
      "Bash(git push -u origin:*)",
      "Bash(gh pr create:*)",
      "Bash(gh pr view:*)",
      "Bash(gh repo view:*)",
      "Bash(gh pr checks:*)",
      "Bash(gh run list:*)",
      "Bash(gh run view:*)",
      "Bash(gh run watch:*)"
    ]
  }
}
```

Leave `gh pr merge` off the list if you want to approve every merge yourself.

### Repository settings worth turning on

- **Automatically delete head branches.** This keeps merged branches from piling up on the remote.
- **Branch protection on the default branch with required status checks.** GitHub then enforces "no merge on red" itself. Together with **Allow auto-merge**, this lets you tell the skill to use `gh pr merge --auto`.
