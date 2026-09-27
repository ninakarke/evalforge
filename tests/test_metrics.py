import unittest

from evalforge.metrics import context_precision, context_recall, exact_match, token_f1


class MetricsTests(unittest.TestCase):
    def test_exact_match_normalizes_case_and_punctuation(self):
        self.assertEqual(exact_match("Hello, WORLD!", "hello world"), 1.0)

    def test_token_f1_rewards_partial_overlap(self):
        self.assertAlmostEqual(token_f1("red green blue", "red green"), 0.8)

    def test_context_precision(self):
        self.assertEqual(context_precision([{"relevant": True}, {"relevant": False}]), 0.5)

    def test_context_recall_uses_reference_count(self):
        self.assertEqual(context_recall([{"relevant": True}], 2), 0.5)


if __name__ == "__main__":
    unittest.main()
