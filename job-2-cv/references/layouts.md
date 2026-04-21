# Layout catalogue

Ten layout archetypes for two-page A4 CVs. Each is ATS-safe when the DOM order is sensible (summary → experience → education → skills, or sidebar-first-then-main). Use this file to:

1. Pick one layout per CV, based on the role, company culture, and career narrative.
2. Recommend it to the user in Phase 6 with one-line reasoning, then build the HTML using the listed CSS knobs.

All layouts share the print rules in `cv-rendering.md` (CSS @page, break control, two-page pattern, quality gates). The catalogue only varies the **visual structure**, not the rendering plumbing.

## How to pick

Match the layout to signal from the JD and company, not personal taste. Some guiding heuristics:

- **Regulated / traditional** (banks, law, big consultancies, public sector) → 1, 3, 8
- **Modern tech / product** (SaaS, fintech front-office, AI labs) → 4, 6, 9, 10
- **Creative-adjacent / design-led** (agencies, media, consumer brand) → 2, 5, 8
- **Dense-skills senior IC** (staff+ engineer, architect) → 6, 9
- **Career-story / long tenure** (director+, multi-company, leadership arc) → 7, 8
- **Brand-forward company with strong colour identity** → 4

If two fit, prefer the quieter one — ATS-safe and readable wins.

---

## 1. Classic Left Sidebar *(default — safe pick)*

Left rail holds Skills / Education / Languages. Main column holds Summary + Experience. Rail disappears on page 2; page 2 is full-width.

**When to use**: Most roles. Safe default when unsure.

**Sketch**
```
+------+--------------------------+
| NAME · subtitle · contact        |
+------+--------------------------+
|SKILLS| SUMMARY                   |
| ...  |                           |
|EDU   | EXPERIENCE                |
| ...  | flagship role...          |
|LANG  |                           |
+------+--------------------------+
  page 1 · grid 57mm | 1fr, gap 8mm
  page 2 · full-width single column
```

**Key CSS**
- `.page-one { display: grid; grid-template-columns: 57mm 1fr; gap: 8mm; }`
- `.page-two { break-before: page; /* full-width */ }`

---

## 2. Right Sidebar

Mirror of the classic. Rail on the right. Slightly less expected but still conservative.

**When to use**: Creative-adjacent corporate roles (brand, media, product design-led teams) where the reader eye lands on the experience first.

**Sketch**
```
+--------------------------+------+
| NAME · subtitle · contact        |
+--------------------------+------+
| SUMMARY                  |SKILLS|
|                          | ...  |
| EXPERIENCE               |EDU   |
|                          |LANG  |
+--------------------------+------+
```

**Key CSS**
- `.page-one { display: grid; grid-template-columns: 1fr 57mm; gap: 8mm; }`
- Swap the DOM order: `<main>` first, `<aside>` second.

---

## 3. Single Column Traditional

No sidebar at all. Strict linear flow: header, summary, experience, education, skills. Very conservative.

**When to use**: Law, legacy banking, public-sector, senior government-adjacent. Also when the user has a very long career and needs every mm for narrative bullets.

**Sketch**
```
+---------------------------------+
| NAME · subtitle                  |
| contact                          |
+---------------------------------+
| SUMMARY                          |
| EXPERIENCE                       |
|   role 1 ...                     |
|   role 2 ...                     |
| EDUCATION                        |
| SKILLS                           |
+---------------------------------+
```

**Key CSS**
- No grid. `main { max-width: 100%; }`
- Skills rendered as inline chips (`display: inline-block`) or compact 2-column list using `columns: 2` *inside* the Skills section only (NOT across whole page — ATS gets confused).

---

## 4. Header Band

Full-width coloured header strip (paper-coloured band with brand colour background) holds Name + Title + Contact. Body below is single column or narrow sidebar.

**When to use**: Company has a strong brand colour and the role is corporate/identity-heavy (marketing ops, partnerships at a brand-forward company, product at a design-led company).

**Sketch**
```
+=================================+
| ██ NAME · subtitle              |   ← solid brand band, white text
| ██ contact line                 |
+=================================+
| SUMMARY                          |
| EXPERIENCE                       |
| ...                              |
+---------------------------------+
```

**Key CSS**
- Header block: `background: var(--accent); color: #fff; padding: 10mm 13mm; margin: -11mm -13mm 5mm -13mm;` (negative margins so the band bleeds edge-to-edge against the `@page` margin).
- Body section uses single-column or classic left-sidebar underneath.
- Coloured band requires the **coloured-background print rules** in `cv-rendering.md` section 5. Do not skip those rules.

---

## 5. Two-Column Balanced (50/50)

Equal columns. Left column: summary + earlier/compact roles. Right column: flagship role + current role. Both columns live on page 1; page 2 is full-width as usual.

**When to use**: Candidates with many roles but nothing individually long-winded. Good for consultancy-style CVs (multiple short projects).

**Sketch**
```
+-------------+-------------------+
| NAME · subtitle · contact        |
+-------------+-------------------+
| SUMMARY     | EXPERIENCE         |
|             |  flagship role...  |
| SKILLS      |                    |
| EDU         |                    |
+-------------+-------------------+
```

