---
name: pr-review
description: Use when the user asks for a local review of their changes, a diff, a set of decisions, or a pull request.
argument-hint: "What should be reviewed? A PR number, branch, path, or nothing for the current changes."
---

# PR Review

Run two Opus/Sol sub-agents, then triage their findings with the user. You are the advisor between the reviewers and the user, not the reviewers' executor.

**Correctness reviewer**

> Invoke the `code-review` skill with `high <target>`. Do not pass `--comment` or `--fix`: nothing gets posted to GitHub and no files get changed. Intent of the change: <summary>. Return the findings as a list with file, line, the claim, and a concrete failure scenario.

**Quality reviewer**

> Invoke the `thermo-nuclear-code-quality-review` skill against <target>.

When both reviewers report back, merge overlapping findings into a list. Then, load `/pr-triage` skill and run its verdict process over the responses as they come in. This is a local review. Skip the GitHub parts of `/pr-triage`: no replies, no resolving threads.