---
name: pr-open
description: Open a PR on GitHub, with a short and well-structured description of the changes, and a clear outline of the next steps in the project.
---

# PR Open Skill

Open a PR for the current branch on GitHub, against the main branch, with a description aimed first and foremost to humans - easy to read, with a clear outline, succinct.

Analyze the changes made in the current branch, take into account the context of the current conversation, and use MCP servers to read the Jira ticket. If the user did not provide a Jira ticket, ask them to provide one, and explain that it is crucial to help you write a better description for the PR.

## Title

The title should follow the format of "feat: T40NOA-1234 add new feature X", "fix: resolve issue Y", "refactor: improve code structure for Z", etc. This helps reviewers quickly understand the nature of the changes being proposed. The title should be concise, ideally under 50 characters, sacrifice grammar, caveman style, and should clearly convey the main purpose of the PR. Do not use symbols in the title.

## Description

The description should start with an explanation of WHY this was done - what is the use case and the problem it solves. The descriptions starts non-technical and becomes more technical and complex as it goes deeper into the details.

Start the body with links to Jira and Figma. Then, follow these steps to structure the description:

1. The first paragraph should explain in two simple sentences, in non-technical terms, what the purpose of the task was, and where the boundaries of its scope are.
2. Then, create line items for large actions that were performed, grouping related changes together. For example:
   - Handlers were moved into a specific folder for better organization.
   - Error handlers were added to all APIs that were missing them, improving error handling across the board.
3. Finally, write down any additional details or exceptions where the implementation deviates from the original plan. This can include any challenges faced during development, any trade-offs made, or any future considerations that should be kept in mind when working with this code. This section can also include any relevant technical details that may be useful for reviewers or future developers who will work on this codebase.
4. Add relevant links, to Jira tickets, Figma designs, Chromatic or local Storybook pages, local or preview API docs url or any other relevant resources that provide context for the changes made in this PR. This helps reviewers understand the background and motivation behind the changes. (If you have none, skip and suggest some ideas to the user in the response).
5. Attach any relevant screenshots or images that can help reviewers visualize the changes, especially if they involve UI modifications. This can make it easier for reviewers to grasp the impact of the changes without having to run the code. (If you have none, skip and suggest some ideas to the user in the response).
6. Test plan is not needed. Please skip it.
7. Claude signatures are not needed. Please skip them.

## Response to user

After the PR is created, respond to the user with a message confirming that the PR has been opened successfully, and provide a link to the PR for easy access. Additionally, include any suggestions (as mentioned in the description section) for further improvements the user could manually make for the PR, such as suggestions for relevant link ideas or screenshot ideas.
