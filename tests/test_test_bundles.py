import importlib.util
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
