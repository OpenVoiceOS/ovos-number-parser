import unittest

from ovos_number_parser.numbers_it import (extract_number_it,
                                           pronounce_number_it)


class TestItalianHundredsMultiplier(unittest.TestCase):
    def test_bare_cento_after_thousand_adds(self):
        # "mille cento" is 1000 + 100, not 1000 * 100
        self.assertEqual(extract_number_it("mille cento"), 1100)
        self.assertEqual(extract_number_it("mille cento uno"), 1101)
        self.assertEqual(extract_number_it("duemila cento"), 2100)
        self.assertEqual(extract_number_it("tremila cento cinquanta"), 3150)

    def test_solid_and_spaced_agree(self):
        self.assertEqual(extract_number_it("millecento"),
                         extract_number_it("mille cento"))
        self.assertEqual(extract_number_it("milleduecento"), 1200)

    def test_cento_as_multiplier_still_works(self):
        # a hundreds multiplier still scales a smaller preceding value
        self.assertEqual(extract_number_it("due cento"), 200)
        self.assertEqual(extract_number_it("cinque cento"), 500)
        self.assertEqual(extract_number_it("cento"), 100)
        self.assertEqual(extract_number_it("cento mila"), 100000)
        self.assertEqual(extract_number_it("duecentomila"), 200000)

    def test_natural_sentences(self):
        self.assertEqual(
            extract_number_it("ho bisogno di mille cento pezzi"), 1100)
        self.assertEqual(
            extract_number_it("il costo è di duemila cento euro"), 2100)

    def test_roundtrip_up_to_100000(self):
        # every value the engine can pronounce must extract back to itself
        bad = []
        for n in list(range(0, 3000)) + list(range(3000, 100001, 331)):
            if extract_number_it(pronounce_number_it(n)) != n:
                bad.append(n)
        self.assertEqual(bad, [], f"round-trip failures: {bad[:10]}")


if __name__ == "__main__":
    unittest.main()
