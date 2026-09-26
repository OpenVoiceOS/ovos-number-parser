import unittest

from ovos_number_parser import (extract_number, pronounce_number,
                                pronounce_ordinal, pronounce_fraction,
                                is_fractional, is_ordinal, numbers_to_digits)
from ovos_number_parser.numbers_ar import extract_numbers_ar


def extract_number_ar(text, ordinals=False):
    return extract_number(text, lang="ar", ordinals=ordinals)


class TestArabicPronounce(unittest.TestCase):
    """Anchors for spoken Modern Standard Arabic numbers (masculine forms)."""

    def test_pronounce_number(self):
        expected = {
            0: 'صفر', 1: 'واحد', 2: 'اثنان', 3: 'ثلاثة', 4: 'أربعة',
            5: 'خمسة', 6: 'ستة', 7: 'سبعة', 8: 'ثمانية', 9: 'تسعة',
            10: 'عشرة', 11: 'أحد عشر', 12: 'اثنا عشر', 13: 'ثلاثة عشر',
            14: 'أربعة عشر', 15: 'خمسة عشر', 16: 'ستة عشر', 17: 'سبعة عشر',
            18: 'ثمانية عشر', 19: 'تسعة عشر', 20: 'عشرون',
            # units come before tens, joined by the conjunction و
            21: 'واحد وعشرون', 25: 'خمسة وعشرون', 30: 'ثلاثون',
            42: 'اثنان وأربعون', 50: 'خمسون', 66: 'ستة وستون', 70: 'سبعون',
            80: 'ثمانون', 90: 'تسعون', 99: 'تسعة وتسعون', 100: 'مئة',
            101: 'مئة وواحد', 123: 'مئة وثلاثة وعشرون',
            # duals
            200: 'مئتان', 2000: 'ألفان', 2000000: 'مليونان',
            300: 'ثلاثمئة', 500: 'خمسمئة', 999: 'تسعمئة وتسعة وتسعون',
            1000: 'ألف', 1985: 'ألف وتسعمئة وخمسة وثمانون',
            2023: 'ألفان وثلاثة وعشرون',
            # scale nouns are masculine, 3-10 take the ة-marked numeral
            3000: 'ثلاثة آلاف', 10000: 'عشرة آلاف', 100000: 'مئة ألف',
            1000000: 'مليون', 3000000: 'ثلاثة ملايين',
            1000000000: 'مليار',
        }
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="ar"), spoken)

    def test_pronounce_negative_and_decimal(self):
        expected = {-7: 'سالب سبعة', -42: 'سالب اثنان وأربعون',
                    5.2: 'خمسة فاصلة اثنان',
                    5.25: 'خمسة فاصلة اثنان خمسة',
                    0.5: 'صفر فاصلة خمسة',
                    -3.5: 'سالب ثلاثة فاصلة خمسة'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="ar"), spoken)

    def test_pronounce_ordinal(self):
        expected = {1: 'الأول', 2: 'الثاني', 3: 'الثالث', 4: 'الرابع',
                    5: 'الخامس', 6: 'السادس', 7: 'السابع', 8: 'الثامن',
                    9: 'التاسع', 10: 'العاشر', 11: 'الحادي عشر',
                    12: 'الثاني عشر', 20: 'العشرون',
                    21: 'الحادي والعشرون', 25: 'الخامس والعشرون',
                    30: 'الثلاثون', 100: 'المئة', 1000: 'الألف'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_ordinal(number, lang="ar"), spoken)

    def test_pronounce_fraction(self):
        self.assertEqual(pronounce_fraction("1/2", lang="ar"), 'نصف')
        self.assertEqual(pronounce_fraction("1/3", lang="ar"), 'ثلث')
        self.assertEqual(pronounce_fraction("1/4", lang="ar"), 'ربع')
        self.assertEqual(pronounce_fraction("2/3", lang="ar"), 'ثلثان')
        self.assertEqual(pronounce_fraction("3/4", lang="ar"), 'ثلاثة أرباع')


