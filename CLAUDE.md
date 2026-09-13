# personal_website

Source for Hans Fredrik Sunde's academic site, replacing a Squarespace site currently served at hansfredriksunde.com.

Read `PLAN.md` before starting work. Deferred work is in `LONG_TERM_TODO.md`.

## Stack

Quarto static site on GitHub Pages. The repo is public at `github.com/hafsunde/personal_website` (a project repo, remote `origin`).

Rendering happens in `.github/workflows/publish.yml` on every push to `main`, so a local Quarto install is for `quarto preview` only, not a publishing dependency. Pages use the knitr engine: `R/publications.R` generates the publication lists, so the build needs R with `knitr`, `rmarkdown` and `yaml`. Quarto is pinned to 1.10.18 in the workflow; bump it there and locally together.

## Hard rules

Pushing to `main` publishes the site (once Pages is enabled). Treat a push as publishing: don't push unless asked.

The domain cutover and Squarespace retirement are **frozen** and require an explicit go-ahead from Hans Fredrik. Without one, do not:

- change DNS, add a `CNAME` file, set a custom domain, or touch anything at the registrar
- cancel or modify the Squarespace site

The live site stays on Squarespace until the new one is reviewed at the `github.io` URL and approved.

## Publications

`data/publications.yml` is the single source of truth **for the site**. `publications.qmd` and the selected-papers block on `index.qmd` both generate from it at render time via `R/publications.R` — never hand-edit a publication list into a `.qmd`. Adding a paper should be one YAML entry and nothing else.

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

For very large collaborations, list only the first author and add `et_al: true`.

`year` is the issue year of the version of record, falling back to the online date when there is no issue. This matches ORCID; don't use the online-first year.

Grouping (preprints first, then years descending) and ordering are computed, not stored.

### Zotero

A Zotero MCP server is available and Hans Fredrik's library contains his papers. Use it as the **input** for building and updating `data/publications.yml` — it beats retyping metadata off a web page.

Zotero is not a build-time dependency. The GitHub Action that renders the site has no access to it, so the generated YAML is committed and is what the site reads. Never make a page query Zotero directly.

Working with the library:

- His own papers are a subset of the library, and there is no collection or saved search holding them — filter by author (`Sunde, Hans Fredrik`). Author substring search also matches unrelated `Sundet` / `Sundelin` entries, so check the full name.
- Watch for the **preprint/published duplicate**: the same paper often exists twice, once as an OSF, SSRN or medRxiv preprint and once as the journal version. Only genuinely unpublished work should end up as `type: preprint`. When both exist, keep the published version and drop the preprint entry. Recheck existing preprints too — they get published.
- Zotero can lag behind ORCID; cross-check ORCID for papers missing from the library.
- Zotero metadata is often imported rather than curated, so expect title-case inconsistency, missing DOIs, "Advance online publication" venues, and author name variants. Normalise these on the way into the YAML.
- `selected: true` and the `links:` block are editorial, not bibliographic. They don't come from Zotero — preserve whatever is already in the YAML when regenerating, and ask before changing which papers are featured.

For maintenance later: adding a new paper should be "pull it from Zotero, append the entry, push" — not a manual transcription.

## Accuracy

Bibliographic metadata must be verified, not transcribed from memory or from a rendered page. Every DOI must resolve, and author strings and venues should be checked against Zotero, ORCID `0000-0001-8797-5422`, or the publisher record. Where Zotero and the old Squarespace list disagree, resolve the DOI and use the publisher record — don't silently prefer one source. An unverifiable entry stays out of the file rather than going in provisionally; flag it instead.

Some publishers (Wiley, PNAS) return 403 to scripted HTML requests. Check DOIs with content negotiation (`Accept: application/vnd.citationstyles.csl+json` against `https://doi.org/<doi>`), not by loading the landing page.

## Conventions

- `_site/` and `.quarto/` are build output — gitignored, never committed.
- Assets (headshot, CV PDF, SCSS) live in `assets/`.
- Styling goes in `assets/styles.scss` as theme variables and rules, not inline HTML or per-page CSS blocks. The same file feeds both the light (cosmo) and dark (darkly) themes; dark overrides sit under `body.quarto-dark`.
- `_quarto.yml` has an explicit `render:` list so the planning docs at the repo root stay out of the site. New top-level pages must match it (`*.qmd`, `blog/*.qmd`).
- The blog under `blog/` is a scaffolded listing page with no posts yet. Leave it empty unless asked. The render warning that the listing matches no files is expected until the first post.
- Prose on the site is Hans Fredrik's own voice — port existing text as-is rather than rewriting it, and flag anything that reads as stale instead of silently updating it.
- The contact page keeps pointing at the FHI employee page; no email address on the site.

## Open questions

Don't guess at these; ask.

- Whether the CV should stay a PDF link only, or also get an HTML version (see `LONG_TERM_TODO.md`).
