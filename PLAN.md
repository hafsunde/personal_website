# Migration plan: Squarespace → Quarto + GitHub Pages

**Goal:** replace hansfredriksunde.com (Squarespace) with a static site on GitHub Pages, where adding a paper means editing one data file and pushing.

**Decisions made:** Quarto as the framework; publications kept in a YAML data file; domain stays with its current registrar and DNS gets repointed; phase 1 stops at a working local site, before anything is pushed.

Deferred work lives in `LONG_TERM_TODO.md` — nothing there is implemented without an explicit go-ahead.

---

## What the current site contains

| Page | Content |
|---|---|
| Home | Bio (postdoc, Centre for Fertility and Health, FHI; PARMENT project), research focus, headshot, social links |
| Scientific Papers | "Selected papers" (4) + full list: 2 preprints, 2026 (8), 2025 (4), 2024 (5), 2023 (2), 2022 (2) |
| CV | Direct link to `HFS_AcadamicCV_june25.pdf` |
| Contact | Points to the FHI employee page; BlueSky + Twitter. No email, no form |
| External | Google Scholar, ORCiD 0000-0001-8797-5422 |

Structure to carry over: Home / Publications / CV / Contact, plus a blog section stubbed for later.

---

## Target architecture

```
personal_website/
├── _quarto.yml              # site config, nav, theme
├── index.qmd                # landing: bio + selected papers
├── publications.qmd         # full list, generated from YAML at render time
├── cv.qmd                   # CV page + link to the PDF
├── contact.qmd
├── blog/
│   ├── index.qmd            # listing page (empty for now)
│   └── posts/
├── data/
│   └── publications.yml     # ← the only file touched when a paper lands
├── assets/
│   ├── cv.pdf
│   ├── headshot.jpg
│   └── styles.scss
├── .github/workflows/publish.yml
└── CNAME
```

One entry in `data/publications.yml`:

```yaml
- id: sunde2025indirect
  authors: ["Sunde, H.F.", "Eilertsen, E.M.", "Torvik, F.A."]
  title: "Understanding indirect assortative mating and its intergenerational consequences for educational attainment"
  venue: "Nature Communications"
  year: 2025
  doi: "10.1038/s41467-025-60483-0"
  type: article          # article | preprint
  selected: true
  links:
    bluesky: "https://..."
```

`publications.qmd` reads that file in a code chunk and emits the grouped, year-ordered list; `index.qmd` reads the same file and emits only `selected: true`. Adding a paper is one YAML block and a push — both pages update, ordering and grouping handled automatically.

Rendering happens in a GitHub Action (`quarto-actions/setup` + `render` + deploy), so publishing never requires Quarto to be installed locally. Installing it locally is still worth doing for `quarto preview`.

---

## Active phases

### Phase 1 — Content extraction and verification
Pull every page's text, the headshot, and the CV PDF off the live site.

Build `publications.yml` from the **Zotero library** via MCP rather than transcribing the rendered Squarespace page — the page reading is a cross-check, not a source. Filter to his own papers, collapse preprint/published duplicates, normalise imported metadata, and **verify each DOI resolves**. Where Zotero and the old site disagree, resolve the DOI and follow the publisher record. Roughly 23 items are expected, including 2 genuine preprints.

Zotero is an input, not a runtime dependency: the committed YAML is what the site reads, since the CI build has no access to the library.

### Phase 2 — Scaffold
Create the Quarto project, with nav, page stubs, `.gitignore`, and the publications rendering logic. Initialise git locally; nothing pushed.

### Phase 3 — Content and design
Port the bio and contact text; add the CV page; write the SCSS theme (typography, spacing, responsive layout, light/dark). Not a copy of the Squarespace design — a cleaner academic layout.

### Phase 4 — Local review
Render, check every internal and external link, confirm the CV and headshot load, review in a browser. **Gate: nothing is pushed until this is signed off.**

### Phases 5–7 — Deferred
GitHub repo and Pages setup, domain cutover, and retiring Squarespace are all parked in `LONG_TERM_TODO.md`.

---

## Open items

- GitHub username / whether the repo should be `<username>.github.io` or a project repo.
- Which Zotero collection or saved search holds his own publications, if there is one.
- Whether the CV should stay a PDF link only, or also get an HTML version (see `LONG_TERM_TODO.md`).
- Whether to add an email address to the contact page or keep pointing at the FHI employee page.
- Google Scholar profile URL (needs to be read off the live nav — it wasn't captured in the page text).
