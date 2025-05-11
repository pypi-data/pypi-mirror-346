import unittest
from maybankpdf2json.extractor import MaybankPdf2Json
import os


class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.test_pdf_path = os.path.join(os.path.dirname(__file__), "test.pdf")
        self.test_password = "04Nov1997"  # Update with actual test password
        with open(self.test_pdf_path, "rb") as f:
            self.extractor = MaybankPdf2Json(f, self.test_password)
            self.data = self.extractor.json()

    def test_output_is_list(self):
        self.assertIsInstance(self.data, list)

    def test_transaction_count(self):
        self.assertEqual(len(self.data), 47)

    def test_first_item_keys_and_types(self):
        first = self.data[0]
        self.assertIn("desc", first)
        self.assertIn("bal", first)
        self.assertIn("trans", first)
        self.assertIn("date", first)
        self.assertIsInstance(first["desc"], str)
        self.assertIsInstance(first["bal"], float)
        self.assertIsInstance(first["trans"], (int, float))
        self.assertIsInstance(first["date"], str)

    def test_first_transaction_values(self):
        first = self.data[0]
        self.assertEqual(first["desc"], "BEGINNING BALANCE")
        self.assertEqual(first["bal"], 3285.77)
        self.assertEqual(first["trans"], 0)
        self.assertEqual(first["date"], "01/09/24")

    def test_specific_transaction(self):
        t = self.data[10]
        self.assertEqual(
            t["desc"],
            "FPX PAYMENT FR A/ 2392442593 * PACIFIC & ORIENT INS 2409151125380674",
        )
        self.assertEqual(t["bal"], 2395.67)
        self.assertEqual(t["trans"], -222.1)
        self.assertEqual(t["date"], "15/09/24")


if __name__ == "__main__":
    unittest.main()
