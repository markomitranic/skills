---
name: pr-story
description: Turn a pull request, branch diff, or any substantial changeset into a structured HTML walkthrough — chapters grouped by what (and why) the changes happen, ordered so nothing is referenced before it's introduced, each explaining why it exists and how it's used — delivered as a single HTML file. This explains a changeset; it does not review or critique it. Use whenever the user needs to understand or get oriented in a large, unfamiliar, or AI-generated diff — "explain what this branch changes", "walk me through this diff", "I inherited a huge slop PR".
---

# PR Story

GitHub's UI for reading a PR is not good, human-centric UX. It displays changes in alphabetic order, broken down into commits, so a human reviewer needs to perform huge cognitive load to read the code out-of-order, in order to understand what was done and why - before they can begin to review side effects or architecture.

Your mission is to eliminate that cognitive load. Create a HTML page for the human to read, that presents the PR broken down into a sequence of easy to follow chapters.

This page is a precursor, not a replacement: the reader will still open the real diff on GitHub. Completeness is GitHub's job; yours is the story. A file that isn't part of the story simply doesn't appear on the page — no inventory, no accounting for what was left out.

Analyze the changes, take into account the context and architecture, and if possible, use MCP servers to read the Jira ticket to learn more about the intent.

- Skill structures are templates, not checklists. Every section below is optional — skip what doesn't apply rather than filling it with filler.
- Length is governed by the Budgets section. Every budget is a ceiling, not a quota: coming in under budget is success, not laziness.
- Cut test for every paragraph: does it change what the reviewer does next? If not, delete it.
- If the whole point fits in 3 sentences, the artifact is barely longer than that: header, moral, one visual, done.

## Tone of voice

This MUST NOT sound like a dry legal/technical document. It should explain conceptually what has changed, in a friendly way like a senior teaching a junior. Short sentences, human sounding, pragmatic, concise and plainspoken, like explaining to a colleague. If a sentence would fit in a scientific paper or an audit report, rewrite it in spoken words or delete it.

bad:  "This refactoring consolidates the type definitions to ensure consistency across both API integration layers."
good: "There are 2 APIs but only 1 shared type. This makes the second API use it too."

The whole page is what the author would say walking you through the PR at a whiteboard. If they wouldn't say it out loud, it doesn't go in.

- Talk to "you", the reader: "you'll hit this again in chapter 3", not "the reader will encounter".
- Answer the questions a junior would actually ask out loud ("wait, why is this in the worker?") — and no others.
- Shrugging is a valid explanation. "The rest is plumbing, nothing surprising" is a complete, honest sentence, and often the kindest one.
- Phrases like "it is worth noting", "this ensures", "leverages", "furthermore" are a smell: nobody says them out loud. When you catch one, suspect the whole sentence — usually it's restating rather than explaining, and the fix is rewriting the thought as speech, not swapping the word.
- Never announce what a chapter is about to explain, and never close it by summarizing what it just said. Start at the point, stop at the end.

bad:  "In this chapter we'll walk through how the validation logic was restructured."
good: "The 2-character minimum isn't new — it just moved."

- A technical term appears only if the same sentence explains it in plain words, or an earlier part of the page already introduced it.

bad:  "Search submits are debounced to reduce churn."
good: "Typing waits 300ms after the last keystroke before submitting — a debounce — so five letters cost one request, not five."

Build a story, tell a narrative. Iteratively onboard the reader to the problem-space. Explain what things are. Give concrete examples, not abstract or imperative language, and plan a figure wherever a picture beats a paragraph.

## Storytelling

In the GitHub PR UI, the reader is presented with a dry, alphabetic code dump. This is bad because it does not assist the human reader in seeing the zoomed-out wider perspective. It focuses on things that matter little - code style, syntax - but doesn't help explain the intended effect the PR has. It doesn't present the information in a logical reading order. Your job is to rebuild that order and explain the change in it, to someone who does not know this codebase.

