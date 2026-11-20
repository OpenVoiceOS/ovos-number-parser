"""numbers_to_digits reads Portuguese "e meio" after a scale noun as
extract_number does: half of that noun. After the numeral "mil" the half is
half of one.

"Um milhão e meio" is 1500000 and a decimal needs the decimal marker
("um milhão vírgula cinco" is 1000000.5); the numbers_pt module docstring
states the rule. Expected values are hand arithmetic: the scale times 1.5,
plus the count before the scale.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


class TestNumbersToDigitsScaleAndAHalf(unittest.TestCase):
    #: text, expected output, language tag
    ROWS = [("um milhão e meio", "1500000", "pt-PT"),
            ("dois milhões e meio", "2500000", "pt-PT"),
            ("mil milhões e meio", "1500000000", "pt-PT"),
            ("um bilião e meio", "1500000000000", "pt-PT"),
            ("vendeu um milhão e meio de discos",
             "vendeu 1500000 de discos", "pt-PT"),
            ("menos um milhão e meio", "-1500000", "pt-PT"),
            ("um milhão e meio", "1500000", "pt-BR"),
            ("dois bilhões e meio", "2500000000", "pt-BR"),
            ("um milhão e meia", "1500000", "pt-BR"),
            ("dois milhões e meio e mais nada",
             "2500000 e mais nada", "pt-PT")]

    def test_half_of_the_scale(self):
        for text, expected, lang in self.ROWS:
            with self.subTest(text=text, lang=lang):
                self.assertEqual(numbers_to_digits(text, lang=lang), expected)

    def test_agrees_with_extract_number(self):
        for text, expected, lang in self.ROWS:
            with self.subTest(text=text, lang=lang):
                digits = [w for w in expected.split()
                          if w.lstrip("-").isdigit()]
                self.assertEqual([str(extract_number(text, lang=lang))],
                                 digits)

    def test_the_decimal_reading_needs_the_marker(self):
        for lang in ("pt-PT", "pt-BR"):
            with self.subTest(lang=lang):
                self.assertEqual(
                    numbers_to_digits("um milhão vírgula cinco", lang=lang),
                    "1000000.5")

    def test_a_half_after_a_number_below_a_thousand_stays_a_word(self):
        # extract_number reads "dois e meio" as 2.5; numbers_to_digits
        # writes the whole number in digits and keeps the fraction word
        for text, expected in [("dois e meio", "2 e meio"),
                               ("cem e meio", "100 e meio"),
                               ("mil e quinhentos e meio", "1500 e meio")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt"), expected)

    def test_a_half_after_a_noun_stays_a_word(self):
        # the half is of the noun, "hora", and no part of the number
        self.assertEqual(numbers_to_digits("uma hora e meia", lang="pt"),
                         "1 hora e meia")

    def test_a_half_after_mil_stays_a_word(self):
        # "mil" is a numeral: "mil e meio" is 1000.5 in extract_number, and
        # here the half keeps its word as after any other numeral
        for text, expected, value in [("mil e meio", "1000 e meio", 1000.5),
                                      ("mil e meia", "1000 e meia", 1000.5),
                                      ("dois mil e meio", "2000 e meio", 2000.5)]:
            for lang in ("pt-PT", "pt-BR"):
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(numbers_to_digits(text, lang=lang), expected)
                    self.assertEqual(extract_number(text, lang=lang), value)

    def test_the_half_does_not_cross_another_word(self):
        for text, expected in [
                ("mil euros e meio", "1000 euros e meio"),
                ("comprei mil livros e meio quilo de café",
                 "comprei 1000 livros e meio quilo de café"),
                ("um milhão de pessoas e meia hora",
                 "1000000 de pessoas e meia hora")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt"), expected)

    def test_only_the_half_is_of_the_scale(self):
        # extract_number adds a quarter after a scale as a quarter of one
        # ("dois milhões e um quarto" = 2000000.25), so the quarter keeps
        # its fraction word here too
        for text, expected in [("dois milhões e um quarto",
                                "2000000 e 1 quarto"),
                               ("dois milhões e quarto",
                                "2000000 e quarto")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt"), expected)


    def test_the_half_of_a_scale_needs_the_joiner(self):
        for text, expected in [("um milhão meio", "1000000 meio"),
                               ("um milhão mais meio", "1000000 mais meio")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt"), expected)

    def test_a_half_before_a_noun_counts_that_noun(self):
        # "meia dúzia" is half a dozen: a thousand and six eggs, not 1500
        for text, expected in [
                ("mil e meia dúzia de ovos", "1006 de ovos"),
                ("um milhão e meio quilo", "1000000 e meio quilo")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt"), expected)


class TestFractionPastTheFloatRange(unittest.TestCase):
    """A fraction whose whole part has no float writes its count in digits
    and keeps the fraction words, as a smaller one does: it raises
    nothing."""

    def test_the_count_keeps_its_digits(self):
        for text, expected, langs in (
                ("9" * 309 + " e meio", "9" * 309 + " e meio",
                 ("pt-PT", "pt-BR", "pt")),
                ("1" + "0" * 400 + " e meio", "1" + "0" * 400 + " e meio",
                 ("pt-PT", "pt-BR", "pt")),
                ("9" * 400 + " e um quarto", "9" * 400 + " e 1 quarto",
                 ("pt-PT",)),
                ("nove centiliões e um quarto",
                 str(9 * 10 ** 600) + " e 1 quarto", ("pt-PT", "pt"))):
            for lang in langs:
                with self.subTest(text=text[-16:], lang=lang):
                    self.assertEqual(numbers_to_digits(text, lang=lang), expected)


if __name__ == "__main__":
    unittest.main()
