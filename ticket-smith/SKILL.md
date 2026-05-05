---
name: ticket-smith
description: Decompose PRDs, feature specs, meeting transcripts, or any text describing work into well-structured Jira tickets. Creates epics, stories, and subtasks with acceptance criteria, dependencies, and smart gap-detection. Use when asked to "create tickets", "break this into stories", "decompose this feature", "turn this spec into Jira issues", or "plan this work".
homepage: https://github.com/ianpcook/ticket-smith
metadata: {"openclaw":{"emoji":"🎫"}}
---

# Ticket Smith — Intelligent Work Decomposition for Jira

Turn any description of work into well-structured Jira tickets. Accepts PRDs, feature specs, meeting transcripts, bug reports, Slack threads, or even rough ideas — and produces a complete ticket tree with epics, stories, subtasks, acceptance criteria, and dependency mapping.

## Prerequisites

### Atlassian MCP Server

This skill requires the Atlassian MCP server for Jira integration. The user must have it configured in their MCP client.

**Installation (Claude Code):**
```bash
claude mcp add atlassian -- npx -y @anthropic-ai/mcp-remote https://mcp.atlassian.com/v1/sse
```

**Installation (OpenClaw via mcporter):**
Check if the user has the `mcporter` skill available, or guide them to configure the Atlassian MCP server manually.

The MCP server provides these Jira tools:
- `createJiraIssue` — create issues (Epic, Story, Task, Subtask, Bug)
- `editJiraIssue` — update fields, add links
- `getJiraIssue` — read issue details
- `getVisibleJiraProjects` — discover available projects
- `getJiraProjectIssueTypesMetadata` — discover issue types per project
- `getJiraIssueTypeMetaWithFields` — discover available fields per issue type
- `lookupJiraAccountId` — find users for assignment
- `searchJiraIssuesUsingJql` — search existing issues (duplicate detection)
- `addCommentToJiraIssue` — add comments

If the MCP server is not available, inform the user and provide the installation instructions above.

---

## Workflow

### Phase 1: Intake

Accept the source material. This can be:
- A PRD or feature spec (pasted text or file path)
- A meeting transcript
- A bug report or incident description
- A rough feature idea described conversationally
- A Slack/Discord thread dump
- Any text that describes work to be done

Read the source material carefully. Identify:
- The core objective (what is being built/fixed/changed)
- Explicit requirements vs. implied requirements
- Technical constraints mentioned
- Stakeholders or teams referenced
- Any timelines or deadlines mentioned

### Phase 2: Project Discovery

Before decomposing, understand the user's Jira setup:

1. **Ask which Jira project** to create tickets in (or use context if obvious)
2. Use `getVisibleJiraProjects` to validate the project exists
3. Use `getJiraProjectIssueTypesMetadata` to discover available issue types
4. Use `getJiraIssueTypeMetaWithFields` to understand required/optional fields for each issue type
5. Optionally use `searchJiraIssuesUsingJql` to check for existing related tickets

Cache this metadata for the session — don't re-fetch for each ticket.

### Phase 3: Scope Questions

Ask the user three quick questions:

**1. Decomposition depth:**
> How deep should I break this down?
> - **Epic only** — one high-level ticket capturing the full scope
> - **Epic + Stories** — an epic with individual stories for each distinct piece of work
> - **Epic + Stories + Subtasks** — full decomposition with implementation-level subtasks

**2. Assignment:**
> Should I assign these tickets?
> - **Assign to you** — I'll assign everything to your account
> - **Leave unassigned** — tickets created without an assignee
> - **Assign to specific people** — tell me who handles what

If assigning, use `lookupJiraAccountId` to resolve the user's account ID.

**3. Placement:**
> Where should these land?
> - **Current sprint** — add to the active sprint
> - **Backlog** — add to the product backlog
> - **Specific sprint** — tell me which one

### Phase 4: Smart Interview

This is the critical differentiator. After reading the source material, identify **information gaps** that would result in vague or incomplete tickets.

**Rules for the interview:**
- Ask **3-5 targeted questions maximum** — respect the user's time
- Questions must be **specific**, not open-ended ("What's the session timeout?" not "Tell me more about auth")
- Offer **suggested answers** where possible ("Should this support OAuth providers like Google/GitHub, or just email/password? Or both?")
- Group related questions together
- If the source material is thorough, say so and skip to Phase 5 ("Your spec is detailed enough — I don't have gaps to fill. Moving to decomposition.")

**What to look for:**
- Ambiguous scope boundaries ("user management" — does that include roles? permissions? invitations?)
- Missing non-functional requirements (performance, security, accessibility)
- Unstated integration points (which services does this touch?)
- Edge cases not covered (error handling, empty states, concurrent access)
- Missing acceptance criteria inputs (what constitutes "done"?)

### Phase 5: Decomposition

Generate the ticket tree. Apply these principles:

**Epic:**
- Title: clear, noun-phrase style ("User Authentication System", "Payment Processing Integration")
- Description: the "why" and high-level scope. Reference the original source material.
- Acceptance criteria: high-level outcomes that indicate the epic is complete

