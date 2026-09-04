---
name: pr-story
description: Only use when user explicitly asks for /pr-story skill.
---
# PR Story

Turn a pull request, branch diff, problem space or any substantial changeset into a structured walkthrough. A story-driven onboarding/explainer HTML document to help with context-switching. This explains a changeset; it does not review or critique it. Use only when user explicitly asks for it.

GitHub's UI for reading a PR is bad. It displays changes in alphabetic order, broken down into commits, so a human reviewer needs to perform huge cognitive load to read the code out-of-order, in order to understand what was done and why - before they can begin to review side effects or architecture.

Your mission is to eliminate that cognitive load. Create a HTML page for the human to read, that presents the PR broken down into a sequence of easy to follow chapters.

This page is not a replacement for GitHub - it is an onboarding document the user reads separately first, before they go to do the actual review. This means that we do not have to show every single piece of code, our job is to tell a story with snippets and illustrations. A file that isn't part of the story simply doesn't appear on the page, we don't focus on exhaustiveness, but on the intent.

Analyze the changes, take into account the context and architecture, Jira ticket or Figma, api or package docs or other resources to learn more about the intent and splash zone of the PR.

## Tone of voice

In the GitHub PR UI, the reader is presented with a dry, alphabetic code dump. This is bad because it does not assist the human reader in seeing the zoomed-out wider perspective. It focuses on things that matter little - code style, syntax - but doesn't help explain the intended effect the PR has. It doesn't present the information in a logical reading order. Your job is to rebuild that order and explain the change in it, to someone who does not know this codebase.

This MUST NOT sound like a dry legal/technical document. It should explain conceptually what has changed, in a friendly way like a senior teaching a junior. The whole page is what the author would say walking you through the PR at a whiteboard. If they wouldn't say it out loud, it doesn't deserve to go in.

- Address the reader as "you" (fx. "you'll hit this again in chapter 3")
- Answer the questions a junior would actually ask out loud ("wait, why is this in the worker?").
- Always place an INSERT-FIGURE in the introduction chapter. A slide-sized, boundaried, contained card that visualizes the single most important concept of the PR's intent.
- Don't restate or announce things you'll say, just jump into the meat of it.
  ```
  bad:  "In this chapter we'll walk through how the validation logic was restructured."
  good: "The 2-character minimum was moved from the zod schema without any actual changes to the rule."
  ```

**No Critique:** Your job is NOT to review the code, it is purely to help the reader understand it. Explain a behaviour so the human can judge it themselves, then stop — no verdicts, no critique, no severity flags. Judging the code is the human's task, your job is to provide the context, details, explanations, edge cases, examples etc.

## Page Structure

1. Introduction, ~100 words, 1 hero figure
2. Explainer Chapters, ~150 words, 2 figures (the opening figure aimed at non-technical readers, like a PM)
3. Architecture Chapter, ~80 words, a large figure

Don't do more than 3 explainer chapters, most PRs don't deserve that much breakdown, and nobody will read that much text. Aim at 2 chapters and let the storytelling decide the count. This means you'll need to think about how to onboard the user gently, the problem space matters more than the amount of code or call-sites a chapter covers. Optimize for reading flow, not for symmetry with the diff.

We classify a chapter as business-logic if observable behavior changes. For example a user, a caller, UI, or an API sees something different afterwards. It takes more effort to explain those concepts, and these changes deserve our full attention. These chapters additionally deserve some before/after examples of the actual output or behavior, rather than code diff. Examples: a API response field changes, sample database row grid, prompts or payloads, URL changes etc.

Architecture chapter is a short paragraph that focuses on how the changes sit in our layered architecture. The figure should illustrate the breakdown and display what files/responsibilities/changes sit on which layer and which seam. This will help illustrate how the data flows through the application.

Pro tips:

- Act like a good technical writer would, and teach it gradually, like a story.
- The prose beside a code chunk or a figure must point at something specific inside it.
- Get inspired by the way skillshare, blogposts or good science communicators add illustrations to their explainers.

## Pipeline

### Step 1: Research

First, you do the research, gather all the information. Checkout, or pull PR stats, listing and metadata, so that you can be careful about accidentally reading a huge diff wholesale. Read the PR description and the associated Jira ticket and/or Figma (if any). Who uses it? Grep the changed symbols across the repo *outside* the diff: callers, dependents, config. Understanding this blast radius is what separates the page from a dumb file listing.

Be careful not to load the obviously irrelevant files like lockfiles, vendored deps, `dist/`, generated code, snapshots, formatting and license sweeps — they don't deserve a mention on the page.

If you legitimately need to actually analyse a large file, you may want to use jq or spin up a sub-agent to give you reports instead of reading the files yourself as that will pollute the context.

Reminder: your job is not to review, its only to compile knowledge about what the author wanted to achieve and why.

### Step 2: Write Prose

Time to write all the prose as a markdown file in the temporary folder or scratch location. That will be our baseline for the rest of the process. You'll need to decide how to tell the story, what chapters are needed, and all the prose for them, according to our rules above. Put your technical writer hat on, and optimize for lowering the cognitive load for the reader.

When done, do a quick, rough check of the chapter lengths, and resize them as needed.

**Pro tips:**

