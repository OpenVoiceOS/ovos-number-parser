"""The Unicode RBNF fallback speaks the rule set of the requested gender.

``unicode_rbnf`` returns in ``FormatResult.text`` the output of the shortest
rule set name, so "spellout-ordinal-feminine" won over
"spellout-ordinal-masculine" and every Hindi ordinal came out feminine. The
expected strings are the output of the named rule set, read straight from
``unicode_rbnf``. The Hindi words follow Wiktionary "दूसरा" (Hindi ordinal
"second", an adjective in -ā whose feminine is "दूसरी"). Where the CLDR data
is wrong, the expected words come from Wiktionary: Belarusian "першы",
"другі", "пяты", Luxembourgish "éischt".
"""
import unittest

from unicode_rbnf import FormatPurpose, RbnfEngine

from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.util import GrammaticalGender

M = GrammaticalGender.MASCULINE
F = GrammaticalGender.FEMININE
N = GrammaticalGender.NEUTRAL


def _rbnf(lang, number, ruleset):
    engine = RbnfEngine.for_language(lang)
    return engine.format_number(number, ruleset_names=[ruleset]).text


class TestRbnfFallbackGender(unittest.TestCase):

    def test_hindi_ordinal_literals(self):
        self.assertEqual(pronounce_ordinal(2, "hi", gender=M), "दूसरा")
        self.assertEqual(pronounce_ordinal(2, "hi", gender=F), "दूसरी")
        self.assertEqual(pronounce_ordinal(2, "hi"), "दूसरा")
        self.assertEqual(pronounce_number(2, "hi", ordinals=True), "दूसरा")

    def test_russian_ordinal_literals(self):
        # Russian ordinals decline as adjectives: второй, вторая, второе
        self.assertEqual(pronounce_ordinal(2, "ru", gender=M), "второй")
        self.assertEqual(pronounce_ordinal(2, "ru", gender=F), "вторая")
        self.assertEqual(pronounce_ordinal(2, "ru", gender=N), "второе")

    def test_ordinal_rule_set_by_gender(self):
        for lang in ("hi", "vec", "ru", "fr", "es", "it"):
            for gender, name in ((M, "masculine"), (F, "feminine")):
                ruleset = f"spellout-ordinal-{name}"
                for number in (1, 2, 3, 21):
                    with self.subTest(lang=lang, gender=gender, number=number):
                        self.assertEqual(
                            pronounce_ordinal(number, lang, gender=gender),
                            _rbnf(lang, number, ruleset))

    def test_cardinal_rule_set_by_gender(self):
        for lang in ("be", "is", "mk", "sr", "lt"):
            for number in (1, 2, 21, 22):
                with self.subTest(lang=lang, number=number):
                    self.assertEqual(
                        pronounce_number(number, lang, gender=F),
                        _rbnf(lang, number, "spellout-cardinal-feminine"))
        for lang in ("be", "is", "mk"):
            with self.subTest(lang=lang, gender=N):
                self.assertEqual(
                    pronounce_number(1, lang, gender=N),
                    _rbnf(lang, 1, "spellout-cardinal-neuter"))

    def test_default_cardinal_keeps_counting_form(self):
        # spellout-numbering is the bare counting form; the masculine set of
        # Maltese is the form before a noun
        self.assertEqual(pronounce_number(2, "mt"),
                         _rbnf("mt", 2, "spellout-numbering"))

    def test_maltese_feminine_keeps_counting_form(self):
        # the CLDR feminine set holds the forms before a noun, and 2 to 10 do
        # not inflect for gender, so the feminine reads like the default
        for number in (3, 10, 11):
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "mt", gender=F),
                                 pronounce_number(number, "mt"))
        self.assertEqual(pronounce_number(3, "mt", gender=F), "tlieta")

    def test_maltese_feminine_one(self):
        # Wiktionary "wieħed": the feminine is "waħda"; a count before "elf"
        # keeps "wieħed" (CLDR spellout-cardinal-feminine)
        cases = {
            1: "waħda", 21: "waħda u għoxrin", 101: "mija u waħda",
            1001: "elf u waħda", 100001: "mitt elf u waħda",
            21000: "wieħed u għoxrin elf", 11: "ħdax", 111: "mija u ħdax",
            103: "mija u tlieta",
        }
        for number, expected in cases.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, "mt", gender=F),
                                 expected)
        self.assertEqual(pronounce_number(1, "mt"), "wieħed")

    def test_luxembourgish_feminine_ordinal(self):
        # Wiktionary "éischt": masculine éischten, neuter éischt; the feminine
        # after a determiner is éischt (déi éischt Kéier)
        self.assertEqual(pronounce_ordinal(1, "lb", gender=F), "éischt")
        self.assertEqual(pronounce_ordinal(1, "lb", gender=N), "éischt")
        self.assertEqual(pronounce_ordinal(1, "lb", gender=M), "éischten")

    def test_belarusian_ordinals(self):
        # the CLDR masculine set misspells 3 and 4 ("трэйці", "чацьверты"),
        # so the default keeps the engine default
        engine = RbnfEngine.for_language("be")
        for number in (1, 3, 4):
            with self.subTest(number=number):
                self.assertNotIn(pronounce_ordinal(number, "be"),
                                 ("трэйці", "чацьверты"))
                self.assertEqual(
                    pronounce_ordinal(number, "be"),
                    engine.format_number(number, FormatPurpose.ORDINAL).text)
        # Wiktionary "першы", "другі", "пяты"
        cases = {
            (1, F): "першая", (2, F): "другая", (5, F): "пятая",
            (1, N): "першае", (2, N): "другое", (5, N): "пятае",
        }
        for (number, gender), expected in cases.items():
            with self.subTest(number=number, gender=gender):
                self.assertEqual(pronounce_ordinal(number, "be", gender=gender),
                                 expected)

    def test_bosnian_feminine_rule_set_is_not_used(self):
        # the CLDR Bosnian feminine set spells 1 as the noun "jedinica"
        self.assertEqual(pronounce_number(1, "bs", gender=F),
                         _rbnf("bs", 1, "spellout-numbering"))
        self.assertEqual(pronounce_number(1, "bs", gender=N), "jedno")

    def test_language_without_gender_unchanged(self):
        self.assertEqual(pronounce_number(3, "ja", gender=F),
                         _rbnf("ja", 3, "spellout-numbering"))
        self.assertEqual(pronounce_ordinal(3, "ja", gender=F),
                         _rbnf("ja", 3, "spellout-ordinal"))


if __name__ == "__main__":
    unittest.main()
