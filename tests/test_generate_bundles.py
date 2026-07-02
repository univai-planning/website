import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_generator():
    path = ROOT / "_scripts" / "generate_bundles.py"
    spec = importlib.util.spec_from_file_location("generate_bundles", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class BundleGeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = load_generator()

    def test_content_root_spec_supports_aliases(self):
        root = self.generator.parse_content_root("posts:posts:/posts:/blog")

        self.assertEqual(root.source_dir, Path("posts"))
        self.assertEqual(root.render_route, "posts")
        self.assertEqual(root.public_route, "/posts")
        self.assertEqual(root.alias_routes, ("/blog",))

    def test_route_keys_are_manifest_safe(self):
        self.assertEqual(
            self.generator.route_key("/learning", "probability"),
            "learning/probability",
        )
        self.assertEqual(
            self.generator.route_key("blog", "entropy"),
            "blog/entropy",
        )


if __name__ == "__main__":
    unittest.main()
