---
name: unslop
description: Cut AI tells from any writing. Must always apply.
---
# Unslop

Edit text to remove AI patterns and add human voice.

## Process

1. Scan for the patterns below.
2. Rewrite. Preserve meaning, match intended tone.
3. Add soul (see next section).
4. Self-audit: "What makes this obviously AI generated?" and "Would a human say this sentence out loud?" Fix remaining tells.

## Adding soul

Removing patterns is half the job. Sterile, voiceless writing is just as obvious.

- **Have opinions.** React to facts instead of neutrally listing pros and cons.
- **Vary rhythm.** Short sentences. Then longer ones that take their time. Mix it up.
- **Acknowledge complexity.** "Impressive but also kind of unsettling" beats "impressive."
- **Use "I" when it fits.** First person isn't unprofessional.
- **Let some mess in.** Perfect structure looks machine-made.
- **Be specific.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am."

## Explaining things

Structure for anything that teaches or reports.

- **Onboard in order: the thing, the problem, the fix.** Say what the thing is before why it matters, and why it matters before what changed. The reader stays patient because each step lands on solid ground.
- **Ground new terms.** Never lean on a domain concept the reader hasn't met. Land the idea and its name in the same sentence: "When a customer starts checkout we freeze their price for 10 minutes (the commitment window)." After that, the term is fair game. Bad: "The sync now respects the commitment window, so stale offers stop leaking into the feed" (three house terms, reader has met none).
- **Anchor with short concrete examples.** One real input and output beats a paragraph of description. An ASCII drawing helps when describing structure or flow; a picture says a thousand words.

## Patterns to detect and fix

### Content

1. **Puffery.** "pivotal moment", "testament to", "evolving landscape", "load-bearing", "setting the stage for", "indelible mark", "deeply rooted". Cut puffery, state what happened.
2. **Name-dropping.** Listing media outlets without context. Pick one, say what was said.
3. **Superficial -ing phrases.** "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering...". Delete or expand with real sources.
4. **Promotional language.** "nestled", "vibrant", "breathtaking", "groundbreaking", "renowned", "stunning", "must-visit". Use neutral descriptions.
5. **Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source or delete.
6. **Formulaic challenges.** "Despite challenges... continues to thrive." Replace with specific facts.

### Language

7. **AI vocabulary.** Additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant. Replace with plain words.
8. **Fancy ways to say "is".** "serves as", "stands as", "boasts", "features". Just say "is" or "has".
9. **Unearned antithesis.** "Not just X, but Y", "This isn't error handling — it's a philosophy of resilience", "We didn't simply move the file; we redefined the module boundary". The negation exists to make the sentence sound clever. State the point directly. Antithesis is fine when both halves are concrete and the contrast is the mechanism: "The lock is a ref rather than useState, because rerendering resets it." When the contrast is real, "instead of" and "rather than" say it in the shape of natural speech.
10. **Rule of three.** Forcing ideas into groups of three. Use the natural number.
11. **Synonym cycling.** Protagonist, main character, central figure, hero all in one paragraph. Pick one, repeat it.
12. **False ranges.** "from X to Y" where X and Y aren't on a meaningful scale. List topics directly.
13. **Absolutes.** "complete", "exhaustive", "definitive", "always", "never". "The ladder is the complete list of roles" overclaims; nothing in this life is certain. Drop the absolute or state the actual bound.

### Style

