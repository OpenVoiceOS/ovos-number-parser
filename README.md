# OVOS Number Parser

OVOS Number Parser is a tool for extracting, pronouncing, and detecting numbers from text across multiple languages. It
supports functionalities like converting numbers to their spoken forms, extracting numbers from text, identifying
fractional and ordinal numbers, and more.

## Features

- **Pronounce Numbers:** Converts numerical values to their spoken forms.
- **Pronounce Ordinals:** Converts numbers to their ordinal forms.
- **Extract Numbers:** Extracts numbers from textual inputs.
- **Detect Fractions:** Identifies fractional expressions.
- **Detect Ordinals:** Checks if a text input contains an ordinal number.

## Supported Languages

- ✅ - supported
- ❌ - not supported
- 🚧 - imperfect placeholder, usually a language agnostic implementation or external library


| Language Code           | Pronounce Number | Pronounce Ordinal | Extract Number | numbers_to_digits |
|-------------------------|------------------|-------------------|----------------|-------------------|
| `en` (English)          | ✅               | 🚧                | ✅             | ✅                |
| `az` (Azerbaijani)      | ✅               | 🚧                | ✅             | ✅                |
| `ca` (Catalan)          | ✅                | 🚧                 | ✅              | 🚧                 |
| `gl` (Galician)         | ✅                | ❌                | ✅              |  🚧                  |
| `cs` (Czech)            | ✅                | 🚧                 | ✅              | ✅                 |
| `da` (Danish)           | ✅                | ✅                 | ✅              | 🚧                 |
| `de` (German)           | ✅                | ✅                 | ✅              | ✅                 |
| `es` (Spanish)          | ✅                | 🚧                 | ✅              | 🚧                 |
| `eu` (Euskara / Basque) | ✅                | ❌                 | ✅              | ❌                 |
| `fa` (Farsi / Persian)  | ✅                | 🚧                 | ✅              | ❌                 |
| `fr` (French)           | ✅                | 🚧                 | ✅              | ❌                 |
| `hu` (Hungarian)        | ✅                | ✅                 | ❌              | ❌                 |
| `it` (Italian)          | ✅                | 🚧                | ✅              | ❌                 |
| `kab` (Kabyle)          | ✅                | ✅                 | ✅              | 🚧                 |
| `nl` (Dutch)            | ✅                | ✅                 | ✅              | ✅                 |
| `pl` (Polish)           | ✅                | 🚧                 | ✅              | ✅                 |
| `pt` (Portuguese)       | ✅                | ✅                  | ✅              | ✅                |
| `mwl` (Mirandese)       | ✅                | ✅                  | ✅              | ✅                |
| `ast` (Asturian)        | ✅                | ✅                  | ✅              | ✅                |
| `oc` (Occitan)          | ✅                | ✅                  | ✅              | ✅                |
| `ro` (Romanian)         | ✅                | ✅                  | ✅              | ✅                |
| `an` (Aragonese)        | ✅                | ✅                  | ✅              | ✅                |
| `fy` (West Frisian)     | ✅                | ✅                  | ✅              | ✅                |
| `ru` (Russian)          | ✅                | 🚧                 | ✅              | ✅                 |
| `sv` (Swedish)          | ✅                | ✅                 | ✅              | ❌                 |
| `sl` (Slovenian)        | ✅                | 🚧                 | ❌              | ❌                 |
| `uk` (Ukrainian)        | ✅                | 🚧                 | ✅              | ✅                 |


> 💡 If a language is not implemented for `pronounce_number` or `pronounce_ordinal` then [unicode-rbnf](https://github.com/rhasspy/unicode-rbnf) will be used as a fallback

## Installation

To install OVOS Number Parser, use:

```bash
pip install ovos-number-parser
```

## Usage

```python
from ovos_number_parser import (pronounce_number, pronounce_ordinal,
                                extract_number, is_fractional, is_ordinal,
                                numbers_to_digits)

pronounce_number(123, "en")            # 'one hundred and twenty three'
pronounce_number(4.5, "pt")            # 'quatro vírgula cinco'
pronounce_number(21, "de")             # 'einundzwanzig'
pronounce_number(3, "en", ordinals=True)  # 'third'
pronounce_ordinal(5, "de")             # 'fünfte'

extract_number("set a timer for twenty one minutes", "en")   # 21
extract_number("one hundred and one dalmatians", "en")       # 101
extract_number("dos mil veintitrés", "es")                   # 2023
extract_number("einundzwanzig Katzen", "de")                 # 21
extract_number("hello world", "en")                          # False

is_fractional("half", "en")            # 0.5
is_ordinal("third", "en")              # 3

numbers_to_digits("set a timer for five minutes", "en")
# 'set a timer for 5 minutes'
```

Grammatical gender is supported for languages that inflect numerals:

```python
from ovos_number_parser.util import GrammaticalGender

pronounce_number(2, "pt", gender=GrammaticalGender.FEMININE)  # 'duas'
```

## Documentation

- [API reference](docs/api.md) — every public function and its parameters
- [Language notes](docs/languages.md) — per-language behaviour and known gaps
- [Adding a language](docs/adding-a-language.md) — implementation guide
- [examples/](examples/) — runnable example scripts

## Related Projects

- [ovos-date-parser](https://github.com/OpenVoiceOS/ovos-date-parser) - for handling dates and times
- [ovos-lang-parser](https://github.com/OVOSHatchery/ovos-lang-parser) - for handling languages
- [ovos-color-parser](https://github.com/OVOSHatchery/ovos-color-parser) - for handling colors

## License

This project is licensed under the Apache License 2.0.
