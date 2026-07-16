"""Extract numbers from natural-language phrases."""
from ovos_number_parser import extract_number, is_fractional, is_ordinal, numbers_to_digits

print(extract_number("set a timer for twenty one minutes", "en"))   # 21
print(extract_number("one hundred and one dalmatians", "en"))       # 101
print(extract_number("two and a half cups", "en"))                  # 2.5

# compound-written languages split automatically
print(extract_number("einundzwanzig Katzen", "de"))                 # 21
print(extract_number("jag har tjugoen katter", "sv"))               # 21

# vigesimal Basque
print(extract_number("hogeita bat", "eu"))                          # 21

# no number -> False
print(extract_number("hello world", "en"))                          # False

# helpers
print(is_fractional("half", "en"))                                  # 0.5
print(is_ordinal("third", "en"))                                    # 3

# rewrite numbers as digits inside a phrase
print(numbers_to_digits("set a timer for five minutes", "en"))
# 'set a timer for 5 minutes'
