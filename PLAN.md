# Migration plan: Squarespace → Quarto + GitHub Pages

**Goal:** replace hansfredriksunde.com (Squarespace) with a static site on GitHub Pages, where adding a paper means editing one data file and pushing.

**Decisions made:** Quarto as the framework; publications kept in a YAML data file, rendered by an R chunk; public project repo `hafsunde/personal_website`, deployed by a GitHub Action; domain stays with its current registrar and DNS gets repointed.

**Status:** phases 1–4 are done. For phase 5, the repo exists and the deploy workflow is in place. The domain cutover and retiring Squarespace are still frozen.

Deferred work lives in `LONG_TERM_TODO.md` — nothing there is implemented without an explicit go-ahead.

---

## What the Squarespace site contains

Still live, and still serving the domain.

| Page | Content |
|---|---|
| Home | Bio (postdoc, Centre for Fertility and Health, FHI; PARMENT project), research focus, headshot, social links |
| Scientific Papers (`/scientific-papers`) | "Selected papers" (4) + full list: 2 preprints, 2026 (8), 2025 (4), 2024 (5), 2023 (2), 2022 (2) |
| CV | Direct link to `/s/HFS_AcadamicCV_june25.pdf` |
| Contact (`/contact`) | Points to the FHI employee page; BlueSky + Twitter. No email, no form |
| External | Google Scholar (`scholar.google.com/citations?user=obk155AAAAAJ`), ORCiD 0000-0001-8797-5422 |

Structure carried over: Home / Publications / CV / Contact, plus a blog section stubbed for later.

The Squarespace list is out of date. The verified list in `data/publications.yml` has 24 entries: 22 articles and 2 preprints. "The cost of caring" moved from an SSRN preprint to PNAS 2026, a new bioRxiv preprint was added, and "Intergenerational transmission of ADHD behaviors" moved from 2023 to 2024 under the issue-year rule.

---

## Architecture

```
personal_website/
├── _quarto.yml              # site config, nav, theme, render list
├── index.qmd                # landing: bio + selected papers
├── publications.qmd         # full list, generated from YAML at render time
├── cv.qmd                   # CV page + link to the PDF
├── contact.qmd
├── blog/
│   ├── index.qmd            # listing page (empty for now)
│   └── posts/
├── data/
│   └── publications.yml     # ← the only file touched when a paper lands
├── R/
│   └── publications.R       # renders the YAML for both pages
├── assets/
│   ├── cv.pdf
│   ├── headshot.jpg
│   └── styles.scss
├── .github/workflows/publish.yml
└── CNAME                    # not yet — added at the domain cutover
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

`publications.qmd` reads that file through `R/publications.R` and emits the grouped, year-ordered list; `index.qmd` reads the same file and emits only `selected: true`. Adding a paper is one YAML block and a push — both pages update, ordering and grouping handled automatically.

Rendering happens in `.github/workflows/publish.yml`, which sets up Quarto (pinned to 1.10.18), R, and the packages `knitr`, `rmarkdown` and `yaml`, then deploys with GitHub's Pages actions. Publishing never requires Quarto locally; a local install is for `quarto preview`.

---

## Phases

### Phase 1 — Content extraction and verification ✓
Pulled every page's text, the headshot, and the CV PDF off the live site.

Built `publications.yml` from the **Zotero library** via MCP, filtered to his own papers by author, with preprint/published duplicates collapsed and imported metadata normalised. Every DOI resolves; titles, authors and venues follow the publisher record, and the list was cross-checked for completeness against ORCID.

Zotero is an input, not a runtime dependency: the committed YAML is what the site reads, since the CI build has no access to the library.

### Phase 2 — Scaffold ✓
Quarto project with nav, pages, `.gitignore`, and the publications rendering logic.

### Phase 3 — Content and design ✓
Bio and contact text ported as-is; CV page added; SCSS theme with light and dark from one file.

### Phase 4 — Local review ✓
Rendered and checked every internal and external link, and reviewed the site in a browser.

### Phase 5 — Repo and Pages (in progress)
Done: public repo `hafsunde/personal_website`, pushed, deploy workflow added.
Remaining: set the Pages source to "GitHub Actions", then review the site at `hafsunde.github.io/personal_website/`.

### Phases 6–7 — Frozen
Domain cutover and retiring Squarespace, tracked in `LONG_TERM_TODO.md`.

---

## Open items

- Whether the CV should stay a PDF link only, or also get an HTML version (see `LONG_TERM_TODO.md`).
- Whether the old CV URL `/s/HFS_AcadamicCV_june25.pdf` needs to keep working after DNS moves (see `LONG_TERM_TODO.md`).
