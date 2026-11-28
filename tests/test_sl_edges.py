"""Edge-path tests for the Slovenian number module."""
import unittest

from ovos_number_parser import extract_number, is_ordinal

from ovos_number_parser.numbers_sl import nice_number_sl, pronounce_number_sl


class TestSlovenianEdges(unittest.TestCase):
    def test_decimal_digit_run_stops_at_word(self):
        self.assertEqual(extract_number("pet celih dve mačke", lang="sl"), 5.2)

    def test_long_scale_pronounce(self):
        self.assertEqual(pronounce_number_sl(1000000, short_scale=False),
                         "milijon")

    def test_scientific(self):
        spoken = pronounce_number_sl(2e100, scientific=True)
        self.assertIn("krat deset na", spoken)

    def test_nice_number(self):
        self.assertEqual(nice_number_sl(0.5), "1 polovica")
        self.assertEqual(nice_number_sl(4.5, speech=False), "4 1/2")

    def test_declined_scale_words(self):
        self.assertEqual(extract_number("pet milijonov", lang="sl"), 5000000)
        self.assertEqual(extract_number("trije milijoni", lang="sl"), 3000000)

    def test_ordinal_pronounce_flag(self):
        self.assertEqual(pronounce_number_sl(3, ordinals=True), "tretji")
        self.assertEqual(pronounce_number_sl(21, ordinals=True),
                         "enaindvajseti")


class TestSlovenianPronounceLegacy(unittest.TestCase):
    """Anchors for the plural/declension branches of pronounce_number_sl."""

    def test_decimals(self):
        self.assertEqual(pronounce_number_sl(5.2), "pet celih dve")
        self.assertEqual(pronounce_number_sl(-5.2), "minus pet celih dve")
        self.assertEqual(pronounce_number_sl(2.5), "dve celi pet")

    def test_million_declension(self):
        self.assertEqual(pronounce_number_sl(2000000), "dva milijona")
        self.assertEqual(pronounce_number_sl(3000000), "tri milijoni")
        self.assertEqual(pronounce_number_sl(5000000), "pet milijonov")

    def test_long_scale(self):
        self.assertEqual(
            pronounce_number_sl(1000000000, short_scale=False), "milijarda")
        self.assertEqual(extract_number("milijarda", lang="sl"), 1000000000)
        self.assertEqual(
            extract_number("dva bilijona", short_scale=False, lang="sl"),
            2000000000000)

    def test_large_composite_round_trip(self):
        for n in (1234567, 2000001, 100100100):
            spoken = pronounce_number_sl(n)
            self.assertEqual(extract_number(spoken, lang="sl"), n, spoken)


class TestSlovenianLongScaleMixedMagnitudes(unittest.TestCase):
    """Long-scale groups spanning both the milijarda (10^9) and milijon (10^6)
    tiers must emit both tiers.

    A million-group value (0..999999) carries a 'milijarda' part (its thousands)
    and a 'milijon' part (its remainder); the remainder used to be dropped, so
    281 407 million came out as '... milijard' with the '407 milijonov' lost.
    """

    def test_milijarda_and_milijon_both_emitted(self):
        # 1 milijarda + 407 milijonov
        self.assertEqual(
            pronounce_number_sl(1407000000, short_scale=False),
            "milijarda štiristo sedem milijonov")

    def test_full_mixed_magnitude_number(self):
        self.assertEqual(
            pronounce_number_sl(281407561516, short_scale=False),
            "dvesto enainosemdeset milijard štiristo sedem milijonov "
            "petsto enainšestdeset tisoč petsto šestnajst")

    def test_bilijon_group_keeps_milijon_remainder(self):
        self.assertEqual(
            pronounce_number_sl(2000407000000, short_scale=False),
            "dva bilijona štiristo sedem milijonov")

    def test_long_scale_round_trip_sweep(self):
        cases = [1407000000, 407000000, 281407561516, 2000407000000,
                 281000000000, 123456789012, 1000407000000, 999999000000,
                 5000005000000, 1002003000000]
        for n in cases:
            spoken = pronounce_number_sl(n, short_scale=False)
            self.assertEqual(
                extract_number(spoken, short_scale=False, lang="sl"), n, spoken)

    def test_pure_tiers_unchanged(self):
        # regression guard: single-tier groups keep their established forms
        anchors = {
            2000000000: "dve milijardi",
            3000000000: "tri milijarde",
            5000000000: "pet milijard",
            2000000: "dva milijona",
            3000000: "trije milijoni",
            5000000: "pet milijonov",
            1000000000: "milijarda",
        }
        for n, expected in anchors.items():
            self.assertEqual(
                pronounce_number_sl(n, short_scale=False), expected, n)


