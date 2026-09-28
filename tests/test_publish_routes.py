import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "_scripts" / "publish_routes.py"
SPEC = importlib.util.spec_from_file_location("publish_routes", SCRIPT_PATH)
publish_routes = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(publish_routes)


class PublishRoutesTest(unittest.TestCase):
    def test_learning_route_replaces_courses_and_removes_source_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            site_dir = Path(tmp)
            courses_dir = site_dir / "courses"
            courses_dir.mkdir()
            courses_dir.joinpath("index.html").write_text("learning")
            courses_dir.joinpath("notebooks.html").write_text(
                '<a href="../courses/probability/index.html">Probability</a>'
            )
            courses_dir.joinpath("distributions.html").write_text(
                '<a href="/courses/probability/index.html">Random Variable</a>'
            )
            courses_dir.joinpath("intro-to-sampling.html").write_text(
                '<meta property="og:image" '
                'content="https://univ.ai/courses/intro-to-sampling-card.png">'
            )

            publish_routes.publish_learning(site_dir)

            self.assertFalse(courses_dir.exists())
            self.assertEqual(site_dir.joinpath("learning/index.html").read_text(), "learning")
            for page in ("notebooks.html", "distributions.html"):
                html = site_dir.joinpath("learning", page).read_text()
                self.assertIn('href="/learning/probability/index.html"', html)
                self.assertNotIn("../courses/", html)
            self.assertIn(
                'content="https://univ.ai/learning/intro-to-sampling-card.png"',
                site_dir.joinpath("learning/intro-to-sampling.html").read_text(),
            )

    def test_blog_route_copies_posts_and_rewrites_listing_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            site_dir = Path(tmp)
            posts_dir = site_dir / "posts"
            posts_dir.mkdir()
            posts_dir.joinpath("example.html").write_text("post")
            site_dir.joinpath("posts.html").write_text(
                '<html><head></head><body><a href="./posts/example.html">Example</a></body></html>'
            )

            publish_routes.publish_blog(site_dir)

            blog_index = site_dir.joinpath("blog/index.html").read_text()
            self.assertIn('<base href="/">', blog_index)
            self.assertIn('href="/blog/example.html"', blog_index)
            self.assertEqual(site_dir.joinpath("blog/example.html").read_text(), "post")


if __name__ == "__main__":
    unittest.main()
