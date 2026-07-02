import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_manifest_module():
    path = ROOT / "_scripts" / "write_cx_manifest.py"
    spec = importlib.util.spec_from_file_location("write_cx_manifest", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CxManifestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest_module()

    def test_site_manifest_excludes_generated_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "_quarto.yml").write_text("project:\n  type: website\n")
            (root / "index.qmd").write_text("# Home\n")
            (root / "assets").mkdir()
            (root / "assets" / "download-bundle.js").write_text("ok")
            (root / "assets" / "llm-prompts.json").write_text("{}")
            (root / "_site").mkdir()
            (root / "_site" / "index.html").write_text("generated")

            payload = self.manifest.build_manifest(root, "site-build", [("out_dir", "_site")])
            paths = {item["path"] for item in payload["files"]}

        self.assertIn("_quarto.yml", paths)
        self.assertIn("index.qmd", paths)
        self.assertIn("assets/download-bundle.js", paths)
        self.assertNotIn("assets/llm-prompts.json", paths)
        self.assertNotIn("_site/index.html", paths)
        self.assertEqual(payload["args"], {"out_dir": "_site"})

    def test_bundle_manifest_includes_notebook_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "_scripts").mkdir()
            (root / "_scripts" / "build_bundles_public.sh").write_text("#!/usr/bin/env bash\n")
            (root / "_scripts" / "generate_bundles.py").write_text("print('bundles')\n")
            (root / "_scripts" / "stamp_command.sh").write_text("#!/usr/bin/env bash\n")
            post = root / "posts" / "demo"
            post.mkdir(parents=True)
            (post / "index.ipynb").write_text("{}")
            (post / "assets").mkdir()
            (post / "assets" / "data.csv").write_text("x\n")

            payload = self.manifest.build_manifest(root, "bundles", [])
            paths = {item["path"] for item in payload["files"]}

        self.assertIn("_scripts/build_bundles_public.sh", paths)
        self.assertIn("_scripts/generate_bundles.py", paths)
        self.assertIn("_scripts/stamp_command.sh", paths)
        self.assertIn("posts/demo/index.ipynb", paths)
        self.assertIn("posts/demo/assets/data.csv", paths)


if __name__ == "__main__":
    unittest.main()