class TestSlovenianCompoundOrdinals(unittest.TestCase):
    """Ordinals above one hundred join the hundred to the remainder.

    The cardinal masculine allomorphs "dva"/"trije" that the number "two"
    and "three" take inside a hundreds group ("sto dve", "sto trije") must
    not leak into the ordinal, which stays "stodrugi"/"stotretji".
    """

    def test_hundred_ordinals(self):
        cases = [(101, "stoprvi"), (102, "stodrugi"), (103, "stotretji"),
                 (111, "stoenajsti"), (121, "stoenaindvajseti"),
                 (150, "stopetdeseti"), (203, "dvestotretji"),
                 (303, "tristotretji"),
                 (999, "devetstodevetindevetdeseti")]
        for n, expected in cases:
            self.assertEqual(pronounce_number_sl(n, ordinals=True),
                             expected, n)

    def test_hundred_ordinals_have_no_cardinal_suffix(self):
        # regression: 103rd was "stotretjije", 203rd "dvestotretjije"
        for n in (103, 203, 303, 403, 503):
            self.assertNotIn("je", pronounce_number_sl(n, ordinals=True)[-2:])

    def test_is_ordinal_recognises_compounds(self):
        self.assertEqual(is_ordinal("stoprvi", "sl"), 101)
        self.assertEqual(is_ordinal("stotretji", "sl"), 103)
        self.assertEqual(is_ordinal("dvestopetdeseti", "sl"), 250)
        self.assertFalse(is_ordinal("stotretjije", "sl"))
        self.assertFalse(is_ordinal("mačka", "sl"))

    def test_ordinal_round_trip(self):
        hundreds = range(200, 1000, 100)
        for n in [n for n in range(1, 1000) if n not in hundreds] + [1000]:
            spoken = pronounce_number_sl(n, ordinals=True)
            self.assertEqual(is_ordinal(spoken, "sl"), n, f"{n} -> {spoken!r}")

    def test_round_hundreds_read_back(self):
        for n in range(200, 1000, 100):
            with self.subTest(n=n):
                spoken = pronounce_number_sl(n, ordinals=True)
                self.assertEqual(is_ordinal(spoken, "sl"), n, f"{n} -> {spoken!r}")

    def test_the_millionth_reads_back(self):
        spoken = pronounce_number_sl(1000000, ordinals=True)
        self.assertEqual(is_ordinal(spoken, "sl"), 1000000, spoken)

    def test_extract_compound_ordinal_in_sentence(self):
        self.assertEqual(
            extract_number("stoprvi poskus", ordinals=True, lang="sl"), 101)
        self.assertEqual(
            extract_number("stopetdeseti dan", ordinals=True, lang="sl"), 150)


class TestSlovenianAdversarial(unittest.TestCase):
    def test_empty_and_junk(self):
        self.assertFalse(extract_number("", lang="sl"))
        self.assertFalse(extract_number("   ", lang="sl"))
        self.assertFalse(extract_number("brez številk tukaj", lang="sl"))

    def test_mixed_case(self):
        self.assertEqual(extract_number("PetInDvajset", lang="sl"), 25)
        self.assertEqual(extract_number("STO", lang="sl"), 100)

    def test_punctuation_affixes(self):
        self.assertEqual(extract_number("imam petindvajset!", lang="sl"), 25)
        self.assertEqual(extract_number("dvesto...", lang="sl"), 200)
        self.assertEqual(extract_number("koliko? sto", lang="sl"), 100)

    def test_dual_forms_in_context(self):
        # the dual: two takes "dva"/"dve" and dual noun agreement
        self.assertEqual(extract_number("dve uri", lang="sl"), 2)
        self.assertEqual(extract_number("dva dni", lang="sl"), 2)
        self.assertEqual(extract_number("dve minuti", lang="sl"), 2)
        self.assertEqual(extract_number("dva milijona", lang="sl"), 2000000)


if __name__ == "__main__":
    unittest.main()
