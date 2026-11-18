---
name: github-flow
description: Use when starting, continuing, or finishing a change that should land through a pull request, such as "start work on X", "open a PR for this", "ship this", or "merge it". Runs GitHub flow end to end. It branches from the latest default branch, commits, pushes, opens a PR, waits for CI, merges, and cleans up, following any conventions the repository defines.
argument-hint: "[what the change is, or a task reference]"
---

# GitHub flow

GitHub flow is a lightweight, branch-based workflow:

1. The default branch is always releasable. Nobody commits to it directly.
2. Every change gets its own short-lived branch, created from the latest default branch.
3. Work is committed in small, logical steps and pushed early.
4. A pull request is the place where the change is described, reviewed, and checked by CI.
5. The change is merged only after its checks pass and any required reviews are in.
6. The branch is deleted after the merge. If merging deploys, the merge is the release.

This skill carries out that flow. If it was invoked with arguments (`$ARGUMENTS`), treat them as the description of the change, or as a pointer to where that description lives.

## Repository conventions come first

This skill is generic on purpose. Each repository decides its own specifics, and those always override the defaults below. Before starting, look for conventions in:

- `CLAUDE.md` / `AGENTS.md` (look for a git, workflow, or contributing section)
- `CONTRIBUTING.md`
- `.github/pull_request_template.md` (or the `.github/PULL_REQUEST_TEMPLATE/` directory)
- `.github/workflows/*.yml`, to learn which checks run on pull requests and which workflows run on push to the default branch (deploys)
- `git log --oneline -20` on the default branch, to learn the existing commit and merge style

A repository can set any of these:

| Setting | Default when the repository says nothing |
|---|---|
| Branch naming | 2–5 word kebab-case summary, e.g. `fix-login-redirect` |
| Commit / PR title format | Imperative summary, matching the style in `git log` |
| Work-item references (task IDs, issue numbers) | Include one if the user gave one; reference issues with `Closes #N` in the PR body |
| Local checks to run before pushing | Whatever the PR workflows run that can feasibly run locally |
| Extra steps that must land in the same PR | None |
| Merge method | The only method the repo allows; otherwise ask |
| Merge authorization | **Ask before merging** |
| Post-merge verification (deploys) | Report the deploy run if one was triggered |

## 1. Preflight

```bash
gh auth status
gh repo view --json defaultBranchRef,mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed,deleteBranchOnMerge
git status --porcelain
git branch --show-current
```

- **Already on a non-default branch:** run `gh pr view --json number,state,url,headRefName`. If an open PR exists, you are continuing that change. Skip to the step that fits (keep implementing, push, or watch CI). Do not start a new branch. If there is no PR and the branch clearly belongs to this change, continue on it. Otherwise, ask.
- **Uncommitted changes on the default branch:** if they belong to this change, carry them onto the new branch (`git switch -c` keeps them). If they are unrelated or unclear, stop and ask whether to stash, commit them separately, or leave them.
- If `gh` is not authenticated or there is no GitHub remote, stop and tell the user. Do not work around it.

## 2. Sync and branch

```bash
git switch <default>
git pull --ff-only origin <default>
git switch -c <branch>
```

- If `--ff-only` fails, the local default branch has diverged from the remote. Stop and report it. Do not reset or rebase it on your own.
- Before creating the branch, check that the name is free locally and on the remote (`git ls-remote --heads origin <branch>`). If it is taken, stop and ask.

## 3. Implement and commit

- Keep commits small and logical. Each one should leave the tree in a working state.
- Follow the repository's commit message format, and add any attribution trailer your instructions require.
- Keep to one change per branch. If you find unrelated problems, write them down as follow-ups in the PR body rather than fixing them here.
- Do any extra same-PR steps the repository requires (changelog entry, ticking a roadmap item, version bump).

## 4. Verify locally

Run the checks the repository names, or the parts of its PR workflows that can run locally, such as build, lint, and tests. Fix any failures before pushing. If a check cannot run locally, say so and let CI cover it.

## 5. Push and open the pull request

```bash
git push -u origin HEAD
gh pr create --base <default> --title "<title>" --body-file <file>
```

- If the repository has a PR template, fill it in. Otherwise the body covers: what changed and why, how it was verified, linked work items, and follow-ups.
- Open the PR as a draft (`--draft`) if the user said the work is not finished.
- Report the PR URL to the user.

## 6. Wait for CI

```bash
gh pr checks --watch --fail-fast
```

- Checks can take a few seconds to register after a push. If the output says no checks were reported, wait briefly and try again before concluding the repository has no CI.
- **On failure:** find the failing run (`gh pr checks` lists the links) and read `gh run view <run-id> --log-failed`. Fix the cause, commit, push, and watch again.
- Stop after 3 failed fix attempts. Hand back to the user with a summary of what is failing and what you tried.
- Never weaken, skip, or delete a check to make it pass unless the user explicitly asks.

## 7. Merge

Check that the PR is ready:

```bash
gh pr view --json mergeStateStatus,reviewDecision,statusCheckRollup
```

- If `reviewDecision` is `REVIEW_REQUIRED` or `CHANGES_REQUESTED`, stop. Report that the PR is waiting on review. Do not approve your own PR.
- **Authorization:** merge without asking only if the repository's instructions or the user explicitly say so. Otherwise, show the PR URL and check status, then ask for confirmation.
- **Method:** use what the repository specifies. If it says nothing, use the only allowed method. If several are allowed, ask.

```bash
gh pr merge <number> --<merge|squash|rebase> --delete-branch
```

If the repository says to use auto-merge, run `gh pr merge <number> --auto --<method>` once the PR is open. GitHub then merges it when the required checks pass. If auto-merge is not enabled on the repository, this command fails. In that case, report it and fall back to the normal flow.

## 8. Clean up

`gh pr merge --delete-branch` already deletes the remote and local branch and switches to the default branch. Bring the default branch up to date:

```bash
git switch <default>
git pull --ff-only origin <default>
git fetch --prune
```

- If the local branch still exists (for example after an auto-merge, or if `gh` could not delete it), confirm the PR shows `MERGED` (`gh pr view <number> --json state`), then delete it. After a squash or rebase merge, `git branch -d <branch>` refuses because the branch commits are not ancestors of the default branch, so use `git branch -D <branch>`.
- If merging triggered a deploy workflow, find the run (`gh run list --branch <default> --limit 5`), watch it (`gh run watch <run-id>`), and report the result and any URL it published.

## Guardrails

- Never commit or push directly to the default branch.
- Never force-push, unless the user asks. If they do, use `--force-with-lease` and only on your own branch.
- Never bypass protections: no `gh pr merge --admin`, no `--no-verify`, and no disabling of checks.
- Never merge while checks are failing or pending.
- Never approve your own pull request.
- Stop and ask whenever the state is surprising (diverged branches, a name collision, someone else's commits on the branch) instead of resolving it destructively.
