"""ASR post-processing / inverse text normalization (ITN).

Speech-to-text engines emit numbers as *words* ("twenty three", "three point
five"). Downstream systems (search, commands, databases) want *digits*. This
script turns spoken-form transcripts into digit form.

Pure Python, no OVOS assistant stack required:

    pip install ovos-number-parser
    python asr_itn.py

`numbers_to_digits` rewrites the numbers inside a sentence and leaves the rest
of the words untouched. `extract_number` pulls a single value out when you only
want the number itself (e.g. slot filling).
"""
from ovos_number_parser import numbers_to_digits, extract_number

# --- Rewrite whole ASR transcripts (English) ------------------------------
TRANSCRIPTS = [
    "set a timer for five minutes",
    "the meeting is at three thirty",
    "i need twenty three of them",
    "order two hundred units please",
]
for t in TRANSCRIPTS:
    print(f"{t!r:48} -> {numbers_to_digits(t, 'en')!r}")

# --- Pull one value out for slot filling ----------------------------------
print()
print("point five  ->", extract_number("three point five liters", "en"))   # 3.5
print("fractions   ->", extract_number("two and a half cups", "en"))       # 2.5

# --- Works in other languages too -----------------------------------------
print()
print("es:", numbers_to_digits("quiero cinco manzanas", "es"))
print("de:", numbers_to_digits("ich haette gern dreihundert gramm", "de"))
print("nl:", numbers_to_digits("ik wil eenentwintig appels", "nl"))

# Expected output (verified):
# 'set a timer for five minutes'                   -> 'set a timer for 5 minutes'
# 'the meeting is at three thirty'                 -> 'the meeting is at 3 30'
# 'i need twenty three of them'                    -> 'i need 23 of them'
# 'order two hundred units please'                 -> 'order 200 units please'
#
# point five  -> 3.5
# fractions   -> 2.5
#
# es: quiero 5 manzanas
# de: ich haette gern 300 gramm
# nl: ik wil 21 appels
