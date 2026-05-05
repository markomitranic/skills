---
name: jira-ticket
description: Write a Jira ticket with a clear 3-part structure. Use this skill whenever the user asks you to write, draft, refine, restructure, or split Jira tickets, work items, user stories, backlog items, or sprint tickets — including when they paste raw context, transcripts, meeting notes, or product specs and want them turned into tickets.
---

# Jira ticket writing

Summarize all the information, context, and decisions, so that developers can easily catch up and clearly understand what they need to do. Make sure to include all the information and not lose information or context.

## Workflow

When the user dumps raw context (a transcript, a meeting note, a Slack thread, a spec) or the prior part of the current conversation, use the project manager personality to deeply understand the request:

1. Research dependencies and understand the request:
   - The core objective (what is being built/fixed/changed)
   - Explicit requirements vs. implied requirements
   - Technical constraints and dependencies
   - Stakeholders or teams impacted
2. Initiate a team of agents to perform deeper research:
   - Sub-agent to use the Atlassian skills and MCP tools to look up relevant Confluence pages or Jira tickets that duplicate or relate to the request.
   - Sub-agent to access the codebase or documentation to understand technical constraints or terms.
3. Ask the user clarifying questions until all gaps are filled and decisions are made.
   - Analyze the problem from multiple angles and identify **information gaps** that would result in vague or incomplete ticket
   - Correct technical wording (uniform component or uniform composition)
   - Edge cases, error states or logical conflicts
   - Missing non-functional requirements (performance, security, accessibility)
   - Ambiguous scope boundaries
   - Unstated integration points (which services does this touch?)
   - Edge cases not covered (error handling, empty states, concurrent access)
4. Print the ticket(s) on screen for the user to review and copy-paste into Jira.
5. Offer some ideas for assets/images/screenshots they could attach to the ticket.

## Structure

Every ticket has exactly three sections, in this order:

1. **Why** — 2 sentences in a "note" block. Paint a picture of the scenario/goal of the ticket. Avoid generic value props and marketing language. Be specific.
2. **Description** — plain language, succinct and information dense, using technical language. If there are any relevant Confluence documents, Figma designs, URLs of note or Jira ticket references, include them in the description.
3. **Acceptance criteria** — a testable list. Each item is something a human or test could verify.
   - A flat list without emoji
   - Each item starts with the system or actor: "The CMS field exists...", "The endpoint accepts...", "The frontend renders..."
   - Is testable. Either by a human or by an automated check.
   - Covers the happy path AND at least one fallback, edge case, or error condition.
   - Aim for 4–8 items. More than 8 is a smell that the ticket is too big and should be split.