class TestArabicExtract(unittest.TestCase):
    """Anchors for extracting numbers from Arabic text."""

    def test_extract_number(self):
        expected = {
            0: 'صفر', 1: 'واحد', 2: 'اثنان', 3: 'ثلاثة', 10: 'عشرة',
            11: 'أحد عشر', 12: 'اثنا عشر', 15: 'خمسة عشر', 20: 'عشرون',
            25: 'خمسة وعشرون', 99: 'تسعة وتسعون', 100: 'مئة',
            123: 'مئة وثلاثة وعشرون', 200: 'مئتان', 1000: 'ألف',
            2000: 'ألفان', 3000: 'ثلاثة آلاف', 1000000: 'مليون',
        }
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ar"), number)

    def test_extract_gender_and_case_variants(self):
        # numbers 3-10 show gender polarity: both genders are accepted
        expected = {1: 'واحدة', 2: 'اثنتان', 3: 'ثلاث', 4: 'أربع',
                    5: 'خمس', 8: 'ثمان', 10: 'عشر',
                    # oblique case endings
                    22: 'اثنين وعشرين', 200: 'مئتين', 2000: 'ألفين',
                    # alternative hundred spelling and unfused hundreds
                    100: 'مائة', 300: 'ثلاث مئة', 400: 'أربعمائة',
                    # feminine teens
                    11: 'إحدى عشرة', 13: 'ثلاث عشرة'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number(spoken, lang="ar"), number)

    def test_extract_negative_and_decimal(self):
        expected = {-7: 'سالب سبعة', -9: 'ناقص تسعة',
                    -42: 'سالب اثنان وأربعون',
                    5.2: 'خمسة فاصلة اثنان',
                    5.25: 'خمسة فاصلة خمسة وعشرون',
                    3.14: 'ثلاثة فاصلة واحد أربعة',
                    5.5: 'خمسة ونصف', 2.25: 'اثنان وربع',
                    0.5: 'نصف', 0.25: 'ربع'}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertAlmostEqual(extract_number(spoken, lang="ar"),
                                       number)

    def test_extract_eastern_digits(self):
        # Eastern Arabic-Indic digits and the ٫ decimal separator
        self.assertEqual(extract_number("٢٥", lang="ar"), 25)
        self.assertEqual(extract_number("لدي ٣ قطط", lang="ar"), 3)
        self.assertAlmostEqual(extract_number("٥٫٢", lang="ar"), 5.2)
        self.assertEqual(extract_number("١٩٨٥", lang="ar"), 1985)

    def test_extract_from_sentence(self):
        self.assertEqual(extract_number("لدي خمسة وعشرون كتاباً", lang="ar"),
                         25)
        self.assertEqual(extract_number("اشتريت ثلاث تفاحات", lang="ar"), 3)
        self.assertEqual(
            extract_number("هذا هو اليوم الثالث", lang="ar", ordinals=True), 3)
        self.assertEqual(
            extract_number("الخامس والعشرون", lang="ar", ordinals=True), 25)

    def test_no_number(self):
        self.assertIn(extract_number("مرحبا كيف حالك", lang="ar"),
                      (False, None))
        self.assertIn(extract_number("", lang="ar"), (False, None))

    def test_is_fractional(self):
        self.assertEqual(is_fractional("نصف", lang="ar"), 0.5)
        self.assertEqual(is_fractional("ربع", lang="ar"), 0.25)
        self.assertEqual(is_fractional("الربع", lang="ar"), 0.25)
        self.assertAlmostEqual(is_fractional("ثلث", lang="ar"), 1 / 3)
        self.assertAlmostEqual(is_fractional("خمس", lang="ar"), 0.2)
        self.assertAlmostEqual(is_fractional("عشر", lang="ar"), 0.1)
        self.assertFalse(is_fractional("كتاب", lang="ar"))

    def test_is_ordinal(self):
        self.assertEqual(is_ordinal("الأول", lang="ar"), 1)
        self.assertEqual(is_ordinal("الأولى", lang="ar"), 1)
        self.assertEqual(is_ordinal("الثالثة", lang="ar"), 3)
        self.assertEqual(is_ordinal("الحادي عشر", lang="ar"), 11)
        self.assertEqual(is_ordinal("الخامس والعشرون", lang="ar"), 25)
        self.assertFalse(is_ordinal("مرحبا", lang="ar"))

    def test_numbers_to_digits(self):
        self.assertEqual(
            numbers_to_digits("لدي خمسة وعشرون قطة", lang="ar"),
            "لدي 25 قطة")


