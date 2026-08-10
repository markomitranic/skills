---
name: pr-story
description: Turn a pull request, branch diff, or any substantial changeset into a structured HTML walkthrough. A story-driven onboarding document, ordered so nothing is referenced before it's introduced, each explaining why it exists and how it's used — delivered as a single HTML file. This explains a changeset; it does not review or critique it. Use to help user understand the problem space, like a Senior would to a Junior.
---
# PR Story

GitHub's UI for reading a PR is bad. It displays changes in alphabetic order, broken down into commits, so a human reviewer needs to perform huge cognitive load to read the code out-of-order, in order to understand what was done and why - before they can begin to review side effects or architecture.

Your mission is to eliminate that cognitive load. Create a HTML page for the human to read, that presents the PR broken down into a sequence of easy to follow chapters.

This page is not a replacement for GitHub - it is an onboarding document the user reads first, before they go to do the actual review. This means that we do not have to show every single piece of code, our job is to tell a story with snippets and link them to the GitHub PR. A file that isn't part of the story simply doesn't appear on the page — no inventory, no accounting for what was left out.

Analyze the changes, take into account the context and architecture, and if possible, use MCP servers to read the Jira ticket or Figma to learn more about the intent.

- This is a template. Every section below is optional — skip what doesn't apply rather than filling it with filler.
- Length is governed by the Budgets section. Every budget is a ceiling, not a quota: coming in under budget is success, not laziness.

## Tone of voice

This MUST NOT sound like a dry legal/technical document. It should explain conceptually what has changed, in a friendly way like a senior teaching a junior. Short sentences, human sounding, pragmatic, concise and plainspoken, like explaining to a colleague.

bad:  "This refactoring consolidates the type definitions to ensure consistency across both API integration layers."
good: "There are 2 APIs but only 1 shared type. This makes the second API use it too."

The whole page is what the author would say walking you through the PR at a whiteboard. If they wouldn't say it out loud, it doesn't go in.

- Our north star is to lower cognitive load. If a sentence you write sounds too technical, scientific or legal, rewrite it in spoken words or delete it.
- Talk to "you", the reader: "you'll hit this again in chapter 3", not "the reader will encounter".
- Answer the questions a junior would actually ask out loud ("wait, why is this in the worker?").
- Shrugging is a valid explanation. "The rest is plumbing, nothing surprising" is a complete, honest sentence, and often the kindest one.
- Phrases like "it is worth noting", "this ensures", "leverages", "furthermore" are a smell: nobody says them out loud. When you catch one, suspect the whole sentence — usually it's restating rather than explaining, and the fix is rewriting the thought as speech, not swapping the word.
- Never announce what a chapter is about to explain, and never close it by summarizing what it just said. Start at the point, stop at the end.

bad:  "In this chapter we'll walk through how the validation logic was restructured."
good: "The 2-character minimum isn't new, it just moved here from the zod schema."

- A technical term appears only if the same sentence explains it in plain words, or an earlier part of the page already introduced it.

bad:  "Search submits are debounced to reduce churn."
good: "Search waits 300ms after the last keystroke before submitting (debounce), so that we don't send out 5 requests."

Build a story, tell a narrative. Iteratively onboard the reader to the problem-space. Explain what things are. Give concrete examples, not abstract or imperative language, and plan a figure wherever a picture beats a paragraph.

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

## Storytelling

In the GitHub PR UI, the reader is presented with a dry, alphabetic code dump. This is bad because it does not assist the human reader in seeing the zoomed-out wider perspective. It focuses on things that matter little - code style, syntax - but doesn't help explain the intended effect the PR has. It doesn't present the information in a logical reading order. Your job is to rebuild that order and explain the change in it, to someone who does not know this codebase.

**No Critique:** Your job is NOT to review the code, it is purely to help the reader understand it. Explain a behaviour so the human can judge it themselves, then stop — no verdicts, no critique, no severity flags. Judging the code is the human's task, your job is to provide the context, details, explanations, edge cases, examples etc.

## Budgets

Every part of the page has a prose budget. Budgets count prose only — words inside code fences are exempt — and every number is a ceiling, not a quota. Do not pad to reach one.

Boilerplate:

- Introduction, ~200 words, 1 hero figure
- Test chapter (optional), ~150 words, no figures