**Stories:**
- Title: action-oriented, verb-first ("Implement JWT token refresh rotation", "Add password reset email flow")
- Description: what and why, NOT how. Leave implementation decisions to the developer.
- Acceptance criteria: specific, testable Given/When/Then format where possible
- Each story should be independently deliverable (can be deployed on its own or has clear dependencies noted)

**Subtasks:**
- Title: implementation-specific ("Create refresh_tokens database migration", "Write token rotation middleware")
- Description: brief, focused on the specific technical task
- Acceptance criteria: concrete completion checklist

**For all tickets:**
- Add `[NEEDS CLARIFICATION]` tag in the description for anything the source material was vague about and the interview didn't resolve
- Include a `## Dependencies` section listing which tickets block this one
- Include a `## Context` section with relevant quotes or references from the source material

**Dependency Mapping:**
Think like a tech lead about sequencing:
- Database schema before API endpoints
- API before frontend
- Auth before protected resources
- Shared libraries before consumers
- Infrastructure before application code

Express dependencies as "blocked by" relationships.

### Phase 6: Review

Present the complete ticket tree to the user in a clear, hierarchical format:

```
📋 EPIC: [Title]
  ├── 📖 STORY: [Title]
  │   ├── ✅ [Acceptance Criterion 1]
  │   ├── ✅ [Acceptance Criterion 2]
  │   ├── 🔗 Blocked by: [Story X]
  │   ├── 📝 SUBTASK: [Title]
  │   └── 📝 SUBTASK: [Title]
  ├── 📖 STORY: [Title]
  │   ├── ✅ [Acceptance Criterion 1]
  │   └── ✅ [Acceptance Criterion 2]
  └── 📖 STORY: [Title]
      └── ⚠️ [NEEDS CLARIFICATION]: [What's unclear]
```

**Ask for approval:**
> Here's the proposed ticket tree. You can:
> - ✅ **Approve** — I'll create all tickets in Jira now
> - ✏️ **Edit** — tell me what to change (add/remove/modify tickets)
> - 🔄 **Regenerate** — I'll take another pass with different guidance
> - ❌ **Cancel** — discard everything

Allow iterative editing. The user might say "split that story into two" or "add a story for error handling" or "remove the subtasks, those are too granular."

### Phase 7: Creation

Once approved, create tickets in Jira:

1. **Create the Epic first** — need its key for linking
2. **Create Stories** — link each to the Epic (parent or Epic Link field, depending on Jira config)
3. **Create Subtasks** — link to parent Story
4. **Add dependency links** — use `editJiraIssue` to add "is blocked by" links between issues
5. **Assign** — if requested, set assignee on all tickets
6. **Sprint placement** — if requested, move to the specified sprint

**Important Jira field mapping:**
- Use `getJiraIssueTypeMetaWithFields` to discover the correct field IDs — don't assume field names
- Epic Name / Epic Link fields vary by Jira instance
- Custom fields for story points, sprints, etc. are instance-specific
- If a field isn't available, skip it and note what couldn't be set

**After creation, report:**
```
✅ Created 1 Epic + 5 Stories + 12 Subtasks in PROJECT

📋 PROJ-100: User Authentication System (Epic)
  ├── 📖 PROJ-101: Implement JWT token generation → blocked by: —
  ├── 📖 PROJ-102: Add refresh token rotation → blocked by: PROJ-101
  ├── 📖 PROJ-103: Build login/signup UI → blocked by: PROJ-101
  ├── 📖 PROJ-104: Add password reset flow → blocked by: PROJ-101, PROJ-103
  └── 📖 PROJ-105: Implement OAuth provider support → blocked by: PROJ-101

🔗 View Epic: https://your-instance.atlassian.net/browse/PROJ-100
```

---

## Formatting Notes

- **Telegram/WhatsApp:** Use the tree format above with emoji prefixes. No markdown tables.
- **Discord:** Wrap in code blocks for alignment if needed. Suppress link embeds with `<url>`.
- **Terminal/CLI:** Plain text tree works fine.

## Edge Cases

- **Very large specs:** If the source material would produce 20+ stories, suggest breaking it into multiple epics and confirm with the user before proceeding.
- **Bug reports:** For bugs, create a single Bug issue type (not Epic/Story) with reproduction steps, expected vs. actual behavior, and severity assessment. Ask if decomposition is even needed.
- **Vague ideas:** For rough ideas ("we need better search"), lean heavily on Phase 4 interview to flesh out scope before decomposing. It's OK to say "this needs more definition before I can create good tickets — let me ask some questions."
- **Meeting transcripts:** Extract action items and decisions first, then decompose only the agreed-upon work. Flag anything that sounded like a decision but might not have been finalized.
- **No MCP server:** If Jira MCP tools aren't available, complete Phases 1-6 (decomposition and review) and output the ticket tree as structured text the user can manually create from. Offer to format as CSV or JSON for bulk import tools.

## State

This skill is stateless. All context is gathered per invocation.

## Future Adapters

This skill is designed for Jira first. The decomposition engine (Phases 1-6) is platform-agnostic. Future platform skills can reuse the decomposition logic and swap Phase 7 for their own creation step:
- `ticket-smith-linear` — Linear adapter
- `ticket-smith-asana` — Asana adapter
- `ticket-smith-github` — GitHub Issues adapter
