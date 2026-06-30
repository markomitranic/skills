---
name: pr-triage
description: Walk through unresolved review comments on the current branch's PR, one at a time. For each comment (human or AI bot like Greptile/Codex/Coderabbit), help the user decide whether it's a real issue worth fixing or a hallucination worth pushing back on, draft a rebuttal in their voice if it's noise, or propose a concrete fix if it's real. Use whenever the user wants to handle PR feedback, address review comments, respond to reviewers, triage Greptile/Codex/Coderabbit feedback, work through review threads, or "go through the PR comments" — even if they don't explicitly say "review". Especially valuable on PRs with multiple AI reviewers where signal-to-noise is mixed and the user needs help separating real bugs from confident-sounding nonsense.
---

# PR review triage

Help the user work through unresolved review comments on the open PR for the current branch — one at a time, with explicit user input on each.

The user is a tech lead. Their PRs typically get 2–3 AI reviewers (Greptile, Codex, Coderabbit, etc.) plus humans. Both AI and humans can be sharp, and both can hallucinate. The user's goal is to triage quickly without either (a) capitulating to confident-sounding nonsense or (b) dismissing real bugs. They want your help separating signal from noise.

## Core principles

- **One comment at a time.** Never barrel through the list. After each comment is handled, stop and wait for the user to say "next" (or equivalent).                
- **The user decides, you assist.** You investigate, judge, and propose. They approve before you edit code or before they paste a rebuttal.
- **Default to skepticism on both sides.** AI reviewers invent constraints; humans leave drive-by style preferences dressed as bugs. Check the actual code before agreeing with anyone.
- **Don't push, don't sign.** Commits are local-only and unattributed to Claude. The user batches pushes manually to avoid retriggering AI review loops.

## Workflow

1. Gather PR context (description, review summaries, checks, mergeability)
2. If AI reviewers have not yet completed their reviews, poll for completion on a 3-minute loop (see Step 1b)
3. Fetch unresolved review threads
4. Triage one comment (or one tightly-related group):
   - **Simple, low-risk win** → auto-fix it (implement → lint/test → commit), then report what you did and move on
   - **Bug, hallucination, or non-straightforward fix** → present verdict + proposal and wait for the user
5. Wait for user direction (only for the non-trivial cases)
6. If a fix is approved: implement → lint/test → commit (no Co-Authored-By, no push)
7. Move to the next comment

## Step 1 — Gather context before triaging

Reviewers (especially AI ones) often miss the *intent* of the PR. Before judging individual comments, read the big picture so you can defend the PR knowledgeably.

```bash
gh pr view --json number,title,body,headRefName,baseRefName,url,mergeable,mergeStateStatus
gh api repos/{owner}/{repo}/pulls/{number}/reviews   # top-level review summaries
gh pr checks                                          # CI status
```

Read:
- **PR description** — the user's stated intent and scope. The single most important context for deciding whether a comment is on-target.
- **Review summary bodies** from Greptile/Codex/etc. — these are the "thesis" of each AI's review. Don't address them directly (they're noise/marketing), but read them — they explain the framing of each line-level comment that follows.
- **Failing checks and merge conflicts** — these count as issues to triage too. Surface them up front alongside the comment count, e.g.: *"3 unresolved threads, 1 failing check (typecheck), no merge conflicts."*

## Step 1b — Wait for AI reviewers to finish (if needed)

AI reviewers (Greptile, Copilot, BugBot) often take a few minutes to post their reviews after a push.
If their reviews haven't landed yet, use `/loop` tool sleep for 3min between checks. 
There is no point in proceeding until they are all done.

## Step 2 — Fetch unresolved review threads

GitHub's REST `/pulls/{n}/comments` does not expose `isResolved`. Use GraphQL:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          comments(first: 50) {
            nodes {
              author { login }
              body
              diffHunk
              url
              createdAt
            }
          }
        }
      }
    }
  }
}' -f owner=OWNER -f repo=REPO -F pr=NUMBER \
| jq '.data.repository.pullRequest.reviewThreads.nodes
       | map(select(.isResolved == false and .isOutdated == false))'