class TestArabicRobustDigits(unittest.TestCase):
    """Robustness to Persian/Arabic-Indic digits and glued punctuation."""

    def test_persian_digits(self):
        # Persian/Urdu (extended Arabic-Indic) digits carry 0-9 values
        self.assertEqual(extract_number("۲۵", lang="ar"), 25)
        self.assertEqual(extract_number("۱۹۸۵", lang="ar"), 1985)
        self.assertEqual(extract_number("عندي ۳ قطط", lang="ar"), 3)
        self.assertAlmostEqual(extract_number("۵٫۲", lang="ar"), 5.2)

    def test_punctuation_glued_digits(self):
        # a number glued to an Arabic comma/semicolon/question mark or an
        # ASCII period is still recognised as a number
        for text, value in [("10،", 10), ("25.", 25), ("٢٥؛", 25),
                             ("۲۰۲۴،", 2024), ("۳؟", 3),
                             ("لدي ٢٥، كتاب", 25)]:
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="ar"), value)

    def test_regression_clean_and_decimal(self):
        # clean integers and decimals keep working unchanged
        self.assertEqual(extract_number("٢٥", lang="ar"), 25)
        self.assertEqual(extract_number("مئة وثلاثة وعشرون", lang="ar"), 123)
        self.assertAlmostEqual(extract_number("٥٫٢", lang="ar"), 5.2)
        self.assertEqual(extract_number("سالب سبعة", lang="ar"), -7)


