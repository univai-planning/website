import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ContentMigrationManifestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest_path = ROOT / "internal_docs" / "content_migration_source_manifest.json"
        with open(manifest_path) as f:
            cls.manifest = json.load(f)

    def test_manifest_counts_match_selected_copy_set(self):
        counts = self.manifest["post_counts"]

        self.assertEqual(counts["total"], 86)
        self.assertEqual(counts["copied"], 81)
        self.assertEqual(counts["notebooks_total"], 72)
        self.assertEqual(counts["notebooks_copied"], 71)
        self.assertEqual(counts["markdown_qmd_total"], 14)
        self.assertEqual(counts["markdown_qmd_copied"], 10)
        self.assertEqual(len(self.manifest["software"]), 3)

    def test_boundary_exclusions_are_explicit(self):
        excluded = {
            post["slug"]: post["status"]
            for post in self.manifest["posts"]
            if post["status"].startswith("excluded")
        }

        self.assertEqual(
            excluded,
            {
                "cricsdb": "excluded_first_two",
                "seasons": "excluded_first_two",
                "votingforcongress": "excluded_last_three",
                "vizasstory": "excluded_last_three",
                "lawoflargenumbers": "excluded_last_three",
            },
        )

    def test_representative_files_exist_or_are_absent(self):
        self.assertTrue((ROOT / "courses" / "corr" / "index.ipynb").exists())
        self.assertTrue((ROOT / "courses" / "boxloop.md").exists())
        self.assertTrue((ROOT / "courses" / "software" / "awk.qmd").exists())
        self.assertFalse((ROOT / "courses" / "seasons").exists())
        self.assertFalse((ROOT / "courses" / "votingforcongress").exists())


if __name__ == "__main__":
    unittest.main()
