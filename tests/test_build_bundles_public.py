import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BuildBundlesPublicTest(unittest.TestCase):
    def test_standalone_bundle_refresh_writes_public_routes(self):
        script = (ROOT / "_scripts" / "build_bundles_public.sh").read_text()

        self.assertIn("--content-root posts:posts:/posts", script)
        self.assertIn("--content-root posts:blog:/blog", script)
        self.assertIn("--content-root courses:learning:/learning", script)
        self.assertNotIn("courses:courses:/learning", script)
        self.assertNotIn("posts:posts:/posts:/blog", script)


if __name__ == "__main__":
    unittest.main()
