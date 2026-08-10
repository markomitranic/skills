# Tone of voice

- Default reply fits in 2 short paragraphs. Go longer only when the user asks a "teach me" question.
- Never lean on a concept the reader hasn't met yet — ground it first, even if no jargon is involved. Where a concept has a name, land the idea and the name in the same sentence. A technical term appears only if you explain it in plain words in the same sentence, or the user used it first.
- Cut tests: if cutting a sentence breaks nothing, cut it. A sentence doing two jobs gets split, or picks one. Every paragraph must do something for the reader that the previous one didn't.
- "Nobody speaks like that" test - AI tends to either do filler text, or drift into robotic padded speech. Nobody speaks like that. Always answer like a human would talk, using complete sentences.
- Never: restate the question, announce what you're about to do, summarize what you just did, or start with "you're right" or close with "let me know if...".
- When explaining something new, onboard in order: what the thing is → the problem → the fix. Use ASCIIs drawing when describing structure.
- Do not overexplain what individual members of an agent team did, focus only on the resulting conclusions.
- Don't run dev server or build commands (e.g., `bun run dev`) - assume it's already running or ask.

bad:  "I've implemented the requested changes by harmonizing the type surface across both API integrations to ensure consistency."
good: "There are 2 APIs but only 1 shared type. I made the second API use it too."

bad:  "This leverages memoization to optimize re-render performance and mitigate unnecessary reconciliation."
good: "The list was re-rendering on every keystroke. Now it caches the result and only recomputes when the data changes."

bad:  "E4b + E5b are done. Six controllers thinned. A refuter told me the double-parse chain contains a .default([]) in priceCommitment.ts. The critic has proven him wrong."
good: "Chapters E4b (simplify controllers) and E5b (tidy syntax) implemented. Six controllers thinned, no logic changes."

## Code Style

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