**Key CSS**
- `.page-one { display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; }`
- Risk: ATS can mis-order the reading. Mitigate by putting the main column *first* in the DOM and using `order: 2` only visually.

---

## 6. Top Skill Bar

Skills rendered as a horizontal tag/chip strip directly under the header, then single-column body. Puts technical keywords right at the top for ATS and skim-reading.

**When to use**: Senior IC roles in tech (staff eng, architect, SRE). Any role where the keyword list matters more than narrative.

**Sketch**
```
+---------------------------------+
| NAME · subtitle · contact        |
+---------------------------------+
| [ GCP ] [ Agile ] [ API ] [...]  |   ← inline chips, accent border
+---------------------------------+
| SUMMARY                          |
| EXPERIENCE                       |
| EDUCATION                        |
+---------------------------------+
```

**Key CSS**
- Skills block: `display: flex; flex-wrap: wrap; gap: 1.5mm;`
- Chip: `border: 1px solid var(--rule); border-radius: 3mm; padding: 0.6mm 2.2mm; font-size: 8.5pt;`

---

## 7. Timeline Dates

Each role has a fixed-width date "rail" on the left (e.g., "Jun 2025 — Present" aligned), with role title and body flowing to the right. Dates act as a visual spine.

**When to use**: Leadership / director+ CVs where the *arc* of the career matters. Emphasises tenure and progression.

**Sketch**
```
+---------------------------------+
| NAME · subtitle                  |
+---------------------------------+
| SUMMARY                          |
+---------------------------------+
| 2025-now | Role · Company        |
|          |   bullets...          |
| 2022-25  | Role · Company        |
|          |   bullets...          |
+---------------------------------+
```

**Key CSS**
- Each role: `display: grid; grid-template-columns: 24mm 1fr; column-gap: 5mm;`
- Date column: `font-variant-numeric: tabular-nums; color: var(--ink-muted); font-size: 9pt;`
- ATS caveat: keep the date as real text in the flow (not absolutely positioned).

---

## 8. Editorial / Serif Heritage

Display serif headings (Fraunces / Crimson Pro / EB Garamond), minimal colour (usually just a hairline rule), tight typography. Reads like a New Yorker profile.

**When to use**: Consultancy, senior advisory, writer/editor-adjacent roles, academic-adjacent. Any role where the reader values *restraint*.

**Sketch**
```
+---------------------------------+
| Amir Harel                       |   ← serif, large
| subtitle in italic               |
| --------                         |   ← single hairline rule
| contact                          |
+---------------------------------+
| SUMMARY (sans body)              |
| EXPERIENCE                       |
|   Role title (serif)             |
|     Company · date (sans small)  |
|     body...                      |
+---------------------------------+
```

**Key CSS**
- Headings: `font-family: 'Fraunces', Georgia, serif; font-weight: 500;`
- Body: `font-family: 'Inter', sans-serif;`
- Accent: a single horizontal rule under the name; otherwise no colour.

---

## 9. Compact Monospace

Dense information, mono accent for metadata (dates, locations, tech tags), clean sans for body. Very high information-per-mm ratio.

**When to use**: Senior tech IC where *fitting it all* is the design challenge. Good for CVs with long tech stacks and many projects.

**Sketch**
```
+---------------------------------+
| Amir Harel                       |
| harel.amir1@gmail.com · mobile   |
+---------------------------------+
| role ················ 2025-now   |   ← mono aligns dates
| company, city                    |
|   · bullet ...                   |
|   · bullet ...                   |
+---------------------------------+
```

**Key CSS**
- Metadata: `font-family: 'JetBrains Mono', 'IBM Plex Mono', monospace; font-size: 9pt;`
- Body: `font-family: 'Inter', sans-serif; font-size: 9.5pt;`
- No accent colour, or a very muted one on section rules only.

---

## 10. Card Stack

Each role in a subtly bordered card with interior padding. Clean SaaS/modern product aesthetic.

**When to use**: Modern tech company (AI labs, startups, product-led SaaS). The role has a contemporary, design-aware culture signal.

**Sketch**
```
+---------------------------------+
| NAME · subtitle · contact        |
+---------------------------------+
| SUMMARY (no card)                |
| +-----------------------------+  |
| | Role · Company · date       |  |
| | body + bullets              |  |
| +-----------------------------+  |
| +-----------------------------+  |
| | Next role...                |  |
| +-----------------------------+  |
+---------------------------------+
```

**Key CSS**
- `.role { border: 1px solid var(--rule); border-radius: 3mm; padding: 4mm 5mm; margin-bottom: 3mm; }`
- `break-inside: avoid` is critical on cards — a card split across pages looks broken.
- Keep borders hairline (1px / 0.25mm) so they don't dominate.

---

## Implementation notes

- Don't mix archetypes. Pick one and commit.
- The two-page quality gates in `cv-rendering.md` apply to every archetype — verify each render.
- If a layout fights the content (e.g. 2-column balanced with only 2 roles and a huge summary), fall back to Classic. The layout should serve the content.
- Card stack, timeline and 2-column 50/50 are the most likely to fail ATS if DOM order is wrong. Always put main content before secondary content in the HTML, regardless of visual order.
