# Long-term to-do

Parked work. **Nothing here gets implemented without an explicit go-ahead from Hans Fredrik.**

Phases 1–4 of the migration plan (content extraction, scaffold, design, local review) are the active work. Everything below is deferred.

---

## Domain and deployment (plan phases 5–7)

Treat the whole domain/deployment track as frozen. Do not create the GitHub repo, enable Pages, touch DNS, or cancel anything without a go-ahead.

- [ ] **Create the GitHub repo and push.** Decide first whether it should be `<username>.github.io` or a project repo — both work with a custom domain.
- [ ] **Set up the Pages build.** GitHub Action running `quarto render` + deploy, so publishing never needs Quarto installed locally.
- [ ] **Verify at the `*.github.io` URL.** The Squarespace site stays live and keeps serving the domain throughout. This is the gate before anything DNS-related.
- [ ] **Redirect hansfredriksunde.com to GitHub Pages.**
  - Confirm where the domain is actually registered (the Squarespace DNS panel shows this).
  - Apex A records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (plus AAAA equivalents).
  - `www` CNAME → `<username>.github.io`.
  - Set the custom domain in the repo's Pages settings, wait for the certificate, then enable "Enforce HTTPS".
  - Propagation usually under an hour.
- [ ] **Decide on the registrar.** Recommendation is *not* to transfer during the migration — a transfer adds a 5–7 day lock and one more failure mode, and GitHub Pages works with any registrar. Revisit moving to Cloudflare or Namecheap once the new site has been stable for a few weeks.
- [ ] **Retire the Squarespace site.** Check *before* cancelling whether the domain registration is bundled with the website plan — if the domain came free with the subscription, cancelling can put the registration at risk, in which case transfer the domain out first.

---

## Build the CV inside the repo

Right now the CV is a PDF (`HFS_AcadamicCV_june25.pdf`) linked from the nav — updating it means editing a document elsewhere and re-uploading. The goal is the same as for publications: one source of truth in the repo, updated by editing a data file.

- [ ] **Decide the source format.** Options, roughly in order of effort:
  - *CV as a `.qmd`* — write it in markdown, render to HTML and PDF from the same file. Simplest, and the version most likely to actually stay current.
  - *CV from YAML* — `data/cv.yml` with sections (positions, education, grants, teaching, service) rendered by a template. More setup; pays off if the CV gets long or needs reordering.
  - *Reuse `data/publications.yml`* — either way, the publications section of the CV should be generated from the existing publications data rather than maintained twice. This is the main argument for doing it at all, and it means the chain runs Zotero → `publications.yml` → both the site and the CV.
- [ ] **Render to both HTML and PDF.** HTML page for search and phones; PDF kept as a download link. Quarto does both from one source, but the PDF path needs a LaTeX engine (TinyTeX) available in the build.
- [ ] **Decide whether the PDF is built in CI or committed.** Building it in the Action keeps it always in sync; committing it avoids adding TinyTeX to the build.
- [ ] **Keep the current PDF as a fallback** until the generated one looks right side by side.

---

## Smaller parked items

- [ ] Add a blog section (the plan scaffolds an empty listing page; actual posts and any RSS/feed setup are later).
- [ ] Decide whether to put an email address on the contact page or keep pointing at the FHI employee page.
- [ ] Revisit the design once the site is built and content is stable.