Chapters:

- Mechanical chapter, 2 sentences (≤120 characters total) + a quick list of ≤3 items, 1 tiny technical figure
- Business-logic chapter, ~400 words, quick list included, 2 figures (one whimsy, one technical)

Chapters: minimum 1, hard ceiling 7. Most PRs honestly land at 2–3 — let the story decide the count, never target one. A huge mechanical PR can be a single chapter, and so can a small, tightly-coupled business-logic PR. Onboarding the reader to the problem space matters more than the amount of code or call-sites a chapter covers, so act like a good technical writer would. The intro and the test chapter don't count toward the ceiling.

**Classification** A chapter is business-logic only if observable behaviour changes — a user, a caller, or an API sees something different afterwards. Refactors, moves, renames and rewiring are mechanical even when they're large. When unsure, mechanical. One tie-breaker: when the rewiring itself is what changes the observable behaviour — the same lines do both — the chapter is business-logic; rewiring earns mechanical only when nobody outside the diff sees a different result.

**Figure kinds** A business-logic chapter pairs one whimsy figure with one technical figure — two perspectives on the same chapter. That way, both the technical and non-technical readers have something to help them.

**Code is exempt from the budget** the same way a figure does: the prose beside a hunk must point at something specific inside it. Never include a hunk for coverage — this page is the explainer, GitHub already has the full diff.

## Pipeline

Three phases. All prose is written and edited as markdown; the HTML exists only at the very end, written by a sub-agent, and never enters your context.

```
Phase 1 — WRITE       you, + research sub-agents (Sonnet)
  story.md            header, intro, chapters — with <!-- INSERT-FIGURE-…: … -->
                      placeholders and diff hunks in fenced blocks

Phase 2 — EDIT        you, a separate cutting pass over story.md

Phase 3 — RENDER
  page-writer (Sonnet)  loads the artifact-design skill, then
                      story.md → pr-story-{title}.html, figures drawn in place
                      you open in browser when done
```

### Phase 1 — write story.md

1. Checkout, or pull PR stats, listing and metadata, so that you can be careful about accidentally reading a huge diff wholesale.
2. Read the PR description and the associated Jira ticket and/or Figma (if any). If the image test (Figures section) passes — the story will have to describe what something looks like — export the Figma frame or pull the ticket's screenshot while you're there.
3. Silently drop lockfiles, vendored deps, `dist/`, generated code, snapshots, formatting and license sweeps — they don't deserve a mention on the page.
4. Decide on how to tell the story: write a table of contents, with a title, slug, classification and budget per chapter (the chapter meta line below).
5. Write the chapters into `story.md` in a scratch location. Use sub-agents (Sonnet) for grunt-work: reading the surrounding module, grepping callers, chasing blast radius.
6. Write the introduction, and optionally the test chapter: commands to run, UI actions that replicate the issue.

#### Introduction

Reading the abstract is when the human's attention is at its sharpest, but their knowledge of the intent at the lowest.

The document's `#` title states the problem, declaratively — "Double-clicking Next could skip a checkout step", never the solution ("One lock stops the double-click race"). The reader meets the problem in the title, the fix in the blurb.

Lead with the moral of the story — one plain sentence a colleague would say out loud: "There are 2 APIs but only 1 shared type in our codebase; this PR fixes that." If the reviewer reads nothing else, this sentence must carry the PR. In story.md the moral IS the header blurb — the plain paragraph right under the doc meta. The intro section continues from it without repeating it, in WHY-first order: the problem, then the approach. The intro is allowed to stop after a sentence or two.

- Line items only if the PR genuinely did several separate things.
- Deviations from the plan, trade-offs, challenges — only if they actually happened. Skip the section entirely rather than writing "no major trade-offs were made".
- Links to Jira tickets, Figma, Storybook, API docs — only ones that exist, as a bare link list.
- The hero figure sits here: a slide-sized, boundaried, contained card that visualizes the single most important concept of the PR's intent.

#### Table of contents

Chapters are grouped by change intent and ordered to onboard the reader top-down: the changes that anchor the PR's purpose first, utilities later. A chapter answers "what does this group of changes DO" — never "what's in this directory", and never "where else the same change landed". Optimize for reading flow, not for symmetry with the diff — chapter count follows the story, not the size of the PR.

