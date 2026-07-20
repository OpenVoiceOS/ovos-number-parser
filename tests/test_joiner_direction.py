"""Direction rules for the additive joiner in Romance numerals.

Romance languages build the numbers between the round tens with an additive
joiner: "vinte **e** um", "vingt **et** un", "veinte **y** uno". The joiner is
not free word order -- it is *strictly descending*. The value written after the
joiner is always smaller than the value written before it:

    vinte e um        20 + 1     descending, one number  (21)
    cento e um       100 + 1     descending, one number  (101)
    mil e quinhentos 1000 + 500  descending, one number  (1500)

The reverse order is not a numeral at all. "três e vinte" is two separate
numbers -- most commonly a spoken clock time ("three twenty"), which is exactly
how a voice assistant receives it. Reading it as 23 silently corrupts the
utterance, and because the parsers share one engine the same misreading applied
to every Romance language at once.

The engine used to *discard* the joiner before parsing, which made the
distinction impossible to express: "três e vinte" and "vinte e três" both
reduced to a bare pair of numbers and accumulated additively to 23. The joiner
is now retained and the descending rule enforced.

One word wearing two hats
-------------------------
Romanian lists two words as joiners, and only one of them is additive:

    douăzeci **și** unu     20 + 1       additive, descending  (21)
    douăzeci **de** mii     20 x 1000    multiplicative, ASCENDING (20000)
    jumătate **de** milion  1/2 of 10^6  partitive, ASCENDING  (500000)

"de" is a preposition inserted before a scale word, not a joiner, so the value
after it is *larger* by design. It is declared in
``MULTIPLICATIVE_JOIN_WORD`` and exempted from the descending rule. Those cases
are asserted here so the distinction cannot be collapsed again.
"""
import unittest

from ovos_number_parser import extract_number, numbers_to_digits


#: (lang, ascending phrase, value of its first number, descending phrase, value)
#:
#: The ascending phrase must parse as ONLY its leading number -- the tail is a
#: separate number and must not be absorbed. The descending phrase must parse
#: as the single combined numeral.
JOINER_CASES = [
    # lang    ascending           head  descending          combined
    ("es", "tres y veinte", 3, "veinte y uno", 21),
    ("ca", "tres i vint", 3, "vint i un", 21),
    ("gl", "tres e vinte", 3, "vinte e un", 21),
    ("pt", "três e vinte", 3, "vinte e um", 21),
    ("fr", "trois et vingt", 3, "vingt et un", 21),
    ("it", "tre e venti", 3, "mille e cento", 1100),
    ("ro", "trei și douăzeci", 3, "douăzeci și unu", 21),
]


class TestJoinerIsDescending(unittest.TestCase):
    """An ascending pair is two numbers; a descending pair is one number."""

    def test_ascending_pair_is_not_absorbed(self):
        for lang, phrase, head, _, _ in JOINER_CASES:
            with self.subTest(lang=lang, phrase=phrase):
                self.assertEqual(extract_number(phrase, lang), head)

    def test_descending_pair_is_one_number(self):
        for lang, _, _, phrase, combined in JOINER_CASES:
            with self.subTest(lang=lang, phrase=phrase):
                self.assertEqual(extract_number(phrase, lang), combined)

    def test_ascending_tail_survives_digit_substitution(self):
        """The tail must still be in the output, not swallowed by the span.

        This is the failure that reached the date parser: collapsing
        "las tres y veinte" to "las 23" destroyed the minutes, so the time
        could not be recovered downstream.
        """
        for lang, phrase, head, _, _ in JOINER_CASES:
            with self.subTest(lang=lang, phrase=phrase):
                converted = numbers_to_digits(phrase, lang)
                self.assertIn(str(head), converted)
                # the trailing number survived as digits of its own
                self.assertTrue(
                    converted.rstrip().endswith("20")
                    or converted.rstrip().endswith("100"),
                    f"tail lost in {converted!r}")


class TestDescendingChains(unittest.TestCase):
    """Longer numerals chain several descending steps and must stay intact."""

    CHAINS = [
        ("pt", "duzentos e cinquenta e sete", 257),
        ("pt", "mil e quinhentos", 1500),
        ("pt", "cento e um", 101),
        ("pt", "quarenta e dois mil", 42000),
        ("pt", "um milhão e quinhentos mil", 1500000),
        ("es", "treinta y cuatro", 34),
        ("es", "ciento veintitrés", 123),
        ("fr", "quatre-vingt-dix", 90),
        ("ca", "vint-i-un", 21),
    ]

    def test_chains(self):
        for lang, phrase, expected in self.CHAINS:
            with self.subTest(lang=lang, phrase=phrase):
                self.assertEqual(extract_number(phrase, lang), expected)


class TestRomanianMultiplicativeDe(unittest.TestCase):
    """Romanian "de" is a preposition, not a joiner: it ascends by design."""

    def test_de_before_scale_multiplies(self):
        # "douăzeci de mii" is 20 x 1000, not 20 followed by 1000
        self.assertEqual(extract_number("douăzeci de mii", "ro"), 20000)

    def test_de_before_fraction_base(self):
        self.assertEqual(extract_number("jumătate de milion", "ro"), 500000)
        self.assertEqual(extract_number("jumătate de mie", "ro"), 500)

    def test_si_still_descends(self):
        self.assertEqual(extract_number("douăzeci și unu", "ro"), 21)
        # ... and still refuses to ascend
        self.assertEqual(extract_number("trei și douăzeci", "ro"), 3)


class TestNaturalSentences(unittest.TestCase):
    """Real sentences, which is where the ascending pair actually shows up."""

    SENTENCES = [
        # spoken clock times -- the original regression
        ("es", "el tren sale a las tres y veinte", 3),
        ("gl", "o tren sae ás tres e vinte", 3),
        ("pt", "o comboio sai às três e vinte", 3),
        ("fr", "le train part à trois et vingt", 3),
        # genuine numerals inside a sentence still read whole
        ("pt", "tenho vinte e um anos", 21),
        ("es", "tengo veinte y uno años", 21),
        ("pt", "custa mil e quinhentos euros", 1500),
        ("ro", "am cumpărat douăzeci de mii de pixeli", 20000),
    ]

    def test_sentences(self):
        for lang, sentence, expected in self.SENTENCES:
            with self.subTest(lang=lang, sentence=sentence):
                self.assertEqual(extract_number(sentence, lang), expected)


if __name__ == "__main__":
    unittest.main()