class TestArabicNumbersToDigitsRobust(unittest.TestCase):
    """Verbalizing digits inside text keeps adjacent punctuation."""

    def test_persian_and_arabic_indic_digits(self):
        self.assertEqual(
            numbers_to_digits("الرقم ٢٠٢٤", lang="ar"), "الرقم 2024")
        self.assertEqual(
            numbers_to_digits("عندي ۳ قطط", lang="ar"), "عندي 3 قطط")

    def test_glued_punctuation_is_reattached(self):
        # the Arabic comma / semicolon must survive verbalization, not vanish
        self.assertEqual(
            numbers_to_digits("لدي ٢٥، كتاب", lang="ar"), "لدي 25، كتاب")
        self.assertEqual(
            numbers_to_digits("لدي خمسة؛ كتب", lang="ar"), "لدي 5؛ كتب")
        self.assertEqual(
            numbers_to_digits("السنة ۱۹۸۵.", lang="ar"), "السنة 1985.")
        self.assertEqual(
            numbers_to_digits("خمسة وعشرون كتاباً", lang="ar"), "25 كتاباً")

    def test_standalone_digit_run_preserves_leading_zeros(self):
        # live bug found in a production Arabic voice pipeline: numbers_to_digits
        # re-parses a digit run that is ALREADY digits, round-trips it
        # through an int, and destroys leading zeros. A phone number, OTP
        # code, or any zero-padded identifier must survive byte-for-byte.
        self.assertEqual(
            numbers_to_digits("رقمي 0553175817", lang="ar"),
            "رقمي 0553175817")
        self.assertEqual(
            numbers_to_digits("الرمز 007", lang="ar"), "الرمز 007")
        self.assertEqual(
            numbers_to_digits("الرمز 4729 والاحتياطي 007", lang="ar"),
            "الرمز 4729 والاحتياطي 007")
        # Eastern Arabic-Indic digits: script is converted to Western per
        # existing pinned behaviour, but leading zeros must still survive
        self.assertEqual(
            numbers_to_digits("رقمي ٠٥٥٣١٧٥٨١٧", lang="ar"),
            "رقمي 0553175817")

    def test_mixed_digit_and_word_still_multiplies(self):
        # this is why digits are re-read through extract_number at all:
        # a digit run adjacent to a scale word must still multiply
        self.assertEqual(
            numbers_to_digits("355 ألف ريال", lang="ar"), "355000 ريال")

    def test_extract_dual_nouns(self):
        # the dual of common counting nouns carries the value 2 lexically
        for spoken in ["يومين", "يومان", "ساعتين", "ساعتان", "دقيقتين",
                       "دقيقتان", "ثانيتين", "أسبوعين", "شهرين", "سنتين",
                       "عامين", "ليلتين", "مرتين", "مرتان", "اثنتين",
                       "ريالين", "دولارين", "درهمين", "جنيهين"]:
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number_ar(spoken), 2)

    def test_extract_dual_in_context(self):
        # timer / duration phrasing
        self.assertEqual(extract_number_ar("اضبط مؤقت لمدة ساعتين"), 2)
        self.assertEqual(extract_number_ar("بعد يومين"), 2)
        self.assertAlmostEqual(extract_number_ar("ساعتين ونصف"), 2.5)
        self.assertEqual(extract_number_ar("سالب ساعتين"), -2)

    def test_definite_article_on_cardinals(self):
        # the ال- article is tolerated on cardinals
        self.assertEqual(extract_number_ar("الخمسة"), 5)
        self.assertEqual(extract_number_ar("العشرون"), 20)
        self.assertEqual(extract_number_ar("المئة"), 100)
        self.assertEqual(extract_number_ar("الألف"), 1000)
        self.assertEqual(extract_number_ar("الثلاثة والعشرون"), 23)

    def test_consecutive_units_are_separate_numbers(self):
        # two units cannot combine into one Arabic number: they are a list
        self.assertEqual(extract_numbers_ar("ثلاثة وخمسة وسبعة"), [3, 5, 7])
        self.assertEqual(extract_numbers_ar("واحد واثنان"), [1, 2])
        self.assertEqual(extract_numbers_ar("خمسة ثلاثة"), [5, 3])
        self.assertEqual(
            extract_numbers_ar("عندي ثلاثة كتب وخمسة أقلام"), [3, 5])

    def test_connector_compounds(self):
        expected = {121: "مئة وواحد وعشرون",
                    123: "مئة وثلاثة وعشرون",
                    111: "مئة وأحد عشر",
                    225: "مئتان وخمسة وعشرون",
                    250: "مئتين وخمسين",
                    1200: "ألف ومئتان",
                    1994: "ألف وتسعمئة وأربعة وتسعون",
                    2024: "ألفان وأربعة وعشرون",
                    5300: "خمسة آلاف وثلاثمئة",
                    123456: "مئة وثلاثة وعشرون ألف وأربعمئة وستة وخمسون",
                    1001000000: "مليار ومليون"}
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number_ar(spoken), number)

    def test_extract_diacritized(self):
        # fully / partially voweled input parses like the bare form
        self.assertEqual(extract_number_ar("ثَلاثة"), 3)
        self.assertEqual(extract_number_ar("وَاحِد"), 1)
        self.assertEqual(extract_number_ar("ثَمَانِيَة"), 8)

    def test_extract_hundreds_variants(self):
        expected = [(700, "سبعمئة"), (800, "ثمانمئة"), (800, "ثمانمائة"),
                    (999, "تسعمائة وتسعة وتسعون"), (300, "ثلاث مئة")]
        for number, spoken in expected:
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number_ar(spoken), number)

    def test_extract_mixed_digit_systems(self):
        self.assertEqual(extract_number_ar("٢5"), 25)
        self.assertEqual(extract_numbers_ar("لدي ٥ و 3"), [5, 3])


