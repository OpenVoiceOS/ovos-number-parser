import unittest

from ovos_number_parser.numbers_pl import (extract_number_pl,
                                           pronounce_number_pl)


class TestPolishThousandGrouping(unittest.TestCase):
    def test_explicit_one_thousand_compound(self):
        # "jeden tysiąc" (explicit one thousand) must keep its 1000 when
        # followed by lower-order groups
        self.assertEqual(extract_number_pl("jeden tysiąc"), 1000)
        self.assertEqual(extract_number_pl("jeden tysiąc dwieście"), 1200)
        self.assertEqual(
            extract_number_pl("jeden tysiąc dwieście trzydzieści cztery"),
            1234)
        self.assertEqual(extract_number_pl("milion"), 1000000)

    def test_negative_compound_keeps_sign(self):
        self.assertEqual(
            extract_number_pl(
                "minus jeden tysiąc dwieście trzydzieści cztery"), -1234)
        self.assertEqual(extract_number_pl("minus tysiąc"), -1000)
        self.assertEqual(extract_number_pl("minus milion"), -1000000)

    def test_signed_roundtrip_to_one_million(self):
        bad = []
        for n in list(range(0, 4000)) + list(range(4000, 1000001, 997)):
            for m in (n, -n):
                if extract_number_pl(pronounce_number_pl(m)) != m:
                    bad.append(m)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
