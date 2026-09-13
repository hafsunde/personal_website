# Long-term to-do

Parked work. **Nothing here gets implemented without an explicit go-ahead from Hans Fredrik.**

Phases 1–4 of the migration plan (content extraction, scaffold, design, local review) are done. Phase 5 is in progress.

---

## Domain and deployment (plan phases 5–7)

The repo and deploy workflow have the go-ahead. The domain cutover and Squarespace retirement are still frozen: don't touch DNS, add a `CNAME`, set a custom domain, or cancel anything without a go-ahead.

- [x] **Create the GitHub repo and push.** Public project repo `hafsunde/personal_website`. A project repo works with a custom domain; until then the site is served under `/personal_website/`, which is fine because Quarto's internal links are relative.
- [x] **Add the Pages build.** `.github/workflows/publish.yml` renders with Quarto 1.10.18 plus R (`knitr`, `rmarkdown`, `yaml`) and deploys with GitHub's Pages actions on every push to `main`.
- [ ] **Enable Pages.** Repo Settings → Pages → Build and deployment → Source: "GitHub Actions". Then re-run the workflow (Actions tab → Publish site → Run workflow) if the first deploy failed because Pages was off.
- [ ] **Verify at `hafsunde.github.io/personal_website/`.** The Squarespace site stays live and keeps serving the domain throughout. This is the gate before anything DNS-related.
- [x] **Keep old URLs working.** The Squarespace papers page is `/scientific-papers`; the new one is `/publications`. `publications.qmd` has `aliases: [scientific-papers.html]`, so Quarto emits a client-side redirect page. `/contact` and `/` already match.
- [ ] **Old CV URL.** `/s/HFS_AcadamicCV_june25.pdf` 404s after the cutover unless a copy of the PDF sits at that path. Decide whether that link matters.
- [ ] **Redirect hansfredriksunde.com to GitHub Pages.**
  - Confirm where the domain is actually registered (the Squarespace DNS panel shows this).
  - Apex A records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
  - Apex AAAA records → `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.
  - `www` CNAME → `hafsunde.github.io`.
  - Set the custom domain in the repo's Pages settings, wait for the certificate, then enable "Enforce HTTPS".
  - Propagation usually under an hour.
  - Extensionless URLs (`/publications`) are served directly by Pages; a trailing slash (`/publications/`) 404s.
- [ ] **Decide on the registrar.** Recommendation is *not* to transfer during the migration — a transfer adds a 5–7 day lock and one more failure mode, and GitHub Pages works with any registrar. Revisit moving to Cloudflare or Namecheap once the new site has been stable for a few weeks.
- [ ] **Retire the Squarespace site.** Check *before* cancelling whether the domain registration is bundled with the website plan — if the domain came free with the subscription, cancelling can put the registration at risk, in which case transfer the domain out first.

---

## Build the CV inside the repo

Right now the CV is a PDF (`assets/cv.pdf`, originally `HFS_AcadamicCV_june25.pdf`) linked from the nav — updating it means editing a document elsewhere and re-uploading. The goal is the same as for publications: one source of truth in the repo, updated by editing a data file.

- [ ] **Decide the source format.** Options, roughly in order of effort:
  - *CV as a `.qmd`* — write it in markdown, render to HTML and PDF from the same file. Simplest, and the version most likely to actually stay current.
  - *CV from YAML* — `data/cv.yml` with sections (positions, education, grants, teaching, service) rendered by a template. More setup; pays off if the CV gets long or needs reordering.
  - *Reuse `data/publications.yml`* — either way, the publications section of the CV should be generated from the existing publications data rather than maintained twice. This is the main argument for doing it at all, and it means the chain runs Zotero → `publications.yml` → both the site and the CV.
- [ ] **Render to both HTML and PDF.** HTML page for search and phones; PDF kept as a download link. Quarto does both from one source, but the PDF path needs a LaTeX engine (TinyTeX) available in the build (`quarto-actions/setup` has a `tinytex` input).
- [ ] **Decide whether the PDF is built in CI or committed.** Building it in the Action keeps it always in sync; committing it avoids adding TinyTeX to the build.
- [ ] **Keep the current PDF as a fallback** until the generated one looks right side by side.

---

## Smaller parked items

- [ ] Add blog posts (the listing page is scaffolded and empty; actual posts and any RSS/feed setup are later).
- [x] Email on the contact page — decided: no email, keep pointing at the FHI employee page.
- [ ] Revisit the design once the site is built and content is stable.