14. **Em dashes.** Never use em dashes. Use periods or commas only (no parentheses, no en dashes, no hyphen-as-dash substitutes). Em dashes are an AI tell, and reaching for parentheses instead just trades one tell for another. If a thought needs separation, end the sentence or use a comma.
15. **Colon overuse.** Colons are fine before a list or example. Not as mid-sentence connectors. "If you're coming from traditional automation: instead of registering event handlers, you describe conditions" adds nothing with the colon. Rewrite to let the point stand on its own without comparison framing. "Describing when the scheduler should fire works best as plain English." Same meaning, no crutch punctuation.
16. **Boldface overuse.** Don't bold every proper noun or acronym.
17. **Inline-header lists.** The tell is a bold label and colon that restates the line: "**Performance:** Performance improved...". Convert those to prose. A bold lead-in that ends in a period, names the item, and is followed by genuinely new detail ("**Schema in TypeScript.** Tables live in one file.") is fine, not a tell.
18. **Title case headings.** Use sentence case.
19. **Decorative emojis.** Remove from headings and bullets.
20. **Curly quotes.** Replace with straight quotes.
21. **Telling me how many things had to be true. "**Two things had to be true before any of this worked, and both are easy to get wrong." Nobody cares, the sentence adds zero value, just say what you meant.

### Communication artifacts

21. **Chatbot phrases.** "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", "Found the smoking gun!" Remove.
22. **Cutoff disclaimers.** "One thing you shoud know", "While specific details are limited..." Find sources or remove.
23. **Sycophantic tone.** "Great question! You're absolutely right!" Respond directly.

### Filler

24. **Filler phrases.** "In order to" becomes "To". "Due to the fact that" becomes "Because". "It is important to note that" gets deleted.
25. **Excessive hedging.** "could potentially possibly be argued that it might" becomes "may".
26. **Generic conclusions.** "The future looks bright." State specific plans or facts.
27. **Repeated points.** Every paragraph must do something new for the reader. Summaries that restate the intro, conclusions that restate the body, the same claim in new clothes. Delete the repeat.
28. **Babysitter clauses.** Justifying a rule by imagining someone breaking it: "It names every role that may exist, so nobody invents a thirteenth." Nobody was going to. Delete the clause.

### Jargon

29. **Abstract metaphor nouns.** Substrate, wedge, vector, locus, vantage, nexus, primitive (as noun), harness (as metaphor), surface (as in "API surface"), bedrock, scaffolding (as metaphor), modality, paradigm, gold-plating, ratchet (as metaphor), evacuate (for moving code), endgame, north star, flywheel. These read as technical but usually have a plainer concrete word. "Substrate" becomes "base". "Wedge in" becomes "add". "Vector" becomes "way" or "method". "Gold-plating" becomes "more than the job needs". "Ratchet" becomes the mechanism's real name or "a limit that only tightens". "Evacuate" becomes "move out". "Endgame" becomes "the last phase". Pick the concrete word.

### Plain speech

30. **Presentation voice.** Test each sentence against spoken conversation; if no human would produce it in normal speech, it doesn't deserve to be here. "Within the three groups live twelve named roles" becomes "We've got 12 roles in these 3 groups". "Skip any rung that has no complexity to house" becomes "Skip the parts your project doesn't need".
31. **Say what it does, not how it feels.** "the database stays close at hand", "SQL you can read", "types that follow your schema" name a feeling. The fix names the mechanism or a number: "`.toSQL()` returns the exact string sent to the database", "a column rename fails the build". Ask what the sentence tells the reader to do or know, then write that. If you can't restate it as a concrete instruction, fact, or number, cut it. One more check: if the sentence could appear unchanged in another project's docs, it says nothing about this one. Cut it.
32. **Shorten or split dense sentences.** If the reader has to backtrack to parse a sentence, break it in two or drop clauses. One idea per sentence. "The 300ms debounce applies to typing only. Whereas, picking a filter in the dropdown still submits instantly." Two sentences, one edge case each.
33. **Active voice.** Prefer it. Catch "is/are/was/were + past participle" and name the actor: "queries are validated" becomes "the compiler validates queries", "the file is parsed by the loader" becomes "the loader parses the file". Passive is fine only when the actor is unknown or genuinely doesn't matter.
34. **Cut adverbs, or use a stronger verb.** "runs quickly" becomes "is fast" or the number. "significantly improves" becomes the measured delta. An adverb propping up a weak verb means the verb is wrong.
35. **Prefer the plain word.** "utilize" becomes "use", "leverage" becomes "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if". The fancier synonym is rarely clearer.

