---
name: pr-open
description: Use when opening or editing a pull request.
---

# File PR

Open a PR for the current branch on GitHub, against the main branch, with a description aimed first and foremost to humans - easy to read, with a clear outline.

Analyze the changes made in the current branch, take into account the context of the current conversation, and use MCP servers to read the Jira ticket. If the user did not provide a Jira ticket, ask them to provide one, and explain that it is crucial to help you write a better description for the PR.

**Rebase onto latest 'main' before opening.** Stale branches conflict and waste a review round.

## Title

Make sure titles follow conventions from the repo. They should be simple and easy to understand. Conventional commit styles in projects that use them, i.e. "fix: new threads no longer spike CPU"

The title should follow the format "feat: T40NOA-1234 add new feature X", "fix: resolve issue Y", "refactor: improve code structure for Z", etc. This helps reviewers quickly understand the nature of the changes being proposed. The title should be concise, ideally under 60 characters, but must clearly convey the main purpose of the PR or why the change matters. Do not use symbols in the title.

BAD: perf: negotiate permessage-deflate on the websocket
GOOD: perf: cut websocket frame size by 70%+ with gzip

## Description

PR descriptions should aim for simplicity. Open with a minimal, clear description of the problem. Follow up with how you solved it.

The PR must open with an explanation of WHY this was done - what is the use case and the problem it solves. Simple explanation of the problem, with a concrete example, based on the user's original prompt and task, and a brief explanation of the solution.

BAD: Removed explicit workspace carry-over from every new thread entrypoint (cmd+n / cmd+shift+o, sidebar v1/v2, command pallete). New threads inherit only the project from context, branch worktree, and env mode always come from configured defaults. Deleted buildContextualThreadOptions, and the v1 sidebar's seed-context machinery.

GOOD: The "new worktree" setting was ignored when starting new threads on existing worktrees, which was super unintuitive for the user. The user-preferences now always apply, regardless of the screen you are on.

This is also where you'd attach a Jira or Figma links, API docs links, Chromatic or local Storybook links for easy navigation. Whatever matches the context of the PR. This helps reviewers understand the background and motivation behind the changes.

After the opening, expand with a description, which begins non-technical and becomes more technical as it goes deeper into the details:

1. The first paragraph should explain in two simple sentences, in non-technical terms, what the purpose of the task was, and where the boundaries of its scope are.
2. Then, create line items for large actions that were performed, grouping related changes together. For example:
   - Handlers were moved into a specific folder for better organization.
   - Error handlers were added to all APIs that were missing them, improving error handling across the board.
3. Finally, write down any additional details or exceptions where the implementation deviates from the original plan. This can include any challenges faced during development, any trade-offs made, or any future considerations that should be kept in mind when working with this code. This section can also include any relevant technical details that may be useful for reviewers or future developers who will work on this codebase.

**Appendices:**

Attach UI screenshots, videos or images that can help reviewers visualize the changes. This can make it easier for reviewers to grasp the impact of the changes without having to run the code.

Test plan is not needed. Please skip it. For how to capture and upload media, see the next chapter.

## Screenshots and videos

Upload media with `gh --attach` (gh 2.100+). It works on `gh pr create`, `gh pr edit`, `gh pr comment` and `gh issue comment`, up to 50 files per command, and stores them as GitHub's own `user-attachments`, same as dragging into the web editor. Never commit media to the repo or an assets branch.

### 1. Capture before and after from the same setup

- Use `agent-browser` with a named session and a fixed viewport: `agent-browser set viewport 1280 640 2` (2x for crisp images; pick a height that crops empty space).
- Prefer Storybook's iframe URL. It renders one story without the chrome, and args and globals go in the query string: `iframe.html?id=<story-id>&viewMode=story&globals=theme:CBB&args=theme:pale-orange;itemsTheme:none`. Story ids are listed at `/index.json`.
- One scenario per variant that matters: the bug, the case the fix must not regress, any case the reviewer must decide on.
- After: check out the PR head without touching branch names: `git fetch origin pull/<n>/head:pr-<n> && git checkout pr-<n>`.
- Before: revert only the changed source files with `git checkout main -- <files>` (leave stories alone so the same story ids exist), let HMR rebuild, then rerun the same capture script with a `before` prefix. Restore with `git checkout pr-<n> -- <dir>`.
- Script the capture loop (open, `wait --load networkidle`, screenshot) so before and after are pixel-comparable.
- External images that can't load (sandbox, no network) leave empty boxes. Swap them before the screenshot with an `agent-browser eval` that strips `srcset` and sets every `img.src` to an SVG gradient data URI. Put the JS in a file and pass `"$(cat stub.js)"`; inline quoting breaks silently. Say in the comment that images are stand-ins.
- Read one before and one after image yourself before uploading, to confirm the difference is visible.

### 2. Upload them into a table

Reference each file as `![alt](./file.png)` in the body, and attach the same paths. gh uploads them and rewrites each reference to its `user-attachments` URL:

```md
### CBB, items theme `none` (the bug)
Bottom corners were square against the invisible card; now rounded.

| Before | After |
|---|---|
| ![before-cbb-no-item-theme](./before-cbb-no-item-theme.png) | ![after-cbb-no-item-theme](./after-cbb-no-item-theme.png) |
```

```sh
cd "$SHOTS"
ARGS=(); for f in before-*.png after-*.png; do ARGS+=(--attach "./$f"); done
gh pr comment <n> --body-file "$BODY" "${ARGS[@]}"
```

- Only `![alt](./path)` is rewritten. `<img src="./path">` is left as a broken relative path, and the file gets appended at the end of the body instead.
- Run from the folder holding the files, and write the `--attach` paths exactly as the body spells them (`./name.png`).
- Attached files the body doesn't reference are appended at the end.
- `--edit-last` with `--attach` rewrites your last comment in place, which is useful for reshooting.
- Videos attach the same way and render as a player.
- One heading and one sentence per scenario saying what to look at.
- Check the result: `gh api <comment-api-path> -q .body | grep -cF '](./'` must print 0.

### 4. Clean up

Stop the dev server, run `agent-browser close`, switch back to the worktree's branch and delete the local `pr-<n>` branch. The harness may rename the worktree branch during a session; if checkout fails, find the current name with `git reflog`.

## Tone of voice

- Explain conceptually what has changed, in a friendly way like a senior teaching a junior.
- Group related concepts together
- Order by intent, cluster into themes
- Describe user-visible and system-visible impact
- Real examples are better than abstract language
- ASCII drawings are a useful tool to illustrate change's place in the architecture.
- Do not sign as Claude, you are acting in my name.

## After PR is opened

- Respond to the user with a message confirming that the PR has been opened successfully, and provide a link.
- Babysit/monitor the PR, and load the /pr-triage skill to handle any follow-up actions or updates needed for the PR.
