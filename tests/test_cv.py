"""Regression checks for CV synchronization and lossless HTML conversion."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("cv", Path(__file__).resolve().parents[1] / "scripts/cv.py")
cv = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cv)


class FreshnessTests(unittest.TestCase):
    def setUp(self):
        temp_root = cv.ROOT / "tmp"
        temp_root.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=temp_root)
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.source = root / "source.tex"
        self.source.write_bytes(b"Original\n")
        self.pdf = root / "cv.pdf"
        self.pdf.write_bytes(b"PDF fixture")
        self.manifest = root / "build.json"
        for name, value in (("ROOT", root), ("INPUTS", ("source.tex",)),
                            ("PDF", self.pdf), ("MANIFEST", self.manifest)):
            patcher = patch.object(cv, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.manifest.write_text(json.dumps({"inputs": cv.fingerprints(),
                                             "pdf_sha256": cv.digest(self.pdf.read_bytes())}),
                                 encoding="utf-8")

    def test_matching_build_and_cross_platform_line_endings(self):
        cv.check()
        self.source.write_bytes(b"Original\r\n")
        cv.check()

    def test_source_change_requires_rebuild(self):
        self.source.write_text("New talk\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "stale"):
            cv.check()

    def test_pdf_replacement_is_detected(self):
        self.pdf.write_bytes(b"Different PDF")
        with self.assertRaisesRegex(RuntimeError, "stale"):
            cv.check()


class ConversionTests(unittest.TestCase):
    def test_authorship_roles_include_confirmed_joint_roles(self):
        self.assertEqual(cv.author_role({"authors": ["Sunde, H.F.", "Other, A."]}), "first")
        self.assertEqual(cv.author_role({"authors": ["Other, A.", "Sunde, H.F."]}), "last")
        middle = {"authors": ["Other, A.", "Sunde, H.F.", "Other, B."]}
        self.assertEqual(cv.author_role(middle), "other")
        self.assertEqual(cv.author_role(dict(middle, authorship="joint-first")), "first")
        self.assertEqual(cv.author_role(dict(middle, authorship="joint-last")), "last")
        self.assertEqual(cv.author_role({"authors": ["Other, A."], "et_al": True}), "other")

    def test_publications_are_separated_by_authorship_without_duplicates(self):
        refs = cv.publications()
        lead, other = refs.split(r"\subsection*{Other co-authored publications}")
        self.assertIn(r"\subsection*{First- and last-author publications}", lead)
        self.assertIn("10.1017/thg.2026.10050", lead)
        self.assertIn("10.64898/2026.09.01.748516", lead)
        self.assertIn("10.1016/j.paid.2024.112862", lead)
        self.assertIn("10.1038/s41586-025-09844-9", other)
        self.assertNotIn("10.64898/2026.09.01.748516", other)
        self.assertNotIn("10.1016/j.paid.2024.112862", other)

    def test_canonical_tex_contains_the_current_generated_publications(self):
        source = (cv.ROOT / "cv/cv.tex").read_text(encoding="utf-8")
        self.assertEqual(source, cv.expanded_source())
        self.assertIn(cv.publications(), source)

    def test_every_publication_has_one_doi_and_preprints_are_labelled(self):
        pubs = cv.yaml.safe_load((cv.ROOT / "data/publications.yml").read_text(encoding="utf-8"))
        refs = cv.publications()
        self.assertEqual(refs.count(r"\item "), len(pubs))
        self.assertEqual(refs.count("[Preprint]"), sum(p["type"] == "preprint" for p in pubs))
        for pub in pubs:
            self.assertEqual(refs.count(r"\url{https://doi.org/" + pub["doi"] + "}"), 1)

    def test_html_keeps_contacts_dates_unicode_and_all_dois(self):
        body = " ".join(cv.html().split())
        for value in ("hafsunde@gmail.com", "+47 995 88 824", "03.2025 – 03.2026",
                      "Skoleforløp", "Lærerkonferansen", "Joint last author"):
            self.assertIn(value, body)
        pubs = cv.yaml.safe_load((cv.ROOT / "data/publications.yml").read_text(encoding="utf-8"))
        for pub in pubs:
            self.assertIn('href="https://doi.org/' + pub["doi"] + '"', body)

    def test_unsupported_latex_fails_instead_of_disappearing(self):
        with patch.object(cv, "expanded_source", return_value=r"\begin{document}\unsupported{Lost content}\end{document}"):
            with self.assertRaisesRegex(ValueError, "Unsupported LaTeX"):
                cv.html()


if __name__ == "__main__":
    unittest.main()
