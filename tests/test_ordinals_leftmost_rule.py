"""T-3982: under ordinals=True the leftmost number of a line wins.

Panel item ``number-parser-ordinals-rule-v2``, ruled 2026-09-23: when a line
carries several numbers and ``extract_number`` is called with
``ordinals=True``, the number written first wins, whether it is the ordinal
or the cardinal.

The rule covers numbers that other words separate, and only those. Two
adjacent number words are how a fraction is written ("two thirds", "zwei
drittel"), and what they mean under the flag is open (T-4416, architecture).
The tests below pin the adjacent readings as they stand, so a later answer to
that question has to move them on purpose.
"""
import unittest

from ovos_number_parser import (extract_number_ca, extract_number_da,
                                extract_number_de, extract_number_en,
                                extract_number_es, extract_number_eu,
                                extract_number_fa, extract_number_fr,
                                extract_number_gl, extract_number_it,
                                extract_number_kab, extract_number_nb,
                                extract_number_nn, extract_number_spans)
from ovos_number_parser.util import leftmost_separated_number

#: idiomatic lines that hold an ordinal and a cardinal with other words
#: between them. The two lines of a pair carry the same two numbers in the
#: opposite order, so the expected answer moves with the order and a parser
#: that always prefers one class fails one line of the pair.
IDIOMATIC = [
    #  lang, extract, line, under ordinals=True, under ordinals=False
    ("en", extract_number_en, "the third of two", 3, False),
    ("en", extract_number_en, "two of the third", 2, 2),
    ("de", extract_number_de, "das dritte von zwei", 3, 2),
    ("de", extract_number_de, "zwei von dem dritten", 2, 2),
    ("da", extract_number_da, "den tredje af to", 3, 2),
    ("da", extract_number_da, "to af den tredje", 2, 2),
    ("kab", extract_number_kab, "wis kṛaḍ seg sin", 3, 3),
    ("kab", extract_number_kab, "sin seg wis kṛaḍ", 2, 2),
]

#: the locales the rule reaches today, with their own words for 2 and 3 and
#: the reading each order keeps once the flag is off. ``qzx`` is a filler: it
#: spells no number in any of them, so it only keeps the two numbers apart.
#: The flag-off values are not uniform, and that is the point of recording
#: them: Kabyle reads its ordinal phrase as 3 without the flag, and English
#: reads nothing at all on the ordinal-first line.
REACHED = {
    #        extract,            card,   ordinal,     off(O x C), off(C x O)
    "da": (extract_number_da, "to", "tredje", 2, 2),
    "de": (extract_number_de, "zwei", "dritte", 2, 2),
    "kab": (extract_number_kab, "sin", "wis kṛaḍ", 3, 2),
    "en": (extract_number_en, "two", "third", False, 2),
}

#: the pair written with no word between them, for each reached locale, and
#: the number of spans the scanner reports. A cardinal followed by an ordinal
#: is the fraction shape, and the scanner grows it into one span, so the rule
#: never reaches it. Any other adjacency stays two spans and the rule does
#: reach it. Kabyle writes its ordinal as a phrase, "wis kṛaḍ", so neither of
#: its orders is one span and the rule reaches both.
ADJACENT_SPANS = {"da": (2, 1), "de": (2, 1), "kab": (2, 2), "en": (1, 2)}

