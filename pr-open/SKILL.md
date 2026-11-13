---
name: pr-open
description: Use when opening or editing a pull request.
---

Open a PR for the current branch. Produce a clear and concise description that will onboard the reader to the problem space.
**Rebase onto latest 'main' before opening.** Stale branches conflict and waste a review round.

Read the Jira ticket. If the user did not provide a Jira ticket, ask them to provide one, and explain that it is crucial to help you understand the intent and request.

Start with short sentences to explain the situation. Maximum 200 characters Avoid generic value props and marketing language. Explain the problem from the outside, with specific and concise language, grounded in terms that normies will understand. You can usually infer intent based on the Jira ticket.

> Example: "Retail agents can create 5G orders and send a payment link via SMS. The payment steps our website gets from the API sometimes come in a failed state. We should display a friendly error."

## Title

Titles follow conventions from the repo. They should be simple and easy to understand. This helps reviewers quickly understand the intent of the PR. The title should be concise, ideally under 72 characters, and must clearly convey the main purpose of the PR or why the change matters. Do not use symbols in the title.

> Example: "fix: prevent CPU spikes on ELT workers"
> Example: "perf: cut websocket frame size by 70%+ with gzip"

## Description

Analyze the changes made in the current branch, take into account the context of the current conversation.

**1. Approach**
Open up with a brief explanation on how you solved the problem. Maximum 150 characters.

> Example: Changed the settings API so that user-preferences now always apply, regardless of the screen you are on.

**2. Scope**
Write a sentence on where the boundaries of its scope of the PR are. Was something left out intentionally? Does the implementation deviate from the original plan? Did we encounter trade-offs?

**3. Changes**
Write a flat list of top-level large actions that were performed, grouping related changes together.

> Example:
>
> - Moved handlers into folder for better organization.
> - Added error handlers to all APIs that were missing them.

**4. Attachments**

Attachment section is meant for providing additional context and resources related to the PR. This is where you'd attach a Jira or Figma links, API docs links, Chromatic or local Storybook links for easy navigation. Whatever matches the context of the PR.

Produce and attach UI screenshots, videos or images that can help reviewers visualize the changes. This can make it easier for reviewers to grasp the impact of the changes without having to run the code. Before/after go in a `| Before | After |` table, one row per scenario.

Upload with `--attach` on `gh pr create|edit|comment`, never via a repo branch. Write each file as `![alt](./file.png)` (an `<img src>` is not rewritten), and run from the files' folder:

```sh
gh pr comment <n> --body-file body.md --attach ./before.png --attach ./after.png
```

## Tone of voice

- Explain conceptually what has changed, in a friendly way like a senior teaching a junior.
- Group related concepts together
- Order by intent, cluster into themes
- Real-world examples are better than abstract or technical language
- ASCII drawings are a useful tool to illustrate change's place in the architecture.
- Do not sign as Claude, you are acting in my name.

## After PR is opened

- Respond to the user with a message confirming that the PR has been opened successfully, and provide a link.
- Babysit/monitor the PR, and load the /pr-triage skill to handle any follow-up actions or updates needed for the PR.
