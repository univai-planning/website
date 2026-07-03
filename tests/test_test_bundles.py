import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_tester():
    path = ROOT / "_scripts" / "test_bundles.py"
    spec = importlib.util.spec_from_file_location("test_bundles", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_bundle(path: Path, *, readme: str, notebook: str = "{}") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("index.ipynb", notebook)
        zf.writestr("README.md", readme)


class TestBundlesHelpersTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tester = load_tester()

    def test_selectors_match_slug_or_route_slug(self):
        site_dir = Path("_site")
        zip_path = site_dir / "learning" / "nnreg" / "nnreg.zip"

        self.assertTrue(self.tester.matches_selectors(zip_path, site_dir, {"nnreg"}))
        self.assertTrue(self.tester.matches_selectors(zip_path, site_dir, {"learning/nnreg"}))
        self.assertFalse(self.tester.matches_selectors(zip_path, site_dir, {"posts/nnreg"}))

    def test_selectors_expand_public_aliases_to_rendered_roots(self):
        self.assertIn("posts/entropy", self.tester.split_selectors(["blog/entropy"]))
        self.assertIn("learning/nnreg", self.tester.split_selectors(["courses/nnreg"]))

    def test_plain_qmd_public_alias_can_skip_bundle_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "posts" / "plain-post" / "index.qmd"
            page.parent.mkdir(parents=True)
            page.write_text("---\ntitle: Plain\n---\n")

            self.assertEqual(
                self.tester.source_page_for_selector("blog/plain-post", root),
                page,
            )
            self.assertTrue(
                self.tester.selectors_resolve_to_non_bundle_source_pages(
                    {"blog/plain-post", "posts/plain-post"},
                    root,
                )
            )

    def test_non_executable_archive_notebook_can_skip_bundle_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "courses" / "archive-note" / "index.ipynb"
            page.parent.mkdir(parents=True)
            page.write_text('{"cells": [{"cell_type": "raw", "source": ["---\\ntitle: Archive\\n---\\n"]}]}')

            self.assertEqual(
                self.tester.source_page_for_selector("learning/archive-note", root),
                page,
            )
            self.assertTrue(
                self.tester.selectors_resolve_to_non_bundle_source_pages(
                    {"learning/archive-note", "courses/archive-note"},
                    root,
                )
            )

    def test_executable_notebook_missing_bundle_is_not_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "courses" / "executable-note" / "index.ipynb"
            page.parent.mkdir(parents=True)
            page.write_text('{"cells": [{"cell_type": "code", "source": ["print(1)"]}]}')

            self.assertEqual(
                self.tester.source_page_for_selector("learning/executable-note", root),
                page,
            )
            self.assertFalse(
                self.tester.selectors_resolve_to_non_bundle_source_pages(
                    {"learning/executable-note", "courses/executable-note"},
                    root,
                )
            )

    def test_unknown_selector_is_not_treated_as_skippable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            self.assertIsNone(self.tester.source_page_for_selector("blog/missing", root))
            self.assertFalse(
                self.tester.selectors_resolve_to_non_bundle_source_pages({"blog/missing"}, root)
            )

    def test_cli_skips_valid_plain_qmd_without_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / "_site"
            site.mkdir()
            page = root / "posts" / "plain-post" / "index.qmd"
            page.parent.mkdir(parents=True)
            page.write_text("---\ntitle: Plain\n---\n")
            report = site / "test-report.json"

            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "_scripts" / "test_bundles.py"),
                    "--site-dir",
                    str(site),
                    "--report",
                    str(report),
                    "--slugs",
                    "blog/plain-post",
                ],
                cwd=root,
                capture_output=True,
                text=True,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr)
            payload = json.loads(report.read_text())
            self.assertEqual(payload["status"], "skipped")
            self.assertIn("does not generate", payload["reason"])

    def test_cli_fails_executable_notebook_without_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / "_site"
            site.mkdir()
            page = root / "courses" / "executable-note" / "index.ipynb"
            page.parent.mkdir(parents=True)
            page.write_text('{"cells": [{"cell_type": "code", "source": ["print(1)"]}]}')

            proc = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "_scripts" / "test_bundles.py"),
                    "--site-dir",
                    str(site),
                    "--slugs",
                    "learning/executable-note",
                ],
                cwd=root,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("No zip bundles matched selectors", proc.stdout)

    def test_execution_hash_ignores_route_specific_readme(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "posts" / "nnreg" / "nnreg.zip"
            second = Path(tmp) / "learning" / "nnreg" / "nnreg.zip"
            write_bundle(first, readme="From /posts/nnreg")
            write_bundle(second, readme="From /learning/nnreg")

            first_hash = self.tester.bundle_execution_hash(first)
            second_hash = self.tester.bundle_execution_hash(second)

        self.assertEqual(first_hash, second_hash)

    def test_execution_hash_changes_when_notebook_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "posts" / "demo" / "demo.zip"
            second = Path(tmp) / "learning" / "demo" / "demo.zip"
            write_bundle(first, readme="same", notebook='{"cells": []}')
            write_bundle(second, readme="same", notebook='{"cells": [{"cell_type": "code"}]}')

            first_hash = self.tester.bundle_execution_hash(first)
            second_hash = self.tester.bundle_execution_hash(second)

        self.assertNotEqual(first_hash, second_hash)


if __name__ == "__main__":
    unittest.main()
