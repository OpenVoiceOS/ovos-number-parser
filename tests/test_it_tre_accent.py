"""Italian compounds of "tre" carry a written acute accent.

Accademia della Crusca, consulenza 1077 ("Quarantaquattro gatti in fila per
sei col resto di due, o di quando e come scrivere i numeri in lettere"):

    "I composti di tre si scrivono più correttamente con l'accento; ventitré,
     trentatré, centotré, duemilatré."

so every number whose final digit is 3 -- when that 3 sits at the end of a
longer word -- ends in "-tré". The standalone "tre" (the number 3 itself)
takes no accent. The library wrote the bare "tre" everywhere ("ventitre").

Note num2words is itself inconsistent here (it accents "ventitré" but writes
"centoventitre"); ICU and Crusca agree that the accent is always required, so
the expected values follow Crusca. Source archived under
papers/linguistics/it/.
"""
import unittest

from ovos_number_parser import pronounce_number, extract_number


class TestCompoundsOfTreAreAccented(unittest.TestCase):
    CASES = [
        (23, "ventitré"),
        (33, "trentatré"),
        (43, "quarantatré"),
        (53, "cinquantatré"),
        (63, "sessantatré"),
        (73, "settantatré"),
        (83, "ottantatré"),
        (93, "novantatré"),
    ]

    def test_tens_compounds(self):
        for value, expected in self.CASES:
            with self.subTest(value=value):
                self.assertEqual(pronounce_number(value, "it"), expected)

    def test_compound_inside_hundreds(self):
        # the fused tens-unit still gets the accent within a larger number
        self.assertEqual(pronounce_number(123, "it"), "cento ventitré")
        self.assertEqual(pronounce_number(2023, "it"), "duemila, ventitré")


class TestBareTreHasNoAccent(unittest.TestCase):
    def test_three_is_plain(self):
        self.assertEqual(pronounce_number(3, "it"), "tre")

    def test_words_containing_tre_are_untouched(self):
        # 13, 30, 300, 3000 contain "tre" but not as a final unit digit
        self.assertEqual(pronounce_number(13, "it"), "tredici")
        self.assertEqual(pronounce_number(30, "it"), "trenta")
        self.assertEqual(pronounce_number(300, "it"), "trecento")
        self.assertEqual(pronounce_number(3000, "it"), "tremila")


class TestParsingPermissive(unittest.TestCase):
    """Both accented and bare spellings parse -- ASR/typing drop the accent."""

    def test_both_forms(self):
        for spelled, value in [("ventitré", 23), ("ventitre", 23),
                              ("trentatré", 33), ("trentatre", 33)]:
            with self.subTest(spelled=spelled):
                self.assertEqual(extract_number(spelled, "it"), value)


class TestRoundTrip(unittest.TestCase):
    def test_round_trip(self):
        for value in [3, 23, 33, 93, 123, 333, 1003, 2023, 3, 300, 3000]:
            with self.subTest(value=value):
                spoken = pronounce_number(value, "it")
                self.assertEqual(extract_number(spoken, "it"), value)
