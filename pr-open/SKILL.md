---
name: pr-open
description: Open a PR on GitHub, with a short and well-structured description of the changes, and a clear outline of the next steps in the project.
---

# PR Open Skill

Open a PR for the current branch on GitHub, against the main branch, with a description aimed first and foremost to humans - easy to read, with a clear outline, succinct.

The description should start with an explanation of WHY this was done - what is the use case and the problem it solves. The descriptions starts non-technical and becomes more technical and complex as it goes deeper into the details.

1. The first paragraph should explain in two simple sentences, in non-technical terms, what the purpose of the task was, and where the boundaries of its scope are.
2. Then, create line items for large actions that were performed, grouping related changes together. For example:
   - Handlers were moved into a specific folder for better organization.
   - Error handlers were added to all APIs that were missing them, improving error handling across the board.
3. Finally, write down any additional details or exceptions where the implementation deviates from the original plan. This can include any challenges faced during development, any trade-offs made, or any future considerations that should be kept in mind when working with this code. This section can also include any relevant technical details that may be useful for reviewers or future developers who will work on this codebase.
4. Add relevant links, to Jira tickets, Figma designs, Chromatic or Storybook pages or any other relevant resources that provide context for the changes made in this PR. This helps reviewers understand the background and motivation behind the changes. (If you have none, skip and suggest some ideas to the user in the response).
5. Attach any relevant screenshots or images that can help reviewers visualize the changes, especially if they involve UI modifications. This can make it easier for reviewers to grasp the impact of the changes without having to run the code. (If you have none, skip and suggest some ideas to the user in the response).
