"""When Portuguese joins numeral classes with "e".

Source: Celso Cunha & Lindley Cintra, "Nova Gramática do Português
Contemporâneo" (1984), p. 372:

    "Não se emprega a conjunção entre os milhares e as centenas, salvo
     quando o número terminar numa centena com dois zeros"

so 1892 is "mil oitocentos e noventa e dois" but 1800 is "mil e oitocentos".
Ciberdúvidas da Língua Portuguesa (ISCTE-IUL, resposta 34389) states the other
half of the rule: the conjunction also joins the two rightmost classes when
the second "começa por zero" -- "mil e vinte", "mil e um", "dois milhões e
sete mil".

Combining both: the remainder takes "e" when it is **below 100** or is a
**whole number of hundreds**, and takes none otherwise. The library had the
rule implemented but disabled for Portuguese, so every round-hundred
remainder lost its conjunction ("mil quinhentos" for 1500).

Both sources are archived under papers/linguistics/pt/.
"""
import unittest

from ovos_number_parser import pronounce_number


class TestConjunctionRequired(unittest.TestCase):
    """Remainder below 100, or a whole number of hundreds."""

    ROUND_HUNDREDS = [
        (1100, "mil e cem"),
        (1200, "mil e duzentos"),
        (1500, "mil e quinhentos"),
        (1800, "mil e oitocentos"),      # Cunha & Cintra's own example
        (2100, "dois mil e cem"),
        (2500, "dois mil e quinhentos"),
        (1000100, "um milhão e cem"),
    ]

    BELOW_HUNDRED = [
        (1001, "mil e um"),              # Ciberdúvidas' example
        (1005, "mil e cinco"),
        (1020, "mil e vinte"),           # Ciberdúvidas' example
        (1050, "mil e cinquenta"),
    ]

    def test_round_hundred_remainder_takes_conjunction(self):
        for value, expected in self.ROUND_HUNDREDS:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "pt"), expected)

    def test_sub_hundred_remainder_takes_conjunction(self):
        for value, expected in self.BELOW_HUNDRED:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "pt"), expected)


class TestConjunctionOmitted(unittest.TestCase):
    """Any other remainder carries its own "e" and takes none after the scale."""

    CASES = [
        (1101, "mil cento e um"),
        (1150, "mil cento e cinquenta"),
        (1250, "mil duzentos e cinquenta"),
        (1501, "mil quinhentos e um"),
        (1892, "mil oitocentos e noventa e dois"),   # Cunha & Cintra
    ]

    def test_structured_remainder_has_no_conjunction(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "pt"), expected)


class TestBothVariants(unittest.TestCase):
    """The rule is orthographic, so it holds for pt-PT and pt-BR alike."""

    def test_variants_agree_on_the_conjunction(self):
        for value in (1500, 1800, 1001, 1250, 1892):
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "pt-PT"),
                                 pronounce_number(value, "pt-BR"))


class TestRoundTrip(unittest.TestCase):
    """What we say must be what we can read back."""

    def test_spoken_forms_parse_back(self):
        from ovos_number_parser import extract_number
        for value in (1001, 1050, 1100, 1200, 1500, 1800, 1892, 2500):
            with self.subTest(value=value):
                spoken = pronounce_number(value, "pt")
                self.assertEqual(extract_number(spoken, "pt"), value)
