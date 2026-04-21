# context.md template

Use this structure when seeding `context.md` from a user's CV PDF on first run. Keep the field names and section order below — later runs of the skill read `context.md` and the consistent shape makes tailoring reliable.

`context.md` is a long-lived **raw capture** of the user, not a CV. It can be longer and more detailed than any single CV ever would be. That's the point — the tailoring step decides what to include per role.

## File skeleton

```markdown
This is <Name>'s CV context file. It contains their work experience and skills and should be used to generate a tailored CV.

# CV

## Basic Info
- Name:
- Email:
- Phone:
- LinkedIn:
- Address:
- (any other durable contact info, e.g. GitHub, personal site)

## Work Experience

<one Company block per employer, most recent first>

## Education
<one entry per degree: institution, degree, dates, any notable detail>

## Languages
<language — proficiency level>

## Career Motivation / Why <Industry or Theme>
<a short paragraph on what the user is trying to move toward, what drives them, and the story they want the CV to tell. This is where the CV's voice is anchored.>

### Why <Company> (for applications to <Company>)
<optional per-company motivation block. Add one whenever the user tells you their reason for applying to a specific company — it is gold dust for the cover-letter-ish opening summary.>

## Side Projects & Fun
<bullets or short paragraphs: personal projects, open source, hobbies that matter for the role.>
```

## Company block format

For each employer, use this shape. A single company may contain multiple **Role** blocks if the user was promoted or changed roles internally (very common for long tenures). Keep them in reverse-chronological order.

```markdown
Company: <name>
Started: <Month Year>
Ended: <Month Year>   # or "Still Employed"
Location: <city>

Role: <title>
Started: <Month Year>
Ended: <Month Year>   # omit if still in this role inside the current company
Info: <one paragraph — scope of the role, team size, what the work was about, who they worked with. This is the narrative summary the CV bullets will be distilled from.>
Tech environment: <one paragraph — tools, languages, infra. Critical for ATS keyword matches. Include proprietary stacks too, with a plain-English analogue.>
Responsibilities:
- <bullet>
- <bullet>
Accomplishments:
- <bullet with concrete outcome, metric, or scale signal>
- <bullet>
```

Notes on the fields:
- **Info** is the single most useful field — it's what lets the skill judge whether a role is relevant to a given JD. Err on the side of more detail.
- **Tech environment** separates tech from narrative so ATS keyword matching and technical fit checks have something clean to read.
- **Accomplishments** should be outcome-led (numbers, scale, business impact), not activity-led ("worked on X").
- If the PDF doesn't give you enough to fill a field, leave it empty rather than invent. The skill will ask the user follow-ups in Phase 4 and fill gaps then.

## For earlier / short roles

If the user has older roles from >10 years ago that the PDF only mentions briefly, keep them in the file but compact — `Company / Role / dates / one-line info` is fine. The CV's "earlier experience" section will lean on these.

## What not to put here

- Per-application state (dates applied, status, recruiter names)
- The tailored CVs themselves (those live as `<Company>_<Role>.html/.pdf` in the cwd)
- Transient notes about a specific job posting

context.md is durable truth about the user. Everything ephemeral belongs elsewhere.
