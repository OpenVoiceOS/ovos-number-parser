import unittest

from ovos_number_parser import NumberSpan, extract_number_spans


class SpanAssertions(unittest.TestCase):
    def assertSpans(self, text, lang, expected, **kwargs):
        """Compare (surface, value) pairs and check the offset invariant."""
        spans = extract_number_spans(text, lang, **kwargs)
        self.assertEqual([(s.surface, s.value) for s in spans], expected)
        for span in spans:
            self.assertEqual(text[span.start:span.end], span.surface)
        self.assertEqual(spans, sorted(spans, key=lambda s: s.start))
        return spans


class TestNumberSpansEN(SpanAssertions):
    def test_single_number(self):
        self.assertSpans("set the timer for seven minutes", "en", [("seven", 7)])

    def test_two_separated_numbers(self):
        self.assertSpans("set alarm for 7 and another for 9", "en",
                         [("7", 7), ("9", 9)])

    def test_multi_word_number(self):
        self.assertSpans("two hundred and five people came", "en",
                         [("two hundred and five", 205)])

    def test_decimal_digits(self):
        self.assertSpans("it is 3.5 meters wide", "en", [("3.5", 3.5)])

    def test_number_adjacent_to_punctuation(self):
        self.assertSpans("at 7, please", "en", [("7", 7)])

    def test_hyphenated_compound(self):
        self.assertSpans("twenty-two candles", "en", [("twenty-two", 22)])

    def test_ordinals_are_opt_in(self):
        self.assertSpans("march fifth", "en", [])
        self.assertSpans("march fifth", "en", [("fifth", 5)], ordinals=True)

    def test_text_without_numbers(self):
        self.assertSpans("hello how are you", "en", [])

    def test_number_at_both_ends(self):
        self.assertSpans("7 lives left of 9", "en", [("7", 7), ("9", 9)])

    def test_offsets_are_code_points(self):
        # a byte oriented implementation reads 9 here instead of 7
        spans = self.assertSpans("café ☕ 7 uhr", "en", [("7", 7)])
        self.assertEqual(spans[0].start, 7)

    def test_adjacent_numbers_do_not_merge(self):
        self.assertSpans("twenty two and thirty three", "en",
                         [("twenty two", 22), ("thirty three", 33)])

    def test_neighbouring_numbers_are_not_swallowed(self):
        # the extractor answers "3" for the incoherent fragment "two three",
        # which must not read as the phrase having grown
        self.assertSpans("two three hundred", "en",
                         [("two", 2), ("three hundred", 300)])
        self.assertSpans("twenty twenty-two", "en",
                         [("twenty", 20), ("twenty-two", 22)])
        self.assertSpans("one two three", "en",
                         [("one", 1), ("two", 2), ("three", 3)])

    def test_compound_numbers_still_grow(self):
        self.assertSpans("two hundred and five", "en",
                         [("two hundred and five", 205)])
        self.assertSpans("twenty two", "en", [("twenty two", 22)])
        self.assertSpans("one hundred twenty three thousand four hundred fifty six",
                         "en", [("one hundred twenty three thousand four hundred fifty six",
                                 123456)])

    def test_fraction_before_number_does_not_merge(self):
        self.assertSpans("half past two", "en", [("half", 0.5), ("two", 2)])

    def test_span_is_frozen(self):
        span = extract_number_spans("nine", "en")[0]
        self.assertIsInstance(span, NumberSpan)
        with self.assertRaises(Exception):
            span.value = 3


class TestNumberSpansPT(SpanAssertions):
    def test_single_number(self):
        self.assertSpans("quero dezasseis", "pt", [("dezasseis", 16)])

    def test_two_separated_numbers(self):
        self.assertSpans("alarme às 7 e outro às 9", "pt", [("7", 7), ("9", 9)])

    def test_multi_word_number(self):
        self.assertSpans("quero duzentos e cinquenta e três, por favor", "pt",
                         [("duzentos e cinquenta e três", 253)])

    def test_spoken_decimal(self):
        self.assertSpans("dez ponto cinco graus", "pt", [("dez ponto cinco", 10.5)])

    def test_decimal_digits_with_comma(self):
        self.assertSpans("3,5 metros", "pt", [("3,5", 3.5)])

    def test_number_adjacent_to_punctuation(self):
        self.assertSpans("às 7, por favor", "pt", [("7", 7)])

    def test_conjunction_number_is_one_span(self):
        self.assertSpans("vinte e um dias", "pt", [("vinte e um", 21)])

    def test_ordinals_are_opt_in(self):
        self.assertSpans("o segundo carro", "pt", [])
        self.assertSpans("o segundo carro", "pt", [("segundo", 2)], ordinals=True)

    def test_text_without_numbers(self):
        self.assertSpans("olá como estás", "pt", [])

    def test_offsets_are_code_points(self):
        spans = self.assertSpans("café: vinte e um", "pt", [("vinte e um", 21)])
        self.assertEqual(spans[0].start, 6)


class TestNumberSpansDE(SpanAssertions):
    def test_single_number(self):
        self.assertSpans("stell den wecker auf sieben minuten", "de",
                         [("sieben", 7)])

    def test_two_separated_numbers(self):
        self.assertSpans("wecker um 7 und um 9", "de",
                         [("7", 7), ("9", 9)])

    def test_compound_number_is_one_span(self):
        self.assertSpans("zweihundertdreiundvierzig gäste", "de",
                         [("zweihundertdreiundvierzig", 243)])

    def test_spoken_decimal(self):
        self.assertSpans("sieben komma fünf grad", "de",
                         [("sieben komma fünf", 7.5)])

    def test_number_adjacent_to_punctuation(self):
        self.assertSpans("um 7, bitte", "de", [("7", 7)])

    def test_ordinals_are_opt_in(self):
        self.assertSpans("der dritte", "de", [])
        self.assertSpans("der dritte", "de", [("dritte", 3)], ordinals=True)

    def test_text_without_numbers(self):
        self.assertSpans("hallo wie geht es dir", "de", [])

    def test_offsets_are_code_points(self):
        spans = self.assertSpans("☕ zweiundzwanzig", "de",
                                 [("zweiundzwanzig", 22)])
        self.assertEqual(spans[0].start, 2)


if __name__ == "__main__":
    unittest.main()