The moral is the thread every chapter hangs on. If you can't say in one breath how a chapter serves the moral, either the chapter is mis-scoped or the moral is too narrow — fix whichever is wrong before writing on.

**A chapter is a new idea, not a new location.** The unit is a mechanism, a decision, or a data shape the page hasn't introduced yet. Applying an already-introduced idea at another call site is coverage, not story: it becomes a paragraph — often just a quick-list item — inside the chapter that introduced the idea. The merge test: say each chapter's one-breath link to the moral out loud; if two links are the same sentence with different nouns, they're one chapter.

bad:  "The submit lock outlives the step swap" · "Back and sidebar jumps respect the same lock" · "Payment's button guards itself"
good: "The step machine locks after the first click" — one chapter; back-jumps, sidebar jumps and payment's button are three items in its quick list.

#### Writing a chapter

**Titles name the concrete change** — subject, verb, object, under 50 characters. Plain beats clever: a title that shows off gets rewritten. The test: someone reading only the table of contents can tell what each chapter covers.

bad:  "One writer, not many"          good: "One function now writes the URL"
bad:  "Two speeds, one submit path"   good: "Dropdown submits instantly, search waits 300ms"

**Mechanical chapters** (renames, moves, dependency bumps, formatting): two sentences, a quick list of at most 3 items, one tiny figure. Done — no deep dive, no code blocks. Skip the list when the two sentences already say it all.

**Business-logic chapters** start non-technical and get more technical as they go. After the opening, a quick and dirty list of the biggest changes as an overview of what's below — as many as are genuinely distinct, up to 6; two is fine, never invent a third:

- introduced the new `SearchOfferingContext` model
- Session TTL added to `validate()`
- `tenantId` threaded through 27 components

Then the details: paragraphs, code and the figure interwoven. The reader is technical — but assume zero knowledge of this codebase.

Ground rules:

- Nothing is leaned on before it's grounded. For symbols that's literal — the reader never meets one whose definition hasn't appeared yet. But the unit is the concept, not the word for it: a sentence with no jargon in it can still lose the reader by leaning on an idea the page hasn't introduced. Keep a running ledger of what the page has introduced so far; when the next paragraph needs a concept that isn't on it, grounding that concept IS the next paragraph.

  bad:  "This also fixes the double refresh." — no term to explain, yet the page never said anything refreshed twice
  good: "Both widgets wrote to the URL, so every click refreshed the page twice. With one writer, that's gone."
- Why, not what. The diff already shows what changed. Prose is for intent, consequences, and relationships. Example: "Before this, a session stayed valid until the user logged out. This adds a 24h TTL so abandoned sessions can't be replayed. The TTL is measured from `createdAt` rather than `lastSeenAt`, so it fires 24h after sign-in whether or not the user is still active." Old behaviour, new behaviour, then the detail the diff can't show.
- Who uses it? Grep the changed symbols across the repo *outside* the diff: callers, dependents, config. This blast radius is what separates the page from a file listing. If nothing outside the diff is affected, say so in one sentence and move on.
- Noise is omitted, silently. The goal is to help understand the PR, not offer a definitive list — the reader has GitHub for that.
- Use the project's own layered architecture language, and hyperlink to relevant files or concepts.
- Hover-tooltips explain domain terms in banal plain-language where needed.
- Within a chapter, dependency order — schema → types → logic → call sites → UI → config — with tests beside the code they cover, never batched at the end.
- Write prose the way you'd explain the change out loud: short sentences, plain words, the point of a paragraph in its first sentence. Name the actual value, call site or field instead of describing it in general terms.
- Prose carries argument; lists carry parallel items — each the same kind of thing, said in the same shape. The moment an item starts arguing or explaining, it stops being an item: move it to a paragraph. And when the same shape repeats 3+ times with the same fields — old path → new path, flag → default → effect — that's a table, not a list.

#### Figures

A figure must show something the reader would otherwise have to reconstruct in their head. There are two kinds, doing two different jobs:

