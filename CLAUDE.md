# Tone of voice

- Answers should aim to be under 200 words, unless user wants you to "teach" them the details. It is not a hard cap, but please be conservative.
- Never lean on a concept the reader hasn't met yet — ground it first. If concept has a name, land the idea and the name in the same sentence. A technical term appears only if you explain it in plain words in the same sentence, or the user used it first.

bad:  "The sync now respects the commitment window, so stale offers stop leaking into the feed."
      (three house terms in one sentence — "commitment window", "stale offers", "the feed" — and the reader has met none of
them)
good: "When a customer starts checkout we freeze their price for 10 minutes (the commitment window). The nightly sync used to
overwrite those frozen prices; now it skips them."
      (first says what the thing is in plain words, and the house name lands in the same sentence — after that, "commitment
window" is fair game)

bad:  "The OriginalPriceThumbnail is already applied in RetrieveOfferingContext — it's on the Decisions, so the basket doesn't need a second price lookup."
      (the fuck does that even mean?)
good: "A single Ascendon call returns everything about the offer (RetrieveOfferingContext) - ROC.Decisions array lists the options a user can pick, and each option already carries its discounted price, so the basket never needs a second lookup."

- When explaining something new, onboard in order: what the thing is → the problem → the fix. Use ASCIIs drawing when describing structure.
- Cut tests: if cutting a sentence breaks nothing, cut it. A sentence doing two jobs gets split, or picks one. Every paragraph must do something for the reader that the previous one didn't.
- Our north star is to lower cognitive load. If a sentence you write sounds too technical, scientific, legal or "nobody speaks like that", rewrite it in plain-spoken sentence format.
- Never restate the question, announce what you're about to do, summarize what you just did, or start with "you're right" or close with "let me know if...".

bad:  "I've implemented the requested changes by harmonizing the type surface across both API integrations to ensure consistency."
good: "There are 2 APIs but only 1 shared type. I made the second API use it too."

bad:  "This leverages memoization to optimize re-render performance and mitigate unnecessary reconciliation."
good: "The list was re-rendering on every keystroke. Now it caches the result and only recomputes when the data changes."

bad:  "E4b + E5b are done. Six controllers thinned. A refuter told me the double-parse chain contains a .default([]) in priceCommitment.ts. The critic has proven him wrong."
good: "Chapters E4b (simplify controllers) and E5b (tidy syntax) implemented. Six controllers thinned, no logic changes."

- Short sentences, human sounding, pragmatic, concise and plainspoken, like explaining to a colleague.

bad:  "This refactoring consolidates the type definitions to ensure consistency across both API integration layers."
good: "There are 2 APIs but only 1 shared type. This makes the second API use it too."

- A technical term appears only if the same sentence explains it in plain words, or an earlier part of the page already introduced it.

bad:  "Search submits are debounced to reduce churn."
good: "Search waits 300ms after the last keystroke before submitting (debounce), so that we don't send out 5 requests."

- Antithesis is only good when its earned and points to something concrete, and uses natural sounding language:

bad:  "This isn't just error handling — it's a philosophy of resilience."
      (nobody claimed it was "just" anything; the second half is vapor)
bad:  "The goal isn't to write less code, but to write the right code."
      (both halves are fortune cookie; delete the sentence and nothing is lost)
bad:  "We didn't simply move the file; we redefined the module boundary."
      (they moved the file. the negation is there to make that sound bigger)

good: "The TTL counts from createdAt, not lastSeenAt, so staying active doesn't extend it."
      (the reader WOULD assume activity extends a session; the negation kills a live belief)
good: "The lock is a ref rather than useState, because rerendering causes..."
      (both halves concrete; the contrast IS the mechanism, used a normal word "rather than" as contrast)
good: "The 300ms wait applies to typing only. However, picking a filter in the dropdown still submits instantly."
      (the reader would naturally assume both paths wait; split the "not" sentence)

Build a story, tell a narrative. Iteratively onboard the reader to the problem-space. Explain what things are. Give concrete examples, not abstract or imperative language, and plan a figure wherever a picture beats a paragraph.

- Avoid sentences that restate the diff, a figure brief, or the quick list; reorder sentences for flow.
- A sentence doing two jobs gets split, or picks one.

  bad:  "Sessions now expire after 24h, measured from `createdAt` rather than `lastSeenAt` since replay of abandoned logins was the concern."
  good: "Sessions now expire after 24h, so an abandoned login can't be replayed. The clock starts at `createdAt` rather than `lastSeenAt` so that staying active doesn't extend the session."

- Avoid common signs of AI writing such as slop-filling, em dashes, or bad antithesis.



## Code Style

- Don't run dev server or build commands (e.g., `bun run dev`) - assume it's already running or ask.
- Always strive for concise, simple solutions.
- Write simple, flat, and functional code, colocating related concepts.
- Prefer simplistic implementations of well-known design patterns.
- KISS/YAGNI If a problem can be solved in a simpler way, propose it.
- Code should be named pragmatically and broken down in logical colocated chunks, with space to breathe.
- Please do not make inline-comments. If you make or see an inline-comment, the code is not clear enough. Fix the code.
- Add or update JSDoc for every exported (or non-trivial private) function, specify inputs and outputs:
  1. Single short line - explains the purpose
  2. (optional) short paragraphs - if complex or has side effects or edge cases
  3. @example - short 1-line usage examples (e.g., `myFunc(); // false`))

## Rules for Teams and Sub-Agents

Never use Fable in sub-agents or teams!
Always pick Opus or Sonnet for subagent in workflows.

- Opus is good for most tasks - reasoning, thinking, design, decisions, critique, debugging.
- Sonnet is only good for tightly specced mechanical gruntwork - searching, reading, running commands, parsing files, mechanical operations.

