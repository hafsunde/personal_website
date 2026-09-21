# Updating the CV

`cv.tex` is the canonical source for CV content and PDF layout. Add new talks,
positions, and teaching there, using standard LaTeX paragraphs, headings, lists,
links, and emphasis. Publications come from `../data/publications.yml`; leave the
generated-publications marker in place. The old CV's non-publication content is
preserved, with the UiO position ending in March 2026. Talks and teaching still
cover the period through June 2025 and can be extended manually.

## Build locally

Install Python 3.12+, Quarto 1.10.18 (the version pinned in the site workflow),
and a TeX distribution with `lualatex`. The LaTeX packages used are `fontspec`,
`geometry`, `enumitem`, `titlesec`, `fancyhdr`, and `hyperref`.
The PDF uses Segoe UI for body text and Palatino Linotype for headings, matching
the website on Windows. Both fonts must be installed on the build machine.
The HTML continues to use the website's platform-specific font stacks.

For direct editor builds, select **LuaLaTeX**, not pdfLaTeX. The source includes
an engine hint and `cv/.latexmkrc` configures latexmk accordingly. From `cv/`,
run `lualatex cv.tex` or `latexmk cv.tex`.

From the repository root:

```sh
python -m pip install -r cv/requirements.txt
python scripts/cv.py build
quarto render cv.qmd
python scripts/cv.py check
```

On Windows, use `quarto.exe render cv.qmd` if the `quarto.cmd` launcher fails
because Quarto is installed under a path containing spaces.

Review `assets/cv.pdf` and `_site/cv.html`, then commit the source changes,
`assets/cv.pdf`, and `cv/build.json` together. Update the explicit publication
date near the top of `cv.tex` when updating publications. Update the activities
coverage note when adding newer activities. Nothing is published until pushed.

The build directory is `tmp/cv/` (ignored by Git). Before the first replacement,
the build keeps the previous PDF in `tmp/pdfs/cv-original.pdf` for side-by-side
review. The original is also available in Git history.

## One source, two formats

The build inserts references from the publication YAML into a temporary copy of
`cv.tex`. The PDF is compiled from that copy. After successful compilation the
generated block is also saved in `cv.tex`, so compiling that file directly in a
LaTeX editor includes publications. Do not edit the generated block manually;
run the build command to refresh it whenever the publication YAML changes.
At site render time, `cv.qmd`
invokes the same generator and converts the expanded LaTeX to HTML through
Quarto's bundled Pandoc. Quarto supplies the page header, navigation, and theme.
The content and ordering match; pagination and typography suit each format.
The HTML conversion rejects unsupported raw LaTeX instead of silently losing it.

References are separated into a combined first- and last-author section and
other co-authored publications. Confirmed joint first/last authorships belong in
the combined section; truncated collaboration lists are not used to infer author position.
Within each section, preprints are explicitly labelled and listed first, followed
by journal articles, each in descending year order. Ties follow the YAML. The author's name is
bolded, and confirmed joint authorship is retained. Paper descriptions and
social links are omitted from the compact CV references.

## Freshness and reproducibility

CI does **not** compile a PDF. `python scripts/cv.py check` compares SHA-256
fingerprints of the LaTeX, publication YAML, generator, dependency specification,
and committed PDF against `cv/build.json`, written only after a successful local
build. A change to any of them blocks deployment until rebuilt. Text hashes
normalize CRLF/LF so Windows and Linux agree. Rendering the HTML also runs this
check, so the site cannot quietly show newer CV content beside an old PDF.

This is a build-provenance/freshness check, not an independent CI recompilation
or proof against someone manually falsifying the manifest. The manifest records
the local tool versions. Volatile PDF metadata is suppressed for repeatable
builds on the same toolchain; different TeX/font versions may produce different
PDF bytes. The HTML is generated at render time and is not maintained separately.

To verify the generator and stale-file checks locally:

```sh
python -m unittest discover -s tests -p test_cv.py
```
