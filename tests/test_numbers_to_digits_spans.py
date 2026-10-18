import unittest

from ovos_number_parser import (ConvertedNumber, numbers_to_digits_es,
                                numbers_to_digits_spans_es)
from ovos_number_parser.numbers_it import IT

# sentence -> (written phrase, replacement) of every number the conversion
# replaces. The replacements are what numbers_to_digits_es writes.
SENTENCES = {
    "compra tres panes mañana": [("tres", "3")],
    "compra veinte y tres panes": [("veinte y tres", "23")],
    "treinta y cinco años": [("treinta y cinco", "35")],
    "ciento veinte euros": [("ciento veinte", "120")],
    "dos mil veintiséis": [("dos mil veintiséis", "2026")],
    "a la una de la tarde": [("una", "1")],
    "un pan": [("un", "1")],
    "una semana": [("una", "1")],
    "medio kilo": [],
    "el primero de mayo": [],
    "dentro de dos semanas": [("dos", "2")],
    "tres o cuatro días": [("tres", "3"), ("cuatro", "4")],
    "veintitrés": [("veintitrés", "23")],
    "cien": [("cien", "100")],
    "mil doscientos": [("mil doscientos", "1200")],
    "quince minutos": [("quince", "15")],
    "el tercer día": [],
    "cinco": [("cinco", "5")],
    "dos tres": [("dos tres", "5")],
    "uno dos tres": [("uno dos tres", "6")],
    "a las cinco y media": [("cinco", "5")],
    "en tres días a las ocho": [("tres", "3"), ("ocho", "8")],
    "cuarenta y dos y cinco": [("cuarenta y dos y cinco", "47")],
    "ochenta": [("ochenta", "80")],
}


def replaced(text, spans):
    for span in reversed(spans):
        text = text[:span.start] + span.replacement + text[span.end:]
    return text


class TestNumbersToDigitsSpansEs(unittest.TestCase):
    def test_spans_are_the_phrases_the_conversion_replaced(self):
        for text, expected in SENTENCES.items():
            with self.subTest(text=text):
                spans = numbers_to_digits_spans_es(text)
                self.assertEqual([(s.surface, s.replacement) for s in spans],
                                 expected)

    def test_offsets_point_at_the_written_phrase(self):
        for text in SENTENCES:
            with self.subTest(text=text):
                spans = numbers_to_digits_spans_es(text)
                for span in spans:
                    self.assertEqual(text[span.start:span.end], span.surface)
                self.assertEqual(spans,
                                 sorted(spans, key=lambda s: s.start))

    def test_replacing_the_spans_gives_the_conversion(self):
        for text in SENTENCES:
            with self.subTest(text=text):
                spans = numbers_to_digits_spans_es(text)
                self.assertEqual(" ".join(replaced(text, spans).split()),
                                 numbers_to_digits_es(text))

    def test_value_is_the_number_the_replacement_spells(self):
        for text in SENTENCES:
            for span in numbers_to_digits_spans_es(text):
                with self.subTest(text=text, surface=span.surface):
                    self.assertEqual(span.replacement, str(span.value))

    def test_the_conversion_itself_is_unchanged(self):
        self.assertEqual(numbers_to_digits_es("compra veinte y tres panes"),
                         "compra 23 panes")
        self.assertEqual(numbers_to_digits_es("tres o cuatro días"),
                         "3 o 4 días")
        self.assertEqual(numbers_to_digits_es("a las cinco y media"),
                         "a las 5 y media")
        self.assertEqual(numbers_to_digits_es("medio kilo"), "medio kilo")

    def test_punctuation_and_spacing_do_not_move_the_offsets(self):
        # a number word with punctuation glued on is not converted, and the
        # spans agree with that
        text = "  compra  tres,  panes y veinte y tres. nada  "
        spans = numbers_to_digits_spans_es(text)
        self.assertEqual(" ".join(replaced(text, spans).split()),
                         numbers_to_digits_es(text))
        for span in spans:
            self.assertEqual(text[span.start:span.end], span.surface)

    def test_no_numbers_gives_no_spans(self):
        self.assertEqual(numbers_to_digits_spans_es(""), [])
        self.assertEqual(numbers_to_digits_spans_es("hola mundo"), [])

    def test_span_type(self):
        span = numbers_to_digits_spans_es("compra tres panes")[0]
        self.assertIsInstance(span, ConvertedNumber)
        self.assertEqual((span.start, span.end, span.value), (7, 11, 3))


class TestItalianSpansAreRefused(unittest.TestCase):
    def test_italian_rewrites_the_text_first(self):
        with self.assertRaises(NotImplementedError):
            IT.numbers_to_digits_spans("compra tre pani")