- **Technical** — the schematic, for precision: a timeline, a payload with changed keys highlighted and a small legend, two before/after cards, two bars when the PR is about a number (bundle 412→218 KB). Strictly literal: every label names an actual click, call or value. Its brief states the mechanism and the values that matter.
- **Whimsy** — the intuition: aimed at non technical readers, a metaphor for everyday image the change lives in. Here the metaphor IS the subject and creative, playful labels are welcome — the one-line figcaption ties it back to the mechanism. Its brief is the image: pick it for its shape, don't focus on the technology. Invent the image fresh from this PR's own domain — never reuse an image you've seen used as an example, in this document or elsewhere; an echoed metaphor reads as a stamp, not an insight.

A business-logic chapter carries one of each — whimsy beside the non-technical opening, technical down in the details. A mechanical chapter gets one tiny technical figure. The hero is usually whimsy: the PR's intent as an image. Write every brief while the chapter is fresh in your head; the page-writer owns the how.

**Static-first, with a pulse allowed.** A figure may carry simple CSS animations — a looping transition, a gentle pulse, an element sliding home — when the motion shows the mechanism or gives the whimsy life; guard it behind `prefers-reduced-motion`.

Before/after belongs in one still picture: cross out the old value and write the new one beside it, or draw two small labelled cards. That almost always works — every PR is a before/after, so wanting to show two states is not a reason for a control. But when everything moved and one picture of both states is an unreadable mess, give the card a checkbox that flips it between before and after. That's the only control a figure ever gets, and it costs something: a reader skimming past only sees whichever state the card happens to show.

bad:  a checkbox flipping one value on a payload card
      (both values fit in the picture; the flip just hides one of them)
good: a checkbox on the checkout grid where six blocks moved
      (drawn on top of each other the two layouts are a mess; flipping is the only readable way)

**Images (escape hatch).** Most stories carry no image — a drawn figure explains a mechanism better than pixels do. But an image can stand in for a figure: in place of a chapter's technical figure, or the hero. It replaces that figure, it never becomes a third visual. Two ways one arrives: the user hands you a screenshot or export (jpg, png, gif), or you fetch one yourself during research — a Figma frame via the Figma MCP, a screenshot off the Jira ticket. A user-supplied image is placed, not judged. A fetched one must pass a test that runs on your own prose, not on what's attached: if a chapter has to describe what something looks like, the reader needs the actual pixels and your drawing would be a guess about details. If the chapter explains logic, data or flow, the drawing says it better — leave the attachment where it is.

bad:  the ticket has three screenshots, so the hero becomes one of them
      (attached ≠ relevant; most tickets carry images that explain nothing)
good: the PR fixes "logo overlaps the nav on mobile" — the before-screenshot IS the
      problem statement; any drawing of it would be less honest

Place it with the `INSERT-IMAGE` construct below; the figcaption still ties it to the mechanism. If the user wants a shareable Artifact link, images count toward the 16MB page ceiling — downscale anything over ~2MB.

#### The story.md format

Plain markdown, plus exactly six constructs the page-writer understands:

1. **Doc meta** — an HTML comment right under the `#` title: `<!-- meta: repo · #PR (with URL when one exists) · branch · 1 file (+111 −38) -->`. The page-writer builds the header's metadata line from it and computes the chapter count itself. The plain paragraph right below it is the header blurb — the moral of the story.
2. **Chapter meta** — an HTML comment right under each `##` heading: `<!-- chapter: slug=ch-single-writer type=business budget=400 -->`. Types: `intro`, `business`, `mechanical`, `test`. `budget` is the prose ceiling in words; mechanical chapters omit it — their ceiling is structural (two sentences ≤120 characters, list ≤3 items). Slugs come from the chapter's purpose, never its number, so a deep link a reader shares survives a regeneration.
3. **Fences** — ````diff path=src/foo/bar.ts line=42` with real `+`/`-`/space prefixes on each line; `line` anchors to the head revision so it matches what the reader opens. Any other fence (````bash caption="run the tests"`) is a command card, its caption the card's title.
4. **Tooltips** — `[term]{tip: plain-words explanation}` for domain terms.
5. **Figure placeholders** — `<!-- INSERT-FIGURE-TECH: the mechanism and the values that matter -->` or `<!-- INSERT-FIGURE-WHIMSY: the everyday image -->` alone on its own line where the figure goes.
6. **Image placeholders** — `<!-- INSERT-IMAGE: path=/abs/path/shot.png caption="checkout before the fix" -->` alone on its own line, for a user-supplied jpg/png/gif. The path must be absolute and the file must exist when you write the line.

