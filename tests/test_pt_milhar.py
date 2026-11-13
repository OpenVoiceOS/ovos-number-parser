"""Portuguese "milhar" is a scale noun of 1000, and a plural scale word with
no count before it is no number.

Owner ruling for this repository: "um milhar e meio" is 1500. The
numbers_pt module docstring cites the sources. Expected values are hand
arithmetic: the count times 1000, plus the half of the noun or the group
after it.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits, pronounce_number

LANGS = ("pt-PT", "pt-BR")


class TestMilhar(unittest.TestCase):
    #: text, value
    ROWS = [("um milhar", 1000),
            ("dois milhares", 2000),
            ("um milhar e meio", 1500),
            ("dois milhares e meio", 2500),
            ("três milhares e quinhentos", 3500),
            ("vinte milhares de euros", 20000),
            ("cem milhares", 100000),
            ("menos dois milhares", -2000)]

    def test_milhar_is_a_thousand(self):
        for text, value in self.ROWS:
            for lang in LANGS:
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(extract_number(text, lang=lang), value)

    def test_numbers_to_digits(self):
        for text, expected in [("um milhar e meio", "1500"),
                               ("dois milhares de laranjas", "2000 de laranjas"),
                               ("comprou três milhares e quinhentos livros",
                                "comprou 3500 livros")]:
            for lang in LANGS:
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(numbers_to_digits(text, lang=lang), expected)

    def test_the_writer_keeps_mil(self):
        # "milhar" is read, never written
        for n in list(range(1000, 3001, 7)) + [10 ** 6 + 1000, 2 * 10 ** 9 + 5000]:
            for lang in LANGS:
                with self.subTest(n=n, lang=lang):
                    self.assertNotIn("milhar", pronounce_number(n, lang=lang))


class TestBarePluralScale(unittest.TestCase):
    BARE = ["milhares de pessoas", "milhões de pessoas", "há milhões de anos",
            "biliões de estrelas", "bilhões de estrelas", "milhares e milhares"]

    def test_a_plural_alone_is_no_number(self):
        for text in self.BARE:
            for lang in LANGS:
                with self.subTest(text=text, lang=lang):
                    self.assertIs(extract_number(text, lang=lang), False)
                    self.assertEqual(numbers_to_digits(text, lang=lang), text)

    def test_a_plural_after_a_count_is_a_number(self):
        for text, value, lang in [("dois milhões de pessoas", 2_000_000, "pt-PT"),
                                  ("dois milhões de pessoas", 2_000_000, "pt-BR"),
                                  ("mil milhões", 10 ** 9, "pt-PT"),
                                  ("três biliões", 3 * 10 ** 12, "pt-PT"),
                                  ("três bilhões", 3 * 10 ** 9, "pt-BR")]:
            with self.subTest(text=text, lang=lang):
                self.assertEqual(extract_number(text, lang=lang), value)

    def test_a_plural_alone_does_not_hide_a_later_number(self):
        self.assertEqual(extract_number("milhões de pessoas viram dois golos",
                                        lang="pt-PT"), 2)
        self.assertEqual(numbers_to_digits("milhões de pessoas viram dois golos",
                                           lang="pt-PT"),
                         "milhões de pessoas viram 2 golos")

    def test_an_earlier_number_is_not_the_count(self):
        # the count is the number word right before the plural; a number
        # further back counts something else
        for text, value in [("a equipa marcou dois golos perante milhares de adeptos", 2),
                            ("três dias depois chegaram milhares de refugiados", 3),
                            ("há dois anos milhões de pessoas", 2),
                            ("dois milhões e milhares de pessoas", 2_000_000)]:
            for lang in LANGS:
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(extract_number(text, lang=lang), value)

    def test_numbers_to_digits_keeps_a_plural_after_a_joiner(self):
        for lang in LANGS:
            with self.subTest(lang=lang):
                self.assertEqual(
                    numbers_to_digits("dois milhões e milhares de pessoas", lang=lang),
                    "2000000 e milhares de pessoas")

    def test_a_singular_scale_word_alone_still_reads(self):
        # only the plural names "a great many"; "milhão" alone is one million
        self.assertEqual(extract_number("milhão de pessoas", lang="pt-PT"),
                         1_000_000)


if __name__ == "__main__":
    unittest.main()
