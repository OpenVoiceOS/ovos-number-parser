import unittest

from ovos_number_parser import extract_number


class TestUkrainianNegativeCompound(unittest.TestCase):
    def test_negative_compound_numbers(self):
        self.assertEqual(extract_number("мінус тисяча двісті", lang="uk"), -1200)
        self.assertEqual(
            extract_number("мінус тисяча двісті тридцять чотири", lang="uk"), -1234)
        self.assertEqual(
            extract_number("мінус двісті тридцять чотири", lang="uk"), -234)
        self.assertEqual(extract_number("мінус двісті", lang="uk"), -200)


if __name__ == "__main__":
    unittest.main()
