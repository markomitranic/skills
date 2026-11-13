---
name: jira-ticket
description: Use whenever asked to write a jira ticket.
argument-hint: "What is the ticket about?"
---

# Jira ticket writing

Summarize all the information, context, and decisions, so that developers can easily catch up and clearly understand what they need to do.

- A ticket is not a spec. Focus on intent and requirement.
- Ticket tells a story of what needs to be done and why, but it should not include technical details.
- Nobody likes a wall of text and technical jargon.
- The ticket should be concise and focused on the outcome, not the implementation.
- It should be easy to read by PMs, QAs, designers, and developers alike. A good ticket explains WHAT, not HOW it's done.

## Planning

When the user dumps raw context (a transcript, a meeting note, a Slack thread, a spec) or the prior part of the current conversation, use your project manager persona to deeply understand the request:

1. Research dependencies and understand the request:
   - The core objective (what is being built/fixed/changed)
   - Explicit requirements vs. implied requirements
   - Technical constraints and dependencies
   - Stakeholders or teams impacted
2. Perform deeper research/planning if needed, for example:
   - Look up relevant Confluence pages or Jira tickets that duplicate or relate to the request.
   - Access the codebase or documentation to understand technical constraints or terms.
   - When results are in, analyse the problem from multiple angles and identify **information gaps** that would result in vague or incomplete ticket
3. Ask the user clarifying questions until all gaps are filled and decisions are made. Use `AskUserQuestion` tool.
   - Correct technical wording (double check the verbs and technical terms)
   - Edge cases, error states or logical conflicts
   - Missing non-functional requirements (performance, security, accessibility)
   - Ambiguous scope boundaries
   - Unstated integration points (which services does this touch?)
   - Edge cases not covered (error handling, empty states, concurrent access)
4. Print the ticket(s) on screen for the user to review and copy-paste into Jira.

Never leave any unanswered questions - if there are unanswered questions, repeat the interview process until all questions are answered!

## Structure

Every ticket has exactly three sections, separated with dividers, in this order:

1. Short sentences to explain the situation. Maximum 200 characters Avoid generic value props and marketing language. Explain the problem from the outside, with specific and concise language, grounded in terms that normies will understand.  
   Example: "Retail agents can create 5G orders and send a payment link via SMS. The payment steps our website gets from the API sometimes come in a failed state. We should display a friendly error."
2. Description, using technical language. Maximum 1000 characters. Use clever formatting, tables, chapters, to visually break it up for ease of reading. If there are any relevant Confluence documents, Figma designs, URLs of note or Jira ticket references, include them in the description. All links and jira ticket refs should be clickable. Attach an ASCII diagram if it helps clarify the structure of a system or flow.
3. **Acceptance criteria** — a testable list. Each item is something a human or test could verify.
   - A flat list without emoji
   - Each item starts with the system or actor: "The CMS field exists...", "The endpoint accepts...", "The frontend renders..."
   - Is testable. Either by a human or by an automated check.
   - Covers the happy path AND at least one fallback, edge case, or error condition.
   - Aim for 4–8 items. More than 8 is a smell that the ticket is too big and should be split.
