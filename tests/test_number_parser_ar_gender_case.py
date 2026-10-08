"""Gender and case of Arabic cardinals and ordinals.

Every expected string is a literal taken from a published table, not from
the code under test:

- Karin C. Ryding, "A Reference Grammar of Modern Standard Arabic"
  (Cambridge UP, 2005), chapter 15: sections 1.2 to 1.8 for cardinals,
  sections 2.1 to 2.5 for ordinals.
- W. Wright, "A Grammar of the Arabic Language", 3rd ed. (1896), vol. 1,
  sections 319 to 330.
- English Wikipedia, "Arabic grammar", section Numerals.
- Arabic Wikipedia, "العدد والمعدود".
"""
import unittest

from ovos_number_parser import (extract_number, is_ordinal, pronounce_number,
                                pronounce_ordinal)
from ovos_number_parser.numbers_ar import (pronounce_number_ar,
                                           pronounce_ordinal_ar)
from ovos_number_parser.util import GrammaticalGender

M = GrammaticalGender.MASCULINE
F = GrammaticalGender.FEMININE

NUMBERS = list(range(1, 22)) + [30, 100, 103, 1000]

# (gender, case) -> number -> cardinal
CARDINALS = {
    (M, "nominative"): {
        1: "واحد", 2: "اثنان", 3: "ثلاثة", 4: "أربعة", 5: "خمسة",
        6: "ستة", 7: "سبعة", 8: "ثمانية", 9: "تسعة", 10: "عشرة",
        11: "أحد عشر", 12: "اثنا عشر", 13: "ثلاثة عشر", 14: "أربعة عشر",
        15: "خمسة عشر", 16: "ستة عشر", 17: "سبعة عشر", 18: "ثمانية عشر",
        19: "تسعة عشر", 20: "عشرون", 21: "واحد وعشرون", 30: "ثلاثون",
        100: "مئة", 103: "مئة وثلاثة", 1000: "ألف",
    },
    (M, "oblique"): {
        1: "واحد", 2: "اثنين", 3: "ثلاثة", 4: "أربعة", 5: "خمسة",
        6: "ستة", 7: "سبعة", 8: "ثمانية", 9: "تسعة", 10: "عشرة",
        11: "أحد عشر", 12: "اثني عشر", 13: "ثلاثة عشر", 14: "أربعة عشر",
        15: "خمسة عشر", 16: "ستة عشر", 17: "سبعة عشر", 18: "ثمانية عشر",
        19: "تسعة عشر", 20: "عشرين", 21: "واحد وعشرين", 30: "ثلاثين",
        100: "مئة", 103: "مئة وثلاثة", 1000: "ألف",
    },
    (F, "nominative"): {
        1: "واحدة", 2: "اثنتان", 3: "ثلاث", 4: "أربع", 5: "خمس",
        6: "ست", 7: "سبع", 8: "ثمان", 9: "تسع", 10: "عشر",
        11: "إحدى عشرة", 12: "اثنتا عشرة", 13: "ثلاث عشرة",
        14: "أربع عشرة", 15: "خمس عشرة", 16: "ست عشرة", 17: "سبع عشرة",
        18: "ثماني عشرة", 19: "تسع عشرة", 20: "عشرون",
        21: "واحدة وعشرون", 30: "ثلاثون", 100: "مئة", 103: "مئة وثلاث",
        1000: "ألف",
    },
    (F, "oblique"): {
        1: "واحدة", 2: "اثنتين", 3: "ثلاث", 4: "أربع", 5: "خمس",
        6: "ست", 7: "سبع", 8: "ثمان", 9: "تسع", 10: "عشر",
        11: "إحدى عشرة", 12: "اثنتي عشرة", 13: "ثلاث عشرة",
        14: "أربع عشرة", 15: "خمس عشرة", 16: "ست عشرة", 17: "سبع عشرة",
        18: "ثماني عشرة", 19: "تسع عشرة", 20: "عشرين",
        21: "واحدة وعشرين", 30: "ثلاثين", 100: "مئة", 103: "مئة وثلاث",
        1000: "ألف",
    },
}

