"""Regression guard for the Romance "hundred" apocopation.

Several Romance languages read a bare 100 with a shortened form but use the
full form inside a compound: pt cem / cento e X, gl cen / cento e X, es cien /
ciento X, and likewise Asturian and Mirandese (cien / ciento X). Occitan,
Catalan and Romanian do not apocopate. A shared-vocabulary refactor can easily
flatten this, so both directions are pinned here.
"""
import unittest

from ovos_number_parser import pronounce_number, extract_number


class TestRomanceHundredApocopation(unittest.TestCase):
    # lang -> (bare-100 short form, a compound using the long form, its value)
    APOCOPATING = {
        "es": ("cien", "ciento uno", 101),
        "gl": ("cen", "cento e un", 101),
        "pt": ("cem", "cento e um", 101),
        "ast": ("cien", "ciento un", 101),
        "mwl": ("cien", "ciento i un", 101),
    }

    def test_bare_hundred_is_short_form(self):
        for lang, (short, _compound, _val) in self.APOCOPATING.items():
            self.assertEqual(pronounce_number(100, lang=lang), short,
                             f"{lang}: bare 100 must be {short!r}")

    def test_compound_hundred_uses_long_form(self):
        for lang, (short, compound, _val) in self.APOCOPATING.items():
            spoken = pronounce_number(101, lang=lang)
            self.assertTrue(spoken.startswith(compound.split()[0]),
                            f"{lang}: 101 {spoken!r} must use the long hundred form, "
                            f"not the bare {short!r}")
            self.assertNotEqual(spoken.split()[0], short,
                                f"{lang}: 101 must not start with the bare form {short!r}")

    def test_extract_both_forms(self):
        for lang, (short, compound, val) in self.APOCOPATING.items():
            self.assertEqual(extract_number(short, lang=lang), 100,
                             f"{lang}: {short!r} must extract to 100")
            self.assertEqual(extract_number(compound, lang=lang), val,
                             f"{lang}: {compound!r} must extract to {val}")

    def test_non_apocopating_use_full_form_throughout(self):
        # Occitan/Catalan use "cent" for both; Romanian "o sută".
        for lang in ("oc", "ca"):
            self.assertEqual(pronounce_number(100, lang=lang), "cent",
                             f"{lang}: 100 must be 'cent'")
            self.assertTrue(pronounce_number(101, lang=lang).startswith("cent"),
                            f"{lang}: 101 must still start with 'cent'")
        self.assertEqual(pronounce_number(100, lang="ro"), "o sută")


if __name__ == "__main__":
    unittest.main()
