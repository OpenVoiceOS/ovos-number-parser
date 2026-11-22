"""T-3982: under ordinals=True the leftmost number of a line wins.

Panel item ``number-parser-ordinals-rule-v2``, ruled 2026-09-23: when a line
carries several numbers and ``extract_number`` is called with
``ordinals=True``, the number written first wins, whether it is the ordinal
or the cardinal.

The rule covers numbers that other words separate. numtag, which reads every
language here, also reads two adjacent number words as two numbers (numtag
docs/rulings.md, "The leftmost longest number"), so the rule reaches an
adjacent pair too.
"""
import unittest
from unittest import mock

from ovos_number_parser import extract_number, extract_number_spans
from ovos_number_parser.util import leftmost_separated_number


def reader(lang):
    return lambda line, ordinals: extract_number(line, lang, ordinals=ordinals)


#: idiomatic lines that hold an ordinal and a cardinal with other words
#: between them. The two lines of a pair carry the same two numbers in the
#: opposite order, so the expected answer moves with the order and a parser
#: that always prefers one class fails one line of the pair.
IDIOMATIC = [
    #  lang, extract, line, under ordinals=True, under ordinals=False
    ("en", reader("en"), "the third of two", 3, 2),
    ("en", reader("en"), "two of the third", 2, 2),
    ("de", reader("de"), "das dritte von zwei", 3, 2),
    ("de", reader("de"), "zwei von dem dritten", 2, 2),
    ("da", reader("da"), "den tredje af to", 3, 2),
    ("da", reader("da"), "to af den tredje", 2, 2),
    ("kab", reader("kab"), "wis kṛaḍ seg sin", 3, 2),
    ("kab", reader("kab"), "sin seg wis kṛaḍ", 2, 2),
]

#: the locales the rule reaches, with their own words for 2 and 3 and
#: the reading each order keeps once the flag is off. ``qzx`` is a filler: it
#: spells no number in any of them, so it only keeps the two numbers apart.
#: Without the flag an ordinal is no number, so each order answers the
#: cardinal, 2.
REACHED = {
    #        extract,            card,   ordinal,     off(O x C), off(C x O)
    "da": (reader("da"), "to", "tredje", 2, 2),
    "de": (reader("de"), "zwei", "dritte", 2, 2),
    # T-3864: the cardinal is read under the flag again, so the line reaches
    # two spans and the rule answers.
    "nb": (reader("nb"), "to", "tredje", 2, 2),
    "nn": (reader("nn"), "to", "tredje", 2, 2),
    # the extractors consult is_ordinal_eu and is_ordinal_fa under the flag
    "eu": (reader("eu"), "bi", "hirugarren", 2, 2),
    "fa": (reader("fa"), "دو", "سوم", 2, 2),
    "kab": (reader("kab"), "sin", "wis kṛaḍ", 2, 2),
    "en": (reader("en"), "two", "third", 2, 2),
    # T-4415 ended the Romance sum of two separated numbers, and numtag reads
    # them as two.
    "ca": (reader("ca"), "dos", "tercer", 2, 2),
    "es": (reader("es"), "dos", "tercero", 2, 2),
    "fr": (reader("fr"), "deux", "troisième", 2, 2),
    "gl": (reader("gl"), "dous", "terceiro", 2, 2),
    "it": (reader("it"), "due", "terzo", 2, 2),
}

#: the pair written with no word between them, for each reached locale, and
#: the number of spans the scanner reports. numtag reads the two words as two
#: numbers in both orders, except fa, whose cardinal-then-ordinal order is
#: one span.
ADJACENT_SPANS = {lang: (2, 2) for lang in REACHED}
ADJACENT_SPANS["fa"] = (2, 1)

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

    def test_the_rule_applies_to_adjacent_words(self):
        """numtag reads two adjacent number words as two spans, so the
        helper answers the first."""
        self.assertEqual(
            len(extract_number_spans("zwei dritte", "de", ordinals=True)), 2)
        self.assertEqual(
            leftmost_separated_number("zwei dritte", "de", True), 2)

    def test_a_line_with_no_number_is_not_the_rule(self):
        self.assertIsNone(leftmost_separated_number("qzx qzx", "de", True))

    def test_a_non_string_is_not_the_rule(self):
        self.assertIsNone(leftmost_separated_number(None, "de", True))
        self.assertIsNone(leftmost_separated_number(7, "de", True))

    def test_a_single_word_never_pays_the_span_scan(self):
        """A line of one word cannot hold two spans, so the cheap word
        count is enough to answer None without scanning it."""
        with mock.patch("ovos_number_parser.extract_number_spans") as spans:
            self.assertIsNone(leftmost_separated_number("zwei", "de", True))
        spans.assert_not_called()

    def test_a_separated_line_still_scans(self):
        """Two words is the floor, not a reason to skip a real line."""
        with mock.patch("ovos_number_parser.extract_number_spans",
                        wraps=extract_number_spans) as spans:
            self.assertEqual(
                leftmost_separated_number("zwei qzx dritte", "de", True), 2)
        spans.assert_called_once()


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
    """A fraction keeps its reading, and the table records where the
    scanner ends an adjacent pair.

    "zwei drittel" is a fraction word after a count, so it stays two
    thirds. "zwei dritte" is a count and an ordinal, which numtag reads as
    two numbers.
    """


    def test_the_fraction_reading_survives(self):
        self.assertAlmostEqual(
            extract_number("zwei drittel", "de", ordinals=True), 2 / 3)
        self.assertAlmostEqual(
            extract_number("zwei drittel", "de", ordinals=False), 2 / 3)

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
        self.assertEqual(extract_number("sin wis kṛaḍ", "kab", ordinals=True), 2)
        self.assertEqual(extract_number("wis kṛaḍ sin", "kab", ordinals=True), 3)


if __name__ == "__main__":
    unittest.main()