# (gender, case) -> number -> ordinal; None means no cited form, so it raises
ORDINALS = {
    (M, "nominative"): {
        1: "الأول", 2: "الثاني", 3: "الثالث", 4: "الرابع", 5: "الخامس",
        6: "السادس", 7: "السابع", 8: "الثامن", 9: "التاسع", 10: "العاشر",
        11: "الحادي عشر", 12: "الثاني عشر", 13: "الثالث عشر",
        14: "الرابع عشر", 15: "الخامس عشر", 16: "السادس عشر",
        17: "السابع عشر", 18: "الثامن عشر", 19: "التاسع عشر",
        20: "العشرون", 21: "الحادي والعشرون", 30: "الثلاثون",
        100: "المئة", 1000: "الألف",
    },
    (M, "oblique"): {
        1: "الأول", 2: "الثاني", 3: "الثالث", 4: "الرابع", 5: "الخامس",
        6: "السادس", 7: "السابع", 8: "الثامن", 9: "التاسع", 10: "العاشر",
        11: "الحادي عشر", 12: "الثاني عشر", 13: "الثالث عشر",
        14: "الرابع عشر", 15: "الخامس عشر", 16: "السادس عشر",
        17: "السابع عشر", 18: "الثامن عشر", 19: "التاسع عشر",
        20: "العشرين", 21: "الحادي والعشرين", 30: "الثلاثين",
        100: "المئة", 103: None, 1000: "الألف",
    },
    (F, "nominative"): {
        1: "الأولى", 2: "الثانية", 3: "الثالثة", 4: "الرابعة",
        5: "الخامسة", 6: "السادسة", 7: "السابعة", 8: "الثامنة",
        9: "التاسعة", 10: "العاشرة", 11: "الحادية عشرة",
        12: "الثانية عشرة", 13: "الثالثة عشرة", 14: "الرابعة عشرة",
        15: "الخامسة عشرة", 16: "السادسة عشرة", 17: "السابعة عشرة",
        18: "الثامنة عشرة", 19: "التاسعة عشرة", 20: "العشرون",
        21: "الحادية والعشرون", 30: "الثلاثون", 100: "المئة", 103: None,
        1000: "الألف",
    },
    (F, "oblique"): {
        1: "الأولى", 2: "الثانية", 3: "الثالثة", 4: "الرابعة",
        5: "الخامسة", 6: "السادسة", 7: "السابعة", 8: "الثامنة",
        9: "التاسعة", 10: "العاشرة", 11: "الحادية عشرة",
        12: "الثانية عشرة", 13: "الثالثة عشرة", 14: "الرابعة عشرة",
        15: "الخامسة عشرة", 16: "السادسة عشرة", 17: "السابعة عشرة",
        18: "الثامنة عشرة", 19: "التاسعة عشرة", 20: "العشرين",
        21: "الحادية والعشرين", 30: "الثلاثين", 100: "المئة", 103: None,
        1000: "الألف",
    },
}

ARABIC_CODES = ["ar", "arb", "ars", "acw", "afb", "arz", "apc", "ajp", "acm",
                "ary", "aeb", "ayl", "ar-SA"]