**No Critique:** Your job is NOT to review the code, it is purely to help the reader understand it. Explain a behaviour so the human can judge it themselves, then stop — no verdicts, no critique, no severity flags. Judging the code is the human's task, your job is to provide the context, details, explanations, edge cases, examples etc.

## Budgets

Every part of the page has a prose budget. Budgets count prose only — words inside code fences are exempt — and every number is a ceiling, not a quota. Do not pad to reach one.

| Section | Prose ceiling | Figures |
|---|---|---|
| Introduction | ~200 words | 1 hero |
| Mechanical chapter | 2 sentences (≤120 characters total) + a quick list of ≤3 items | 1 tiny figure |
| Business-logic chapter | ~400 words, quick list included | 1 — see the gate below |
| Test chapter (optional) | ~150 words | none |

Chapters: minimum 1, hard ceiling 7. Most PRs honestly land at 2–3 — let the diff decide the count, never target one. A huge mechanical PR can be a single chapter, and so can a small, tightly-coupled business-logic PR. The intro and the test chapter don't count toward the ceiling.

**Classification decides the budget, so guard it.** A chapter is business-logic only if observable behaviour changes — a user, a caller, or an API sees something different afterwards. Refactors, moves, renames and rewiring are mechanical even when they're large. When unsure, mechanical. One tie-breaker: when the rewiring itself is what changes the observable behaviour — the same lines do both — the chapter is business-logic; rewiring earns mechanical only when nobody outside the diff sees a different result.

**A second figure must be earned.** One figure per business-logic chapter is the rule. A second is allowed only when the chapter explains two distinct mechanisms — write the one-sentence caption of each figure first; if the captions overlap, or the second caption is a detail of the first, there is no second figure. Wanting a second figure usually means the chapter is really two chapters: split it instead. Two figures is the ceiling either way — a third mechanism stays prose-only. And a split must be earned by the diff, not by the figure count: a small, tightly-coupled change stays one chapter even if that leaves a mechanism unillustrated.

**Code is exempt from the budget but earns its place** the same way a figure does: the prose beside a hunk must point at something specific inside it. Never include a hunk for coverage — this page is the explainer, GitHub already has the full diff.

## Pipeline

Three phases. All prose is written and edited as markdown; the HTML exists only at the very end, assembled by a sub-agent, and never enters your context.

```
Phase 1 — WRITE       you, + research sub-agents (Sonnet)
  story.md            header, intro, chapters — with @@FIG:name@@
                      placeholders and diff hunks in fenced blocks

Phase 2 — PARALLEL    one message, every sub-agent at once
  line editor (Opus)     rewords story.md in place
  illustrators (Sonnet)  one per figure, each writes its own fragment file

Phase 3 — ASSEMBLE
  assembler (Sonnet)  story.md + template.html → pr-story-{title}.html
  you                 inline the figures, verify with greps, open in browser
```

### Phase 1 — write story.md

1. Checkout, or pull PR stats, listing and metadata, so that you can be careful about accidentally reading a huge diff wholesale.
2. Read the PR description and the associated Jira ticket (if any).
3. Silently drop lockfiles, vendored deps, `dist/`, generated code, snapshots, formatting and license sweeps — they get no mention on the page.
4. Define the table of contents: a title, slug, classification and budget per chapter (the chapter meta line below).
5. Write the chapters into `story.md` in a scratch location. Use sub-agents (Sonnet) for grunt-work: reading the surrounding module, grepping callers, chasing blast radius.
6. Write the introduction, and optionally the test chapter: commands to run, UI actions that replicate the issue.

#### Introduction

Reading the abstract is when the human's attention is at its sharpest, but their knowledge of the intent at the lowest.

Lead with the moral of the story — one plain sentence a colleague would say out loud: "There are 2 APIs but only 1 shared type in our codebase; this PR fixes that." If the reviewer reads nothing else, this sentence must carry the PR. In story.md the moral IS the header blurb — the plain paragraph right under the doc meta. The intro section continues from it without repeating it, in WHY-first order: the problem, then the approach. The intro is allowed to stop after a sentence or two.

