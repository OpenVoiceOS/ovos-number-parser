"""Norwegian Bokmål and Nynorsk share one engine; these tests pin the shared
core, the variant divergences and the two counting traditions."""
import unittest

from ovos_number_parser import (extract_number, is_fractional, is_ordinal,
                                numbers_to_digits, pronounce_number,
                                pronounce_ordinal)


class TestBokmaal(unittest.TestCase):
    def test_pronounce_number(self):
        expected = {0: 'null', 1: 'en', 2: 'to', 7: 'sju', 10: 'ti',
                    11: 'elleve', 12: 'tolv', 20: 'tjue', 21: 'tjueen',
                    30: 'tretti', 40: 'førti', 90: 'nitti',
                    100: 'hundre', 101: 'hundre og en', 1000: 'tusen',
                    2500: 'to tusen fem hundre'}
        for number, spoken in expected.items():
            with self.subTest(number=number):
                self.assertEqual(pronounce_number(number, lang="nb"), spoken)

    def test_modern_forms_are_pronounced(self):
        # Språkrådet's modern norm: sju/tjue rather than syv/tyve
        self.assertEqual(pronounce_number(7, lang="nb"), 'sju')
        self.assertEqual(pronounce_number(20, lang="nb"), 'tjue')

    def test_traditional_forms_still_extract(self):
        # the older norm remains in wide use and must parse
        self.assertEqual(extract_number('syv', lang="nb"), 7)
        self.assertEqual(extract_number('tyve', lang="nb"), 20)
        self.assertEqual(extract_number('enogtyve', lang="nb"), 21)

    def test_negative_and_decimal(self):
        self.assertEqual(extract_number('minus fem', lang="nb"), -5)
        self.assertEqual(extract_number('fem komma to', lang="nb"), 5.2)

    def test_round_trip_sweep(self):
        values = list(range(0, 121)) + [150, 500, 999, 1000, 1001, 2500,
                                        12345, 100000, 1000000]
        for n in values:
            spoken = pronounce_number(n, lang="nb")
            self.assertEqual(extract_number(spoken, lang="nb"), n,
                             f"{n} -> {spoken!r}")


class TestNynorsk(unittest.TestCase):
    def test_one_is_ein(self):
        self.assertEqual(pronounce_number(1, lang="nn"), 'ein')
        self.assertEqual(pronounce_number(21, lang="nn"), 'tjueein')

    def test_shared_core(self):
        for n, spoken in {7: 'sju', 20: 'tjue', 100: 'hundre',
                          1000: 'tusen'}.items():
            with self.subTest(number=n):
                self.assertEqual(pronounce_number(n, lang="nn"), spoken)

    def test_round_trip_sweep(self):
        values = list(range(0, 121)) + [150, 500, 1000, 2500, 12345]
        for n in values:
            spoken = pronounce_number(n, lang="nn")
            self.assertEqual(extract_number(spoken, lang="nn"), n,
                             f"{n} -> {spoken!r}")


class TestMacrolanguageCode(unittest.TestCase):
    def test_no_resolves_to_bokmaal(self):
        for n in (1, 7, 21, 2500):
            self.assertEqual(pronounce_number(n, lang="no"),
                             pronounce_number(n, lang="nb"))
        self.assertEqual(extract_number('tjueen', lang="no"), 21)


