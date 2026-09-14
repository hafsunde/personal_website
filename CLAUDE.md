# personal_website

Source for Hans Fredrik Sunde's academic site, served at hansfredriksunde.com. It replaced a Squarespace site.

Parked and upcoming work is in `LONG_TERM_TODO.md` — read it before starting work.

## Stack

Quarto static site on GitHub Pages. The repo is public at `github.com/hafsunde/personal_website` (a project repo, remote `origin`).

Rendering happens in `.github/workflows/publish.yml` on every push to `main`, so a local Quarto install is for `quarto preview` only, not a publishing dependency. Pages use the knitr engine: `R/publications.R` generates the publication lists, so the build needs R with `knitr`, `rmarkdown` and `yaml`. Quarto is pinned to 1.10.18 in the workflow; bump it there and locally together.

## Hard rules

Pushing to `main` publishes the site within a couple of minutes. Treat a push as publishing: don't push unless asked.

The domain is registered at Squarespace Domains, which also hosts its DNS. It points at GitHub Pages, and the custom domain is set in the repo's Pages settings (deploys use GitHub Actions, so there is no `CNAME` file and none is needed). Without an explicit go-ahead from Hans Fredrik, do not:

- change DNS records or nameservers, change the Pages custom domain, or touch anything at the registrar
- remove the `_github-pages-challenge-hafsunde` TXT record, which keeps the domain verified to his GitHub account
- cancel or modify anything at Squarespace

The Squarespace DNS panel says "You're using custom nameservers" and that its records are inactive. That is misleading: the domain is delegated to Squarespace's own NS1-backed nameservers, and the records in the panel are live. Don't switch nameservers because of it.

## Publications

`data/publications.yml` is the single source of truth **for the site's bibliographic data**. `publications.qmd` generates from it at render time via `R/publications.R`, and the selected papers on `index.qmd` take their references from it — never hand-edit a publication list into a `.qmd`. Adding a paper should be one YAML entry and nothing else.

Entry shape:

```yaml
- id: sunde2025indirect
  authors: ["Sunde, H.F.", "Eilertsen, E.M.", "Torvik, F.A."]
  title: "Understanding indirect assortative mating and its intergenerational consequences for educational attainment"
  venue: "Nature Communications"
  year: 2025
  doi: "10.1038/s41467-025-60483-0"
  type: article          # article | preprint
  description: "Shows that ..."
  links:
    bluesky: "https://..."
```

For very large collaborations, list only the first author and add `et_al: true`.

`description` is one sentence on what the paper does or finds, shown under the author line. It must add something the title doesn't already say — never restate or paraphrase the title. Write it from the paper's abstract, not from memory. Like `authorship` and `links`, it is editorial: it doesn't come from Zotero, so preserve it when regenerating entries.

First- and last-author markers are computed from his position in `authors`. Joint first or last authorship can't be computed, so it is stored as `authorship: joint-first` or `authorship: joint-last`. Set it only when Hans Fredrik confirms it — don't infer it from author order or publisher footnotes — and preserve it when regenerating entries.

`year` is the issue year of the version of record, falling back to the online date when there is no issue. This matches ORCID; don't use the online-first year.

Grouping (preprints first, then years descending) and ordering are computed, not stored.

### Selected papers

The home page shows a hand-picked set of papers from `data/selected.yml`, ordered by importance rather than date. Ask Hans Fredrik before changing which papers are featured or their order. They don't follow the publications-page rules: no authorship markers and no descriptions.

Each entry references a publication by `id` (title, authors, venue, year, DOI and links come from `data/publications.yml`) and adds:

- `image`: the first page of the **published** PDF, rendered to `assets/selected/<id>.jpg`. Take it from the Zotero attachment, and check it isn't the supplementary PDF, which is often attached to the same item.
- `abstract`: the publisher's abstract, verbatim, as a list of sections with an optional `heading` (for structured abstracts such as JCPP's).

### Zotero

A Zotero MCP server is available and Hans Fredrik's library contains his papers. Use it as the **input** for building and updating `data/publications.yml` — it beats retyping metadata off a web page.

Zotero is not a build-time dependency. The GitHub Action that renders the site has no access to it, so the generated YAML is committed and is what the site reads. Never make a page query Zotero directly.

Working with the library:

- His own papers are a subset of the library, and there is no collection or saved search holding them — filter by author (`Sunde, Hans Fredrik`). Author substring search also matches unrelated `Sundet` / `Sundelin` entries, so check the full name.
- Watch for the **preprint/published duplicate**: the same paper often exists twice, once as an OSF, SSRN or medRxiv preprint and once as the journal version. Only genuinely unpublished work should end up as `type: preprint`. When both exist, keep the published version and drop the preprint entry. Recheck existing preprints too — they get published.
- Zotero can lag behind ORCID; cross-check ORCID for papers missing from the library.
- Zotero metadata is often imported rather than curated, so expect title-case inconsistency, missing DOIs, "Advance online publication" venues, and author name variants. Normalise these on the way into the YAML.
- `description`, `authorship` and the `links:` block are editorial, not bibliographic. They don't come from Zotero — preserve whatever is already in the YAML when regenerating.

For maintenance later: adding a new paper should be "pull it from Zotero, append the entry, push" — not a manual transcription.

## Accuracy

Bibliographic metadata must be verified, not transcribed from memory or from a rendered page. Every DOI must resolve, and author strings and venues should be checked against Zotero, ORCID `0000-0001-8797-5422`, or the publisher record. Where Zotero and the old Squarespace list disagree, resolve the DOI and use the publisher record — don't silently prefer one source. An unverifiable entry stays out of the file rather than going in provisionally; flag it instead.

Some publishers (Wiley, PNAS) return 403 to scripted HTML requests. Check DOIs with content negotiation (`Accept: application/vnd.citationstyles.csl+json` against `https://doi.org/<doi>`), not by loading the landing page.

## Conventions

- `_site/` and `.quarto/` are build output — gitignored, never committed.
- Assets (headshot, CV PDF, SCSS, selected-paper first pages) live in `assets/`.
- Styling goes in `assets/styles.scss` as theme variables and rules, not inline HTML or per-page CSS blocks. The same file feeds both the light (cosmo) and dark (darkly) themes; dark overrides sit under `body.quarto-dark`.
- `_quarto.yml` has an explicit `render:` list so `CLAUDE.md` and `LONG_TERM_TODO.md` at the repo root stay out of the site. New pages must match it (`*.qmd`, `blog/*.qmd`, `blog/posts/*.qmd`).
- Blog posts are `blog/posts/<slug>.qmd` with front matter `title`, `date` and `description` (the listing on `blog/index.qmd` shows all three). Put the title in front matter, not as a `#` heading. Unfinished posts carry `draft: true`, which keeps them out of the published site. Don't write or edit post prose unless asked; posts are Hans Fredrik's voice.
- Prose on the site is Hans Fredrik's own voice — port existing text as-is rather than rewriting it, and flag anything that reads as stale instead of silently updating it.
- The contact page keeps pointing at the FHI employee page; no email address on the site.
