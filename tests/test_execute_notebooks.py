import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_executor():
    path = ROOT / "_scripts" / "execute_notebooks.py"
    spec = importlib.util.spec_from_file_location("execute_notebooks", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ExecuteNotebooksTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.executor = load_executor()

    def test_resolves_blog_route_to_posts_notebook(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            post = root / "posts" / "demo"
            post.mkdir(parents=True)
            (post / "index.ipynb").write_text("{}")

            paths = self.executor.resolve_selectors(["blog/demo"], root)

        self.assertEqual([path.as_posix() for path in paths], [f"{tmp}/posts/demo/index.ipynb"])

    def test_slug_matches_posts_and_courses(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for content_root in ("posts", "courses"):
                folder = root / content_root / "nnreg"
                folder.mkdir(parents=True)
                (folder / "index.ipynb").write_text("{}")

            paths = self.executor.resolve_selectors(["nnreg"], root)

        self.assertEqual(
            sorted(path.relative_to(tmp).as_posix() for path in paths),
            ["courses/nnreg/index.ipynb", "posts/nnreg/index.ipynb"],
        )

    def test_accepts_direct_notebook_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "posts" / "demo"
            folder.mkdir(parents=True)
            (folder / "index.ipynb").write_text("{}")

            paths = self.executor.resolve_selectors(["posts/demo/index.ipynb"], root)

        self.assertEqual(paths[0].relative_to(tmp).as_posix(), "posts/demo/index.ipynb")


if __name__ == "__main__":
    unittest.main()