Example skeleton:

```markdown
# Two filter widgets fight over one URL
<!-- meta: dansk-metal-website #1207 · union-rep-form-state-mng · 1 file (+111 −38) -->

Two filter widgets wrote straight to the URL with no shared rule; now one form owns both.

## What's in here
<!-- chapter: slug=intro type=intro budget=200 -->
…the problem, then the approach — the moral already sits above as the blurb…

<!-- INSERT-FIGURE-WHIMSY: two megaphones shouting over each other, handed a single microphone -->

## One function now writes the URL
<!-- chapter: slug=ch-single-writer type=business budget=400 -->
…opening…

<!-- INSERT-FIGURE-WHIMSY: three tributaries joining one river -->

…quick list, then details with a [debounce]{tip: wait until typing
stops before acting} where terms need it…

```diff path=src/templates/union-rep-overview-page.client.tsx line=59
+const filtersSchema = yup.object({ … })
` ` `

<!-- INSERT-FIGURE-TECH: dropdown, search and reset all funnel into the same submit(); the 300ms wait sits on the search path only -->
```

### Phase 2 — the cutting pass

You edit `story.md` yourself, in a separate pass — never in the same breath as writing. The trap is that you wrote these sentences moments ago and they all look necessary; the pass exists to delete them anyway. A pass that ends with zero deletions didn't happen. The rules:

- Every rewrite says the same thing in plainer, spoken words, and is shorter or equal — never longer. This pass never adds content.
- Delete sentences that restate the diff, a figure brief, or the quick list; reorder sentences for flow.
- Two cut tests on every paragraph: "what does this do for the reader that the previous one didn't?" and "if I cut it, what breaks?" Failing both means deletion. Redundancy with a neighbour is the failure the word counts can't catch.
- A sentence doing two jobs gets split, or picks one.

  bad:  "Sessions now expire after 24h, measured from `createdAt` rather than `lastSeenAt` since replay of abandoned logins was the concern."
  good: "Sessions now expire after 24h, so an abandoned login can't be replayed. The clock starts at `createdAt` rather than `lastSeenAt` so that staying active doesn't extend the session."
- Read each chapter against the header blurb — the moral. A chapter the moral didn't promise means one of them is wrong: re-thread the chapter or widen the moral. Run the merge test from the Table of contents section too: two chapters whose moral-links are the same sentence with different nouns collapse into one, the second surviving as a quick-list item.
- Enforce each chapter's budget from the meta line — `wc -w` on the prose, code fences exempt, before and after. Mechanical chapters carry no number: their ceiling is two sentences totalling ≤120 characters plus at most 3 list items.
- A business chapter carries one `INSERT-FIGURE-WHIMSY` (by the opening) and one `INSERT-FIGURE-TECH` (by the details).
- Rewrite common signs of AI writing such as slop-filling, em dashes, or bad antithesis.

### Phase 3 — render

**Page-writer — one sub-agent, Sonnet.** Give it the `story.md` path and the output path — `pr-story-{title}.html` in a scratch location such as the system tmp folder. Brief it to:

