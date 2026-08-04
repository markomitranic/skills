---
name: pr-story
description: Turn a pull request, branch diff, or any substantial changeset into a structured HTML walkthrough — chapters grouped by what (and why) the changes happen, ordered so nothing is referenced before it's introduced, each explaining why it exists and how it's used — delivered as a single HTML file. This explains a changeset; it does not review or critique it. Use whenever the user needs to understand or get oriented in a large, unfamiliar, or AI-generated diff — "explain what this branch changes", "walk me through this diff", "I inherited a huge slop PR".
---

# PR Story

GitHub's UI for reading a PR is not good, human-centric UX. It displays changes in alphabetic order, broken down into commits, so a human reviewer needs to perform huge cognitive load to read the code out-of-order, in order to understand what was done and why - before they can begin to review side effects or architecture.

Your mission is to eliminate that cognitive load. Create a HTML page for the human to read, that presents the PR broken down into a sequence of easy to follow chapters. 

Analyze the changes, take into account the context and architecture, and if possible, use MCP servers to read the Jira ticket to learn more about the intent.

## Tone of voice
This MUST NOT sound like a dry legal/technical document. It should explain conceptually what has changed, in a friendly way like a senior teaching a junior. Short sentences, human sounding, pragmatic, concise and plainspoken, like explaining to a colleague.

Build a story, tell a narrative. Iteratively onboard the reader to the problem-space. Explain what things are. Give concrete examples, not abstract or imperative language. Use HTML or SVG drawings to visually represent what you are explaining.

## Storytelling

In the GitHub PR UI, the reader is presented with a dry, alphabetic code dump. This is bad because it does not assist the human reader in seeing the zoomed-out wider perspective. It focuses on things that matter little - code style, syntax - but doesn't help explain the intended effect the PR has. It doesn't present the information in a logical reading order. Your job is to rebuild that order and explain the change in it, to someone who does not know this codebase.

**No Critique:** Your job is NOT to review the code, it is purely to help the reader understand it. Explain a behaviour so the human can judge it themselves, then stop — no verdicts, no critique, no severity flags. Judging the code is the human's task, your job is to provide the context, details, explanations, edge cases, examples etc.

## Analysis Pipeline

1. Checkout, or pull PR stats, listing and metadata, so that you can be careful about accidentally reading a huge diff wholesale.
2. Read the PR description and the associated Jira ticket (if any).
3. Demote lockfiles, vendored deps, `dist/`, generated code, snapshots, formatting and license sweeps. Huge changesets, that are usually irrelevant to the goal of understanding the PR.
4. Define a table of contents
5. Write each chapter independently. Use sub-agents to do grunt-work, research and gather the needed information for each and explore its effects and dependencies.
6. Write a top-level introduction the the document.
7. As the last chapter, write any suggestions for how the reviewer can test the changes. What commands they may want to run, or UI actions they can take to replicate the issue.
8. Use a sub-agent to review and analyze the resulting document, with the goal to see if anything needs to be reordered or reworded in order to make the readability flow easier.
9. Spin up a sub agent to generate the "Hero Illustration".
10. Open the HTML file in the system default browser: `open /tmp/pr-story.html`.

### Introduction to the PR

This is possibly the most important step - reading the abstract is when the human's attention is at its sharpest, but their knowledge of the intent at the lowest. 

The description should start with an explanation of WHY this was done - what is the use case and the problem it solves. The description should assume a low-technical level of understanding, and focus on the problem, and the approach to the solution, calling out the details by name only where unavoidable. The description should focus on what this part of the system is and why the change exists, what is the intended behaviour before vs after.

1. The first paragraph should explain in two simple sentences, in non-technical terms, what the purpose of the task was, and where the boundaries of its scope are.
2. Then, create line items for large actions that were performed, grouping related changes together. For example:
   - Handlers were moved into a specific folder for better organization.
   - Error handlers were added to all APIs that were missing them, improving error handling across the board.
3. Finally, write down any additional details or exceptions where the implementation deviates from the original plan. This can include any challenges faced during development, any trade-offs made, or any future considerations that should be kept in mind when working with this code. This section can also include any relevant technical details that may be useful for reviewers or future developers who will work on this codebase.
4. If available, add relevant links, to Jira tickets, Figma designs, Chromatic or local Storybook pages, local or preview API docs url or any other relevant resources that provide context for the changes made in this PR. This helps reviewers understand the background and motivation behind the changes.
5. Inline any relevant hand-written SVG, ASCII diagrams, Figma frames or images that help reviewers visualize the change without running the code.

### Table of Contents

