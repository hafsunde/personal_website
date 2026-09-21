"""Build the CV locally, render its HTML body, or check committed provenance.

Run from any directory: python scripts/cv.py {build,html,check}.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tmp" / "cv"
PDF = ROOT / "assets" / "cv.pdf"
MANIFEST = ROOT / "cv" / "build.json"
INPUTS = ("cv/cv.tex", "data/publications.yml", "scripts/cv.py", "cv/requirements.txt")
BEGIN = "% BEGIN GENERATED PUBLICATIONS"
END = "% END GENERATED PUBLICATIONS"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fingerprints():
    # Git may check out CRLF on Windows and LF on Linux.
    return {name: digest((ROOT / name).read_text(encoding="utf-8").encode("utf-8"))
            for name in INPUTS}


def tex(text):
    escapes = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%",
               "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{",
               "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
               "–": "--", "—": "---", "’": "'", "‘": "'", "“": "``", "”": "''"}
    return "".join(escapes.get(char, char) for char in str(text))


def author_role(pub):
    if pub.get("authorship") in ("joint-first", "joint-last"):
        return pub["authorship"].removeprefix("joint-")
    # Truncated collaboration lists cannot establish the author's position.
    if pub.get("et_al"):
        return "other"
    if pub["authors"][0] == "Sunde, H.F.":
        return "first"
    if pub["authors"][-1] == "Sunde, H.F.":
        return "last"
    return "other"


def publications():
    pubs = yaml.safe_load((ROOT / "data/publications.yml").read_text(encoding="utf-8"))
    ids = [p["id"] for p in pubs]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate publication IDs")
    if any(p["type"] not in ("article", "preprint") for p in pubs):
        raise ValueError("Unknown publication type")
    groups = [(heading, sorted([p for p in pubs if author_role(p) in roles],
                               key=lambda p: (p["type"] != "preprint", -p["year"])))
              for roles, heading in ((("first", "last"), "First- and last-author publications"),
                                     (("other",), "Other co-authored publications"))]
    lines = []
    for heading, entries in groups:
        if not entries:
            continue
        lines.append(r"\subsection*{" + heading + "}")
        previous_type = None
        for p in entries:
            if p["type"] != previous_type:
                if previous_type is not None:
                    lines.append(r"\end{itemize}")
                label = "Preprints" if p["type"] == "preprint" else "Journal articles"
                lines += [r"\subsubsection*{" + label + "}", r"\begin{itemize}"]
                previous_type = p["type"]
            authors = [r"\textbf{" + tex(a) + "}" if a == "Sunde, H.F." else tex(a)
                       for a in p["authors"]]
            if p.get("et_al"):
                author_line = authors[0] + ", et al."
            elif len(authors) > 1:
                author_line = ", ".join(authors[:-1]) + r", \& " + authors[-1]
            else:
                author_line = authors[0]
            role = {"joint-first": "Joint first author", "joint-last": "Joint last author"}.get(p.get("authorship"))
            note = (r" \textit{" + role + ".}") if role else ""
            title = tex(p["title"])
            if not title.endswith((".", "?", "!")):
                title += "."
            lines.append(r"\item " + author_line + " (" + str(p["year"]) + "). "
                         + title + r" \textit{" + tex(p["venue"]) + "}. "
                         + ("[Preprint]. " if p["type"] == "preprint" else "")
                         + r"\url{https://doi.org/" + p["doi"] + "}" + note)
        lines.append(r"\end{itemize}")
    return "\n".join(lines)


def expanded_source():
    source = (ROOT / "cv/cv.tex").read_text(encoding="utf-8")
    if source.count(BEGIN) != 1 or source.count(END) != 1:
        raise ValueError("Expected exactly one publications insertion point in cv/cv.tex")
    before, tail = source.split(BEGIN)
    _, after = tail.split(END)
    return before + BEGIN + "\n" + publications() + "\n" + END + after


def quarto():
    # Prefer the native launcher on Windows; quarto.cmd fails with spaced paths.
    command = shutil.which("quarto.exe" if os.name == "nt" else "quarto")
    if not command:
        raise RuntimeError("Quarto is required for LaTeX-to-HTML conversion")
    return command


def run(args, **kwargs):
    result = subprocess.run(args, cwd=ROOT, text=True, encoding="utf-8",
                            errors="replace", capture_output=True, **kwargs)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def pandoc():
    # The Windows Quarto launcher cannot forward redirected stdin reliably.
    # Use its bundled Pandoc directly, keeping the same pinned toolchain.
    if os.name == "nt":
        return [str(Path(quarto()).parent / "tools/pandoc.exe")]
    return [quarto(), "pandoc"]


def html():
    # Parse once to an AST, reject unsupported content rather than silently
    # dropping it, then write HTML. PDF-only pagination has no HTML equivalent.
    source = (expanded_source().replace(r"\newpage", "")
              .replace(r"\thispagestyle{plain}", "").replace(r"\LARGE", ""))
    ast = json.loads(run(pandoc() + ["--from=latex+raw_tex", "--to=json"], input=source))

    def validate(node):
        if isinstance(node, dict):
            if node.get("t") in ("RawBlock", "RawInline"):
                raise ValueError("Unsupported LaTeX in HTML conversion: " + str(node["c"]))
            for value in node.values():
                validate(value)
        elif isinstance(node, list):
            for value in node:
                validate(value)

    validate(ast)
    return run(pandoc() + ["--from=json", "--to=html5", "--shift-heading-level-by=1"],
               input=json.dumps(ast))


def check():
    if not MANIFEST.exists() or not PDF.exists():
        raise RuntimeError("CV PDF or build manifest missing. Run python scripts/cv.py build")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("inputs") != fingerprints() or manifest.get("pdf_sha256") != digest(PDF.read_bytes()):
        raise RuntimeError("CV PDF is stale or modified. Run python scripts/cv.py build, review it, "
                           "and commit assets/cv.pdf and cv/build.json together with the sources.")


def build():
    BUILD.mkdir(parents=True, exist_ok=True)
    source = BUILD / "cv.tex"
    source.write_text(expanded_source(), encoding="utf-8", newline="\n")
    # Ensure the source is supported by both formats before replacing the PDF.
    (BUILD / "cv.html").write_text(html(), encoding="utf-8")
    compiler = shutil.which("lualatex")
    if not compiler:
        raise RuntimeError("Install a TeX distribution providing lualatex (with Segoe UI and Palatino Linotype fonts)")
    command = [compiler, "-interaction=nonstopmode", "-halt-on-error", "-no-shell-escape",
               "-output-directory=" + str(BUILD), str(source)]
    for _ in range(2):
        run(command)
    log = (BUILD / "cv.log").read_text(encoding="utf-8", errors="replace")
    if "Overfull \\hbox" in log or "Overfull \\vbox" in log or "Missing character:" in log:
        raise RuntimeError("CV has overflowing content or missing glyphs; inspect tmp/cv/cv.log")
    # Keep the canonical .tex independently compilable. Its generated block is
    # always replaced from YAML, never used as a second bibliographic source.
    (ROOT / "cv/cv.tex").write_text(source.read_text(encoding="utf-8"),
                                   encoding="utf-8", newline="\n")
    # Keep the original until visual review is complete; never overwrite it.
    backup = ROOT / "tmp/pdfs/cv-original.pdf"
    if PDF.exists() and not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PDF, backup)
    shutil.copyfile(BUILD / "cv.pdf", PDF)
    manifest = {"inputs": fingerprints(), "pdf_sha256": digest(PDF.read_bytes()),
                "toolchain": {"lualatex": run([compiler, "--version"]).splitlines()[0],
                              "quarto": run([quarto(), "--version"]).strip(),
                              "pyyaml": yaml.__version__}}
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "html", "check"))
    args = parser.parse_args()
    # R's captured stdout must be UTF-8 on Windows as well as Linux.
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        if args.command == "build":
            build()
            print("Built assets/cv.pdf and cv/build.json. Review PDF and HTML before committing.")
        elif args.command == "check":
            check()
            print("CV source and PDF fingerprints match.")
        else:
            check()
            # ASCII entities survive R/knitr even under a non-UTF-8 Windows
            # locale, while browsers display the original Unicode characters.
            print(html().encode("ascii", "xmlcharrefreplace").decode("ascii"))
    except (RuntimeError, ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