1. **Load the `artifact-design` skill first** (via the Skill tool) for its craft fundamentals — cascade hygiene, spacing via `gap`, focus states. The shell below is the existing design system, and per that skill's own precedence rule it always wins: apply it verbatim, invent nothing it already decides. Light theme only — no dark-mode plumbing.
2. Convert story.md into one self-contained HTML file: no CDN, no external requests, no sibling assets, every style and script inline. Page shape is the shell's skeleton, top to bottom: masthead (title, metadata line from the doc meta, blurb), linked table of contents, the intro chapter with its hero, then the chapters — each `##` a section whose `id` is the meta slug. Every chapter h2 carries its number (`.ch-num`, zero-padded, matching the table of contents) and a `.ch-tag` from the meta type — "business logic" or "mechanical change"; the intro and test chapter get neither. Every meta and placeholder comment is dropped from the output.
3. Diff fences become the shell's code cards with `path:line` in the card header, keeping the real `+`/`-`/space prefixes, added/removed lines tinted. Each code line is one `<span class="ln …">…</span>`; a blank line is an empty span (the shell gives it height, and newlines between spans are inert). Non-diff fences become command cards, the `caption=` as the card title. All code content HTML-escaped (`&` `<` `>`) — systematically, not per-line by eye; this is the most common rendering bug. `[term]{tip: …}` becomes `<span class="tip" title="…">term</span>`.
4. Draw each placeholder in place from its brief, in HTML/CSS or inline SVG inside a `.fig-frame`. `INSERT-FIGURE-TECH` is a schematic: every label names an actual click, call or value — if it could caption a children's book, it drew a metaphor instead of the mechanism. `INSERT-FIGURE-WHIMSY` draws its brief's image as itself — simple, warm, playful labels welcome — with a one-line figcaption tying it to the mechanism. Either kind may carry simple CSS animations (a loop, a pulse, an element sliding home) guarded behind `prefers-reduced-motion`. Before/after goes in one still drawing — old crossed out beside new, or two small labelled cards; only if that drawing would be an unreadable mess, a checkbox that flips the card between the two states — CSS only, never JS. Strong contrast: anything that carries meaning — text, lines, arrows — must read like body text, and the figure must survive grayscale. Pale tints are backgrounds only, never ink.
5. `INSERT-IMAGE` placeholders become `<figure><div class="fig-frame"><img src="@@IMG:/abs/path.png@@" alt="…" style="max-width:100%;display:block"></div><figcaption>…</figcaption></figure>`. The base64 must never pass through model context: after writing the HTML, run one script (bash/python) that finds every `@@IMG:…@@` token, base64-encodes that file, and splices a `data:image/{type};base64,…` URI into the page on disk — file to file. Verify with `grep -c '@@IMG:' page.html` printing 0.
6. Never author prose: every word on the page comes from story.md.
7. Write the page top-to-bottom in at most two Write calls — no revision loop, no previewing, no rendering. The image-splicing script runs after them and doesn't count.
8. Return the output path plus three counts: chapters, figures, prose words — never the document.

#### The page shell

This is the page's design system — tokens, type and components are settled; the page-writer types content into them. Anything the shell doesn't cover (figure internals, a one-off layout) is styled in its spirit: same tokens, same restraint.

