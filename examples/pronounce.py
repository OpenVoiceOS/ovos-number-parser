"""Pronounce numbers in several languages."""
from ovos_number_parser import pronounce_number, pronounce_ordinal
from ovos_number_parser.util import GrammaticalGender

LANGS = ["en", "de", "es", "pt", "gl", "cs", "sv", "eu", "fa", "ru"]

for lang in LANGS:
    print(f"--- {lang}")
    for n in [7, 21, 123, 2023]:
        print(f"  {n:>6} -> {pronounce_number(n, lang)}")

# decimals and negative numbers
print(pronounce_number(-3.14, "en", places=2))   # minus three point one four
print(pronounce_number(4.5, "pt"))               # quatro vírgula cinco

# ordinals
print(pronounce_number(3, "en", ordinals=True))  # third
print(pronounce_ordinal(5, "de"))                # fünfte

# grammatical gender (Portuguese: "uma hora" vs "um minuto")
print(pronounce_number(1, "pt", gender=GrammaticalGender.FEMININE))  # uma
print(pronounce_number(2, "pt", gender=GrammaticalGender.FEMININE))  # duas
