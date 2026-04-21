# CV rendering: CSS print rules, layout, and quality gates

Read this file before writing or editing HTML. It's long — if you're only touching one area (e.g., fixing a coloured-background bleed), jump to the relevant section. The final section (**Quality gates**) is the checklist you MUST pass before telling the user the CV is done.

## Table of contents

1. Running the renderer
2. Reading the output
3. Iteration loop
4. CSS print rules — white background
5. CSS print rules — coloured / tinted background
6. Break control
7. Layout pattern: two-page CV with sidebar
8. Compact formats for fitting page 2
9. Gotchas
10. Quality gates

---

## 1. Running the renderer

```bash
.venv/bin/python <skill-dir>/scripts/render.py <Company>_<Role>.html
# produces <Company>_<Role>.pdf next to the HTML
```

`render.py` launches headless Chromium (cached at `~/Library/Caches/ms-playwright/`), loads the HTML as `file://`, waits for fonts and network idle, emulates `@media print`, and writes an A4 PDF respecting `@page` rules via `prefer_css_page_size=True`.

If `.venv/` is missing or `import playwright` fails, run `bash <skill-dir>/scripts/setup.sh` from the cwd. Do NOT `pip install` globally — Homebrew Python 3.12 blocks that (PEP 668).

To programmatically confirm page count:

```bash
.venv/bin/python -c "
from playwright.sync_api import sync_playwright; import pathlib
with sync_playwright() as p:
    b=p.chromium.launch(); page=b.new_context().new_page()
    page.goto(pathlib.Path('<file>.html').resolve().as_uri(), wait_until='networkidle')
    page.emulate_media(media='print')
    pdf=page.pdf(format='A4', print_background=True, prefer_css_page_size=True)
    b.close()
print(pdf.count(b'/Type /Page') - pdf.count(b'/Type /Pages'))
"
```

## 2. Reading the output

Use the Read tool on the generated PDF. It renders each page at ~900px wide — high enough fidelity to judge layout, page breaks, whitespace balance, font rendering, and content fit. This is how you "see" the CV.

## 3. Iteration loop (mandatory before reporting "done")

1. Write/edit HTML
2. Run the renderer
3. Read the PDF
4. Check every quality gate (section 10)
5. If any gate fails, edit HTML and return to step 2
6. Only after all gates pass, tell the user the CV is ready

## 4. CSS print rules — white background

```css
@page {
  size: A4;
  margin: 11mm 13mm;
}

@media print {
  html, body { background: #ffffff; }
  .sheet {
    box-shadow: none;
    margin: 0;
    padding: 0;
    max-width: none;
  }
  .no-print { display: none; }
}
```

## 5. CSS print rules — coloured / tinted background

**Do not** use the white-background pattern above if the paper colour is anything other than pure white (cream, warm tint, dark mode, etc.). Chrome does not paint the `body`/`html` background into the `@page` margin area, so you will get a white strip around every page.

Use this instead — collapse the `@page` margin to zero and move the spacing into `.sheet` padding, with explicit top padding on each `.page-N` section so pages 2+ still have a visual top margin:

```css
:root {
  --paper: #F7F3EC;  /* your tinted paper colour */
}

@page {
  size: A4;
  margin: 0;
}

@media print {
  html, body {
    background: var(--paper);
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .sheet {
    background: var(--paper);
    box-shadow: none;
    margin: 0;
    padding: 11mm 13mm;  /* visual margins on page 1 + horizontal on every page */
    max-width: none;
  }
  .page-two {
    padding-top: 11mm;   /* sheet's top padding only paints on page 1; each new .page-N needs its own top padding */
  }
  .no-print { display: none; }
}
```

**Why it works:** `.sheet` padding applies at the element's own edges only. Horizontal padding carries to every page, but vertical padding only paints at the very top (page 1) and very bottom (last page). Every `.page-N` wrapper triggered via `break-before: page` must re-assert its own `padding-top` to re-create the visual top margin. If you add a third page, add `padding-top: 11mm` to `.page-three` too.

**Verify by reading the PDF.** If you see any white strip on the sides, top, or bottom, the background is not bleeding and you missed one of the rules above.

## 6. Break control

```css
/* Keep each role/item/project on a single page */
.role, .earlier-item, .project-inline {
  break-inside: avoid;
  page-break-inside: avoid;
}

/* Don't orphan section headings */
h2, h3 {
  break-after: avoid;
  page-break-after: avoid;
}

/* Force page break between page-one and page-two */
.page-two {
  break-before: page;
  page-break-before: always;
}

/* Prevent single-line widows/orphans */
p, li { orphans: 2; widows: 2; }
```