class TestHelpers(unittest.TestCase):
    def test_is_ordinal(self):
        self.assertEqual(is_ordinal('første', lang="nb"), 1)
        self.assertEqual(is_ordinal('andre', lang="nb"), 2)
        self.assertFalse(is_ordinal('katt', lang="nb"))

    def test_pronounce_ordinal(self):
        self.assertEqual(pronounce_ordinal(1, lang="nb"), 'første')
        self.assertEqual(pronounce_ordinal(2, lang="nb"), 'andre')

    def test_is_fractional(self):
        self.assertEqual(is_fractional('halv', lang="nb"), 0.5)
        self.assertFalse(is_fractional('katt', lang="nb"))

    def test_numbers_to_digits(self):
        self.assertEqual(numbers_to_digits('tjueen katter', lang="nb"),
                         '21 katter')

    def test_no_number(self):
        for lang in ("nb", "nn"):
            self.assertFalse(extract_number('god morgen', lang=lang))

    def test_non_decimal_unicode_digits_do_not_crash(self):
        # Superscripts (¹²³) and vulgar fractions (½) are digit-like
        # (str.isdigit()/isnumeric() is True) but int() rejects them; they
        # must be treated as "no number", never raise ValueError.
        for lang in ("nb", "nn"):
            for text in ("¹", "²", "³", "½"):
                with self.subTest(lang=lang, text=text):
                    self.assertFalse(extract_number(text, lang=lang))

    def test_arabic_indic_digits_still_work(self):
        # Arabic-Indic digits (٠١٢...) are true decimal digits and must
        # keep working.
        for lang in ("nb", "nn"):
            self.assertEqual(extract_number('١', lang=lang), 1)
            self.assertEqual(extract_number('٢', lang=lang), 2)
            self.assertEqual(extract_number('٣', lang=lang), 3)


