"""TTS normalization: numbers -> spoken words.

Most speech synthesizers read raw digits badly ("1234" as "one-two-three-four",
"3.5" as "three-dot-five"). Expand numbers into words *before* handing text to
the synthesizer and it reads naturally.

Pure Python, no OVOS assistant stack required:

    pip install ovos-number-parser
    python tts_normalization.py

`pronounce_number` handles cardinals, decimals, negatives and scientific
notation. `pronounce_ordinal` (and `pronounce_number(..., ordinals=True)`)
handle "1st, 2nd, 3rd". `pronounce_fraction` speaks fraction strings.
"""
import re
from ovos_number_parser import pronounce_number, pronounce_ordinal

# --- Expand every standalone integer/decimal in a sentence ----------------
def expand_numbers(text: str, lang: str = "en") -> str:
    def repl(match):
        raw = match.group(0)
        value = float(raw) if "." in raw else int(raw)
        return pronounce_number(value, lang)
    return re.sub(r"-?\d+(?:\.\d+)?", repl, text)


SENTENCES = [
    "the invoice total is 1234.56 dollars",
    "water boils at 100 degrees",
    "the temperature dropped to -3.5 tonight",
]
for s in SENTENCES:
    print(f"{s!r}\n   -> {expand_numbers(s)!r}\n")

# --- Cardinals, decimals, ordinals ----------------------------------------
print("3.5            ->", pronounce_number(3.5, "en"))
print("2023           ->", pronounce_number(2023, "en"))
print("ordinal 21     ->", pronounce_ordinal(21, "en"))
print("5 (ordinal)    ->", pronounce_number(5, "en", ordinals=True))

# Expected output (verified):
# 'the invoice total is 1234.56 dollars'
#    -> 'the invoice total is one thousand, two hundred and thirty four point five six dollars'
#
# 'water boils at 100 degrees'
#    -> 'water boils at one hundred degrees'
#
# 'the temperature dropped to -3.5 tonight'
#    -> 'the temperature dropped to minus three point five tonight'
#
# 3.5            -> three point five
# 2023           -> two thousand, twenty three
# ordinal 21     -> twenty-first
# 5 (ordinal)    -> fifth