class TestArabicRoundTrip(unittest.TestCase):
    """pronounce_number output must be understood by extract_number."""

    def test_round_trip(self):
        numbers = list(range(0, 200)) + [
            201, 222, 300, 345, 400, 456, 500, 678, 700, 891, 900, 999,
            1000, 1001, 1234, 1985, 2000, 2023, 3000, 5000, 9999, 10000,
            11000, 15000, 100000, 123456, 1000000, 2000000, 3000000,
            1000000000, 2000000000]
        for number in numbers:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="ar")
                self.assertEqual(extract_number(spoken, lang="ar"), number)

    def test_round_trip_negative_and_decimal(self):
        for number in [-7, -42, -100, 2.5, 3.14, 5.2, -3.5, 0.5, 5.25,
                       0.75, 12.34]:
            with self.subTest(number=number):
                spoken = pronounce_number(number, lang="ar")
                self.assertAlmostEqual(extract_number(spoken, lang="ar"),
                                       number)

    def test_round_trip_ordinals(self):
        for number in range(1, 100):
            with self.subTest(number=number):
                spoken = pronounce_ordinal(number, lang="ar")
                self.assertEqual(is_ordinal(spoken, lang="ar"), number)


class TestArabicColloquialExtract(unittest.TestCase):
    """Dialectal/colloquial number forms that real speakers actually use.

    Gold values below are computed independently (plain arithmetic on the
    literal digits), never by calling the parser.
    """

    def test_colloquial_hundred_word(self):
        # مية / مئة / مائة are one lexeme (100); مائة is the classical
        # spelling and must keep working too
        for spoken in ["مية", "مِيَّة", "مئة", "مائة"]:
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number_ar(spoken), 100)
        # before a counted noun too
        self.assertEqual(extract_number_ar("مية ريال"), 100)

    def test_meeh_is_water_outside_a_number(self):
        # ميه spells water (English Wiktionary) and the hundred (the SADA
        # transcripts); test_number_parser_ar_meeh holds the number contexts
        self.assertEqual(extract_numbers_ar("شربت ميه"), [])
        self.assertEqual(extract_numbers_ar("الميه سخنة"), [])
        self.assertEqual(numbers_to_digits("شربت ميه", lang="ar"),
                         "شربت ميه")

    def test_maya_is_not_a_hundred(self):
        # ماية is attested as a spelling of "water" (Egyptian مايَّة), not
        # of "hundred"; كباية ماية is "a glass of water"
        self.assertFalse(extract_number_ar("ماية"))
        self.assertEqual(extract_numbers_ar("كباية ماية"), [])

    def test_colloquial_hundred_in_price_sentence(self):
        # "three hundred and fifty five thousand riyals", colloquial مية
        # 300 + 55 = 355; 355 * 1000 = 355000
        self.assertEqual(
            extract_number_ar("ثلاثمية وخمسة وخمسين الف ريال"), 355000)

    def test_colloquial_hundred_bare_alif_scale(self):
        # bare-alif الف (no hamza) must be recognised as the 1000 scale word
        self.assertEqual(extract_number_ar("مية الف ريال"), 100000)

    def test_classical_three_hundred(self):
        # ثلث is the classical spelling of ثلاث: Quran 18:25, "ثَلَٰثَ مِا۟ئَةٍ"
        # 300 + 50 = 350
        self.assertEqual(extract_number_ar("ثلثمئة وخمسين"), 350)
        self.assertEqual(extract_number_ar("ثلثمئة"), 300)

    def test_thulthmiya_has_no_source(self):
        # the hybrid of the classical ثلث and the colloquial مية
        self.assertFalse(extract_number_ar("ثلثمية"))
        self.assertEqual(extract_numbers_ar("ثلثمية وخمسين"), [50])

    def test_colloquial_hundred_plus_tens(self):
        # 100 + 50 = 150
        self.assertEqual(extract_number_ar("مية وخمسين"), 150)

    def test_spaced_unit_plus_colloquial_hundred_multiplies(self):
        # "خمس مية وثلاثين" = 5 * 100 + 30 = 530. The unit may stand apart
        # from the hundred: Dirr, Colloquial Egyptian Arabic Grammar (1904),
        # p. 26, gives 300 as "tultemiya" and "tult mit"; Ryding, A Reference
        # Grammar of Modern Standard Arabic (2005), p. 348: "five hundred
        # xams-u mi'at-in".
        self.assertEqual(extract_number_ar("خمس مية وثلاثين"), 530)
        # with the definite article fronting the unit word
        self.assertEqual(extract_number_ar("الخمس مية وثلاثين"), 530)
        # bare spaced unit + مية: 3 * 100 = 300
        self.assertEqual(extract_number_ar("ثلاث مية"), 300)
        # spaced unit + مية + tail unit: 7 * 100 + 5 = 705
        self.assertEqual(extract_number_ar("سبع مية وخمسة"), 705)

    def test_spaced_unit_plus_hundred_in_sentence(self):
        self.assertEqual(
            numbers_to_digits(
                "وش الفرق بينها وبين الخمس مية وثلاثين", lang="ar"),
            "وش الفرق بينها وبين 530")

    def test_non_regression_bare_hundred_and_fused_hundred(self):
        # a bare مية (no preceding unit) still means 100 + tens, unaffected
        self.assertEqual(extract_number_ar("مية وثلاثين"), 130)
        # the already-fused form (PR #290) keeps working
        self.assertEqual(extract_number_ar("الخمسمية وثلاثين"), 530)

    def test_fused_dialectal_teens(self):
        # the Egyptian fused teens: Dirr, Colloquial Egyptian Arabic Grammar
        # (1904), p. 26; English Wiktionary, حداشر "eleven", اتناشر "twelve"
        expected = {
            11: "حداشر", 12: "اتناشر", 13: "تلتاشر", 14: "اربعتاشر",
            15: "خمستاشر", 16: "ستاشر", 17: "سبعتاشر", 18: "تمنتاشر",
            19: "تسعتاشر",
        }
        for number, spoken in expected.items():
            with self.subTest(spoken=spoken):
                self.assertEqual(extract_number_ar(spoken), number)

    def test_fused_teens_of_the_hijazi_and_gulf_grammars(self):
        # Omar, Saudi Arabic Basic Course: Urban Hijazi Dialect (1975), and
        # Qafisheh, Basic Gulf Arabic (1970); see AR_LECT_FORMS
        expected = {
            11: ["إحدعش", "حدعش"], 12: ["اتنعش", "ثنعش"],
            13: ["تلاطعش", "ثلاطعش"], 14: ["اربعطعش"], 15: ["خمسطعش"],
            16: ["سطعش"], 17: ["سبعطعش"], 18: ["تمنطعش", "ثمنطعش"],
            19: ["تسعطعش"],
        }
        for number, spellings in expected.items():
            for spoken in spellings:
                with self.subTest(spoken=spoken):
                    self.assertEqual(extract_number_ar(spoken), number)

    def test_unattested_teen_spellings_are_no_numbers(self):
        # spellings no grammar, dictionary or SADA transcript gives; the
        # attested ones are in test_number_parser_ar_attested_teens and
        # test_number_parser_ar_sada_teens
        for spoken in ["اتنااشر", "ثلطاشر", "ثمنتاشر", "تلاتاش", "سطش"]:
            with self.subTest(spoken=spoken):
                self.assertFalse(extract_number_ar(spoken))

    def test_fused_teens_join_a_larger_number(self):
        self.assertEqual(extract_number_ar("مية وخمسطعش"), 115)
        self.assertEqual(extract_number_ar("ثلاثة آلاف وسبعطعش"), 3017)
        self.assertEqual(extract_number_ar("اتنعش ألف"), 12000)
        self.assertEqual(numbers_to_digits("عمره ثمنطعش سنة", lang="ar"),
                         "عمره 18 سنة")

    def test_a_fused_teen_spelling_is_no_other_number_word(self):
        from ovos_number_parser import numbers_ar
        others = (set(numbers_ar._UNITS_LOOKUP) | set(numbers_ar._TENS_LOOKUP)
                  | set(numbers_ar._HUNDREDS_LOOKUP)
                  | set(numbers_ar._SCALES_LOOKUP))
        self.assertFalse(set(numbers_ar._FUSED_TEENS_LOOKUP) & others)

    def test_naqis_is_the_sign_of_the_number_after_it(self):
        # ناقص is a minus sign, never a subtraction
        self.assertEqual(extract_number_ar("ناقص واحد"), -1)
        self.assertEqual(extract_numbers_ar("عشرة ناقص اثنين"), [10, -2])
        self.assertEqual(numbers_to_digits("عشرة ناقص اثنين", lang="ar"),
                         "10 ناقص 2")

    def test_colloquial_two_three_and_zero(self):
        self.assertEqual(extract_number_ar("ثنتين وخمسين"), 52)
        self.assertEqual(extract_number_ar("ثنين"), 2)
        self.assertEqual(extract_number_ar("تلاتة وعشرين"), 23)
        self.assertEqual(numbers_to_digits("زيرو خمسة خمسة", lang="ar"),
                         "0 5 5")

    def test_fused_teens_in_sentence(self):
        self.assertEqual(extract_number_ar("عمري اتناشر سنة"), 12)
        self.assertEqual(extract_number_ar("عندي حداشر كتاب"), 11)

    def test_mixed_digit_and_scale_word(self):
        # a digit run directly followed by a scale word multiplies it:
        # 355 * 1000 = 355000
        self.assertEqual(extract_number_ar("355 ألف"), 355000)
        self.assertEqual(extract_number_ar("355 الف"), 355000)
        self.assertEqual(extract_number_ar("٣٥٥ ألف"), 355000)
        self.assertEqual(extract_number_ar("2 مليون"), 2000000)
        self.assertEqual(extract_number_ar("3 مليار"), 3000000000)

    def test_clitic_attached_digit_joins_mixed_number_span(self):
        # a clitic (و/ف/ب/ل) glued directly onto a digit run must not stop
        # that digit run from starting a mixed digit+word number span: the
        # digits still multiply with the following scale word, and the
        # clitic re-attaches to the produced digits exactly as written.
        # Found while verifying PR #296 ("355 ألف" = 355000, bare form
        # below) -- pre-existing, not a #296 regression.
        self.assertEqual(
            numbers_to_digits("و355 ألف ريال", lang="ar"),
            "و355000 ريال")
        self.assertEqual(
            numbers_to_digits("ف355 ألف ريال", lang="ar"),
            "ف355000 ريال")
        self.assertEqual(
            numbers_to_digits("ب355 ألف ريال", lang="ar"),
            "ب355000 ريال")
        self.assertEqual(
            numbers_to_digits("ل355 ألف ريال", lang="ar"),
            "ل355000 ريال")
        # bare form regression: unaffected, no clitic present
        self.assertEqual(
            numbers_to_digits("355 ألف ريال", lang="ar"),
            "355000 ريال")

    def test_colloquial_forms_do_not_over_match(self):
        # words that merely resemble number words must not be extracted
        self.assertIn(extract_number_ar("اخي"), (False, None))
        self.assertIn(extract_number_ar("حي"), (False, None))

    def test_regression_docstring_claims_still_hold(self):
        # gender polarity, dual, oblique tens from the module docstring
        self.assertEqual(extract_number_ar("اثنين وعشرين"), 22)
        self.assertEqual(extract_number_ar("ثلاث تفاحات"), 3)
        self.assertEqual(extract_number_ar("عشرين"), 20)
        self.assertAlmostEqual(extract_number_ar("٢٠٢٤،") or 0, 2024)
        self.assertEqual(extract_number_ar("25."), 25)


if __name__ == "__main__":
    unittest.main()