class TestOrdinalsFlagKeepsTheCardinal(unittest.TestCase):
    """ordinals=True asks for ordinals to be read, not for cardinals to go.

    nb and nn returned False for a bare cardinal under the flag, because
    _extract_number returned False when no word in the line was an ordinal
    instead of falling through to the cardinal. Sixteen of the eighteen
    languages in this package never did that.
    """

    def test_a_bare_cardinal_survives_the_flag(self):
        for lang in ("nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number('fem', lang=lang), 5)
                self.assertEqual(
                    extract_number('fem', lang=lang, ordinals=True), 5,
                    "ordinals=True dropped the cardinal")

    def test_a_bare_ordinal_still_reads(self):
        """The behaviour that must not regress."""
        for lang in ("nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(
                    extract_number('femte', lang=lang, ordinals=True), 5)
                # and without the flag an ordinal is still not a number
                self.assertFalse(extract_number('femte', lang=lang))

    def test_an_ordinal_wins_over_a_cardinal_in_the_same_line(self):
        """The line that separates a fall-through from no preference at all.

        A line holding both readings is the only instrument that tells a
        dropped preference from a dropped cardinal: with the fall-through
        alone and no ordinal loop, these would answer the cardinal.
        """
        for lang in ("nb", "nn"):
            with self.subTest(lang=lang):
                self.assertEqual(
                    extract_number('tre femte', lang=lang, ordinals=True), 5)
                self.assertEqual(
                    extract_number('femte tre', lang=lang, ordinals=True), 5)
                self.assertEqual(
                    extract_number('tre femte sju', lang=lang,
                                   ordinals=True), 5)
                # without the flag the same lines read their first cardinal
                self.assertEqual(extract_number('tre femte', lang=lang), 3)

    def test_other_languages_answer_the_same_way(self):
        """The control: this is the fleet behaviour nb and nn deviated from."""
        for lang, cardinal, ordinal in (("en", "five", "fifth"),
                                        ("da", "fem", "femte"),
                                        ("de", "fünf", "fünfte")):
            with self.subTest(lang=lang):
                self.assertEqual(
                    extract_number(cardinal, lang=lang, ordinals=True), 5)
                self.assertEqual(
                    extract_number(ordinal, lang=lang, ordinals=True), 5)

    def test_a_line_with_no_number_is_still_false(self):
        """The fall-through must not invent a number."""
        for lang in ("nb", "nn"):
            with self.subTest(lang=lang):
                self.assertFalse(
                    extract_number('god morgen', lang=lang, ordinals=True))


class TestOgCompoundsUnderTheFlag(unittest.TestCase):
    """An "og"-inverted compound ("en og tjuende") is one ordinal, not two.

    "en og tjuende" is the spoken twenty-first in the "og"-inverted counting
    tradition: the smaller unit ("en") is named before the larger ordinal
    tens word ("tjuende"), the same arithmetic `_is_ordinal` already gives
    the glued spelling "enogtjuende" (1 + 20 = 21). Before the fix, the
    ordinal scan answered the ordinal word alone (20), the
    leftmost-separated rule's span-growth probe read that as a cardinal and
    an unrelated ordinal in one line, the line reached two spans, and the
    leftmost one, the cardinal, won (1). nb, nn and da share the inverted
    spelling and the fix; the other rows below are a different, wider
    compound shape (a cardinal of any size before "og" before an ordinal
    remainder, inverted or not) that the fix does not touch, and they keep
    the leftmost-separated reading unchanged (T-6195).
    """

    #: line, the reading under ordinals=True, the reading with the flag off
    NB = [("hundre og femte", 100, 100),
          ("hundre og første", 100, 100),
          ("tjue og tredje", 20, 20),
          ("to hundre og tredje", 200, 200),
          ("tusen og andre", 1000, 1000),
          ("en og tjuende", 21, False)]

    NN = [("hundre og femte", 100, 100),
          ("ein og tjuande", 21, False)]

    #: the fraction shape: with the flag on the leading cardinal answers, and
    #: with the flag off the fraction still does. No ordinal word appears on
    #: these lines, so the og-inverted fix does not reach them.
    FRACTIONS_NB = [("en halv", 1, 0.5),
                    ("en kvart", 1, 0.25),
                    ("tre en halv", 3, 3.5)]

    def _assert_rows(self, lang, rows):
        for line, under_flag, flag_off in rows:
            with self.subTest(lang=lang, line=line):
                self.assertEqual(
                    extract_number(line, lang=lang, ordinals=True),
                    under_flag)
                self.assertEqual(extract_number(line, lang=lang), flag_off)

    def test_nb_og_compounds(self):
        self._assert_rows("nb", self.NB)

    def test_nn_og_compounds(self):
        self._assert_rows("nn", self.NN)

    def test_a_fraction_line_answers_its_leading_cardinal_under_the_flag(self):
        self._assert_rows("nb", self.FRACTIONS_NB)
        self.assertEqual(extract_number('ein halv', lang="nn",
                                        ordinals=True), 1)
        self.assertEqual(extract_number('ein halv', lang="nn"), 0.5)

    def test_da_og_inverted_compound_joins_the_family(self):
        """da now reads its own og-inverted spelling the same way nb does.

        "hundrede og femte" is not changed: it is not an inverted compound
        (the cardinal "hundrede" is larger than the ordinal remainder
        "femte"), so it keeps the leftmost-separated reading, 100.
        """
        self.assertEqual(extract_number('en og tyvende', lang="da",
                                        ordinals=True), 21)
        self.assertEqual(extract_number('hundrede og femte', lang="da",
                                        ordinals=True), 100)

    def test_de_glued_compound_is_unaffected(self):
        """German never reaches this fix: a spaced "und" stays two numbers.

        `numbers_de._NUMBER_CONNECTORS` is empty by design (see the comment
        there): German folds a written compound into one word before
        tokenization runs, so "einundzwanzigste" already reads 21, and a
        spaced "ein und zwanzigste" is the same conjunction as English "and"
        and is left as two numbers, same as "hundert und fünfte" staying
        the leftmost reading, 100.
        """
        self.assertEqual(extract_number('einundzwanzigste', lang="de",
                                        ordinals=True), 21)
        self.assertEqual(extract_number('hundert und fünfte', lang="de",
                                        ordinals=True), 100)
        self.assertEqual(extract_number('hundert und fünfte', lang="de",
                                        ordinals=True), 100)

    def test_the_flag_off_reading_of_a_fraction_is_untouched(self):
        """The regression guard: nothing moves with the flag off."""
        for lang, half in (("nb", 'en halv'), ("nn", 'ein halv')):
            with self.subTest(lang=lang):
                self.assertEqual(extract_number(half, lang=lang), 0.5)


if __name__ == "__main__":
    unittest.main()
