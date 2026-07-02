import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_generator():
    path = ROOT / "_scripts" / "generate_llm_context.py"
    spec = importlib.util.spec_from_file_location("generate_llm_context", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class LlmContextGeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = load_generator()

    def test_flat_pages_resolve_images_against_route_root(self):
        root = self.generator.ContentRoot(Path("courses"), "courses", "/learning")
        base = self.generator.source_page_base(
            root,
            "distributions",
            Path("courses/distributions.md"),
        )

        self.assertEqual(base, "https://univ.ai/learning/")
        self.assertEqual(
            self.generator.rewrite_relative_images("![CDF](images/2tosscdf.png)", base),
            "![CDF](https://univ.ai/learning/images/2tosscdf.png)",
        )

    def test_directory_pages_resolve_images_against_slug(self):
        root = self.generator.ContentRoot(Path("courses"), "courses", "/learning")
        base = self.generator.source_page_base(
            root,
            "probability",
            Path("courses/probability/index.ipynb"),
        )

        self.assertEqual(base, "https://univ.ai/learning/probability/")

    def test_frontmatter_can_disable_llm_context(self):
        source = ROOT / "courses" / "software" / "index.qmd"

        self.assertFalse(self.generator.llm_context_enabled(source))


if __name__ == "__main__":
    unittest.main()