#: locales whose parser cannot answer the rule yet, with the value each one
#: returns today and the task that unblocks it. Each entry is a defect in the
#: locale's own reading, not in the rule: the line never reaches two number
#: spans, so there is no "leftmost" to choose.
BLOCKED = {
    # the plain cardinal stops being read once ordinals=True
    "nb": (extract_number_nb, "to", "tredje", 3, 3, "cardinal unread"),
    "nn": (extract_number_nn, "to", "tredje", 3, 3, "cardinal unread"),
    # the ordinal word is not recognised at all
    "eu": (extract_number_eu, "bi", "hirugarren", 2, 2, "ordinal unread"),
    "fa": (extract_number_fa, "دو", "سوم", 2, 2, "ordinal unread"),
    # T-4415: the Romance extractor adds the two numbers together
    "ca": (extract_number_ca, "dos", "tercer", 5, 5, "T-4415 additive"),
    "es": (extract_number_es, "dos", "tercero", 5, 5, "T-4415 additive"),
    "fr": (extract_number_fr, "deux", "troisième", 5, 5, "T-4415 additive"),
    "gl": (extract_number_gl, "dous", "terceiro", 5, 5, "T-4415 additive"),
    "it": (extract_number_it, "due", "terzo", 5, 5, "T-4415 additive"),
}

FILLER = "qzx"


class TestLeftmostSeparatedNumber(unittest.TestCase):
    """The helper itself, before any language calls it."""

    def test_the_first_span_answers_when_two_are_separated(self):
        self.assertEqual(
            leftmost_separated_number("zwei qzx dritte", "de", True), 2)
        self.assertEqual(
            leftmost_separated_number("dritte qzx zwei", "de", True), 3)

    def test_the_rule_does_not_apply_without_the_flag(self):
        self.assertIsNone(
            leftmost_separated_number("zwei qzx dritte", "de", False))

    def test_the_rule_does_not_apply_to_one_number(self):
        self.assertIsNone(leftmost_separated_number("zwei", "de", True))

    def test_the_rule_does_not_apply_to_adjacent_words(self):
        """Two adjacent number words are one span, so the helper stands
        aside and the language's own reading answers."""
        self.assertEqual(
            len(extract_number_spans("zwei dritte", "de", ordinals=True)), 1)
        self.assertIsNone(
            leftmost_separated_number("zwei dritte", "de", True))

    def test_a_line_with_no_number_is_not_the_rule(self):
        self.assertIsNone(leftmost_separated_number("qzx qzx", "de", True))

    def test_a_non_string_is_not_the_rule(self):
        self.assertIsNone(leftmost_separated_number(None, "de", True))
        self.assertIsNone(leftmost_separated_number(7, "de", True))


class TestIdiomaticMixedLines(unittest.TestCase):
    """The lines the #359 review named, in the languages it named."""

    def test_the_leftmost_number_wins(self):
        for lang, extract, line, expected, _ in IDIOMATIC:
            with self.subTest(lang=lang, line=line):
                self.assertEqual(extract(line, ordinals=True), expected)

    def test_the_flag_off_reading_is_recorded_and_unchanged(self):
        """The rule runs under the flag alone, so each line keeps the
        reading it had without it. The values are recorded per line: German
        answered 2 on "das dritte von zwei" before the rule and still does,
        while under the flag it now answers the leftmost, 3."""
        for lang, extract, line, _, off in IDIOMATIC:
            with self.subTest(lang=lang, line=line):
                self.assertEqual(extract(line, ordinals=False), off)

    def test_the_flag_changes_at_least_one_line(self):
        """Fail-before control. If the flag changed nothing on any of these
        lines, the assertions above would pass on a parser that never read
        the rule at all."""
        moved = [line for _, extract, line, on, off in IDIOMATIC
                 if extract(line, ordinals=True) != off]
        self.assertTrue(moved, "the flag moved no line: the rule is dead")


class TestEveryReachedLocale(unittest.TestCase):
    """Each locale the rule reaches, on both orders of the same pair."""

    def test_the_ordinal_first_answers_the_ordinal(self):
        for lang, (extract, card, ordinal, _, _) in REACHED.items():
            with self.subTest(lang=lang):
                line = f"{ordinal} {FILLER} {card}"
                self.assertEqual(extract(line, ordinals=True), 3, line)

    def test_the_cardinal_first_answers_the_cardinal(self):
        for lang, (extract, card, ordinal, _, _) in REACHED.items():
            with self.subTest(lang=lang):
                line = f"{card} {FILLER} {ordinal}"
                self.assertEqual(extract(line, ordinals=True), 2, line)

    def test_the_flag_off_is_untouched(self):
        """The rule never runs under ordinals=False, so each order keeps the
        reading it had before the rule existed. The values differ by
        language, so they are recorded rather than assumed."""
        for lang, (extract, card, ordinal, off_oc,
                   off_co) in REACHED.items():
            with self.subTest(lang=lang):
                self.assertEqual(
                    extract(f"{ordinal} {FILLER} {card}", ordinals=False),
                    off_oc)
                self.assertEqual(
                    extract(f"{card} {FILLER} {ordinal}", ordinals=False),
                    off_co)


