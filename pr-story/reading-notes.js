/**
 * Reading Notes — select text on any page, queue notes about it, copy them as AI prompts.
 *
 * Distributed by replacing the @@READING-NOTES@@ needle in the page template
 * with this whole file (see SKILL.md). Since it ends up inside an inline
 * <script>, it must stay free of a literal closing script tag.
 * When the user selects text,
 * a "?" bubble appears above the selection. Clicking it opens a panel (lower right)
 * with the queued notes list and a textarea. Each queued note stores the selected
 * text plus ±100 characters of surrounding context. Notes live in memory only.
 *
 * @example html.replace("@@READING-NOTES@@", readingNotesSource)
 */
(function () {
  const CONTEXT_RADIUS = 200;

  /** @type {{ note: string, selection: string, context: string }[]} */
  const notes = [];

  /** Selection captured at the moment the bubble is shown. */
  let pending = null;

  const host = document.createElement("div");
  const root = host.attachShadow({ mode: "open" });
  document.documentElement.appendChild(host);

  root.innerHTML = `
    <style>
      :host { all: initial; }
      * {
        box-sizing: border-box;
        --ground: #F1F4F3;
        --surface: #FFFFFF;
        --ink: #14201E;
        --muted: #5D6B68;
        --line: #D4DCD9;
        --line-strong: #A9B7B3;
        --accent: #0B6E6A;
        --accent-soft: #E0EDEB;
        --font-display: "Helvetica Neue", Helvetica, -apple-system, "Segoe UI", Arial, sans-serif;
        --font-mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
        font-family: var(--font-display);
      }

      .bubble {
        position: fixed;
        display: none;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        border: 1px solid var(--accent);
        background: var(--accent);
        color: #fff;
        font: 700 14px/26px var(--font-mono);
        text-align: center;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(20,32,30,.3);
        z-index: 2147483647;
      }
      .bubble:hover { background: #0A4A47; }

      .panel {
        position: fixed;
        right: 16px;
        bottom: 16px;
        display: none;
        flex-direction: column;
        width: 360px;
        max-height: 500px;
        background: var(--surface);
        color: var(--ink);
        border: 1px solid var(--line);
        border-radius: 10px;
        box-shadow: 0 16px 48px rgba(20,32,30,.18), 0 2px 8px rgba(20,32,30,.08);
        overflow: hidden;
        z-index: 2147483647;
      }
      .panel.open { display: flex; }

      .head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 16px 0;
        font: 700 14px var(--font-display);
        letter-spacing: -.01em;
      }
      .head .close {
        border: none;
        background: none;
        color: var(--muted);
        font-size: 14px;
        padding: 3px 6px;
        cursor: pointer;
      }
      .head .close:hover { color: var(--ink); }

      .tagline {
        padding: 4px 16px 14px;
        font: 12px/1.55 var(--font-display);
        color: var(--muted);
        border-bottom: 1px solid var(--line);
      }

      .copy-all {
        margin: 2px 16px 14px;
        padding: 7px;
        border: 1px solid var(--line-strong);
        border-radius: 5px;
        background: var(--surface);
        color: var(--accent);
        font: 600 12px var(--font-display);
        cursor: pointer;
      }
      .copy-all:hover { background: var(--accent-soft); border-color: var(--accent); }
      .copy-all:disabled { display: none; }

      .list {
        flex: 1;
        overflow-y: auto;
        min-height: 60px;
      }
      .list.blank {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 120px;
        background: var(--ground);
        box-shadow: inset 0 7px 9px -7px rgba(20,32,30,.22), inset 0 -7px 9px -7px rgba(20,32,30,.22);
      }
      .list .empty { font: 13.5px var(--font-display); color: var(--muted); }

      .item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 9px 16px;
        border-bottom: 1px solid var(--ground);
        font-size: 13px;
      }
      .item:last-child { border-bottom: none; }
      .item .num { font: 11px var(--font-mono); color: var(--line-strong); }
      .item .title {
        flex: 1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .item button {
        border: none;
        background: none;
        color: var(--muted);
        cursor: pointer;
        font: 700 9.5px var(--font-mono);
        text-transform: uppercase;
        letter-spacing: .06em;
        padding: 3px 2px;
      }
      .item button:hover { color: var(--accent); }

      .compose { padding: 12px 16px 16px; border-top: 1px solid var(--line); }
      .compose .quote {
        font: 11px/1.5 var(--font-mono);
        color: var(--muted);
        margin-bottom: 8px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .compose textarea {
        width: 100%;
        height: 68px;
        resize: none;
        border: 1px solid var(--line);
        border-radius: 5px;
        padding: 8px 10px;
        background: var(--ground);
        color: var(--ink);
        font: 13px/1.5 var(--font-display);
      }
      .compose textarea:focus { outline: none; border-color: var(--accent); background: var(--surface); }
      .compose .queue {
        margin-top: 8px;
        width: 100%;
        padding: 8px;
        border: none;
        border-radius: 5px;
        background: var(--accent);
        color: #fff;
        font: 600 12.5px var(--font-display);
        cursor: pointer;
      }
      .compose .queue:hover { background: #0A4A47; }
    </style>

    <button class="bubble" title="Add a note about this selection">?</button>

    <div class="panel">
      <div class="head">
        <span>Ask AI about this page</span>
        <button class="close" title="Close">✕</button>
      </div>
      <div class="tagline">Queue up questions while you read. When you're done, copy them all as one prompt and paste it into any AI chat.</div>
      <div class="list"></div>
      <button class="copy-all" disabled>Copy prompt for AI</button>
      <div class="compose">
        <div class="quote"></div>
        <textarea placeholder="What do you want to ask about the highlighted text?"></textarea>
        <button class="queue">Queue question&nbsp;&nbsp;⌘↩</button>
      </div>
    </div>
  `;

  const marker = window.Highlight && CSS.highlights ? new Highlight() : null;
  if (marker) {
    CSS.highlights.set("reading-notes", marker);
    const markStyle = document.createElement("style");
    markStyle.textContent = `::highlight(reading-notes) { background: #B8DAD6; }`;
    document.head.appendChild(markStyle);
  }

  /** Keeps the pending selection visibly highlighted on the page; pass null to clear. */
  function markSelection(range) {
    if (!marker) return;
    marker.clear();
    if (range) marker.add(range.cloneRange());
  }

  const bubble = root.querySelector(".bubble");
  const panel = root.querySelector(".panel");
  const list = root.querySelector(".list");
  const quote = root.querySelector(".quote");
  const textarea = root.querySelector("textarea");
  const copyAll = root.querySelector(".copy-all");

  /** Extracts the selection and ±CONTEXT_RADIUS chars around it from the nearest block. */
  function captureSelection() {
    const sel = window.getSelection();
    if (!sel || sel.isCollapsed || !sel.toString().trim()) return null;

    const range = sel.getRangeAt(0);

    const whole = range.cloneRange();
    whole.selectNodeContents(document.body);
    const full = whole.toString();

    const before = range.cloneRange();
    before.selectNodeContents(document.body);
    before.setEnd(range.startContainer, range.startOffset);
    const start = before.toString().length;

    const text = sel.toString();
    const context = full.slice(
      Math.max(0, start - CONTEXT_RADIUS),
      Math.min(full.length, start + text.length + CONTEXT_RADIUS)
    ).replace(/\s+/g, " ").trim();

    return { text, context, range, rect: range.getBoundingClientRect() };
  }

  function hideBubble() {
    bubble.style.display = "none";
  }

  function showBubble(rect) {
    bubble.style.display = "block";
    bubble.style.left = `${rect.left + rect.width / 2 - 14}px`;
    bubble.style.top = `${Math.max(4, rect.top - 36)}px`;
  }

  const SEPARATOR = "------------------------";
  const FOOTER = () =>
    `These are my comments, made on the document {${location.href}}. ` +
    `Can you please analyze my notes and help me challenge, spar, brainstorm and understand this better?`;

  /** Formats one note as a numbered question block (no separators). */
  function questionBlock(item, num) {
    return [
      `# Question ${num}`,
      `Selected text: "${item.selection.trim()}"`,
      "",
      `Surrounding context: "…${item.context}…"`,
      "",
      `My question: ${item.note}`,
    ].join("\n");
  }

  /** Wraps question blocks in separators and appends the global footer prompt. */
  function assemblePrompt(blocks) {
    return [SEPARATOR, blocks.join(`\n${SEPARATOR}\n`), SEPARATOR, "", FOOTER()].join("\n");
  }

  function copy(text) {
    navigator.clipboard?.writeText(text).catch(() => {
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      ta.remove();
    });
  }

  function render() {
    list.textContent = "";
    list.classList.toggle("blank", !notes.length);
    copyAll.disabled = !notes.length;
    copyAll.textContent = notes.length
      ? `Copy all ${notes.length} question${notes.length > 1 ? "s" : ""} as one AI prompt`
      : "Copy prompt for AI";
    if (!notes.length) {
      const empty = document.createElement("div");
      empty.className = "empty";
      empty.textContent = "Nothing queued yet…";
      list.appendChild(empty);
      return;
    }
    notes.forEach((item, i) => {
      const row = document.createElement("div");
      row.className = "item";

      const num = document.createElement("span");
      num.className = "num";
      num.textContent = String(i + 1).padStart(2, "0");

      const title = document.createElement("span");
      title.className = "title";
      title.textContent = item.note;
      title.title = questionBlock(item, i + 1);

      const copyBtn = document.createElement("button");
      copyBtn.textContent = "copy";
      copyBtn.title = "Copy just this question as an AI prompt";
      copyBtn.onclick = () => {
        copy(assemblePrompt([questionBlock(item, i + 1)]));
        copyBtn.textContent = "✓";
        setTimeout(() => { copyBtn.textContent = "copy"; }, 1200);
      };

      const editBtn = document.createElement("button");
      editBtn.textContent = "edit";
      editBtn.title = "Move back into the textarea for rewording";
      editBtn.onclick = () => {
        pending = { text: item.selection, context: item.context };
        textarea.value = item.note;
        notes.splice(i, 1);
        render();
        setQuote();
        markSelection(null);
        textarea.focus();
      };

      const delBtn = document.createElement("button");
      delBtn.textContent = "delete";
      delBtn.title = "Delete";
      delBtn.onclick = () => { notes.splice(i, 1); render(); };

      row.append(num, title, copyBtn, editBtn, delBtn);
      list.appendChild(row);
    });
  }

  function setQuote() {
    quote.textContent = pending
      ? `Asking about: "${pending.text}"`
      : "Nothing highlighted yet. Select some text on the page.";
  }

  function openPanel() {
    setQuote();
    markSelection(pending?.range ?? null);
    panel.classList.add("open");
    render();
    textarea.focus();
  }

  document.addEventListener("mouseup", (e) => {
    if (e.composedPath().includes(host)) return;
    setTimeout(() => {
      const captured = captureSelection();
      if (captured) {
        pending = captured;
        if (panel.classList.contains("open")) {
          setQuote();
          markSelection(captured.range);
        } else {
          showBubble(captured.rect);
        }
      } else {
        hideBubble();
      }
    }, 0);
  });

  document.addEventListener("scroll", hideBubble, true);

  bubble.addEventListener("mousedown", (e) => e.preventDefault());
  bubble.addEventListener("click", () => {
    hideBubble();
    openPanel();
  });

  root.querySelector(".close").addEventListener("click", () => {
    panel.classList.remove("open");
    markSelection(null);
  });

  copyAll.addEventListener("click", () => {
    if (!notes.length) return;
    copy(assemblePrompt(notes.map((item, i) => questionBlock(item, i + 1))));
    copyAll.textContent = "Copied ✓ Paste it into your AI chat";
    setTimeout(render, 1600);
  });

  function queueNote() {
    const note = textarea.value.trim();
    if (!note || !pending) return;
    notes.push({ note, selection: pending.text, context: pending.context });
    textarea.value = "";
    render();
    textarea.focus();
  }

  root.querySelector(".queue").addEventListener("click", queueNote);

  textarea.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      queueNote();
    }
  });
})();