```html
<style>
:root {
  --ground:#F1F4F3; --surface:#FFFFFF; --ink:#14201E; --muted:#5D6B68;
  --line:#D4DCD9; --line-strong:#A9B7B3;
  --accent:#0B6E6A; --accent-soft:#E0EDEB;
  --warn:#8F5200; --warn-soft:#F8EEDD;
  --add-bg:#E7F1E8; --add-ink:#1D5A2B; --del-bg:#FAE6E6; --del-ink:#8B2B2B;
  --font-display:"Helvetica Neue",Helvetica,-apple-system,"Segoe UI",Arial,sans-serif;
  --font-body:Charter,"Iowan Old Style",Palatino,Georgia,serif;
  --font-mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}
* { box-sizing:border-box }
body { margin:0; background:var(--ground); color:var(--ink);
       font:17px/1.65 var(--font-body) }
.page { max-width:960px; margin:0 auto; padding:0 24px 96px }
a { color:var(--accent); text-underline-offset:2px }
p { text-wrap:pretty; }
code { font-family:var(--font-mono); font-size:.86em; background:var(--accent-soft);
       color:#0A4A47; padding:.1em .34em; border-radius:3px }
.tip { border-bottom:1px dotted var(--line-strong); cursor:help }

header.masthead { border-top:3px solid var(--accent); padding-top:28px; margin-top:56px }
h1 { font-family:var(--font-display); font-weight:700; letter-spacing:-.025em;
     font-size:clamp(30px,5.2vw,44px); line-height:1.08; text-wrap:balance; margin:0 0 18px }
.meta { font:12px/1.9 var(--font-mono); color:var(--muted); margin:0 0 26px }
.blurb { font-family:var(--font-display); font-size:clamp(18px,2.6vw,21px); line-height:1.45;
         margin:0; padding:20px 0 22px 22px; border-left:3px solid var(--line-strong) }

nav.toc { margin:40px 0 8px; padding:16px 20px; background:var(--surface);
          border:1px solid var(--line); border-radius:4px }
section { margin-top:56px; display:flex; flex-direction:column; gap:20px }
section > * { margin:0 }
h2 { font-family:var(--font-display); font-size:clamp(22px,3.4vw,28px); font-weight:700;
     letter-spacing:-.02em; text-wrap:balance; padding-bottom:12px;
     border-bottom:1px solid var(--line) }
h2 .ch-num { font:0.55em var(--font-mono); color:var(--line-strong);
             letter-spacing:.05em; margin-right:10px; vertical-align:2px }
h2 .ch-tag { font:10.5px var(--font-mono); font-weight:400; text-transform:uppercase;
             letter-spacing:.08em; color:var(--muted); background:var(--surface);
             border:1px solid var(--line-strong); border-radius:3px;
             padding:3px 8px; margin-left:12px; vertical-align:4px; white-space:nowrap }
h2 .ch-tag.business { color:var(--accent); border-color:var(--accent);
                      background:var(--accent-soft) }

.card { background:var(--surface); border:1px solid var(--line);
        border-radius:4px; overflow:hidden }
.card-head { font-family:var(--font-mono); font-size:11.5px; color:var(--muted);
             background:#FAFBFB; border-bottom:1px solid var(--line);
             padding:8px 14px; white-space:nowrap; overflow-x:auto }
.card-body { overflow-x:auto; padding:10px 0 }
pre { margin:0; font:12.5px/1.7 var(--font-mono); tab-size:2; white-space:normal }
pre .ln { display:block; min-height:1.7em; padding:0 14px; white-space:pre; width:max-content; min-width:100% }
pre .add { background:var(--add-bg); color:var(--add-ink) }
pre .del { background:var(--del-bg); color:var(--del-ink) }
pre .ctx { color:#3C4A47 }
.cmd .card-head { background:var(--ink); color:#C9D6D3; border-bottom:none;
                  text-transform:uppercase; letter-spacing:.11em }
.cmd .card-body { background:var(--ink) } .cmd pre .ctx { color:#EAF1EF }

figure { margin:8px 0; display:flex; flex-direction:column; gap:12px }
.fig-frame { background:var(--surface); border:1px solid var(--line);
             border-radius:4px; padding:22px 20px; overflow-x:auto }
figcaption { font:11.5px/1.6 var(--font-mono); color:var(--muted) }
svg { display:block } svg text { font-family:var(--font-mono) }
```

Body skeleton:

```html
<body><div class="page">
  <header class="masthead">
    <h1>…</h1> <p class="meta">repo · #PR · branch · files (+/−)</p>
    <p class="blurb">the moral</p>
  </header>
  <nav class="toc">…numbered links to every section…</nav>
  <section id="intro">…prose… <figure><div class="fig-frame">hero</div>
    <figcaption>…</figcaption></figure></section>
  <section id="{slug}">
    <h2><span class="ch-num">01</span>…title…<span class="ch-tag business">business logic</span></h2>
    …prose…
    <div class="card"><div class="card-head">path.ts:42</div>
      <div class="card-body"><pre><span class="ln add">+ …</span></pre></div></div>
    …figure…
  </section>
</div></body>
```

**Verify without reading.** The finished page is large, and every re-read of it inflates every subsequent request for the rest of the session — never read the assembled page back. Instead: `grep -c 'INSERT-' page.html` must print 0 (no placeholder survived), `grep -c '@@IMG:' page.html` must print 0 when the story used images (every one got spliced), the page-writer's prose word count should be within a few percent of your cutting pass's summed after-counts, and `open` the page in the system default browser for the visual once-over.

The deliverable is the local file. If the user asks for a shareable link, publish the same file with the Artifact tool instead.

## Other tips

- You are in charge of the codebase, you are allowed to switch branches or use git commands to do comparisons, or github commands to read stats and file lists.
- Detect moves so relocations don't read as rewrites — git's `-M`/`-C`, or compare the blocks on large delete+insert pairs. Report "moved, unchanged" or "moved, plus these edits", showing only the real edits.
- Anchor line numbers to the **head** revision so they match what the reader opens. The hunk header's second number (`@@ -40,7 +42,9 @@` → 42) is the head start line; count forward.