- Line items only if the PR genuinely did several separate things.
- Deviations from the plan, trade-offs, challenges — only if they actually happened. Skip the section entirely rather than writing "no major trade-offs were made".
- Links to Jira tickets, Figma, Storybook, API docs — only ones that exist, as a bare link list.
- The hero figure sits here: a slide-sized, boundaried, contained card that visualizes the single most important concept of the PR's intent.

#### Table of contents

Chapters are grouped by change intent and ordered to onboard the reader top-down: the changes that anchor the PR's purpose first, utilities later. A chapter answers "what does this group of changes DO", never "what's in this directory". Optimize for reading flow, not for symmetry with the diff — chapter count follows the story, not the size of the PR.

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

- Nothing is referenced before it's introduced. The reader never meets a symbol whose definition hasn't appeared yet.
- Why, not what. The diff already shows what changed. Prose is for intent, consequences, and relationships. Example: "Before this, a session stayed valid until the user logged out. This adds a 24h TTL so abandoned sessions can't be replayed. The TTL is measured from `createdAt` rather than `lastSeenAt`, so it fires 24h after sign-in whether or not the user is still active." Old behaviour, new behaviour, then the detail the diff can't show.
- Who uses it? Grep the changed symbols across the repo *outside* the diff: callers, dependents, config. This blast radius is what separates the page from a file listing. If nothing outside the diff is affected, say so in one sentence and move on.
- Noise is omitted, silently. The goal is to help understand the PR, not offer a definitive list — the reader has GitHub for that.
- Use the project's own layered architecture language, and hyperlink to relevant files or concepts.
- Hover-tooltips explain domain terms in banal plain-language where needed.
- Within a chapter, dependency order — schema → types → logic → call sites → UI → config — with tests beside the code they cover, never batched at the end.
- Write prose the way you'd explain the change out loud: short sentences, plain words, the point of a paragraph in its first sentence. Name the actual value, call site or field instead of describing it in general terms.

#### The story.md format

Plain markdown, plus exactly five constructs the assembler understands:

1. **Doc meta** — an HTML comment right under the `#` title: `<!-- meta: repo · #PR (with URL when one exists) · branch · 1 file (+111 −38) -->`. The assembler builds the header's metadata line from it and computes the chapter count itself. The plain paragraph right below it is the header blurb — the moral of the story.
2. **Chapter meta** — an HTML comment right under each `##` heading: `<!-- chapter: slug=ch-single-writer type=business budget=400 -->`. Types: `intro`, `business`, `mechanical`, `test`. `budget` is the prose ceiling in words; mechanical chapters omit it — their ceiling is structural (two sentences ≤120 characters, list ≤3 items). Slugs come from the chapter's purpose, never its number, so a deep link a reader shares survives a regeneration.
3. **Fences** — ` ```diff path=src/foo/bar.ts line=42 ` with real `+`/`-`/space prefixes on each line; `line` anchors to the head revision so it matches what the reader opens. Any other fence (` ```bash caption="run the tests" `) is a command card, its caption the card's title.
4. **Tooltips** — `[term]{tip: plain-words explanation}` for domain terms.
5. **Placeholders** — `@@FIG:name@@` alone on its own line for a figure an illustrator will draw; `@@IMG:name@@` inside `<img src="@@IMG:name@@">` for a raster that already exists as pixels (screenshot, Figma export, Jira attachment). Each is followed by its brief as a comment: `<!-- fig name: one-line concept the figure must show -->`. These comments are the illustrators' briefs, written while the chapter is fresh in your head.

Example skeleton:

````markdown
# Union rep filters become a validated form
<!-- meta: dansk-metal-website #1207 · union-rep-form-state-mng · 1 file (+111 −38) -->

Two filter widgets wrote straight to the URL with no shared rule; now one form owns both.

## What's in here
<!-- chapter: slug=intro type=intro budget=200 -->
…the problem, then the approach — the moral already sits above as the blurb…

@@FIG:hero@@
<!-- fig hero: before/after toggle — two loose widgets become one form boundary -->