Draft a flow of chapters based on change intent groups, ordered to iteratively onboard the reader from top-down. A chapter is a tasteful contextual group, that helps the reviewer put themselves in the author's shoes and follow the thought process. One chapter per distinct purpose.

Chapters should be ordered by purpose, never by path or technical complexity. A chapter answers "what does this group of changes DO", not "what's in this directory". For example, The first chapter names the changes that anchor the entire PR's purpose and should be read first as an onboarding, whereas utility additions may come later in the document. Optimize for ease of onboarding and reading flow.

The size of the PR doesn't dictate how many chapters it has. Some huge PRs may be mechanical in nature and have just a single chapter, whereas others may touch upon multiple concepts and require multiple chapters. Optimize the chapter amount for storytelling and readability - not for size of the PR, and never do more than 7 chapters.

### Writing a Chapter

A chapter should intenrally focus on telling its own story. Each chapter has a title, that in less than 50 characters explains the intent/effect. And a description which starts non-technical and becomes more technical as it goes deeper into the details. It may also be useful to use HTML or SVG to make small illustrations or cards as a visual aid.

After the description of a chapter, you can provide a short quick and dirty list of biggest changes in this chapter, just 3-6 items as an overview of what they'll see below, such as:
- introduced the new `SearchOfferingContext` model
- Session TTL added to `validate()`
- Retry backoff capped at 30s
- `tenantId` threaded through 27 components

Finally, we jump into the details of the implementation. Here you thread paragraphs and code blocks together. The reader is technical - but do not assume knowledge of the codebase.

A chapter should be classified between simply mechanical or changes business logic. This is because logic change (such as Interface Changes) are where explanation matters the most to the reader. A mechanical chapter rarely needs the subsequent detailed deep dive, while business logic changes may need the user to understand why and how things are changed. Its up to your taste to decide what is relevant. Be conservative, nobody likes a useless wall of text that simply restates what the code does.

In this part, work out what the touched subsystem is — the thing a newcomer can't get from changed lines. Read the surrounding module, its entry points, a README, usages. Analyse and present the influence, dependencies and side effects changes have, and provide short examples in a table, where it helps tell the story.

**Ground rules:**
- Nothing is referenced before it's introduced. The reader never meets a symbol whose definition hasn't appeared yet.
- Why, not what. The diff already shows what changed. Prose is for intent, consequences, and relationships. Example: "Before this, a session stayed valid until the user logged out. This adds a 24h TTL so abandoned sessions can't be replayed. The TTL is measured from `createdAt` rather than `lastSeenAt`, so it fires 24h after sign-in whether or not the user is still active." Old behaviour, new behaviour, then the detail the diff can't show.
- Who uses it? Grep the changed symbols across the repo *outside* the diff: callers, dependents, config. This blast radius is what separates the page from a file listing, and it's what a newcomer most needs.
- Noise is demoted, the goal is to help understand the PR, not offer a definitive list.
- Use the project's own layered architecture language.
- Create hyperlinks to relevant files or concepts.
- Use hover-tooltips to quickly explain domain concepts in banal plain-language where needed.
- Within a chapter, dependency order — schema → types → logic → call sites → UI → config — with tests beside the code they cover, never batched at the end.
- Write prose the way you'd explain the change out loud: short sentences, plain words, the point of a paragraph in its first sentence, the project's own vocabulary. Name the actual value, call site or field instead of describing it in general terms.

### PR Hero Illustration

Every good blogpost starts with a custom made illustrated hero that exemplifies the soul of the blogpost. And so should a PR!

Each PR should have at least 1 serious hero visualization placed at the top, just below the introduction segment.

Use HTML, CSS or Canvas or SVG - with animations to produce it, ideally inline, but allowed to use CDN libraries. It should be a slide-sized, boundaried, contained, hero card, that visualizes the most important concept of the PR's intent. 

**Always Spin up a sub agent to do this work as a standalone change. A sub agent is an artist, a technology creative**

For example, in a pr that reorganizes code, you might wanna draw a symbolic directory tree before and after, where files are animated to move around. A PR that deals with utilities and math, you may wanna draw some items on a grid system, or an illustration of what the utility does. The illustrations can even be interactive where that makes sense. Be creative here!

## Rendering

Use the skill's own @assets/template.html as a baseline — it is a worked example of a finished page, so replace the content and keep the shapes. Delete any section you have nothing to put in.

We want a NEW, real HTML file, so don't publish it as an artifact. Write `pr-story-{title}.html` to a scratch location such as the system's tmp folder. The delivered file must reference nothing outside itself: no sibling assets, no image files, no separate stylesheet. Every SVG, diagram, style and script lives inside the HTML or a CDN.

