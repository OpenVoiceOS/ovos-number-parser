"""Portuguese "e meio" after a scale noun is half of that noun.

"Mil" is a numeral, not a noun, so "mil e meio" is 1000.5; the numbers_pt
module docstring cites the sources.

Owner ruling for this repository: "1000000.5 would be 'um milhão virgula
cinco'". So "um milhão e meio" is 1500000, and the decimal reading needs the
decimal marker. Expected values are hand arithmetic: the scale times 1.5.
"""
import unittest

from ovos_number_parser import extract_number


class TestScaleAndAHalf(unittest.TestCase):
    #: text, value, language tag
    ROWS = [("um milhão e meio", 1_500_000, "pt-PT"),
            ("dois milhões e meio", 2_500_000, "pt-PT"),
            ("vendeu um milhão e meio de discos", 1_500_000, "pt-PT"),
            ("mil milhões e meio", 1_500_000_000, "pt-PT"),
            ("dois mil milhões e meio", 2_500_000_000, "pt-PT"),
            ("um bilião e meio", 1_500_000_000_000, "pt-PT"),
            ("dois biliões e meio", 2_500_000_000_000, "pt-PT"),
            ("um milhão e meio", 1_500_000, "pt-BR"),
            ("dois bilhões e meio", 2_500_000_000, "pt-BR")]

    def test_half_of_the_scale(self):
        for text, value, lang in self.ROWS:
            with self.subTest(text=text, lang=lang):
                got = extract_number(text, lang=lang)
                self.assertEqual(got, value)
                self.assertIsInstance(got, int)

    def test_a_half_after_mil_is_half_of_one(self):
        # "mil" is a numeral, not a noun: the half after it is half of one,
        # as after "dois"; the value is the thousands plus 0.5
        for text, value in [("mil e meio", 1000.5), ("mil e meia", 1000.5),
                            ("dois mil e meio", 2000.5),
                            ("cem mil e meio", 100000.5)]:
            for lang in ("pt-PT", "pt-BR"):
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(extract_number(text, lang=lang), value)

    def test_the_last_scale_word_decides(self):
        # "mil milhões" ends on the noun "milhões": half of 10 ** 9
        self.assertEqual(extract_number("dois mil milhões e meio", lang="pt-PT"),
                         2_500_000_000)

    def test_the_decimal_reading_needs_the_marker(self):
        self.assertEqual(extract_number("um milhão vírgula cinco", lang="pt"),
                         1_000_000.5)

    def test_a_half_after_a_number_below_a_thousand_is_still_a_half(self):
        for text, value in [("dois e meio", 2.5), ("dez e meio", 10.5),
                            ("cem e meio", 100.5),
                            ("uma hora e meia", 1.5)]:
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="pt"), value)

    def test_half_before_the_scale_still_multiplies(self):
        self.assertEqual(extract_number("meio milhão", lang="pt"), 500_000)

    def test_the_half_does_not_cross_another_word(self):
        # extract_number reads one number; a noun between the scale and
        # "e meio" ends the scale run, so the half adds as it does on its own
        for text, value in [("comprei mil livros e meio quilo de café", 1000.5),
                            ("mil euros e meio", 1000.5),
                            ("um milhão de pessoas e meia hora", 1000000.5)]:
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="pt"), value)

    def test_only_the_half_is_of_the_scale(self):
        # the ruling names "e meio" only; a quarter keeps its reading
        for text, value in [("dois milhões e quarto", 2000000.25),
                            ("dois mil e terço", 2000 + 1 / 3)]:
            with self.subTest(text=text):
                self.assertAlmostEqual(extract_number(text, lang="pt"), value)


if __name__ == "__main__":
    unittest.main()
