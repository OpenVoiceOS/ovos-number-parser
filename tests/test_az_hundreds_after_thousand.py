import unittest

from ovos_number_parser import extract_number


class TestAzerbaijaniHundredsAfterThousand(unittest.TestCase):
    def test_bare_hundred_after_thousand_adds(self):
        self.assertEqual(extract_number("min yüz", lang="az"), 1100)
        self.assertEqual(extract_number("iki min yüz", lang="az"), 2100)

    def test_multiplier_uses_unchanged(self):
        self.assertEqual(extract_number("iki yüz", lang="az"), 200)
        self.assertEqual(extract_number("yüz min", lang="az"), 100000)
        self.assertEqual(extract_number("min", lang="az"), 1000)


if __name__ == "__main__":
    unittest.main()
