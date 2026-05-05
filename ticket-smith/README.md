# 🎫 Ticket Smith

**Intelligent work decomposition for Jira.** Turn PRDs, feature specs, meeting transcripts, or rough ideas into well-structured Jira tickets — with epics, stories, subtasks, acceptance criteria, and dependency mapping.

## What It Does

Feed it any description of work:
- Product requirements documents
- Feature specs
- Meeting transcripts
- Bug reports
- Slack thread dumps
- Even a rough idea described in plain English

Ticket Smith will:
1. **Analyze** the source material for scope, requirements, and gaps
2. **Interview** you with 3-5 targeted questions to fill information holes
3. **Decompose** into a structured ticket tree (Epic → Stories → Subtasks)
4. **Review** the plan with you before touching Jira
5. **Create** all tickets in Jira with proper linking, dependencies, and acceptance criteria

## Install

### OpenClaw / Clawdbot

```bash
# From ClawHub (when published)
clawhub install ticket-smith

# Or clone directly
cd ~/.openclaw/skills   # or your skills directory
git clone https://github.com/ianpcook/ticket-smith.git
```

### Claude Code

Ticket Smith is an agent skill — it works with any AI agent that reads `SKILL.md` files. Point your agent at the `SKILL.md` in this repo.

## Prerequisites

**Atlassian MCP Server** — required for Jira integration.

```bash
# Claude Code
claude mcp add atlassian -- npx -y @anthropic-ai/mcp-remote https://mcp.atlassian.com/v1/sse

# OpenClaw — configure via mcporter skill or manually
```

Without the MCP server, Ticket Smith still works for decomposition — it just outputs structured text instead of creating Jira tickets directly.

## Usage

Just ask your agent naturally:

> "Break this PRD into Jira tickets"
>
> "Decompose this feature spec into stories"
>
> "Turn these meeting notes into actionable tickets"
>
> "Create tickets for: we need user authentication with OAuth, email/password, and password reset"

The skill handles the rest — asking you about decomposition depth, assignment, sprint placement, and filling gaps in the spec before creating anything.

## Features

- **Smart gap detection** — identifies ambiguities and asks targeted questions before decomposing
- **Dependency mapping** — understands sequencing (DB before API, auth before protected resources)
- **Acceptance criteria** — Given/When/Then format for stories, checklists for subtasks
- **`[NEEDS CLARIFICATION]` tags** — flags anything still vague after the interview
- **Iterative review** — edit, regenerate, or approve the ticket tree before creation
- **Jira-aware** — discovers your project's issue types, fields, and custom metadata automatically

## Example Output

```
📋 EPIC: User Authentication System
  ├── 📖 STORY: Implement JWT token generation
  │   ├── ✅ Tokens issued on successful login
  │   ├── ✅ Tokens expire after configured TTL
  │   └── 🔗 Blocked by: —
  ├── 📖 STORY: Add refresh token rotation
  │   ├── ✅ Old refresh token invalidated on use
  │   └── 🔗 Blocked by: JWT token generation
  ├── 📖 STORY: Build login/signup UI
  │   └── 🔗 Blocked by: JWT token generation
  └── 📖 STORY: Implement OAuth provider support
      ├── ✅ Google and GitHub providers supported
      └── 🔗 Blocked by: JWT token generation
```

## No Jira? No Problem

Without the Atlassian MCP server, Ticket Smith completes the full decomposition workflow and outputs the ticket tree as structured text. You can:
- Copy/paste into Jira manually
- Use CSV/JSON export for bulk import tools
- Adapt the output for Linear, Asana, GitHub Issues, etc.

## License

MIT
