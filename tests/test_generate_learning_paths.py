import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_generator():
    path = ROOT / "_scripts" / "generate_learning_paths.py"
    spec = importlib.util.spec_from_file_location("generate_learning_paths", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class LearningPathGeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = load_generator()

    def test_learning_urls_follow_public_route(self):
        self.assertEqual(
            self.generator.get_post_url("probability"),
            "/learning/probability/",
        )
        self.assertEqual(
            self.generator.get_post_url("distributions"),
            "/learning/distributions.html",
        )

    def test_intro_to_sampling_order_is_explicit(self):
        yml_path = ROOT / "_learning-paths" / "intro-to-sampling.yml"
        config = self.generator.parse_yaml(yml_path.read_text())
        nodes = [node for part in config["parts"] for node in part["nodes"]]
        ordered = [node["slug"] for node in self.generator.toposort(nodes)]

        self.assertEqual(
            ordered,
            [
                "probability",
                "distributions",
                "distrib-example",
                "expectations",
                "samplingclt",
                "basicmontecarlo",
                "montecarlointegrals",
                "inversetransform",
                "rejectionsampling",
                "importancesampling",
            ],
        )


if __name__ == "__main__":
    unittest.main()
