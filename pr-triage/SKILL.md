---
name: pr-triage
description: Walk through unresolved review comments on the current branch's PR, one at a time. For each comment (human or AI bot like Greptile/Codex/Coderabbit), help the user decide whether it's a real issue worth fixing or a hallucination worth pushing back on, draft a rebuttal in their voice if it's noise, or propose a concrete fix if it's real. Use whenever the user wants to handle PR feedback, address review comments, respond to reviewers, triage Greptile/Codex/Coderabbit feedback, work through review threads, or "go through the PR comments" — even if they don't explicitly say "review". Especially valuable on PRs with multiple AI reviewers where signal-to-noise is mixed and the user needs help separating real bugs from confident-sounding nonsense.
disable-model-invocation: true
---
# PR review triage

All the repos we work in have various review bots + human reviews. They're helpful, even tho they aren't always right. Both AI and humans can be sharp, but both can also hallucinate. The user's goal is to triage quickly without either (a) capitulating to confident-sounding nonsense or (b) dismissing real bugs. Help me separate signal from noise.

Monitor the PR as the review comments come in, and help the user work through unresolved review comments. However, you mustn't blindly trust the reviews. You should verify every bot finding against the source code before making changes and decisions.

Fix real findings and and obvious issues such as CI failures. When encountering false positives, rebut/reply with a written reasoning and resolve the comment.

## Core principles

- One problem at a time. Never barrel through the list at random, and don't attempt to fix multiple problems at the same time.
- Please don't attribute commits and comments to Claude.
- Feel free to push the changes, but batch them together (for example at the end of one full pass), so that we don't re-trigger costly CI/AI review pipelines for every single tiny commit.
- Default to skepticism on both sides. AI reviewers invent constraints, whereas humans tend to leave drive-by style preferences dressed as bugs.
- Do not allow the review feedback to expand the PR beyond the user's original goal. Sure, address real shortcomings, but avoid scope creep.

## Workflow

1. Gather PR context (description, ticket, review summaries, checks, mergeability)
2. If AI reviewers have not yet completed their reviews, wait for completion on a 3-minute loop.
3. Fetch unresolved review threads and group them if multiple refer to a similar problem.
4. Thats it, now triage each problem and figure out what to do - you'll either make a fix, or rebut.
  - **Simple, low-risk win** → fix it, lint commit etc, and resolve relevant threads
  - **Hallucination** → rebut, comment and resolve relevant threads.
5. Once you make a full pass, push any changes, and monitor for the next batch of reviews.

Strip each claim to its actual core assertion and investigate before judging. That means reading the files and surrounding context and analyzing or testing the claim. Sometimes reviewers are convinced that there is a bug or constraint, which is actually not there, or misunderstand the code. Other times, the concern may be real, but already handled elsewhere in the codebase.

If you do notice a hallucination, post a rebuttal in my tone of voice. As a tech lead, I must remain friendly, while challenging what they said, pushing back without making people defensive. So, while you can start gently with "I suspect…", "I think…", "I'd push back here because…", make sure to always add technical reasoning, code references, documentation links etc. And it is wise to leave the door open - sometimes you may be wrong, so ending a message with *"perhaps I'm misunderstanding?"* or *"do you see it differently"* is a nice, polite way to push back.

**Beware:** there will sometimes be non-trivial cases, where a legitimate (and usually dangerous) decision needs to be made by the user. Be on the lookout for those, explain the issue and wait for the user. For example, usually these are cases that push the implementation away from the original intent, or present security issues, or architecture changes, or too broad for the brief. This is rare but not impossible.

- Onboard me to the problem space, explain *why* it needs to be fixed in concrete terms - what breaks, what user-facing effect, what invariant is violated. Don't just say a dry and unhelpful "the reviewer is right".
- Give a short example if it helps make it tangible (e.g., *"if* `userId` *is undefined here, the API call returns 500 instead of redirecting to login"*).
- Try to lower my cognitive load in your question, I may be spread too thin and and can't see the code, so a ASCII art illustration, diagram and a before/after, that explain how the parts fit into the layered architecture helps a lot.
- Propose a 1–2 sentence fix summary about what you'd change. The literal code diff isn't super important here.

## Gathering context

Reviewers (especially AI ones) often miss the *intent* of the PR. Before judging individual comments, read the big picture so you can defend the PR knowledgeably.

```bash
gh pr view --json number,title,body,headRefName,baseRefName,url,mergeable,mergeStateStatus
gh api repos/{owner}/{repo}/pulls/{number}/reviews   # top-level review summaries
gh pr checks                                          # CI status
```

Read:

- **PR description** - the user's stated intent and scope. The single most important context for deciding whether a comment is on-target.
- **Tickets** - (ONLY WHEN AVAILABLE) such as Jira tickets or Figma design.
- **Review summary bodies** from Greptile/Copilot/etc. - these are the "thesis" of each AI's review and  explain the framing of each line-level comment that follows.
- **Failing checks and merge conflicts** - these count as issues to triage too

### Fetch unresolved review threads

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

Use GitHub GraphQL to resolve review threads:

```bash
gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: { threadId: $threadId }) {
    thread { id isResolved }
  }
}' -f threadId=THREAD_ID
```

Use `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies` or the GitHub API equivalent to post an approved rebuttal before resolving the thread. The rebuttal should be exactly what the user approved, without extra agent commentary.

