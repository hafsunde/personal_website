# Long-term to-do

Parked work. **Nothing here gets implemented without an explicit go-ahead from Hans Fredrik.**

The site is live on GitHub Pages at `hafsunde.github.io/personal_website/` and has been reviewed. Every push to `main` redeploys it. Squarespace still serves hansfredriksunde.com.

---

## Domain cutover

Frozen: don't touch DNS, add a `CNAME`, set a custom domain, or cancel anything without a go-ahead.

- [ ] **Point hansfredriksunde.com at GitHub Pages.**
  - Confirm where the domain is actually registered (the Squarespace DNS panel shows this).
  - Apex A records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
  - Apex AAAA records → `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.
  - `www` CNAME → `hafsunde.github.io`.
  - Set the custom domain in the repo's Pages settings, wait for the certificate, then enable "Enforce HTTPS". The site then moves from `/personal_website/` to the domain root; internal links are relative, so nothing else changes.
  - Propagation usually under an hour.
  - Old URLs: `/` and `/contact` match the new site, and `/scientific-papers` redirects to `/publications`. The old CV link (`/s/HFS_AcadamicCV_june25.pdf`) is deliberately not kept.
  - Extensionless URLs (`/publications`) are served directly by Pages; a trailing slash (`/publications/`) 404s.
- [ ] **Decide on the registrar.** Recommendation is *not* to transfer during the migration — a transfer adds a 5–7 day lock and one more failure mode, and GitHub Pages works with any registrar. Revisit moving to Cloudflare or Namecheap once the new site has been stable for a few weeks.
- [ ] **Retire the Squarespace site.** Check *before* cancelling whether the domain registration is bundled with the website plan — if the domain came free with the subscription, cancelling can put the registration at risk, in which case transfer the domain out first.

---

## Build the CV PDF from LaTeX in the repo

Decided: the CV PDF will be built from a LaTeX source kept in this repo, replacing the hand-uploaded `assets/cv.pdf`. The goal is the same as for publications: one source of truth in the repo.

- [ ] **Rebuild the CV in LaTeX**, reproducing the content of the current `assets/cv.pdf`.
- [ ] **Generate the publications section from `data/publications.yml`** rather than maintaining the list twice, so the chain runs Zotero → `publications.yml` → both the site and the CV.
- [x] **Decide whether the PDF is built in CI or committed.** Building it in the workflow keeps it in sync but adds a LaTeX engine to the build (`quarto-actions/setup` has a `tinytex` input); committing the PDF avoids that but can drift from the source.
**Decision:** build locally and commit, and add a workflow check that the source code matches the committed pdf.
- [ ] **Keep the current `assets/cv.pdf` as a fallback** until the generated one looks right side by side.
- [x] **Decide whether the CV also gets an HTML page**, or stays a PDF linked from `cv.qmd`.
**Decision:** HTML page that matches the PDF, with a link to download the PDF. The HTML page is generated from the same LaTeX source (or alternatively, a workflow makes sure they match).

---

## Smaller parked items

- [ ] Add blog posts (the listing page is scaffolded and empty; actual posts and any RSS/feed setup are later).
- [ ] Revisit the design once content is stable.
- [ ] Add a skill or workflow that checks that the publication list is up to date (e.g., new preprints, published papers, or updated details in published papers). This will normally be a manual check, but could be automated down the line.
- [x] Add a LinkedIn link.
- [x] Add color or another visual marker for first-author and last-author publications (including joint-first and joint-last). Also add explainer note at the top of the publications page.
