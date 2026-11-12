"""Spanish ordinals in both genders, read by the Castilian engine.

Every expected value is an example from the Diccionario panhispánico de dudas
(RAE and ASALE, 2nd ed.), entry "ordinales" (https://www.rae.es/dpd/ordinales):

- § 1, table: "1.º (1.er), 1.ª ... primero (apocopado primer), fem. primera";
  "120.º, 120.ª ... centésimo vigésimo, fem. centésima vigésima"; "1248.º ...
  milésimo ducentésimo cuadragésimo octavo"; "2000.º ... dosmilésimo";
  "10 000.º ... diezmilésimo"; "100 000.º ... cienmilésimo"; "500 000.º ...
  quinientosmilésimo"; "1 000 000.º ... millonésimo". Table note: "se entiende
  que el femenino se forma sustituyendo la -o final por una -a".
- § 2c: "las etimológicas simples undécimo y duodécimo, que son las preferidas
  en el uso culto".
- § 2d: "tresmilésimo tricentésimo cuadragésimo quinto (3345.º) ...
  milmillonésimo (1 000 000 000.º)".
- § 3: for the first and second decade "siempre preferible la grafía
  univerbal (decimotercero, decimocuarto, vigesimoprimero, vigesimoctavo,
  etc.)"; from the third decade "trigésimo primero"; one-word ordinals vary
  only in the second part ("vigesimoprimera"), two-word ordinals in both
  ("vigésima primera").
- § 5: "vigesimoctavo (mejor que vigesimooctavo)".

A count before a scale ordinal joins it as one word, by § 2d: "se forman
prefijando al ordinal simple el cardinal que lo multiplica". The count keeps
the form it has before the scale noun ("treinta y un mil", "doscientos un
mil"), written as one word as DPD "cardinales" § 2 allows: "treintaicinco,
cuarentaitrés, cincuentaiocho ... Estas grafías simples son asimismo
válidas". One word has one written accent, on its last part (§ 3: "se
acentúa gráficamente teniendo en cuenta su único acento prosódico, el que
recae sobre la sílaba tónica del último componente"), so "dieciséis" and
"veintidós" lose theirs. DPD "fraccionarios" § 4 writes the fraction noun of
the same number the same way ("cienmilmillonésimo"), and the fraction noun
of a multiple of mil or millón is its ordinal (§ 2), so the two readings
agree.
"""
import unittest

from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.numbers_es import fraction_noun_es
from ovos_number_parser.util import GrammaticalGender

M = GrammaticalGender.MASCULINE
F = GrammaticalGender.FEMININE

# "el ___ piso", "la ___ edición"
CASES = [
    (1, "primero", "primera"),
    (4, "cuarto", "cuarta"),
    (10, "décimo", "décima"),
    (11, "undécimo", "undécima"),
    (12, "duodécimo", "duodécima"),
    (13, "decimotercero", "decimotercera"),
    (14, "decimocuarto", "decimocuarta"),
    (21, "vigesimoprimero", "vigesimoprimera"),
    (28, "vigesimoctavo", "vigesimoctava"),
    (31, "trigésimo primero", "trigésima primera"),
    (101, "centésimo primero", "centésima primera"),
    (120, "centésimo vigésimo", "centésima vigésima"),
    (134, "centésimo trigésimo cuarto", "centésima trigésima cuarta"),
    (800, "octingentésimo", "octingentésima"),
    (1000, "milésimo", "milésima"),
    (1248, "milésimo ducentésimo cuadragésimo octavo",
     "milésima ducentésima cuadragésima octava"),
    (2000, "dosmilésimo", "dosmilésima"),
    (3345, "tresmilésimo tricentésimo cuadragésimo quinto",
     "tresmilésima tricentésima cuadragésima quinta"),
    (10000, "diezmilésimo", "diezmilésima"),
    (100000, "cienmilésimo", "cienmilésima"),
    (500000, "quinientosmilésimo", "quinientosmilésima"),
    (10 ** 6, "millonésimo", "millonésima"),
    (10 ** 9, "milmillonésimo", "milmillonésima"),
    (16000, "dieciseismilésimo", "dieciseismilésima"),
    (22000, "veintidosmilésimo", "veintidosmilésima"),
    (31000, "treintaiunmilésimo", "treintaiunmilésima"),
    (201000, "doscientosunmilésimo", "doscientosunmilésima"),
    (10 ** 11, "cienmilmillonésimo", "cienmilmillonésima"),
]


class TestSpanishOrdinals(unittest.TestCase):
    def test_pronounce_number_ordinals(self):
        for number, masculine, feminine in CASES:
            for gender, expected in ((M, masculine), (F, feminine)):
                with self.subTest(number=number, gender=gender.name):
                    self.assertEqual(
                        pronounce_number(number, "es", ordinals=True,
                                         gender=gender),
                        expected)

    def test_pronounce_ordinal(self):
        for number, masculine, feminine in CASES:
            for gender, expected in ((M, masculine), (F, feminine)):
                with self.subTest(number=number, gender=gender.name):
                    self.assertEqual(
                        pronounce_ordinal(number, "es", gender=gender),
                        expected)

    def test_ordinal_and_fraction_noun_agree(self):
        for count in (2, 16, 21, 22, 31, 45, 100, 201, 999):
            for scale in (10 ** 3, 10 ** 6):
                number = count * scale
                with self.subTest(number=number):
                    self.assertEqual(pronounce_ordinal(number, "es"),
                                     fraction_noun_es(number))

    def test_no_ordinal_from_ten_to_the_24(self):
        # the vocabulary has no ordinal scale word past "trillonésimo"
        for number in (10 ** 24, 10 ** 30):
            with self.subTest(number=number):
                with self.assertRaises(NotImplementedError):
                    pronounce_ordinal(number, "es")


if __name__ == "__main__":
    unittest.main()
