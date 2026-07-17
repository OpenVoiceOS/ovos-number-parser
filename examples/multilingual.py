"""Multilingual round-trip across several supported languages.

The same API (`pronounce_number` + `extract_number`) works for 40 languages.
Dialects resolve by prefix, so "pt-BR", "pt-PT" and "pt" all reach Portuguese.

    pip install ovos-number-parser
    python multilingual.py
"""
from ovos_number_parser import pronounce_number, extract_number

LANGS = {
    "en": "English", "es": "Spanish", "pt": "Portuguese", "de": "German",
    "fr": "French", "it": "Italian", "nl": "Dutch", "ru": "Russian",
    "uk": "Ukrainian", "ca": "Catalan",
}

print("2023 spoken in every language, then parsed back to digits:\n")
for code, name in LANGS.items():
    spoken = pronounce_number(2023, code)
    back = extract_number(spoken, code)
    print(f"  {name:12} ({code}) {spoken:38} -> {back}")

# Expected output (verified):
# 2023 spoken in every language, then parsed back to digits:
#
#   English      (en) two thousand, twenty three                -> 2023
#   Spanish      (es) dos mil veintitrés                        -> 2023
#   Portuguese   (pt) dois mil e vinte e três                   -> 2023
#   German       (de) zweitausenddreiundzwanzig                 -> 2023
#   French       (fr) deux mille vingt-trois                    -> 2023
#   Italian      (it) duemila, ventitre                         -> 2023
#   Dutch        (nl) tweeduizenddrieentwintig                  -> 2023
#   Russian      (ru) две тысячи двадцать три                   -> 2023.0
#   Ukrainian    (uk) дві тисячі двадцять три                   -> 2023
#   Catalan      (ca) dos mil vint-i-tres                       -> 2023
