---
name: pr-triage
description: Use when monitoring a pull request, after opening a PR or when analyzing review comments from sub-agent reviewers.
---

# pr-triage

Every repo we work in has review bots plus human reviewers. They're useful, and they're often wrong. They follow the code, not the task/intent. They can't see the ticket, don't know what "good enough" means for this feature, and will happily rip apart a correct implementation over a 0.1% edge case.

Your job is to be the user's advisor, not the reviewers' executor. Read each comment with the user, explain it, prove or disprove it, and help them decide.

1. Gather PR context: description, ticket, review summaries, checks, mergeability.
2. If AI reviewers haven't finished, wait on a 3-minute loop.
3. Fetch unresolved review threads. Group only threads that are clearly the same issue; when unsure, don't group.
4. For each problem: strip the comment to its core assertion, verify it in the code, look for the judo move and classify it.
5. After a full pass, push, then monitor for the next batch.

The PR was shaped by someone who read the task and the surrounding code. We must assume good will and competence on their part.
Review comments are not orders, they are suggestions. Always evaluate them in the context of the author's intent.

## Verdicts

- **Wrong** The reviewer misread the code, invented a constraint, or doesn't know the framework. Rebut and click resolve button.
- **Obvious** A real defect a user would hit in the normal path of the feature, a security hole, data loss, a broken invariant, feature logic leaking into a shared path etc. Fix it yourself. Be extra careful to not overcomplicate or explode scope.
- **YAGNI** A case that is rare, harmless, already handled elsewhere, or outside what the task asked for. Acknowledge it in one line, decline, click resolve button. This is the most common bucket and tends to blow the scope up.
- **KISS** Code judo that can remove complexity, a small move makes the issue moot: show an error, disable a button, add a guard, tighten the copy, or reframe the flow so the case can't occur. Implement it.
- **Unsure** Anything that pushes the implementation away from the original intent, increases complexity, changes architecture, changes UX, endangeres security, or is broader than the brief. Stop and explain the context of the issue to the user. The user might not know the details so be gentle and explain in less technical tone. What breaks, for whom, how often, and what the user-facing effect is. Give a tangible example. A short before/after or ASCII sketch of how the fix threads through the layers is worth more than the diff. Give a cheap recommendation. Propose the fix in one or two sentences.

## The KISS (Keep It Simple, Stupid) test

When no judo move is available and the fix would have to be additive, think before proposing it:

- How often does this actually happen, for the people who will actually use this?
- What happens if we do nothing? An error message shown to the user is usually an acceptable outcome. Silent corruption is not.
- Would a senior dev who owns this feature bother, or would they say "if it fails we show an error, boo hoo"?
- Does the fix cost more than the problem? Count the fix in shape, not lines. Threading new state through five layers to handle one branch is expensive even when it's short.
- Is the reviewer exploding the scope?

If the fix would make the code visibly more complicated than the baseline to cover something the task never asked for, the answer is no. Write that down as the reason and move on. Complexity is the enemy.

## Core principles

- One concern at a time. Never fix several concerns in one edit.
- Verify every claim against the source before judging it. Read the file, read the callers, run it if you can. Reviewers sound equally confident when right and wrong, you are there to discipline them.
- Defend the task's intent. Scope creep dressed as correctness is still scope creep.
- Prefer the smallest change that makes a concern moot over the most complete change that addresses it.
- Don't attribute/sign commits or comments to Claude or AI.
- Batch pushes to the end of a full pass so we don't re-trigger CI and AI review pipelines per commit.
- Some project require you to comment "@claude /rereview" to trigger a re-review by the AI.

## Writing replies

Rebuttals and declines go out in the user's voice. They're a tech lead who stays friendly while pushing back. Open with "I suspect…", "I think…", "I'd push back here because…", then always give the technical reason with code references or docs. Leave the door open at the end: _"perhaps I'm misunderstanding?"_ or _"do you see it differently?"_. Do not go over 70 words.

Out-of-scope declines are shorter and don't argue the point: _"Fair, but out of scope for this PR, which only covers X."_

Post without extra commentary.

## Gathering context

```bash
gh pr view --json number,title,body,headRefName,baseRefName,url,mergeable,mergeStateStatus
gh api repos/{owner}/{repo}/pulls/{number}/reviews   # top-level review summaries
gh pr checks                                          # CI status
```

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

Resolve a thread:

```bash
gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: { threadId: $threadId }) {
    thread { id isResolved }
  }
}' -f threadId=THREAD_ID
```

Reply before resolving with `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies`.
