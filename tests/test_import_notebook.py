import importlib.util
import unittest

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_importer():
    path = ROOT / "_scripts" / "import_notebook.py"
    spec = importlib.util.spec_from_file_location("import_notebook", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ImportNotebookTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.importer = load_importer()

    def test_frontmatter_has_quarto_html_and_lowercase_categories(self):
        cell = self.importer.build_frontmatter_cell(
            "Title",
            "Subtitle",
            "Description.",
            ["Statistics", "MonteCarlo"],
            "2025-01-08",
        )

        source = "".join(cell["source"])
        self.assertIn('title: "Title"', source)
        self.assertIn("    - statistics\n", source)
        self.assertIn("    - montecarlo\n", source)
        self.assertIn("format:\n    html: default\n", source)
        self.assertNotIn("ipynb: default", source)

    def test_fix_paths_rewrites_wiki_paths_to_assets(self):
        cell = {
            "cell_type": "markdown",
            "source": [
                "![Plot](images/plot.png)\n",
                "![Plot](./images/plot2.png)\n",
            ],
        }

        fixed = self.importer.fix_paths(cell)

        self.assertEqual(
            fixed["source"],
            ["![Plot](assets/plot.png)\n", "![Plot](assets/plot2.png)\n"],
        )


if __name__ == "__main__":
    unittest.main()
