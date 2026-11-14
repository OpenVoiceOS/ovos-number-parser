"""Collective nouns count groups of a fixed size.

Priberam: "dezena" is "Grupo de dez.", "dúzia" is "Conjunto de doze." and
"meia dúzia" is "Conjunto de seis.", "centena" is "Conjunto de 100
elementos.". "mil" is a numeral, so the whole cardinal it is part of counts
the noun, as "mil e uma" counts "artimanhas" in Priberam, "mil e um": "Grande
quantidade (ex.: ele tem mil e uma artimanhas)". "milhão" is a noun
(Priberam: "nome masculino", "Mil vezes mil"), so a collective noun after it
counts only the cardinal after it, and counts the "milhão" itself only right
after it, through "de". A collective noun ends its number: after "e" a new
number starts, unless half a group follows. The numbers_pt module docstring
holds the quotes. Expected values are hand arithmetic: the count times the
group size.
"""
import unittest

from ovos_number_parser import (extract_number, extract_number_spans,
                                 numbers_to_digits)


def spans(text, lang):
    return [(sp.value, text[sp.start:sp.end])
            for sp in extract_number_spans(text, lang=lang)]


class TestCountNouns(unittest.TestCase):
    #: text, value
    ROWS = [("uma dúzia de ovos", 12),
            ("duas dúzias", 2 * 12),
            ("meia dúzia de ovos", 12 // 2),
            ("dúzia e meia", 12 + 12 // 2),
            ("duas dúzias e meia", 2 * 12 + 12 // 2),
            ("doze dúzias", 12 * 12),
            ("cento e vinte dúzias", 120 * 12),
            ("mil e duas dúzias", (1000 + 2) * 12),
            ("duas mil e duzentas dúzias", 2200 * 12),
            ("mil duzentas dúzias", 1200 * 12),
            ("três mil e quinhentas centenas", 3500 * 100),
            # after "milhão" the noun counts only the cardinal after it
            ("um milhão e duas dúzias", 10 ** 6 + 2 * 12),
            ("um milhão e duzentas mil dúzias", 10 ** 6 + 200000 * 12),
            ("um milhão e duzentas mil e duas dúzias",
             10 ** 6 + 200002 * 12),
            ("dois milhões e quinhentas mil e uma dúzias",
             2 * 10 ** 6 + 500001 * 12),
            ("um milhão e meia dúzia", 10 ** 6 + 12 // 2),
            ("meio milhão e meia dúzia", 10 ** 6 // 2 + 12 // 2),
            # a half before the noun halves only the group
            ("cem e meia dúzia de ovos", 100 + 12 // 2),
            ("vinte e meia dúzia", 20 + 12 // 2),
            ("um e meia dúzia", 1 + 12 // 2),
            # "uma" right before the half is its article
            ("uma meia dúzia de ovos", 12 // 2),
            ("uma meia dezena", 10 // 2),
            ("uma meia centena", 100 // 2),
            # the article drops only itself: the number before it stays
            ("mil e uma meia dúzia", 1000 + 12 // 2),
            ("vinte e uma meia dúzia", 20 + 12 // 2),
            ("uma dezena de dias", 10),
            ("três dezenas", 3 * 10),
            ("uma centena de pessoas", 100),
            ("duas centenas", 2 * 100)]

    def test_the_count_multiplies_the_group(self):
        for lang in ("pt-PT", "pt-BR"):
            for text, value in self.ROWS:
                with self.subTest(text=text, lang=lang):
                    got = extract_number(text, lang=lang)
                    self.assertEqual(got, value)
                    self.assertIsInstance(got, int)

    def test_a_plural_with_no_count_is_no_number(self):
        for text in ("dúzias de ovos", "centenas de pessoas",
                     "dezenas de carros"):
            with self.subTest(text=text):
                self.assertFalse(extract_number(text, lang="pt-PT"))
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), text)

    def test_numbers_to_digits_writes_the_group(self):
        for text, digits in [("uma dúzia de ovos", "12 de ovos"),
                             ("meia dúzia de ovos", "6 de ovos"),
                             ("dúzia e meia de ovos", "18 de ovos"),
                             ("duas dúzias e meia", "30"),
                             ("um milhão e meia dúzia", "1000006"),
                             ("cem e meia dúzia de ovos", "106 de ovos"),
                             ("uma meia dúzia de ovos", "6 de ovos"),
                             ("três dezenas de carros", "30 de carros")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), digits)

    def test_a_half_before_a_scale_noun_is_a_whole_number(self):
        # half of a thousand is 500 units, written without a decimal part
        for text, digits in [("meio milhar de euros", "500 de euros"),
                             ("meio milhão de pessoas", "500000 de pessoas")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), digits)
                self.assertIsInstance(extract_number(text, lang="pt-PT"), int)

    def test_a_half_of_a_large_scale_is_exact(self):
        # half of 10 ** 24 is 5 * 10 ** 23; the float 5e+23 cast with int()
        # gives 499999999999999991611392
        for lang, text in [("pt-PT", "meio quatrilião"), ("es-ES", "medio cuatrillón"),
                           ("it-IT", "mezzo quadrilione")]:
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang=lang, short_scale=False),
                                 5 * 10 ** 23)
        self.assertEqual(numbers_to_digits("meio quatrilião de euros", lang="pt-PT"),
                         f"{5 * 10 ** 23} de euros")


class TestDecimalBeforeCountNoun(unittest.TestCase):
    def test_a_decimal_counts_the_group(self):
        # as before a scale word ("dois vírgula cinco milhões"), the decimal
        # times the group size
        for text, value, digits in [
                ("dois vírgula cinco dúzias", 30, "30"),
                ("um vírgula cinco centenas", 150, "150"),
                ("dois vírgula cinco dezenas de pessoas", 25, "25 de pessoas"),
                # the noun counts the whole compound, not its unit
                ("dois vírgula vinte e cinco centenas", 225, "225")]:
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="pt-PT"), value)
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), digits)

    def test_a_decimal_after_a_scale_does_not_count_the_group(self):
        # a scale word before the marker keeps the plain decimal, so the
        # collective noun counts nothing and stays text
        for text, value, digits in [
                ("um milhão vírgula cinco dúzias", 1000000.5,
                 "1000000.5 dúzias"),
                ("mil vírgula cinco dúzias de ovos", 1000.5,
                 "1000.5 dúzias de ovos")]:
            with self.subTest(text=text):
                self.assertEqual(extract_number(text, lang="pt-PT"), value)
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), digits)

    def test_a_half_before_a_plural_stays_text(self):
        # a half halves one group, so before a plural it builds no number
        for text, digits in [
                ("meio milhões de pessoas", "meio milhões de pessoas"),
                ("dois e meio milhares de pessoas",
                 "2 e meio milhares de pessoas"),
                ("meias dúzias de ovos", "meias dúzias de ovos")]:
            with self.subTest(text=text):
                self.assertEqual(numbers_to_digits(text, lang="pt-PT"), digits)

    def test_a_marker_before_a_collective_noun_stays_text(self):
        # no number word follows the marker, so no decimal starts there
        self.assertEqual(
            numbers_to_digits("custou dois vírgula dúzias de ovos", lang="pt-PT"),
            "custou 2 vírgula dúzias de ovos")


class TestDigitsBeforeCountNoun(unittest.TestCase):
    """Digits count a collective noun right after them, as a count in words."""

    def test_the_digits_count_the_group(self):
        for lang in ("pt-PT", "pt-BR"):
            for text, value, digits in [
                    ("2 dúzias de ovos", 2 * 12, "24 de ovos"),
                    ("1 dúzia", 12, "12"),
                    ("3 dezenas", 3 * 10, "30"),
                    ("5 centenas de pessoas", 5 * 100, "500 de pessoas"),
                    ("12 dúzias", 12 * 12, "144"),
                    ("-2 dúzias", -2 * 12, "-24"),
                    ("2,5 dúzias", 30, "30"),
                    # a half after the noun is half a group
                    ("2 dúzias e meia", 2 * 12 + 12 // 2, "30"),
                    ("1 dúzia e meia de ovos", 12 + 12 // 2, "18 de ovos"),
                    # a mark after the noun stays in the text
                    ("2 dúzias, disse", 2 * 12, "24, disse"),
                    # after a scale word the noun counts the whole number
                    ("2 mil dúzias", 2 * 1000 * 12, "24000"),
                    # a half after the noun is half a group there too
                    ("2 mil dúzias e meia", 2 * 1000 * 12 + 12 // 2, "24006"),
                    ("2 mil dezenas e meia", 2 * 1000 * 10 + 10 // 2, "20005")]:
                with self.subTest(lang=lang, text=text):
                    got = extract_number(text, lang=lang)
                    self.assertEqual(got, value)
                    self.assertIsInstance(got, int)
                    self.assertEqual(numbers_to_digits(text, lang=lang), digits)

    def test_a_mark_after_the_digits_ends_the_count(self):
        self.assertEqual(extract_number("nota 2, dúzias de vezes", lang="pt-PT"), 2)
        self.assertEqual(numbers_to_digits("nota 2, dúzias de vezes", lang="pt-PT"),
                         "nota 2, dúzias de vezes")


class TestCountNounAfterScale(unittest.TestCase):
    """Right after a scale word a collective noun counts the whole number."""

    def test_the_noun_multiplies_the_whole_number(self):
        for lang in ("pt-PT", "pt-BR"):
            for text, value in [
                    ("mil dúzias", 1000 * 12),
                    ("duas mil dúzias", 2000 * 12),
                    ("cem mil dúzias de ovos", 100000 * 12),
                    ("um milhão de dúzias", 10 ** 6 * 12),
                    ("dois milhões de dúzias", 2 * 10 ** 6 * 12),
                    ("meio milhão de dúzias", 10 ** 6 // 2 * 12),
                    ("um milhão duzentos mil dúzias", 10 ** 6 + 200000 * 12)]:
                with self.subTest(lang=lang, text=text):
                    self.assertEqual(extract_number(text, lang=lang), value)

    def test_after_a_smaller_scale_the_noun_counts_only_its_group(self):
        # pt-PT "bilião" is 10 ** 12, pt-BR "bilhão" is 10 ** 9
        for lang, text, value in [
                ("pt-PT", "um bilião e dois milhões de dúzias",
                 10 ** 12 + 2 * 10 ** 6 * 12),
                ("pt-BR", "um bilhão e dois milhões de dúzias",
                 10 ** 9 + 2 * 10 ** 6 * 12)]:
            with self.subTest(lang=lang, text=text):
                self.assertEqual(extract_number(text, lang=lang), value)

    def test_numbers_to_digits_writes_the_whole_number(self):
        self.assertEqual(numbers_to_digits("duas mil dúzias de ovos", lang="pt-PT"),
                         "24000 de ovos")


class TestNounEndsNumber(unittest.TestCase):
    """A collective noun ends its number: after "e" a new number starts.
    extract_number gives the first number, extract_number_spans each one."""

    #: text, spans, digits
    ROWS = [
        ("mil e duas dúzias", [(1002 * 12, "mil e duas dúzias")], "12024"),
        ("um milhão e duas dúzias",
         [(10 ** 6 + 2 * 12, "um milhão e duas dúzias")], "1000024"),
        ("uma dúzia e duas mil dúzias",
         [(12, "uma dúzia"), (2000 * 12, "duas mil dúzias")], "12 e 24000"),
        ("duas dúzias e um milhão de dúzias",
         [(2 * 12, "duas dúzias"), (10 ** 6 * 12, "um milhão de dúzias")],
         "24 e 12000000"),
        ("comprou duas dúzias de ovos e ganhou um milhão de euros",
         [(2 * 12, "duas dúzias"), (10 ** 6, "um milhão")],
         "comprou 24 de ovos e ganhou 1000000 de euros"),
        ("dois milhões de dúzias e três milhões",
         [(2 * 10 ** 6 * 12, "dois milhões de dúzias"),
          (3 * 10 ** 6, "três milhões")], "24000000 e 3000000"),
        ("uma dúzia e três", [(12, "uma dúzia"), (3, "três")], "12 e 3"),
        ("meia dúzia e uma", [(12 // 2, "meia dúzia"), (1, "uma")], "6 e 1"),
        ("duas dúzias e três dúzias",
         [(2 * 12, "duas dúzias"), (3 * 12, "três dúzias")], "24 e 36"),
        ("uma dúzia e uma dúzia",
         [(12, "uma dúzia"), (12, "uma dúzia")], "12 e 12"),
        ("duas mil dúzias e duas dúzias",
         [(2000 * 12, "duas mil dúzias"), (2 * 12, "duas dúzias")],
         "24000 e 24"),
        ("um milhão de dúzias e duas dúzias",
         [(10 ** 6 * 12, "um milhão de dúzias"), (2 * 12, "duas dúzias")],
         "12000000 e 24"),
        ("três mil dezenas e duas dezenas",
         [(3000 * 10, "três mil dezenas"), (2 * 10, "duas dezenas")],
         "30000 e 20"),
        ("mil dúzias e três centenas",
         [(1000 * 12, "mil dúzias"), (3 * 100, "três centenas")],
         "12000 e 300"),
        ("um milhão e meia dúzia e duas dúzias",
         [(10 ** 6 + 12 // 2, "um milhão e meia dúzia"),
          (2 * 12, "duas dúzias")], "1000006 e 24"),
        ("um milhão e duas dúzias e mil dúzias",
         [(10 ** 6 + 2 * 12, "um milhão e duas dúzias"),
          (1000 * 12, "mil dúzias")], "1000024 e 12000"),
        ("cinco dúzias e meia e duas dúzias",
         [(5 * 12 + 12 // 2, "cinco dúzias e meia"), (2 * 12, "duas dúzias")],
         "66 e 24"),
        ("uma dúzia e meia de ovos e duas dúzias de pães",
         [(12 + 12 // 2, "uma dúzia e meia"), (2 * 12, "duas dúzias")],
         "18 de ovos e 24 de pães"),
        ("comprei duas dúzias e uma meia dúzia",
         [(2 * 12, "duas dúzias"), (12 // 2, "uma meia dúzia")],
         "comprei 24 e 6"),
        ("duas dezenas de milhar e três dúzias",
         [(2 * 10 * 1000, "duas dezenas de milhar"), (3 * 12, "três dúzias")],
         "20000 e 36"),
        ("uma dúzia e duas dezenas de milhar",
         [(12, "uma dúzia"), (2 * 10 * 1000, "duas dezenas de milhar")],
         "12 e 20000"),
        ("mil e duas dúzias e mil e três dúzias",
         [(1002 * 12, "mil e duas dúzias"), (1003 * 12, "mil e três dúzias")],
         "12024 e 12036"),
        ("um milhão de dúzias e dois milhões de dúzias",
         [(10 ** 6 * 12, "um milhão de dúzias"),
          (2 * 10 ** 6 * 12, "dois milhões de dúzias")],
         "12000000 e 24000000"),
        ("mil milhões de dúzias e dois milhões",
         [(10 ** 9 * 12, "mil milhões de dúzias"),
          (2 * 10 ** 6, "dois milhões")], "12000000000 e 2000000"),
        ("duas dezenas de milhar e um milhão",
         [(2 * 10 * 1000, "duas dezenas de milhar"), (10 ** 6, "um milhão")],
         "20000 e 1000000")]

    def test_extract_number_gives_the_first_number(self):
        for lang in ("pt-PT", "pt-BR"):
            for text, expected, _ in self.ROWS:
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(extract_number(text, lang=lang),
                                     expected[0][0])

    def test_each_number_is_a_span(self):
        for lang in ("pt-PT", "pt-BR"):
            for text, expected, _ in self.ROWS:
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(spans(text, lang), expected)

    def test_numbers_to_digits_writes_each_number(self):
        for lang in ("pt-PT", "pt-BR"):
            for text, _, digits in self.ROWS:
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(numbers_to_digits(text, lang=lang), digits)


class TestNounBeforeMilhar(unittest.TestCase):
    """"N dezenas de milhar" counts tens of thousands."""

    def test_milhar_multiplies_the_noun_before_it(self):
        for lang in ("pt-PT", "pt-BR"):
            for text, value, digits in [
                    ("duas dezenas de milhar", 2 * 10 * 1000, "20000"),
                    ("três centenas de milhar de euros", 3 * 100 * 1000,
                     "300000 de euros"),
                    ("meia dúzia de milhar", 6 * 1000, "6000"),
                    ("duas dezenas de milhar de dúzias", 2 * 10 * 1000 * 12,
                     "240000")]:
                with self.subTest(lang=lang, text=text):
                    self.assertEqual(extract_number(text, lang=lang), value)
                    self.assertEqual(numbers_to_digits(text, lang=lang), digits)


class TestHalfEndsNumber(unittest.TestCase):
    """A half after a scale noun ends its number, as a collective noun does."""

    def test_each_count_is_a_span(self):
        for lang in ("pt-PT", "pt-BR"):
            for text, expected, digits in [
                    ("um milhão e meio e duas dúzias",
                     [(10 ** 6 + 10 ** 6 // 2, "um milhão e meio"),
                      (2 * 12, "duas dúzias")], "1500000 e 24")]:
                with self.subTest(text=text, lang=lang):
                    self.assertEqual(spans(text, lang), expected)
                    self.assertEqual(numbers_to_digits(text, lang=lang), digits)
