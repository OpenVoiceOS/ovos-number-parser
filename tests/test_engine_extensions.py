"""Engine-level tests for the declarative NumberVocabulary knobs that model
scale linkers, multiplicative hundreds, articled "one <scale>" groups,
per-scale count gender, bare scale remainders and particle-based ordinals.

Each knob is exercised in isolation on a copy of the Galician vocabulary so
that the test asserts the knob's effect, not any single language's data.
"""
import unittest
from dataclasses import replace

from ovos_number_parser.numbers_gl import _GL
from ovos_number_parser.util import (GrammaticalGender, RomanceNumberExtractor)


def _engine(**overrides) -> RomanceNumberExtractor:
    return RomanceNumberExtractor(replace(_GL, **overrides))


class TestScaleOne(unittest.TestCase):
    def test_articled_one_scale(self):
        eng = _engine(SCALE_ONE={1000: "unha mil", 10 ** 6: "un millón especial"})
        self.assertEqual(eng.pronounce_number(1000), "unha mil")
        self.assertEqual(eng.pronounce_number(1_000_000), "un millón especial")
        # counts above one are untouched
        self.assertEqual(eng.pronounce_number(2000), "dous mil")

    def test_takes_precedence_over_no_prev_unit(self):
        # 1000 is in the Galician NO_PREV_UNIT list; SCALE_ONE must win
        eng = _engine(SCALE_ONE={1000: "unha mil"})
        self.assertEqual(eng.pronounce_number(1001), "unha mil e un")

    def test_default_unchanged(self):
        eng = _engine()
        self.assertEqual(eng.pronounce_number(1000), "mil")


class TestScaleLinker(unittest.TestCase):
    def test_linker_on_counts_ending_20_to_99(self):
        eng = _engine(SCALE_LINKER="de")
        self.assertEqual(eng.pronounce_number(20_000), "vinte de mil")
        self.assertEqual(eng.pronounce_number(45_000), "corenta e cinco de mil")

    def test_linker_on_round_hundred_counts(self):
        eng = _engine(SCALE_LINKER="de")
        self.assertEqual(eng.pronounce_number(100_000_000), "cen de millóns")

    def test_no_linker_below_twenty(self):
        eng = _engine(SCALE_LINKER="de")
        self.assertEqual(eng.pronounce_number(2000), "dous mil")
        self.assertEqual(eng.pronounce_number(15_000), "quince mil")
        # counts ending in 01-19 take no linker either
        self.assertEqual(eng.pronounce_number(101_000), "cento un mil")

    def test_default_no_linker(self):
        eng = _engine()
        self.assertEqual(eng.pronounce_number(20_000), "vinte mil")


class TestScaleGenders(unittest.TestCase):
    def test_count_agrees_with_scale_word(self):
        eng = _engine(SCALE_GENDERS={1000: GrammaticalGender.FEMININE})
        self.assertEqual(eng.pronounce_number(2000), "dúas mil")
        # other scales keep the default masculine agreement
        self.assertEqual(eng.pronounce_number(2_000_000), "dous millóns")

    def test_default_masculine(self):
        eng = _engine()
        self.assertEqual(eng.pronounce_number(2000), "dous mil")


class TestJoinerOnScaleRemainder(unittest.TestCase):
    def test_bare_remainder(self):
        eng = _engine(JOINER_ON_SCALE_REMAINDER=False)
        self.assertEqual(eng.pronounce_number(2001), "dous mil un")
        # the forced conjunction after the hundreds of a thousands-number
        # is suppressed too
        self.assertEqual(eng.pronounce_number(1234),
                         "mil douscentos trinta e catro")

    def test_default_keeps_conjunction(self):
        eng = _engine()
        self.assertEqual(eng.pronounce_number(2001), "dous mil e un")
        self.assertEqual(eng.pronounce_number(1234),
                         "mil douscentos e trinta e catro")


class TestMultiplyHundreds(unittest.TestCase):
    def test_hundred_word_multiplies_preceding_units(self):
        eng = _engine(MULTIPLY_HUNDREDS=True)
        self.assertEqual(eng.extract_number("dous cen"), 200)
        self.assertEqual(eng.extract_number("tres cen corenta e cinco"), 345)

    def test_bare_hundred_still_one_hundred(self):
        eng = _engine(MULTIPLY_HUNDREDS=True)
        self.assertEqual(eng.extract_number("cen"), 100)

    def test_higher_groups_untouched(self):
        # only the sub-hundred residue multiplies: 2000 + 3*100
        eng = _engine(MULTIPLY_HUNDREDS=True)
        self.assertEqual(eng.extract_number("dous mil tres cen"), 2300)

    def test_default_additive(self):
        eng = _engine()
        self.assertEqual(eng.extract_number("dous cen"), 102)