## One function now writes the URL
<!-- chapter: slug=ch-single-writer type=business budget=400 -->
…opening, quick list, then details with a [debounce]{tip: wait until typing
stops before acting} where terms need it…

```diff path=src/templates/union-rep-overview-page.client.tsx line=59
+const filtersSchema = yup.object({ … })
```

@@FIG:single-writer@@
<!-- fig single-writer: three triggers funnel into one submit() -->
````

### Phase 2 — edit and illustrate, in parallel

Spin up the line editor and every illustrator in a single message so they run concurrently — they touch disjoint files, and none of them returns content through your context.

**Line editor — one sub-agent, Opus.** It rewords `story.md` in place with Edit tools:

- Every rewrite says the same thing in plainer, spoken words, and is shorter or equal — never longer. It never adds content.
- It deletes sentences that restate the diff, a figure brief, or the quick list, and reorders sentences for flow. Chapter structure is settled: it never merges, splits or reorders chapters.
- It enforces each chapter's budget from the meta line — `wc -w` on the prose, code fences exempt. Mechanical chapters carry no number: their ceiling is two sentences totalling ≤120 characters plus at most 3 list items.
- When a chapter carries two `@@FIG` placeholders it reads both briefs; if they describe the same mechanism, it says so in its note and the main thread decides — the editor itself never deletes a placeholder.
- Placeholders and meta comments are load-bearing: it may move a `@@FIG:name@@` (with its brief) within its chapter, it never deletes or renames one.
- It returns a one-paragraph note plus per-chapter word counts before/after — never the document.

**Illustrators — one sub-agent per figure, Sonnet.** Text creates cognitive load, visuals lower it — that's why even a mechanical chapter keeps its one tiny figure. Brief each illustrator from the `<!-- fig … -->` comment plus relevant context and pointers — the concept, never the technology. An illustrator is an artist, a technology creative: explain the problem space and let it do its magic.

Scale each figure to its chapter: a business-logic chapter may earn a rich or interactive piece; a mechanical chapter gets a tiny strip (e.g. an animated directory tree of files moving). The test is the same as for prose: the figure must show something the reader would otherwise have to reconstruct in their head. The test governs what the figure shows, never whether it exists — a plain chapter earns a smaller, simpler figure, not a grander fake.

