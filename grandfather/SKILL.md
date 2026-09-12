---
name: grandfather
description: Only use when the user explicitly asks for /grandfather or the grandfather skill. Maintain a local research tracker and handoff in GRANDFATHER.md.
disable-model-invocation: true
argument-hint: "Optional research focus or handoff emphasis"
---

Create or update `GRANDFATHER.md` in the repository root using the current conversation. This is a living research notebook for the top-level brainstorming agent and the agents that follow. Preserve the user's intent, useful reasoning, evidence, failed attempts, and unfinished threads. It is not a specification or authorization to implement its suggestions.

Run in the current conversation, where the research context lives. Do not delegate the synthesis to an agent that has not seen it. Optional arguments focus this update without deleting unrelated research already recorded.

## Keep it local

- Find the repository root with `git rev-parse --show-toplevel`. Read any existing `GRANDFATHER.md` before editing. If there is no repository, ask where to put the file.
- Keep the notebook untracked and unstaged. Check whether Git already tracks it before writing. If it does, tell the user and ask how to proceed. Do not untrack, unstage, or rewrite history on their behalf.
- Protect the file from accidental staging with a root-anchored `/GRANDFATHER.md` entry in the local exclude file resolved by `git rev-parse --git-path info/exclude`. Read that file first if it exists, preserve its contents, and avoid duplicate entries. Do not change the shared `.gitignore` or global Git configuration.
- Verify that the notebook is untracked and ignored. If local exclusion is unavailable, report that protection was not applied rather than claiming the file is protected.
- Do not commit, publish, upload, or turn the notebook into an artifact. Do not include credentials or secrets from logs.

## Preserve intent without inventing authority

Separate what the user said from what agents inferred. Use ordinary prose with explicit attribution where it matters, not a blanket "decisions" or "requirements" section.

- Capture the user's goal and scope in their words where available. Quote only text you actually have. Keep important corrections, rejected interpretations, and explicit boundaries.
- Distinguish a user-stated constraint from an observed technical limitation. Record the source and conditions. Neither an agent recommendation nor the user's silence establishes approval.
- Distinguish measured results, source inspection, earlier handoff claims, hypotheses, and suggestions. Do not promote an inherited claim to a verified fact just by repeating it.
- Preserve uncertainty and disagreements. If the conversation does not settle something, say what remains open. If context is missing, name the gap rather than reconstructing the conversation from guesses.
- Record approval only as far as it actually extends. "Try this on docs" does not authorize a rollout to every app. "Worth exploring" does not mean "must implement."
- Keep conclusions scoped to their evidence. "Slower on this runner in two trials" is useful. "This approach never works" is usually an invention.

## Write for the next researcher

Adapt the headings to the topic and omit empty sections. Prefer a readable narrative with focused tables or snippets where they help. Do not produce a transcript dump or a checklist of generic engineering work.

A useful shape:

### Research focus and user intent

The problem under discussion, the user's stated boundaries, and what remains exploratory. Include the last-updated date and relevant repository, branch, or revision context when known.

### Where we are now

What has changed, what was only investigated, and what is currently in progress. Distinguish committed work, local changes, temporary experiments, reverted work, and untested changes when relevant. Give the next agent enough orientation to resume without implying that the work is finished.

### Findings and attempts

Organize by idea or mechanism rather than by conversation turn. Preserve:

- What we tried or inspected and why it seemed promising.
- The result, evidence, and explanation supported by that evidence.
- Failed variants, retries that mattered, misleading measurements, and correctness traps.
- Whether an approach was implemented, reverted, abandoned after testing, or only discussed.
- Caveats, confounding factors, and what would make a rejected approach worth revisiting.

For measurements, retain the baseline, units, environment, method, and sample count when known. Do not infer missing details. Separate local results from CI results and measured improvements from estimated ceilings. Preserve enough method to reproduce the comparison, not just its headline number.

### Next research, in priority order

Keep an ordered queue of concrete questions or experiments. Respect an order the user supplied. Otherwise label the ordering as the agent's proposed priority and explain the expected payoff or dependency briefly.

For each lead, capture what is known, what is uncertain, and the smallest useful next check. Make the first next step obvious. Research one lead at a time unless the user asks otherwise. This queue proposes work; writing it does not start experiments or authorize implementation.

### Parked threads

Keep useful side quests, alternative strategies, upstream bugs, and questions outside the current focus. Explain why each was parked and what would make it worth returning to. Do not silently promote them into scope or discard them because they are not the next priority.

### Evidence and useful references

Include relevant repository paths, symbols, commits, run IDs, documentation URLs, commands, and short code or log excerpts. Explain what each reference establishes. Prefer durable references, but preserve session-local paths when they are the only evidence and mark them as temporary.

Keep the essential findings and reasoning in the notebook even when linking to longer documentation. A scratchpad link alone is not a handoff. Do not claim to have inspected a source that was only mentioned in the conversation, or run builds and experiments merely to fill gaps in the write-up.

## Keep the notebook alive

Once invoked, update this same file as the current research proceeds, after meaningful findings, failed attempts, user corrections, changed priorities, or new threads. Do not wait until context is exhausted. This instruction applies to the activated research, not to unrelated future conversations.

Merge updates into the relevant sections. Preserve useful negative results and explanations. When new evidence overturns an earlier conclusion, mark it as superseded and explain why rather than silently replacing the history. Remove repetition, not knowledge. Do not impose a length cap that discards useful research.

Include a short continuation note in the notebook: read it before continuing this research, check live state before relying on stale observations, pursue the next agreed question, and update the file with findings and new threads. Suggestions in the notebook do not expand the user's authorization.

If asked for a final handoff, reconcile the current state and next steps in this same file rather than creating a competing handoff document. Do not imply that unavailable earlier context was recovered.

Finish with the file path, whether local Git exclusion was verified, and any consequential gaps. Keep the response short; the research belongs in the file.
