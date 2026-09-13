# personal_website

Source for Hans Fredrik Sunde's academic site, replacing a Squarespace site currently served at hansfredriksunde.com.

Read `PLAN.md` before starting work. Deferred work is in `LONG_TERM_TODO.md`.

## Stack

Quarto static site, destined for GitHub Pages. Rendering will happen in a GitHub Action, so a local Quarto install is for `quarto preview` only, not a publishing dependency.

## Hard rules

Phases 5–7 of the plan are **frozen** and require an explicit go-ahead from Hans Fredrik. Without one, do not:

- create a GitHub repo, add a remote, or push
- enable GitHub Pages or add a deploy workflow
- change DNS, add a `CNAME` file, or touch anything at the registrar
- cancel or modify the Squarespace site

Local commits are fine. The live site stays on Squarespace until the new one is reviewed and approved.

## Publications

`data/publications.yml` is the single source of truth **for the site**. `publications.qmd` and the selected-papers block on `index.qmd` both generate from it at render time — never hand-edit a publication list into a `.qmd`. Adding a paper should be one YAML entry and nothing else.

Entry shape:

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

Grouping (preprints first, then years descending) and ordering are computed, not stored.

### Zotero

A Zotero MCP server is available and Hans Fredrik's library contains his papers. Use it as the **input** for building and updating `data/publications.yml` — it beats retyping metadata off a web page.

Zotero is not a build-time dependency. The GitHub Action that renders the site has no access to it, so the generated YAML is committed and is what the site reads. Never make a page query Zotero directly.

Working with the library:

- His own papers are a subset of the library — filter by author rather than exporting everything, and confirm with him which collection or saved search to treat as authoritative if one exists.
- Watch for the **preprint/published duplicate**: the same paper often exists twice, once as an OSF or SSRN preprint and once as the journal version. Only genuinely unpublished work should end up as `type: preprint`. When both exist, keep the published version and drop the preprint entry.
- Zotero metadata is often imported rather than curated, so expect title-case inconsistency, missing DOIs, "Advance online publication" venues, and author name variants. Normalise these on the way into the YAML.
- `selected: true` and the `links:` block are editorial, not bibliographic. They don't come from Zotero — preserve whatever is already in the YAML when regenerating, and ask before changing which papers are featured.

For maintenance later: adding a new paper should be "pull it from Zotero, append the entry, push" — not a manual transcription.

## Accuracy

Bibliographic metadata must be verified, not transcribed from memory or from a rendered page. Every DOI must resolve, and author strings and venues should be checked against Zotero, ORCID `0000-0001-8797-5422`, or the publisher record. Where Zotero and the old Squarespace list disagree, resolve the DOI and use the publisher record — don't silently prefer one source. An unverifiable entry stays out of the file rather than going in provisionally; flag it instead.

## Conventions

- `_site/` and `.quarto/` are build output — gitignored, never committed.
- Assets (headshot, CV PDF, SCSS) live in `assets/`.
- Styling goes in `assets/styles.scss` as theme variables and rules, not inline HTML or per-page CSS blocks.
- The blog under `blog/` is a scaffolded listing page with no posts yet. Leave it empty unless asked.
- Prose on the site is Hans Fredrik's own voice — port existing text as-is rather than rewriting it, and flag anything that reads as stale instead of silently updating it.

## Open questions

Don't guess at these; ask.

- GitHub username, and whether the repo should be `<username>.github.io` or a project repo.
- Which Zotero collection or saved search holds his own publications, if there is one.
- Whether the contact page gets an email address or keeps pointing at the FHI employee page.
- The Google Scholar profile URL (not yet captured).