**A figure is not necessarily a diagram.** The default failure mode is the dead card — three boxes, two arrows, no life. A figure can be a chart, a toy, a machine the reader operates. Shapes worth stealing (the idea, not the list — it's inspiration, not a menu):

- **Before/after toggle** — one switch flips the whole figure between old and new behaviour. The cheapest interactivity there is, and it fits almost any PR.
- **Step-through sequence** — a "next" button walks a request through the pipeline one hop at a time, each hop lighting up with a one-line caption.
- **Tiny chart** — when the PR is about a number: bundle 412→218 KB, 3 queries became 1, backoff capped at 30s. Two bars beat a paragraph.
- **Live playground** — the PR adds a validator, formatter, slug generator? Reimplement its 10 core lines in JS behind an `<input>` and let the reader type. Nothing explains a regex better.
- **Payload diff** — the JSON or type shape before and after, changed keys highlighted, hover for the why.
- **Fake mini-UI** — a postage-stamp replica of the affected screen with the changed element animating; for UI work this beats a screenshot because it can show the motion.
- **Clickable decision tree** — new branching logic (flags, fallbacks, error paths): the reader picks the conditions and watches the path light up.
- **Animated file tree** — for moves and renames, entries slide from the old locations to the new ones.
- **Blast-radius map** — the changed module in the centre, its callers arranged around it, the ones touched by the diff lit up.

The test: the reader should learn something by touching it, or it should show motion the prose can't. If neither applies, a plain static figure is honest and fine — a dead card still beats a fake-interactive one.

**Choosing the medium** is the illustrator's call, per figure. The bias runs HTML/CSS > SVG > Canvas > raster image, but the shape of the idea decides:

- **HTML/CSS** — the default. Most PR figures are boxes, lists, and arrows-between-things, and that's just markup: a before/after directory tree as two `<ul>`s with entries that slide over on hover, a request pipeline as flex cards with CSS-animated arrows, a config diff as a two-column card. It inherits the page's fonts and colours for free, animates with transitions, and gets interactivity from `:hover` and checkboxes — no script needed.
- **SVG** — when it's genuinely a *drawing*: curved edges between nodes, precise geometry, a timeline with bezier connectors, a gauge, anything where elements must sit at exact coordinates. If you're fighting flexbox to make lines meet boxes, you wanted SVG.
- **Canvas** — only for what the first two can't express: hundreds of moving points, a plot generated from data, particle-style motion. Rare in a PR story; needing Canvas is a hint the figure may be too clever.
- **Raster image** — never drawn, only reused: a screenshot, a Figma export, a Jira attachment that already exists as pixels.

Illustrator rules, to keep them fast and cheap:

- Each illustrator writes its finished figure — in whatever medium it chose — to its own file (e.g. `/tmp/prs-ch-billing.html`) and returns **only the file path plus one sentence** describing it. The markup itself never travels through a report.
- Fragments must be self-contained: any styles scoped inside the fragment (a `<style>` block with classes prefixed by the figure's name, or inline styles), no `<html>`/`<body>` wrapper, free to use the page's colour tokens (`--fg`, `--muted`, `--accent`, `--add`/`--del` tints, `--add-ink`/`--del-ink`/`--warn-ink`).
- **Strong contrast, non-negotiable.** `--add` and `--del` are pale *background tints* — using them as `fill`, `stroke`, or text colour produces invisible marks (`fill: var(--del)` is #ffebe9 on a white card). Anything that carries meaning — text, lines, arrows, icons — is drawn in ink: `--fg`, `--accent`, `--add-ink`, `--del-ink`, `--warn-ink`, all readable on `--bg` and `--card` in both themes. A tint is only ever the wash *behind* ink. Two self-checks: text and strokes should contrast like body text does, and the figure should still read if printed in grayscale.
- **No browser use.** The illustrator should not attempt to open the figures in a browser to preview them.

### Phase 3 — assemble

**Assembler — one sub-agent, Sonnet.** Give it `story.md`, the skill's @assets/template.html and the output path — `pr-story-{title}.html` in a scratch location such as the system tmp folder. Brief it with the conversion rules and template hooks below. The template is a worked example of a finished page: replace the content, keep the shapes, delete any section with nothing in it.

Conversion rules:

- Page shape, top to bottom: header (title, metadata line, blurb), "What's in here" (intro + hero), then chapters with the outline beside them. The header's metadata line comes from the doc meta comment; the chapter count in it is computed, not authored.
- Each `##` becomes a `.chapter` whose `id` is the meta slug — except `type=intro`, which becomes the "What's in here" section: no outline entry, no viewed checkbox. Every meta and fig comment is dropped from the output.
- Diff fences become the template's diff cards: each line its own `<span class="ln add|del|ctx">` inside `<pre class="diff">`, keeping the real `+`/`-`/space prefixes, with `path:line` in the card header. Non-diff fences become the template's command cards, the fence's `caption=` as the card title.
- `[term]{tip: …}` becomes `<span class="tip" title="…">term</span>`.
- `@@FIG:name@@` and `@@IMG:name@@` placeholders survive verbatim — figures standing alone where they go, images inside their `src="…"`.
- All code content HTML-escaped (`&` `<` `>`) — systematically, not per-line by eye; this is the most common rendering bug.
- The delivered file references nothing outside itself: no sibling assets, no image files, no separate stylesheet. CDN libraries only when they truly earn their weight.
- The assembler never authors prose. Template sections with no story.md counterpart (like the architecture primer) are deleted, not filled.
- It returns the output path plus three counts: chapters, placeholders (`@@FIG:` and `@@IMG:` together), prose words — never the document.

Template hooks the assembler keeps wired (nothing is persisted — the page is stateless and every toggle resets on reload):

- `.chapter` + `id` — the chapter wrapper: scrollspy target, `:has()` host for the viewed state, and what the outline links to
- `.chapter-body` — everything below the chapter heading; this is what collapses
- `input[data-viewed]` — per-chapter checkbox. Pure CSS `:has()` collapses the body; JS only updates the counter, dims the outline entry, and bolds whichever chapter is on screen
- `.prs-outline` — outline links, looked up by `href="#id"`
- `#prsProgress`, `#prsViewedCount` — scroll bar and the "3 / 8 chapters viewed" counter
- `.diff` + `.ln` — the `<pre>` deliberately does not preserve newlines and each `.ln` re-enables `pre` itself; drop the wrapper and the whole block collapses onto one line
- `--add-ink` / `--del-ink` / `--warn-ink` — high-contrast counterparts to the `--add`/`--del` background tints; the colour for any text, stroke or icon that means added/removed/careful. The tints themselves are backgrounds only.
- `.tip` — the hover-tooltip span
- `#spPanel` — the scratchpad. The reader selects any text, types a note, and the panel collects it with ±150 characters of surrounding context; "Copy to AI" hands the lot to an agent as markdown. Nothing to fill in, but don't delete it.

**Then you inline the figures.** Never let a figure fragment or image into your own context — one command swaps every placeholder. Raster images (`@@IMG:name@@` inside `src="…"`) come from disk: a screenshot already is, a Figma frame comes from `download_assets`, a Jira or GitHub attachment needs `curl -sL "$url" -o /tmp/prs-login.png`; downscale anything large first (fx gifsicle or `sips -Z 1400 shot.png --out shot-web.png`). Then one pass swaps them all:

```bash
python3 -c 'import base64,pathlib,re,subprocess,sys
f=pathlib.Path(sys.argv[1]); h=f.read_text()
for a in sys.argv[2:]:
    tag,src=a.split("=",1); p=pathlib.Path(src)
    if tag not in h: sys.exit("placeholder not in page: "+tag)
    m=subprocess.run(["file","-b","--mime-type",src],capture_output=True,text=True).stdout.strip()
    inline=tag.startswith("@@FIG:")
    v=re.sub(r"^\s*<\?xml.*?\?>\s*","",p.read_text(),flags=re.S).strip() if inline else "data:%s;base64,%s"%(m,base64.b64encode(p.read_bytes()).decode())
    h=h.replace(tag,v); print("inlined",tag,m,p.stat().st_size,"B")
f.write_text(h)' /tmp/pr-story-{title}.html \
  '@@FIG:hero@@=/tmp/prs-hero.html' '@@IMG:login@@=/tmp/prs-login.png'
```

It prints one line per figure and nothing else. An SVG passed as `@@IMG:` becomes a base64 `data:` URI like any raster — an SVG that should be live in the DOM goes through a `@@FIG:` placeholder instead. Matching is literal, so `/` `+` `$` `\1` in the payload are harmless, and the MIME type comes from `file` rather than the filename, so an extension-less attachment still gets `data:image/png;base64,…`. A missing placeholder exits non-zero and writes nothing. Do not attempt this with `sed` or `perl -i` — the base64 has to travel as an argument, which blows past macOS's 1 MB `kern.argmax`.

**Verify without reading.** The finished page is large, and every re-read of it inflates every subsequent request for the rest of the session — never read the assembled page back. Instead: `grep -c '@@' page.html` must print 0 (no placeholder survived), the assembler's prose word count should be within a few percent of the line editor's summed after-counts, and `open` the page in the system default browser for the visual once-over.

## Other tips

- You are in charge of the codebase, you are allowed to switch branches or use git commands to do comparisons, or github commands to read stats and file lists.
- Detect moves so relocations don't read as rewrites — git's `-M`/`-C`, or compare the blocks on large delete+insert pairs. Report "moved, unchanged" or "moved, plus these edits", showing only the real edits.
- Anchor line numbers to the **head** revision so they match what the reader opens. The hunk header's second number (`@@ -40,7 +42,9 @@` → 42) is the head start line; count forward.
