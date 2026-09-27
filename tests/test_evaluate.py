import json
import tempfile
import unittest
from pathlib import Path

from evalforge.evaluate import evaluate_dataset, load_dataset


class EvaluationTests(unittest.TestCase):
    def test_sample_dataset_produces_stable_report(self):
        root = Path(__file__).parents[1]
        with (root / "examples" / "sample.json").open(encoding="utf-8") as handle:
            report = evaluate_dataset(json.load(handle))
        self.assertEqual(report["cases"], 3)
        self.assertEqual(report["metrics"]["answer_exact_match"], 0.666667)
        self.assertEqual(report["metrics"]["context_precision"], 0.5)

    def test_invalid_dataset_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text(json.dumps({"name": "bad"}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_dataset(path)


if __name__ == "__main__":
    unittest.main()
