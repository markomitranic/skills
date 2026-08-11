---
name: pr-open
description: File a concise pull request. Use when the user asks to file, open or create a PR.
---

# File PR

Open a PR for the current branch on GitHub, against the main branch, with a description aimed first and foremost to humans - easy to read, with a clear outline.

Analyze the changes made in the current branch, take into account the context of the current conversation, and use MCP servers to read the Jira ticket. If the user did not provide a Jira ticket, ask them to provide one, and explain that it is crucial to help you write a better description for the PR.

## Title

The title should follow the format "feat: T40NOA-1234 add new feature X", "fix: resolve issue Y", "refactor: improve code structure for Z", etc. This helps reviewers quickly understand the nature of the changes being proposed. The title should be concise, ideally under 60 characters, but must clearly convey the main purpose of the PR or why the change matters. Do not use symbols in the title.

   BAD: perf: negotiate permessage-deflate on the websocket
   
   GOOD: perf: cut websocket frame size by 70%+ with gzip

## Description

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

Attach UI screenshots or images that can help reviewers visualize the changes. This can make it easier for reviewers to grasp the impact of the changes without having to run the code.

Test plan is not needed. Please skip it.

## Tone of voice

- Explain conceptually what has changed, in a friendly way like a senior teaching a junior.
- Group related concepts together
- Order by intent, cluster into themes
- Describe user-visible and system-visible impact
- Real examples are better than abstract language
- ASCII drawings are a useful tool to illustrate change's place in the architecture.
- Do not sign as Claude, you are acting in my name.

## Response to user

After the PR is created, respond to the user with a message confirming that the PR has been opened successfully, and provide a link to the PR for easy access. Additionally, include any suggestions for further improvements the user could manually make for the PR, such as suggestions for relevant link ideas or screenshot ideas.