- Document title should state what problem we are solving (fx. "Double-clicking Next could skip a checkout step")
- Start with an abstract. That is when the human's attention is at its sharpest, but their knowledge of the intent at the lowest. It should contain the moral of the story, what was fixed, why, and how, from a non-technical perspective, with a believable example.
- After the abstract you can go a bit deeper, in 2 paragraphs, explain the zoomed out approach and list figma, jira, storybook, docs and other relevant links.
- Chapter titles should be simple, short and directly describe the problem. (fx. "Search request was triggered on every keystroke")
- Each chapter should start with a problem statement, and approach to solve it, before diving into the details.
- Chapter paragraphs, code and the figures should be interwoven.
- The reader is technical, but you should assume zero knowledge of this codebase.
- Why, not what. The diff already shows what changed. Prose is for intent, consequences, and relationships. (fx. "Before this, a session stayed valid until the user logged out. This adds a 24h TTL so abandoned sessions can't be replayed. The TTL is measured from `createdAt` rather than `lastSeenAt`, so it fires 24h after sign-in whether or not the user is still active.") Old behaviour, new behaviour, then the detail the diff can't show.
- Hover-tooltips explain business terms or domain terms in banal plain-language, using `[term]{tip: plain-words explanation}`.
- Don't forget to insert the correct amount of `INSERT-FIGURE` placeholders according to the rules, using `<!-- INSERT-FIGURE: alt text, what are we trying to portray -->`.
- Rewrite common signs of AI writing such as slop-filling, em dashes, or bad antithesis.
- When writing code blocks, add fences ````diff path=src/foo/bar.ts line=42`with real`+`/`-`/space prefixes on each line.

### Step 3: Artifact Design

Finally, we are ready to produce the actual HTML and all the figures in it. This must be a separate pass from the prose writing. You must load the artifact-design skill (via the Skill tool), and convert the markdown into HTML, while drawing illustrative figures in the labeled spaces.

You take the markdown file, and then digest that into a visual HTML onboarding guide using the artifact-design skill. Print out the output path to the user, and open the file in the system default browser so that the user can easily access it.

There is no need to run QA passes or validation sub agents on the document. It is an internal report.

**Figure Design**

We must rely on static figures to lower cognitive load, as humans are visual learners. Lowering cognitive load with visual aids is our north star metric. We do not want the figures to be overly detailed and boring however, be creative in the form of the drawing, but do not use outlandish methaphors, instead try to illustrate what the prose is explaining and what is changing, as a visual companion to the prose, like good educators do.

- Chapter paragraphs, code and the figures should be interwoven.
- A figure accompanies a specific piece of prose and shows the thing the prose  
is explaining. It myst always point at the concept from neighbouring paragraphs.
- One idea per figure. A figure that needs a legend is usually two figures.
- Draw the actual mechanism, not a metaphor. Boxes are real components, arrows  
are real calls or data.
- Aim for &gt;20 words of text inside a figure. Detail belongs in the prose, figures are for illustration purposes.

**Images (escape hatch).** 

Most stories carry no image — a drawn figure explains a mechanism much better than pixels do. But if the user asks for images, or provides them, or you decide they are crucial for understanding the PR (fx. a PR that changes the logo), you can add them in addition to figures using the `INSERT-IMAGE` construct. 16MB is the page ceiling — so downscale anything over ~3MB.

`INSERT-IMAGE` placeholders become `<figure><div class="fig-frame"><img src="@@IMG:/abs/path.png@@" alt="…" style="max-width:100%;display:block"></div><figcaption>…</figcaption></figure>`. The base64 must never pass through model context: after writing the HTML, run one script (bash/python) that finds every `@@IMG:…@@` token, base64-encodes that file, and splices a `data:image/{type};base64,…` URI into the page on disk — file to file. Verify with `grep -c '@@IMG:' page.html` printing 0.

**Code**

If a code block or diff fence is needed, display them as code cards with `path:line` in the card header, keeping the real `+`/`-`/space prefixes, added/removed lines tinted. Each code line is one `<span class="ln …">…</span>`; a blank line is an empty span (the shell gives it height, and newlines between spans are inert). Non-diff fences become command cards, the `caption=` as the card title. All code content HTML-escaped (`&` `<` `>`) — systematically, not per-line by eye; this is the most common rendering bug. `[term]{tip: …}` becomes `<span class="tip" title="…">term</span>`.

#### The page shell

The deliverable is the local file. If the user asks for a shareable link, publish the same file with the Artifact tool instead.

This is the page's design system — tokens, type and components are settled; the page-writer types content into them. Anything the shell doesn't cover (figure internals, a one-off layout) is styled in its spirit: same tokens, same restraint.

```html
[[ORCA_RICH_MD:faae59194dc83f78b5bb72b34829e22a:block-html:%3Cstyle%3E]]
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
</div>
<script>
@@READING-NOTES@@
</script>
</body>
```

The `@@READING-NOTES@@` needle is a special JavaScript injection you must perform after writing the HTML.

Replace it with `$HOME/.claude/skills/pr-story/reading-notes.js`. Use the cli script below, so the large file content never pollutes your context. Do not open the file, just ensure that `sed` points to your HTML file, and `sed` will inject it:
```bash
sed -i -e "/@@READING-NOTES@@/r $HOME/.claude/skills/pr-story/reading-notes.js" -e "/@@READING-NOTES@@/d" pr-artifacts/pr-story.html
```

