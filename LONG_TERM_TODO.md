# Long-term to-do

Parked work. **Nothing here gets implemented without an explicit go-ahead from Hans Fredrik.**

The site is live at `https://hansfredriksunde.com` on GitHub Pages; `hafsunde.github.io/personal_website/` redirects there. Every push to `main` redeploys it.

---

## Domain and Squarespace

Done on 2026-09-14: DNS at Squarespace points at GitHub Pages (apex A/AAAA records and a `www` CNAME to `hafsunde.github.io`), the domain is verified to the `hafsunde` GitHub account, and the Pages custom domain is set with HTTPS enforced. Notes on URLs:

- `/` and `/contact` match the old site, and `/scientific-papers` redirects to `/publications`. The old CV link (`/s/HFS_AcadamicCV_june25.pdf`) is deliberately not kept.
- Extensionless URLs (`/publications`) are served directly by Pages; a trailing slash (`/publications/`) 404s.

Remaining:

- [ ] **Cancel the Squarespace website plan** once the new site has been stable for a few days. It renews on 2027-03-21 for $228, so cancel before then. The domain is a separate "Domains" subscription (about $20/year, WHOIS privacy included): keep it with auto-renew on, and if Squarespace asks what to do with the domain, keep it.
- [ ] **Revisit the registrar** (optional). Staying at Squarespace is fine. Moving to Cloudflare or Porkbun would save about $10/year. If done, recreate every DNS record at the new provider first, including the `_github-pages-challenge-hafsunde` TXT record, and don't let the registration lapse (it expires 2027-03-21 unless renewed).

---

## CV from LaTeX in the repo

Goal: one LaTeX source in the repo that produces both the CV PDF and an HTML CV page, replacing the hand-uploaded `assets/cv.pdf`. The chain runs Zotero → `data/publications.yml` → site, CV PDF and CV page.

Decided:

- The PDF is built locally and committed, not built in CI. A workflow check fails the build if the committed PDF doesn't match the source.
- The CV gets an HTML page that matches the PDF, with a link to download the PDF. The page is generated from the same LaTeX source; if that proves impractical, the fallback is a workflow check that the two match.
- The LaTeX is written in a Pandoc-readable subset (standard commands plus simple `\newcommand` macros, no CV class such as `moderncv`), so `cv.qmd` can convert it at render time and keep the Quarto header and theme.
- Fallback if that becomes difficult: make YAML the source instead (like `data/publications.yml`) and generate both the Quarto page and the LaTeX from it. This reverses the "LaTeX is the source" decision, so ask Hans Fredrik before switching.

To do:

- [ ] **Rebuild the CV in LaTeX**, reproducing the content of the current `assets/cv.pdf`.
- [ ] **Generate its publications section from `data/publications.yml`** rather than maintaining the list twice.
- [ ] **Generate the HTML CV page** from the same source, replacing the current `cv.qmd`, with a download link to the PDF.
- [ ] **Add the workflow check** that the committed PDF (and, if needed, the HTML page) matches the source.
- [ ] **Keep the current `assets/cv.pdf` as a fallback** until the generated PDF and page look right side by side.

---

## Smaller parked items

- [ ] Blog RSS feed (optional). The first post went up on 2026-09-14; the listing has `feed: false`, so there is no feed yet. See `blog/README.md` for how to write posts.
- [ ] Revisit the design once content is stable. In particular, consider fonts and colors.
- [ ] Make the site accessible and reasonably optimised for Google and other search engines.
- [ ] Add a skill or workflow that checks that the publication list is up to date (new preprints, preprints that have been published, updated details in published papers). Manual for now; could be automated later.