class TestTheFractionShapeIsUntouched(unittest.TestCase):
    """T-4416 owns what an adjacent pair means; this pins where the line
    falls today.

    The scanner grows a cardinal followed by an ordinal into one span,
    which is the shape a fraction is written in, so the rule never reaches
    it. That is what keeps "zwei drittel" two thirds.
    """

    def test_the_fraction_reading_survives(self):
        self.assertAlmostEqual(
            extract_number_de("zwei drittel", ordinals=True), 2 / 3)
        self.assertAlmostEqual(
            extract_number_de("zwei drittel", ordinals=False), 2 / 3)

    def test_the_scanner_draws_the_line_where_the_table_says(self):
        for lang, (extract, card, ordinal, _, _) in REACHED.items():
            want_oc, want_co = ADJACENT_SPANS[lang]
            with self.subTest(lang=lang, order="ordinal first"):
                self.assertEqual(
                    len(extract_number_spans(f"{ordinal} {card}", lang,
                                             ordinals=True)), want_oc)
            with self.subTest(lang=lang, order="cardinal first"):
                self.assertEqual(
                    len(extract_number_spans(f"{card} {ordinal}", lang,
                                             ordinals=True)), want_co)

    def test_kabyle_writes_its_ordinal_as_a_phrase(self):
        """Disclosed, not hidden. Kabyle's ordinal is two words, so the
        scanner never reads a Kabyle pair as one span and the rule reaches
        both orders, including the one written with nothing between them.
        "sin wis kṛaḍ" answered 3 before the rule and answers 2 under it."""
        self.assertEqual(extract_number_kab("sin wis kṛaḍ", ordinals=True), 2)
        self.assertEqual(extract_number_kab("wis kṛaḍ sin", ordinals=True), 3)


class TestLocalesTheRuleCannotReachYet(unittest.TestCase):
    """Every locale the census found and the rule does not answer.

    These are recorded, not excused. Each one fails to reach two number
    spans for its own reason, named in the table, so there is no leftmost
    to choose. The values are asserted as they stand today, so the locale
    cannot change quietly: when its own defect is fixed, this test fails
    and the locale moves to REACHED.
    """

    def test_each_blocked_locale_answers_what_it_answers_today(self):
        for lang, (extract, card, ordinal, ord_first, card_first,
                   why) in BLOCKED.items():
            with self.subTest(lang=lang, why=why):
                self.assertEqual(
                    extract(f"{ordinal} {FILLER} {card}", ordinals=True),
                    ord_first, f"{lang} ordinal first ({why})")
                self.assertEqual(
                    extract(f"{card} {FILLER} {ordinal}", ordinals=True),
                    card_first, f"{lang} cardinal first ({why})")

    def test_each_blocked_locale_reaches_fewer_than_two_spans(self):
        """The reason the rule cannot answer, stated as a measurement:
        the scanner never sees two numbers on the line."""
        for lang, (_, card, ordinal, _, _, why) in BLOCKED.items():
            with self.subTest(lang=lang, why=why):
                line = f"{card} {FILLER} {ordinal}"
                self.assertLess(
                    len(extract_number_spans(line, lang, ordinals=True)), 2,
                    f"{lang} now reaches two spans: move it to REACHED")


if __name__ == "__main__":
    unittest.main()
