---
name: one-by-one
description: Walk through a list of findings, issues, questions, or suggestions — one at a time, with explicit user input on each. Use whenever the user has just received (or pasted) a list of items from a deep analysis, audit, code review, design critique, or any other multi-point output and wants to triage them deliberately instead of barreling through. Triggers on phrases like "let's go through these one by one", "walk me through this list", "iterate over these", "triage these findings", "go through your analysis", "let's tackle these", or any context where the user wants to handle a multi-item list deliberately. Convert the list into a todo list first, then walk each item with summary → verdict → proposal, waiting for the user between each.
---

# One by one

Help the user work through a list of items — one at a time, with explicit user input on each.

The user is a tech lead. The list usually comes from a deep Claude analysis, audit, or critique — sometimes from another tool, sometimes pasted in. Some items will be real, some speculative, some overstated. The goal is to triage quickly without either (a) acting on every finding by reflex, or (b) dismissing real ones. They want your help separating signal from noise.

## Core principles

- **One item at a time.** Never barrel through the list. After each item is handled, stop and wait for the user to say "next" (or equivalent).
- **The user decides, you assist.** You investigate, judge, and propose. They approve before you edit code or take any action with side effects.
- **Default to skepticism — including toward yourself.** Deep analyses tend to over-produce. If you wrote the original list, be willing to push back on your own findings rather than defending them. Check the actual code before agreeing with anyone, including yourself.
- **Don't auto-commit.** Many items won't even involve code — they may be questions, design choices, or feedback. Even when an item does end in a code edit, leave the change uncommitted unless the user explicitly asks.

## Workflow

1. Find the list (in conversation context, or ask the user to paste it)
2. Convert it into a todo list using Claude Code's todo tool (TodoWrite or equivalent)
3. Triage one item, present verdict + proposal
4. Wait for user direction
5. Carry out whatever the user approves
6. Mark the todo completed, move to the next

## Step 1 — Build the todo list

Find the list — usually in your previous message, or in something the user just pasted. If it's not obvious, ask. Don't guess.

Create a todo entry for each item: short, specific, action-oriented where possible. Show the user the full list once it's created. If the list is long (>10 items), offer to reorder or trim before diving in.

## Step 2 — Group with care, default to one-at-a-time

If two items are clearly the same issue (e.g., "missing null check" on three near-identical functions), group them into one todo. If you're unsure, don't group — the user prefers granular handling over batching.

## Step 3 — Triage each item

Mark the current todo as in-progress. For each item, produce three things in this order:

### a) What this item is about

A 1–3 sentence plain-English summary of the item's claim. Strip any rambling or formal-sounding prose down to the actual assertion. Quote the key snippet only if it's load-bearing. Don't dump the full original text back at the user.

If the item references a file or line, include the path (`bar.ts:42`).

### b) Verdict — real, overstated, or noise?

Investigate before judging. Read the file, read surrounding context, check whether the claimed issue actually exists. Common failure modes to check:

- Does the claimed behavior match the actual code, or did the analysis misread it?
- Did it invent a constraint that doesn't apply here?
- Is it a real bug, or a style preference dressed as a bug?
- Is it a real concern that's already handled elsewhere in the codebase?
- Was the priority overstated?

State your verdict explicitly. Don't hedge into mush — the user wants a clear take they can override. If you're genuinely uncertain, say so and explain what you'd need to check to be sure. If you wrote the original list and now think you overstated it, say so out loud.

### c) The proposed action

**If overstated or noise** — push back plainly: "I think I overstated this — `foo` is already null-checked at the call site in `bar.ts:42`, so the cast here is safe." Suggest closing the item without action.

**If a question, not an issue** — give your best answer with reasoning, then ask the user how they want to record the decision (in-line comment, doc update, ADR, just a verbal "got it").

**If a response needs drafting** (e.g., a reply to paste somewhere) — produce a copypasteable version in the user's voice. The user is a tech lead and their voice is *friendly while challenging*: first person, technical and specific, leaves the door open ("perhaps I'm misunderstanding?"). Format in a fenced code block so it pastes cleanly:

````
```
I suspect this is a false positive — `foo` is already null-checked at the call site in `bar.ts:42`, so the cast here is safe. Perhaps I'm missing something?
```
````

**If real and worth doing** — propose the action without taking it yet:

- Explain *why* it matters in concrete terms — what breaks, what user-facing effect, what invariant is violated. Not just "the analysis is right".
- The reader doesn't know the full context and can't see the code, so a small markdown/ascii illustration, diagram or before/after sketch that explains how the parts fit together helps a lot.
- Propose a 1–2 sentence summary of what you'd change, not the actual diff.
- Stop and wait for user approval before doing anything.

## Step 4 — Carry out the action (only after approval)

Do the thing the user approved — edit code, file the follow-up, save the response, whatever it was. If a code change is non-trivial, run the project's lint and test commands (check `CLAUDE.md`, `package.json` scripts, or `Makefile`). Leave the change uncommitted unless the user explicitly asks you to commit. If they do ask, match the repo's recent style, focus on **why** in the message, do not add a `Co-Authored-By: Claude …` trailer, and do not push.

## Step 5 — Move on

Mark the todo completed. Then say something brief like *"Done. Next?"* and wait. Do not auto-advance to the next item.

## Things to watch for

- **Don't defend findings reflexively just because you wrote them.** If a second look says you overstated it, say so. Honest reassessment beats consistency.
- **If an item spans multiple files or is conceptually a refactor**, flag that to the user before diving in — they may want to defer or split it.
- **If new items emerge while handling one**, surface them and ask whether to add them to the todo list or treat as out of scope.
- **Don't bundle actions across items.** One item, one action — even if items look related — unless the user explicitly says to merge.

## Anti-patterns

- Auto-advancing to the next item without waiting for "next"
- Acting on all items in one pass without per-item approval
- Defending every finding from the original analysis instead of honestly reassessing
- Auto-committing code changes
- Pasting `Co-Authored-By: Claude` trailers or pushing during the session
- Hedged verdicts ("it could go either way…") when you actually have a take
- Forcing every item into a "fix" shape when it's actually a question, a discussion, or just an FYI
