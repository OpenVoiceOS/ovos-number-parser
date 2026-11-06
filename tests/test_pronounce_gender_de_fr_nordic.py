"""German, French, Danish, Swedish and Bokmål numbers agree with the noun.

``pronounce_number`` took ``gender=`` and gave the same word for every gender
in these languages. Sources for the expected values:

- de, fr, da and sv: the ICU RBNF rule sets read from ``unicode_rbnf``. Danish
  and Swedish name their common gender ``common`` and ``reale``; FEMININE
  selects it, because MASCULINE is the default and keeps its output;
- Danish ordinal "andet": RBNF da ``spellout-ordinal-neuter``;
- nb: Wiktionary "ett" (Norwegian Bokmål), usage notes: the numeral is
  "én, ei, ett", after Språkrådet "Et eller ett?".
"""
import unittest

from unicode_rbnf import RbnfEngine

from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.util import GrammaticalGender

M = GrammaticalGender.MASCULINE
F = GrammaticalGender.FEMININE
N = GrammaticalGender.NEUTRAL

NUMBERS = (1, 2, 21, 31, 101, 102)


class TestCardinalGenderMatchesRbnf(unittest.TestCase):

    def _check(self, lang, gender, ruleset, numbers=NUMBERS):
        engine = RbnfEngine.for_language(lang)
        for number in numbers:
            with self.subTest(lang=lang, gender=gender, number=number):
                expected = engine.format_number(
                    number, ruleset_names=[ruleset]).text
                self.assertEqual(pronounce_number(number, lang, gender=gender),
                                 expected)

    def test_german(self):
        self._check("de", F, "spellout-cardinal-feminine", NUMBERS + (1001,))
        self._check("de", N, "spellout-cardinal-neuter", NUMBERS + (1001,))

    def test_french(self):
        self._check("fr", F, "spellout-cardinal-feminine", NUMBERS + (1001,))

    def test_danish(self):
        self._check("da", F, "spellout-cardinal-common")
        self._check("da", N, "spellout-cardinal-neuter")

    def test_swedish(self):
        self._check("sv", F, "spellout-cardinal-reale", NUMBERS + (1001,))


class TestGenderLiterals(unittest.TestCase):

    def test_bokmal(self):
        self.assertEqual(pronounce_number(1, "nb", gender=F), "ei")
        self.assertEqual(pronounce_number(1, "nb", gender=N), "ett")
        self.assertEqual(pronounce_number(101, "nb", gender=N), "hundre og ett")

    def test_german_literals(self):
        self.assertEqual(pronounce_number(1, "de", gender=F), "eine")
        self.assertEqual(pronounce_number(1, "de", gender=N), "ein")
        self.assertEqual(pronounce_number(1000001, "de", gender=F),
                         "eine Million eine")

    def test_french_count_before_mille_stays(self):
        self.assertEqual(pronounce_number(21000, "fr", gender=F),
                         "vingt-et-un mille")
        self.assertEqual(pronounce_number(1000001, "fr", gender=F),
                         "un million une")

    def test_danish_neuter_ordinal(self):
        self.assertEqual(pronounce_ordinal(2, "da", gender=N), "andet")
        self.assertEqual(pronounce_ordinal(2, "da", gender=F), "anden")

    def test_masculine_default_unchanged(self):
        self.assertEqual(pronounce_number(1, "de"), "eins")
        self.assertEqual(pronounce_number(1, "fr", gender=M), "un")
        self.assertEqual(pronounce_number(1, "da"), "en")
        self.assertEqual(pronounce_number(1, "sv"), "ett")
        self.assertEqual(pronounce_number(1, "nb"), "en")

    def test_german_decimal_keeps_eins(self):
        self.assertEqual(pronounce_number(1.5, "de", gender=F, places=1),
                         "eins Komma fünf")


if __name__ == "__main__":
    unittest.main()
