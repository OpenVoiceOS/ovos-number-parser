# OVOS Number Parser

Convert numbers between digits and spoken words, in **40 languages**, with one
small dependency-light library.

```text
   "twenty twenty three"  ⇄  2023  ⇄  "two thousand, twenty three"
```

`ovos-number-parser` goes both ways:

- **words to digits**: turn spoken-form text into numbers
  (`extract_number`, `numbers_to_digits`). Use it for **ASR post-processing /
  inverse text normalization** and **numeric entity extraction**.
- **digits to words**: turn numbers into natural spoken text
  (`pronounce_number`, `pronounce_ordinal`, `pronounce_fraction`). Use it for
  **TTS normalization** before synthesis.

It ships as part of the [OpenVoiceOS](https://openvoiceos.org) voice stack. It
is **plain Python with no assistant dependencies**. Every example below runs
after a single `pip install`, with no voice assistant involved.

## Install

```bash
pip install ovos-number-parser
# or, with uv:
uv pip install ovos-number-parser
```

## 30-second quickstart

```python
from ovos_number_parser import (pronounce_number, pronounce_ordinal,
                                 extract_number, numbers_to_digits,
                                 is_fractional, is_ordinal)

# digits -> words
pronounce_number(3.5, "en")               # 'three point five'
pronounce_number(2023, "en")              # 'two thousand, twenty three'
pronounce_ordinal(21, "en")               # 'twenty-first'

# words -> digits
extract_number("three point five liters", "en")          # 3.5
extract_number("dos mil veintitrés", "es")               # 2023
numbers_to_digits("set a timer for five minutes", "en")  # 'set a timer for 5 minutes'

# classification helpers
is_fractional("half", "en")               # 0.5
is_ordinal("third", "en")                 # 3

# no number in the text -> False
extract_number("hello world", "en")       # False
```

Pass a different language code and the same calls work. See the
[matrix](#supported-languages) for the 40 supported languages.

## What it's good for (beyond voice assistants)

The library is a standalone text/number utility. Four common uses, each with a
runnable script in [`examples/`](examples/):

### 1. ASR post-processing / inverse text normalization

Speech-to-text emits numbers as words. Most downstream systems want digits.

```python
from ovos_number_parser import numbers_to_digits, extract_number

numbers_to_digits("i need twenty three of them", "en")   # 'i need 23 of them'
extract_number("three point five liters", "en")          # 3.5
```

→ [`examples/asr_itn.py`](examples/asr_itn.py)

### 2. TTS normalization

Expand numbers into words *before* synthesis so the voice reads them naturally
("one thousand..." instead of "one-two-three-four dot five six").

```python
from ovos_number_parser import pronounce_number

pronounce_number(1234.56, "en", places=2)
# 'one thousand, two hundred and thirty four point five six'
pronounce_number(-3.5, "en")               # 'minus three point five'
```

→ [`examples/tts_normalization.py`](examples/tts_normalization.py)

### 3. Numeric entity extraction (NER)

Pull cardinal, ordinal and fractional mentions out of free text without an ML
model.

```python
from ovos_number_parser import extract_number, is_fractional, is_ordinal

extract_number("shipped in three boxes", "en")   # 3
is_ordinal("second", "en")                        # 2
is_fractional("quarter", "en")                    # 0.25
```

→ [`examples/ner.py`](examples/ner.py)

### 4. Multilingual round-trips

The same two functions cover 40 languages, with dialect prefixes
(`pt-BR`, `pt-PT` → `pt`).

→ [`examples/multilingual.py`](examples/multilingual.py)

### In an OVOS skill vs. standalone

The API is the same in both cases. Only where you get the language code differs.

```python
# Standalone Python: you pass the language yourself
from ovos_number_parser import extract_number
n = extract_number(text, "en")

# Inside an OVOS skill: the framework already knows the session language
class MySkill(OVOSSkill):
    def handle_intent(self, message):
        n = extract_number(message.data["utterance"], self.lang)
```

## Supported languages

40 languages. Every language supports **every** public function: where a
language has no hand-written implementation for a given function, a documented
generic fallback fills in (`unicode-rbnf` for pronunciation, reverse-lookup for
the rest: see [Full function parity](docs/languages.md#full-function-parity)),
so the call always returns a sensible result rather than raising.

- **Y**: dedicated hand-written implementation
- **·**: supported via the documented generic fallback

| Code | Language | pronounce_number | pronounce_ordinal | extract_number | numbers_to_digits | is_fractional | is_ordinal |
|------|----------|:--:|:--:|:--:|:--:|:--:|:--:|
| `ar` | Arabic | Y | Y | Y | · | Y | Y |
| `an` | Aragonese | Y | Y | Y | Y | Y | Y |
| `ast` | Asturian | Y | Y | Y | Y | Y | Y |
| `az` | Azerbaijani | Y | · | Y | Y | Y | · |
| `eu` | Basque | Y | Y | Y | · | Y | Y |
| `bg` | Bulgarian | Y | · | Y | Y | Y | · |
| `ca` | Catalan | Y | · | Y | Y | Y | · |
| `hr` | Croatian | Y | Y | Y | Y | Y | · |
| `cs` | Czech | Y | Y | Y | Y | Y | · |
| `da` | Danish | Y | Y | Y | Y | Y | Y |
| `nl` | Dutch | Y | Y | Y | Y | Y | · |
| `en` | English | Y | · | Y | Y | Y | Y |
| `et` | Estonian | Y | Y | Y | · | Y | Y |
| `fi` | Finnish | Y | Y | Y | · | Y | Y |
| `fr` | French | Y | · | Y | · | Y | · |
| `gl` | Galician | Y | Y | Y | Y | Y | Y |
| `de` | German | Y | Y | Y | Y | Y | Y |
| `el` | Greek | Y | Y | Y | · | Y | Y |
| `he` | Hebrew | Y | Y | Y | · | Y | Y |
| `hu` | Hungarian | Y | Y | Y | · | Y | Y |
| `id` | Indonesian | Y | Y | Y | Y | Y | · |
| `it` | Italian | Y | · | Y | · | Y | · |
| `kab` | Kabyle | Y | Y | Y | · | Y | Y |
| `ms` | Malay | Y | Y | Y | Y | Y | · |
| `mwl` | Mirandese | Y | Y | Y | Y | Y | Y |
| `nb` | Norwegian Bokmål | Y | Y | Y | Y | Y | Y |
| `nn` | Norwegian Nynorsk | Y | Y | Y | Y | Y | Y |
| `oc` | Occitan | Y | Y | Y | Y | Y | Y |
| `fa` | Persian | Y | Y | Y | · | Y | · |
| `pl` | Polish | Y | Y | Y | Y | Y | · |
| `pt` | Portuguese | Y | Y | Y | Y | Y | Y |
| `ro` | Romanian | Y | Y | Y | Y | Y | Y |
| `ru` | Russian | Y | · | Y | Y | Y | · |
| `sk` | Slovak | Y | Y | Y | Y | Y | · |
| `sl` | Slovenian | Y | · | Y | · | Y | Y |
| `es` | Spanish | Y | · | Y | Y | Y | · |
| `sv` | Swedish | Y | Y | Y | · | Y | · |
| `tr` | Turkish | Y | Y | Y | Y | Y | · |
| `uk` | Ukrainian | Y | Y | Y | Y | Y | · |
| `fy` | West Frisian | Y | Y | Y | Y | Y | · |

Language-specific behaviour (compound-word splitting, vigesimal counting,
grammatical gender, declensions, script handling) is documented in
[docs/languages.md](docs/languages.md).

## Grammatical gender

Languages whose numerals inflect accept a `gender` argument:

```python
from ovos_number_parser import pronounce_number
from ovos_number_parser.util import GrammaticalGender

pronounce_number(2, "pt", gender=GrammaticalGender.FEMININE)  # 'duas'
```

## Documentation

- [API reference](docs/api.md): every public function and its parameters
- [Language notes](docs/languages.md): per-language behaviour and known gaps
- [Adding a language](docs/adding-a-language.md): implementation guide
- [examples/](examples/): runnable scripts (each ends with its verified output)

## Related projects

- [ovos-date-parser](https://github.com/OpenVoiceOS/ovos-date-parser): dates and times
- [ovos-lang-parser](https://github.com/OVOSHatchery/ovos-lang-parser): languages
- [ovos-color-parser](https://github.com/OVOSHatchery/ovos-color-parser): colors

## License

Apache License 2.0.
