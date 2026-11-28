"""French ordinals from the French engine.

Expected values come from the Trésor de la langue française informatisé
(TLFi, ATILF / CNRS), read on cnrtl.fr:

- "-ième": "-ième sert à former des adjectifs numéraux ordinaux signifiant
  « qui occupe le rang marqué par le nombre désigné par la base » : deuxième,
  troisième, centième, cent unième, deux cent troisième, etc."
- "unième": "Adj. numéral ordinal formé au moyen du suff. -ième sur les
  nombres cardinaux composés en et un, (—) un: vingt et unième, quatre
  vingt-unième, cent unième, etc."
- "neuvième": "le dix-neuvième concurrent"; "cinquième": "Qui occupe le rang
  marqué par le nombre cinq".
- "quatre-vingtième": "Qui occupe le rang marqué par le nombre quatre-vingts".
- "millième": "Qui occupe le rang marqué par le nombre mille".
- "millionième": "Adj. numéral ordinal. Qui occupe le rang marqué par le
  nombre d'un million".
- "premier, première, adjectif" (headword).

Académie française, Dire, Ne pas dire, "Étonnants numéraux ordinaux"
(6 janvier 2022): the usual form is "en ‑ième (à l'exception notable de
premier), formée à partir des numéraux cardinaux", and "Unième, sans
existence autonome, ne se rencontre qu'en composition : vingt et unième, cent
unième, etc."

Académie française, Dictionnaire, 9e édition, "vingt" and "cent" (as quoted
in numbers_fr.py): vingt and cent "restent invariables s'ils sont suivis d'un
autre nombre ou de mille", and agree before million and milliard, "qui sont
des noms et non des adjectifs numéraux". "millionième" is an adjective numeral
(TLFi), so "deux cents millions" gives "deux cent millionième", while the noun
"millions" keeps its -s before another number ("deux millions cent
millième").

The ordinal keeps the spelling of the engine's own cardinal ("vingt-et-un",
"cent un"), so "vingt et unième" reads "vingt-et-unième" here. That is the
spelling of the 1990 rectifications: OQLF, Banque de dépannage
linguistique, "Rectifications liées aux nombres composés" (fiche 23163):
"Les nombres composés et les adjectifs ordinaux composés sont
systématiquement reliés par des traits d'union [...] cent-deuxième". The
same fiche hyphenates "cent-deuxième", while the engine keeps the space in
"cent unième", the traditional spelling the TLFi gives.
"""
import unittest

from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.util import GrammaticalGender

FEMININE = GrammaticalGender.FEMININE


class TestFrenchNativeOrdinals(unittest.TestCase):
    def assertOrdinal(self, cases, lang="fr", **kwargs):
        for number, expected in cases:
            with self.subTest(lang=lang, number=number, **{k: str(v) for k, v in kwargs.items()}):
                self.assertEqual(
                    pronounce_number(number, lang, ordinals=True, **kwargs),
                    expected)
                self.assertEqual(pronounce_ordinal(number, lang, **kwargs),
                                 expected)

    def test_tlfi_suffix_examples(self):
        # "le deuxième jour", "la centième représentation"
        self.assertOrdinal([
            (2, "deuxième"),
            (3, "troisième"),
            (100, "centième"),
            (101, "cent unième"),
            (203, "deux cent troisième"),
        ])

    def test_unieme_in_compounds(self):
        # "le vingt et unième siècle", "la quatre-vingt-unième minute"
        self.assertOrdinal([
            (21, "vingt-et-unième"),
            (81, "quatre-vingt-unième"),
            (101, "cent unième"),
            (1001, "mille unième"),
        ])

    def test_stem_changes(self):
        # "le cinquième acte", "le dix-neuvième concurrent"
        self.assertOrdinal([
            (5, "cinquième"),
            (9, "neuvième"),
            (11, "onzième"),
            (19, "dix-neuvième"),
            (35, "trente-cinquième"),
            (99, "quatre-vingt-dix-neuvième"),
        ])

    def test_plural_s_drops(self):
        # "sa quatre-vingtième année"
        self.assertOrdinal([
            (80, "quatre-vingtième"),
            (200, "deux centième"),
            (2 * 10 ** 6, "deux millionième"),
            (2 * 10 ** 8, "deux cent millionième"),
            (80 * 10 ** 6, "quatre-vingt millionième"),
            (2_100_000, "deux millions cent millième"),
        ])

    def test_scale_words(self):
        # "la millième représentation", "le millionième visiteur"
        self.assertOrdinal([
            (1000, "millième"),
            (2000, "deux millième"),
            (10 ** 6, "millionième"),
        ])

    def test_feminine(self):
        # "la première fois", "la vingt et unième fois"
        self.assertOrdinal([
            (1, "première"),
            (2, "deuxième"),
            (21, "vingt-et-unième"),
        ], gender=FEMININE)

    def test_regional_tens(self):
        self.assertOrdinal([(71, "septante-et-unième"),
                            (81, "quatre-vingt-unième"),
                            (91, "nonante-et-unième"),
                            (10 ** 6, "millionième")], lang="fr-BE")
        self.assertOrdinal([(81, "huitante-et-unième"),
                            (1, "première")], lang="fr-CH", gender=FEMININE)


if __name__ == "__main__":
    unittest.main()