The page has this shape, top to bottom. Keep the order; drop anything you can't fill, feel free to adapt to needs of a specific PR:

1. **Header** — title, a metadata line, and the 2-3 sentence blurb.
2. **What's in here** — the introduction described above, with its visual.
3. **Chapters**, with the outline beside them.
4. **Appendices** — Appendix accounting for the demoted noise + why each block/file is noise.

**Binary Images:** never let an image, or its base64, into your own context. Write a placeholder in the HTML and let one command swap the bytes in. Use `@@IMG:name@@` inside `src="…"` for raster images, and `@@SVG:name@@` standing alone where the element goes for SVG — that one is inlined as live markup, so it inherits the page's `--fg`/`--accent` colours.

Get every image onto disk first: a screenshot already is, a Figma frame comes from `download_assets`, a Jira or GitHub attachment needs `curl -sL "$url" -o /tmp/prs-login.png`. Downscale anything large first (fx gifsicle or `sips -Z 1400 shot.png --out shot-web.png`). Then one pass swaps them all:

```bash
python3 -c 'import base64,pathlib,re,subprocess,sys
f=pathlib.Path(sys.argv[1]); h=f.read_text()
for a in sys.argv[2:]:
    tag,src=a.split("=",1); p=pathlib.Path(src)
    if tag not in h: sys.exit("placeholder not in page: "+tag)
    m=subprocess.run(["file","-b","--mime-type",src],capture_output=True,text=True).stdout.strip()
    v=re.sub(r"^\s*<\?xml.*?\?>\s*","",p.read_text(),flags=re.S).strip() if m=="image/svg+xml" else "data:%s;base64,%s"%(m,base64.b64encode(p.read_bytes()).decode())
    h=h.replace(tag,v); print("inlined",tag,m,p.stat().st_size,"B")
f.write_text(h)' /tmp/pr-story.html \
  '@@IMG:login@@=/tmp/prs-login.png' '@@SVG:flow@@=/tmp/prs-flow.svg'
```

It prints one line per image and nothing else. Matching is literal, so `/` `+` `$` `\1` in the payload are harmless, and the MIME type comes from `file` rather than the filename, so an extension-less attachment still gets `data:image/png;base64,…`. A missing placeholder exits non-zero and writes nothing. Do not attempt this with `sed` or `perl -i` — the base64 has to travel as an argument, which blows past macOS's 1 MB `kern.argmax`.

The template offers some baseline utility hooks. Nothing is persisted — the page is stateless and every toggle resets on reload:

- `.chapter` + `id` — the chapter wrapper: scrollspy target, `:has()` host for the viewed state, and what the outline links to
- `.chapter-body` — everything below the chapter heading; this is what collapses
- `input[data-viewed]` — per-chapter checkbox. Pure CSS `:has()` collapses the body; JS only updates the counter, dims the outline entry, and bolds whichever chapter is on screen
- `.prs-outline` — outline links, looked up by `href="#id"`
- `#prsProgress`, `#prsViewedCount` — scroll bar and the "3 / 8 chapters viewed" counter
- `.diff` + `.ln` — every diff line is its own `<span class="ln add|del|ctx">` inside `<pre class="diff">`. The `<pre>` deliberately does not preserve newlines and each `.ln` re-enables `pre` itself; drop the wrapper and the whole block collapses onto one line. Prefix each line with the real `+`/`-`/space — the class only paints it. Each block sits in a bordered card whose header carries `path:headLine`.
- `.tip` — a `<span class="tip" title="…">` for a hover-tooltip on a domain term
- `#spPanel` — the scratchpad. The reader selects any text, types a note, and the panel collects it with ±150 characters of surrounding context; "Copy to AI" hands the lot to an agent as markdown. Nothing for you to fill in, but don't delete it.


### Other tips

- You are in charge of the codebase, you are allowed to switch branches or use git commands to do comparisons, or github commands to read stats and file lists.
- Detect moves so relocations don't read as rewrites — git's `-M`/`-C`, or compare the blocks on large delete+insert pairs. Report "moved, unchanged" or "moved, plus these edits", showing only the real edits.
- Anchor line numbers to the **head** revision so they match what the reader opens. The hunk header's second number (`@@ -40,7 +42,9 @@` → 42) is the head start line; count forward.
- **Chapter ids** — stable slugs from the chapter's purpose (`ch-session-expiry`), never its number, so a deep link a reader shares survives a regeneration.
- **Escaping** — all code content must be HTML-escaped (`&` `<` `>`). This is the most common rendering bug; do it systematically, not per-line by eye.