class TestArabicCardinalGenderCase(unittest.TestCase):

    def test_every_cell(self):
        for (gender, case), table in CARDINALS.items():
            for number in NUMBERS:
                with self.subTest(gender=gender, case=case, number=number):
                    self.assertEqual(
                        pronounce_number(number, lang="ar", gender=gender,
                                         case=case), table[number])
                    self.assertEqual(
                        pronounce_number_ar(number, gender=gender, case=case),
                        table[number])

    def test_genitive_and_accusative_are_the_oblique(self):
        for gender in (M, F):
            for alias in ("genitive", "accusative"):
                for number in NUMBERS:
                    with self.subTest(gender=gender, case=alias,
                                      number=number):
                        self.assertEqual(
                            pronounce_number(number, lang="ar", gender=gender,
                                             case=alias),
                            CARDINALS[(gender, "oblique")][number])

    def test_gender_reaches_the_last_group(self):
        # the count before a scale word counts the masculine scale noun
        self.assertEqual(pronounce_number(3000, lang="ar", gender=F),
                         "ثلاثة آلاف")
        self.assertEqual(pronounce_number(1013, lang="ar", gender=F),
                         "ألف وثلاث عشرة")
        self.assertEqual(pronounce_number(28, lang="ar", gender=F),
                         "ثمان وعشرون")
        self.assertEqual(pronounce_number(22, lang="ar", gender=F,
                                          case="oblique"),
                         "اثنتين وعشرين")

    def test_plain_strings_select_the_gender(self):
        self.assertEqual(pronounce_number_ar(3, gender="feminine"), "ثلاث")
        self.assertEqual(pronounce_number_ar(3, gender="masculine"), "ثلاثة")

    def test_negative_feminine(self):
        self.assertEqual(pronounce_number(-3, lang="ar", gender=F),
                         "سالب ثلاث")


class TestArabicOrdinalGenderCase(unittest.TestCase):

    def test_every_cell(self):
        for (gender, case), table in ORDINALS.items():
            for number, spoken in table.items():
                with self.subTest(gender=gender, case=case, number=number):
                    if spoken is None:
                        with self.assertRaises(NotImplementedError):
                            pronounce_ordinal(number, lang="ar",
                                              gender=gender, case=case)
                        with self.assertRaises(NotImplementedError):
                            pronounce_number(number, lang="ar", ordinals=True,
                                             gender=gender, case=case)
                        continue
                    self.assertEqual(
                        pronounce_ordinal(number, lang="ar", gender=gender,
                                          case=case), spoken)
                    self.assertEqual(
                        pronounce_number(number, lang="ar", ordinals=True,
                                         gender=gender, case=case), spoken)
                    self.assertEqual(
                        pronounce_ordinal_ar(number, gender=gender, case=case),
                        spoken)

    def test_masculine_nominative_above_99_is_unchanged(self):
        # the module's reading above 99 is the definite cardinal; the
        # masculine nominative of it stays as it is
        self.assertEqual(pronounce_ordinal(103, lang="ar"), "المئة وثلاثة")

    def test_ordinal_aliases(self):
        for alias in ("genitive", "accusative"):
            with self.subTest(case=alias):
                self.assertEqual(
                    pronounce_ordinal(21, lang="ar", gender=F, case=alias),
                    "الحادية والعشرين")

    def test_lect_ordinals_default_to_the_nominative(self):
        # a lect's oblique default register applies to cardinals only
        for code in ("afb", "acw", "arz", "ars"):
            with self.subTest(code=code):
                self.assertEqual(pronounce_ordinal(21, lang=code, gender=F),
                                 "الحادية والعشرون")
                self.assertEqual(
                    pronounce_number(21, lang=code, ordinals=True, gender=F),
                    "الحادية والعشرون")
                self.assertEqual(
                    pronounce_ordinal(21, lang=code, gender=F,
                                      case="oblique"),
                    "الحادية والعشرين")


