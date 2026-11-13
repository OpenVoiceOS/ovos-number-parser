"""Fourteen and the -teen fractions in Portuguese.

pt-BR writes "quatorze" and pt-PT writes "catorze", and both variants read
both forms. A pt-BR fraction takes the pt-BR spelling of its cardinal. The
numbers_pt module docstring cites the sources.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits, pronounce_fraction, pronounce_number


class TestFourteen(unittest.TestCase):
    def test_writer(self):
        for lang, word in [("pt-PT", "catorze"), ("pt-BR", "quatorze")]:
            with self.subTest(lang=lang):
                self.assertEqual(pronounce_number(14, lang=lang), word)
                self.assertEqual(pronounce_number(1014, lang=lang), "mil e " + word)
                self.assertEqual(pronounce_number(214, lang=lang), "duzentos e " + word)

    def test_both_variants_read_both_forms(self):
        for lang in ("pt-PT", "pt-BR"):
            for text, value in [("catorze", 14), ("quatorze", 14),
                                ("cento e quatorze", 114), ("dois mil e catorze", 2014)]:
                with self.subTest(lang=lang, text=text):
                    self.assertEqual(extract_number(text, lang=lang), value)
            with self.subTest(lang=lang):
                self.assertEqual(numbers_to_digits("quatorze e catorze", lang=lang),
                                 "14 e 14")

    def test_fraction_spelling_follows_the_variant(self):
        rows = {"pt-PT": {14: "catorze avos", 16: "dezasseis avos",
                          17: "dezassete avos", 19: "dezanove avos"},
                "pt-BR": {14: "quatorze avos", 16: "dezesseis avos",
                          17: "dezessete avos", 19: "dezenove avos"}}
        for lang, words in rows.items():
            for den, word in words.items():
                with self.subTest(lang=lang, den=den):
                    self.assertEqual(pronounce_fraction(f"1/{den}", lang=lang), "um " + word)
                    # each spelling reads back in both variants
                    for reader in rows:
                        self.assertAlmostEqual(extract_number("três " + word, lang=reader),
                                               3 / den)


if __name__ == "__main__":
    unittest.main()