class TestOrdinalPrefix(unittest.TestCase):
    PREFIX = {GrammaticalGender.MASCULINE: "al", GrammaticalGender.FEMININE: "a"}

    def test_prefix_added(self):
        eng = _engine(ORDINAL_PREFIX=self.PREFIX)
        self.assertEqual(eng.pronounce_ordinal(2), "al segundo")
        self.assertEqual(
            eng.pronounce_ordinal(2, gender=GrammaticalGender.FEMININE),
            "a segunda")

    def test_unprefixed_values(self):
        eng = _engine(ORDINAL_PREFIX=self.PREFIX, ORDINAL_UNPREFIXED=[1])
        self.assertEqual(eng.pronounce_ordinal(1), "primeiro")
        self.assertEqual(eng.pronounce_ordinal(2), "al segundo")

    def test_prefix_applied_once_on_compounds(self):
        eng = _engine(ORDINAL_PREFIX=self.PREFIX)
        self.assertEqual(eng.pronounce_ordinal(1001), "al milésimo primeiro")

    def test_is_ordinal_strips_particles(self):
        eng = _engine(ORDINAL_PREFIX=self.PREFIX)
        self.assertEqual(eng.is_ordinal("al segundo"), 2)
        self.assertEqual(eng.is_ordinal("a segunda"), 2)
        self.assertFalse(eng.is_ordinal("al gato"))

    def test_default_no_prefix(self):
        eng = _engine()
        self.assertEqual(eng.pronounce_ordinal(2), "segundo")


class TestOrdinalCompoundCardinalTens(unittest.TestCase):
    def test_cardinal_tens_with_ordinal_unit(self):
        eng = _engine(ORDINAL_COMPOUND_CARDINAL_TENS=True)
        self.assertEqual(eng.pronounce_ordinal(21), "vinte e primeiro")

    def test_compound_unit_override(self):
        eng = _engine(ORDINAL_COMPOUND_CARDINAL_TENS=True,
                      ORDINAL_COMPOUND_UNITS={1: "primo"})
        self.assertEqual(eng.pronounce_ordinal(21), "vinte e primo")
        # the standalone ordinal keeps its own word
        self.assertEqual(eng.pronounce_ordinal(1), "primeiro")
        # the compound spelling is recognised during extraction
        self.assertEqual(eng.is_ordinal("primo"), 1)

    def test_exact_teen_entries_preferred(self):
        eng = _engine(ORDINAL_COMPOUND_CARDINAL_TENS=True)
        # the Galician table carries a single-word entry for 13
        self.assertEqual(eng.pronounce_ordinal(13), "decimoterceiro")

    def test_default_ordinal_tens_decomposition(self):
        eng = _engine()
        self.assertEqual(eng.pronounce_ordinal(21), "vixésimo primeiro")


class TestFractionOne(unittest.TestCase):
    def test_articled_fraction(self):
        eng = _engine(FRACTION_ONE={2: "unha media"})
        self.assertEqual(eng.pronounce_fraction("1/2"), "unha media")
        # only the numerator 1 uses the articled spelling
        self.assertEqual(eng.pronounce_fraction("3/2"), "tres medios")

    def test_numerator_gender(self):
        eng = _engine(FRACTION_NUMERATOR_GENDER=GrammaticalGender.FEMININE)
        self.assertEqual(eng.pronounce_fraction("2/3"), "dúas terzos")

    def test_default_unchanged(self):
        eng = _engine()
        self.assertEqual(eng.pronounce_fraction("1/2"), "un medio")
        self.assertEqual(eng.pronounce_fraction("2/3"), "dous terzos")


class TestNumbersToDigitsTrailingJoiner(unittest.TestCase):
    def test_trailing_joiner_left_in_text(self):
        eng = _engine()
        self.assertEqual(eng.numbers_to_digits("vinte e dous gatos e un can"),
                         "22 gatos e 1 can")
        # a joiner that does not extend the number stays in the sentence
        self.assertEqual(eng.numbers_to_digits("tres e logo catro"),
                         "3 e logo 4")


if __name__ == "__main__":
    unittest.main()