```

Filter out:
- `isResolved: true` — already handled
- `isOutdated: true` — code has changed, comment no longer applies

Owner/repo come from `gh repo view --json owner,name`. PR number from `gh pr view --json number`.

## Step 3 — Group with care, default to one-at-a-time

If two threads are clearly the same issue (e.g., "missing null check" on three near-identical functions), group them into one triage. If you're unsure, don't group — the user prefers granular handling over batching.

## Step 4 — Triage each comment

For each comment (or group), produce three things in this order:                                                                                                   

### a) What they're actually saying

A 1–3 sentence plain-English summary of the comment's claim. AI reviewers especially tend to ramble in formal-sounding prose — strip it to the actual assertion. Quote the key snippet only if it's load-bearing. Don't dump the full comment back at the user.

Include who said it (the author's login) so the user knows whether they're dealing with a bot or a teammate — this changes the rebuttal tone (see below).

**Always lead with a clickable link to the exact comment** so the user can jump straight to the thread on GitHub — it's hard to track down which comment you're talking about otherwise. Use the `url` field from the GraphQL query (the URL of the *first comment* in the thread, which anchors directly to it). Format it on its own line at the top of each triage, e.g.:

> **`path/to/file.ts:42` — @greptile-bot** · [view comment](https://github.com/OWNER/REPO/pull/123#discussion_r456789)

If a group covers multiple threads, list a link per thread so each is individually reachable.

### b) Verdict — hallucination or real?

Investigate before judging. Read the file, read surrounding context, check whether the claimed bug actually exists. Common failure modes to check:

- Does the claimed behavior match the actual code, or did the reviewer misread it?
- Did the reviewer invent a constraint that doesn't apply here? ("This should be async because…" — does that reasoning actually hold?)
- Is it a real bug, or a style preference dressed as a bug?
- Is it a real concern that's already handled elsewhere in the codebase?
- Does the reviewer's mental model of the framework / library / API match reality?

State your verdict explicitly. Don't hedge into mush — the user wants a clear take they can override. If you're genuinely uncertain, say so and explain what you'd need to check to be sure.

### c) The proposed response

**If hallucination** — produce a copypasteable rebuttal in the user's voice.

The user is a tech lead and their voice is *friendly while challenging*. They want to push back without making people defensive. Match this:

- First person: "I suspect…", "I think…", "I'd push back here because…"
- Technical and specific — name the actual reason the comment is wrong, with a code reference if helpful (`bar.ts:42`)
- Leave the door open. For human reviewers, end with something like *"perhaps I'm misunderstanding?"* or *"happy to revisit if you see it differently"* — never a flat "you're wrong"
- For AI reviewers: same first-person technical tone, but the conversational softener at the end is optional — the rebuttal is mostly a record for future humans reading the thread

Format the rebuttal in a fenced code block so the user can paste it cleanly. No prefix/quote markers — just the literal text:

````
```
I suspect this is a false positive — `foo` is already null-checked at the call site in `bar.ts:42`, so the cast here is safe. Perhaps I'm missing something?
```
````

**If real issue** — propose a fix without writing it yet:

- Explain *why* it needs to be fixed in concrete terms — what breaks, what user-facing effect, what invariant is violated. Not just "the reviewer is right".
- Give a short example if it helps make it tangible (e.g., *"if `userId` is undefined here, the API call returns 500 instead of redirecting to login"*).
- The reader doesn't know the full context and can't see the code, so a small markdown/ascii illustration, diagram and a before/after, that explain how the parts fit into the layered architecture helps a lot.
- Propose a 1–2 sentence fix summary — what you'd change, not the actual diff.

## Step 5 — Apply the fix

At this point, you must make a decision - auto-fix or escalate to the user?

When in doubt, escalate. Hallucinations and non-straightforward changes are more likely to be bugs and the
user needs to weigh the risks. Solutions that change logic, control flow or require user's taste and gut feeling
require a human. Sit there and wait for human input.

If the issue is an easy win with low risk, you may fix it yourself. Examples:
- Typos, types, naming, comment/docstring fixes, dead-code or unused-import removal, missing null-guards or awaits.
- Mechanical, obviously-correct changes the reviewer is plainly right about.
- Pure formatting / lint-style nits
- The change is local, reversible, and you have high confidence it's correct and won't alter intended behavior

When we are ready to make a fix:

1. Make the change.
2. Run the project's lint and test commands if the change touches code. Check the project's `CLAUDE.md`, `package.json` scripts, or `Makefile` for the right commands (e.g., `pnpm lint && pnpm test`, `npm test`, `cargo test`).
3. Commit. Do **not** push.

### Commit message style

Match the repo's recent style — run `git log --oneline -20` to confirm if unsure. Common defaults:

- Conventional Commits prefix: `fix:`, `chore:`, `refactor:`, `feat:`, `docs:`, `ci:`, `test:`
- One concise line, ideally under 70 characters
- Focus on **why**, not what. The diff already shows what changed.
  - Bad: `fix: update foo to use bar`
  - Good: `fix: avoid double-render when subscriber id changes mid-flow`
- **Do NOT add a `Co-Authored-By: Claude …` trailer.** Fixes are not attributed to Claude.
- **Do NOT push.** The user batches pushes manually so AI reviewers don't immediately re-review.

```bash
git add <specific files>
git commit -m "fix: <why this matters>"
```

Pass the message via `-m` directly (no heredoc with Claude attribution). If the project has a pre-commit hook that fails, fix the underlying issue and create a new commit — never `--amend` or `--no-verify`.

## Step 6 — Move on

After the commit (or after the user accepts a rebuttal as-is), say something brief like *"Done. Next?"* and wait. Do not auto-advance to the next comment. The user will signal when they're ready.

## Things to watch for

- **Don't address the AI summary at the top of each review.** It's marketing copy. Address the line-level threads it spawned.
- **AI reviewers hallucinate by inventing context** — they'll claim a function is called from somewhere it isn't, or that a type guarantees something it doesn't. When in doubt, check the actual code rather than trusting the comment's confident tone.
- **Humans leave drive-by style preferences** dressed as issues. These deserve the same triage — disagree gently if you disagree.
- **If a comment spans multiple files or is conceptually a refactor**, flag that to the user before diving in — they may want to defer or split it.
- **Don't mark threads as resolved on GitHub.** That's part of the user's batch workflow, not yours.
- **CI failures and merge conflicts are issues too.** Triage them with the same one-at-a-time flow alongside the review comments.

## Anti-patterns

- Batch-fixing the whole list in one pass without working through it comment by comment
- Pasting Claude-attributed commits or `Co-Authored-By` trailers
- Pushing commits during the triage session
- Resolving review threads on GitHub
- Hedged verdicts ("it could be either…") when you actually have an opinion
- Rebuttals written in third person ("Claude thinks this is wrong because…") instead of the user's first-person voice
- Addressing the Greptile/Codex top-level summary as if it were a comment to respond to