class TestArabicCaseAndGenderValidation(unittest.TestCase):

    def test_unknown_case_raises(self):
        for code in ARABIC_CODES:
            for bad in ("banana", "dative", "Genitive", ""):
                with self.subTest(code=code, case=bad):
                    with self.assertRaises(ValueError) as ctx:
                        pronounce_number(12, lang=code, case=bad)
                    for accepted in ("nominative", "oblique", "genitive",
                                     "accusative"):
                        self.assertIn(accepted, str(ctx.exception))
                    with self.assertRaises(ValueError):
                        pronounce_number(12, lang=code, case=bad,
                                         ordinals=True)
                    with self.assertRaises(ValueError):
                        pronounce_ordinal(12, lang=code, case=bad)

    def test_unknown_case_raises_in_the_module_functions(self):
        with self.assertRaises(ValueError):
            pronounce_number_ar(12, case="banana")
        with self.assertRaises(ValueError):
            pronounce_ordinal_ar(12, case="banana")

    def test_none_case_is_accepted(self):
        self.assertEqual(pronounce_number_ar(12, case=None), "اثنا عشر")
        self.assertEqual(pronounce_number(12, lang="ar", case=None),
                         "اثنا عشر")

    def test_neutral_gender_raises(self):
        for code in ARABIC_CODES:
            with self.subTest(code=code):
                with self.assertRaises(ValueError):
                    pronounce_number(3, lang=code,
                                     gender=GrammaticalGender.NEUTRAL)
                with self.assertRaises(ValueError):
                    pronounce_ordinal(3, lang=code,
                                      gender=GrammaticalGender.NEUTRAL)


class TestArabicLectFeminine(unittest.TestCase):
    """The lect tables cite masculine forms. The feminine of 1 to 19 falls
    back to the literary forms; the tens and hundreds have one form for both
    genders and keep the lect word."""

    def test_masculine_keeps_the_lect_form(self):
        self.assertEqual(pronounce_number(3, lang="acw"), "تلاتة")
        self.assertEqual(pronounce_number(12, lang="arz"), "اتناشر")
        self.assertEqual(pronounce_number(15, lang="afb"), "خمسطعش")

    def test_feminine_units_and_teens_fall_back_to_msa(self):
        self.assertEqual(pronounce_number(3, lang="acw", gender=F), "ثلاث")
        self.assertEqual(pronounce_number(2, lang="arz", gender=F), "اثنتين")
        self.assertEqual(pronounce_number(12, lang="arz", gender=F),
                         "اثنتي عشرة")
        self.assertEqual(pronounce_number(15, lang="afb", gender=F),
                         "خمس عشرة")
        self.assertEqual(pronounce_number(8, lang="acw", gender=F), "ثمان")

    def test_feminine_keeps_gender_free_lect_words(self):
        self.assertEqual(pronounce_number(30, lang="acw", gender=F),
                         "تلاتين")
        self.assertEqual(pronounce_number(100, lang="arz", gender=F), "مية")
        self.assertEqual(pronounce_number(115, lang="afb", gender=F),
                         "مية وخمس عشرة")
        self.assertEqual(pronounce_number(33, lang="acw", gender=F),
                         "ثلاث وتلاتين")


class TestArabicRoundTrip(unittest.TestCase):
    """Every form this module can now write extracts back to its number."""

    def test_cardinals(self):
        for (gender, case), table in CARDINALS.items():
            for number, spoken in table.items():
                with self.subTest(gender=gender, case=case, spoken=spoken):
                    self.assertEqual(extract_number(spoken, lang="ar"),
                                     number)
        for spoken, number in {"ثلاثة آلاف": 3000, "ألف وثلاث عشرة": 1013,
                               "ثمان وعشرون": 28, "اثنتين وعشرين": 22,
                               "ثلاث وتلاتين": 33,
                               "مية وخمس عشرة": 115}.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ar"), number)

    def test_ordinals(self):
        for (gender, case), table in ORDINALS.items():
            for number, spoken in table.items():
                if spoken is None:
                    continue
                with self.subTest(gender=gender, case=case, spoken=spoken):
                    self.assertEqual(
                        extract_number(spoken, lang="ar", ordinals=True),
                        number)
                    # above 99 the ordinal is the definite cardinal (المئة),
                    # which is_ordinal does not claim as an ordinal
                    if number < 100:
                        self.assertEqual(is_ordinal(spoken, lang="ar"), number)


if __name__ == "__main__":
    unittest.main()
