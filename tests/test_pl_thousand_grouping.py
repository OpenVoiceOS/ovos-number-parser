import unittest

from ovos_number_parser import extract_number


class TestPolishThousandGrouping(unittest.TestCase):
    def test_explicit_one_thousand_compound(self):
        # "jeden tysiąc" (explicit one thousand) must keep its 1000 when
        # followed by lower-order groups
        self.assertEqual(extract_number("jeden tysiąc", lang="pl"), 1000)
        self.assertEqual(extract_number("jeden tysiąc dwieście", lang="pl"), 1200)
        self.assertEqual(
            extract_number("jeden tysiąc dwieście trzydzieści cztery", lang="pl"),
            1234)
        self.assertEqual(extract_number("milion", lang="pl"), 1000000)

    def test_negative_compound_keeps_sign(self):
        self.assertEqual(
            extract_number(
                "minus jeden tysiąc dwieście trzydzieści cztery", lang="pl"), -1234)
        self.assertEqual(extract_number("minus tysiąc", lang="pl"), -1000)
        self.assertEqual(extract_number("minus milion", lang="pl"), -1000000)


if __name__ == "__main__":
    unittest.main()