## 7. Layout pattern: two-page CV with sidebar

**Do not** wrap all content in a single CSS Grid. When content overflows page 1, the grid's short column (usually the sidebar) becomes a visible empty column on pages 2+. This is the #1 mistake in multi-page CV layouts.

**Do** split the document into two discrete sections, with the page break forced between them:

```html
<div class="sheet">
  <header class="top">name, subtitle, contact</header>

  <section class="page-one">
    <aside class="rail">skills, education</aside>
    <main class="main">summary + flagship role (in full detail)</main>
  </section>

  <section class="page-two">
    <!-- break-before: page forces this onto page 2 -->
    remaining roles, earlier experience (compact), side projects
  </section>
</div>
```

- `.page-one` uses `display: grid; grid-template-columns: 57mm 1fr; gap: 8mm;` for the rail + main split.
- `.page-two` is full-width single-column. `break-before: page` forces it to a new page.
- Content split rule of thumb: page 1 = header + rail + summary + the single most important (usually most recent) role with all its bullets. Page 2 = everything else.

## 8. Compact formats for fitting page 2

When page 2 is tight, these formats save vertical space without looking crammed:

**Earlier experience (compact 2-line format):**

```html
<div class="earlier-item">
  <div class="eh-line"><strong>Role Title</strong> · Company, City · <span class="eh-date">2015 – 2019</span></div>
  <div class="eh-body">One-paragraph description with concrete outcomes.</div>
</div>
```

**Side projects (single-paragraph inline format):**

```html
<p class="project-inline"><strong>ProjectName</strong> &mdash; one-paragraph description mentioning the tech stack and the outcome.</p>
```

These are much more compact than the full role format (separate title / company / date / description / bullets blocks). Use them for any entry that doesn't need bullets.

## 9. Gotchas

- **`break-inside: avoid` on short blocks can backfire.** If a 3-line block has this rule and doesn't fit the remaining space, Chrome pushes the whole block to the next page even when only ~5mm of whitespace would have been needed. If you see a short section alone at the top of a new page, the fix is to shrink content elsewhere on the earlier page (or compact the block itself), NOT to remove `break-inside: avoid` — removing it causes ugly mid-block breaks where the title lands on one page and the body on the next.
- **Accent color on company/location lines reads as a hyperlink** in the final PDF. Keep the accent color for section headers and the top rule only. Everything else stays in charcoal tones (`#202124` / `#3c4043` / `#5f6368`).
- **Google Fonts require network on first render.** `render.py` handles this via `wait_until="networkidle"`. Don't switch the renderer to offline mode without preloading or base64-embedding the font.
- **ATS parseability**: use real text (no images for text), semantic `h1`/`h2`/`ul`/`li`, standard section names ("Experience", "Education", "Skills"). The two-column layout is ATS-safe as long as the DOM order is logical (rail content first or main content first, both valid) and nothing is in a background image.
- **Avoid CSS columns (`column-count`)** for multi-column layouts — ATS parsers can misread the reading order. Use CSS Grid or Flexbox instead.
- **Coloured paper = white strips unless you change `@page`.** If the CV background is anything other than pure white, the default `@page { margin: 11mm 13mm }` pattern leaves an unpainted white border around every page. See section 5 for the fix.

## 10. Quality gates

Before telling the user the CV is ready, **all** of these must be true:

- **Page count is exactly 2** (never 1, never 3+). Verify by reading the PDF.
- **No orphan page**: no page holding less than ~30% content. A page 2 that's 90% empty or a page 3 with a single paragraph is a fail.
- **Page 1 ends cleanly**: last rendered line is the end of a complete thought (ideally a bolded outcome, not mid-sentence or mid-bullet).
- **No empty sidebar on page 2+**: if the design uses a rail/sidebar, it must NOT leave a visible empty left column on later pages.
- **Role blocks don't split**: a single role's title + description + bullets stays on one page.
- **Section headings don't orphan**: a heading is never the last thing on a page while its content is on the next.
- **Company/location lines are not accent-colored**: the small line under a role title (e.g. "Meta · London") must be soft charcoal, not blue. Blue reads as a hyperlink in PDF and looks wrong.
- **Coloured backgrounds bleed to the page edges**: if the paper colour is anything other than pure white, there must be no visible white strip on any edge of any page. If there is, revisit section 5.
- **The CV renders in < 3 seconds and the PDF is < 500KB**. If much larger, something went wrong (embedded images, accidentally included raster content).
