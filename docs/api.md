# API reference

<!-- agent-hint
covers: every public function of ovos_number_parser with its parameters, defaults and examples
source: ovos_number_parser/__init__.py (dispatchers), ovos_number_parser/numtag_readers.py (NUMTAG_LANGS), ovos_number_parser/util.py (enums)
generated: no
verify: sed '/^\x60\x60\x60/d' docs/api.md | .venv/bin/python -I -m doctest -o ELLIPSIS -o NORMALIZE_WHITESPACE /dev/stdin
see: languages.md, adding-a-language.md, ../README.md
-->

This page lists each public function, its parameters and an example. Read it
when you need the exact call for reading a number or for speaking one.

All public functions live in the top-level `ovos_number_parser` package and take a BCP-47 language code (`lang`). The primary language subtag selects the language. It must match exactly, in any letter case and with `-` or `_` between subtags. So `"pt-BR"`, `"pt_PT"` and `"pt"` all reach Portuguese, with variant handling where it matters (Brazilian and European Portuguese), while `"fil"` (Filipino) does not reach Finnish.

Two engines answer the functions.

| Functions | Answered by |
|---|---|
| `extract_number`, `extract_number_spans`, `numbers_to_digits`, `is_fractional`, `is_ordinal` | [numtag](https://github.com/TigreGotico/numtag), for the 40 supported languages |
| `pronounce_number`, `pronounce_ordinal`, `pronounce_fraction`, `nice_number_<code>` | The writers in this package. [unicode-rbnf](https://github.com/rhasspy/unicode-rbnf) writes a value or a language that no writer covers |

All 40 supported languages provide every public function. Where a language has
no hand-written writer, a generic fallback fills in, as
[Full function parity](languages.md#full-function-parity) describes.

A `lang` outside the supported set raises `NotImplementedError` in
`extract_number`, `extract_number_spans` and `is_fractional`. The other
functions answer through unicode-rbnf or return the text unchanged.

```python
>>> from ovos_number_parser import pronounce_number, pronounce_ordinal, is_fractional
>>> pronounce_number(5, "ja")
'五'

>>> pronounce_ordinal(5, "ja")
'第五'

>>> is_fractional("half", "ja")
Traceback (most recent call last):
    ...
NotImplementedError: Unsupported language: 'ja'

```

Every function returns `int`, `float`, `str` or `bool` as documented below. The
extraction and classification helpers return `False`, not `None`, when no
number is present. Test with `is not False` and not with truthiness, because a
valid `0` or `0.0` is falsy.

You can import the language-specific `*_<code>` writers, such as
`pronounce_number_de` and `nice_number_de`, from the top-level package to skip
the dispatcher. `nice_number_<code>` formats a `float` as a mixed fraction with
a spoken denominator. `nice_number_de(5.5)` is `"5 und ein halb"`. It has no
top-level dispatcher, so you reach it per language.

## `pronounce_number(number, lang, places=3, short_scale=None, scientific=False, ordinals=False, digits=None, gender=GrammaticalGender.MASCULINE, scale=None, case=None)`

Convert a numeric value to its spoken form.

```python
>>> from ovos_number_parser import pronounce_number
>>> pronounce_number(4.5, "en")
'four point five'

>>> pronounce_number(21, "cs")
'dvacet jedna'
>>> pronounce_number(2023, "gl")
'dous mil e vinte e tres'

```

- `places`: decimal places to speak.

- `short_scale`: short vs long scale for large numbers
  (https://en.wikipedia.org/wiki/Names_of_large_numbers). `None` keeps the
  scale of the language.

- `scale`: a `Scale` value that takes the place of `short_scale`.
  `pronounce_number(10**9, "en", scale=Scale.LONG)` is
  `'one thousand million'`.

- `case`: `"nominative"` or `"oblique"` (also `"genitive"`, `"accusative"`) for
  Arabic. Other languages ignore it. Arabic raises `ValueError` for any other
  value. `pronounce_number(2, "ar", case="genitive")` is `'اثنين'`, and the
  default is `'اثنان'`.

- `scientific`: read `5e-6` style notation aloud.

- `ordinals`: speak `"first"` instead of `"one"`.

- `digits`: `DigitPronunciation` enum for digit-by-digit reading styles.

- `gender`: `GrammaticalGender` enum for languages whose numerals inflect
  (e.g. Portuguese `"uma hora"` vs `"um minuto"`).

Some values reach unicode-rbnf and come back as digits, such as
`pronounce_number(10**24, "am")`
([ovos-number-parser#544](https://github.com/OpenVoiceOS/ovos-number-parser/issues/544)).
A `Decimal` with more digits than a `float` holds speaks wrong last digits ([ovos-number-parser#409](https://github.com/OpenVoiceOS/ovos-number-parser/issues/409)).

A whole number past the largest scale compound a language uses is read in scientific form. Romanian reads `10 ** 24` as `"un milion de trilioane"` and `10 ** 27` as `"unu ori zece la puterea douăzeci și șapte"`. Belgian and Swiss French (`fr-BE`, `fr-CH`) read 70 and 90 as `septante` and `nonante`, and Swiss French reads 80 as `huitante`. Their ordinals use the same words (`septantième`, `nonantième`, `huitantième`).

## `pronounce_ordinal(number, lang, short_scale=None, gender=GrammaticalGender.MASCULINE, scale=None, case=None)`

Spoken ordinal form (`1 -> "first"`). `short_scale`, `scale` and `case` work
as in `pronounce_number`.

English ordinals come from unicode-rbnf. So do French 0 and French values from 10**15. Unicode-rbnf has no ordinal for some large values, and the call raises `NotImplementedError` for them. These are Azerbaijani from 10**24 and Spanish from 10**24 (from 10**18 on the short scale). Russian has none from 10**96 on its default short scale.

```python
>>> pronounce_ordinal(21, "en"), pronounce_ordinal(70, "fr-BE")
('twenty-first', 'septantième')

>>> pronounce_ordinal(10**24, "es")
Traceback (most recent call last):
    ...
NotImplementedError: 'es' has no spoken ordinal for 1000000000000000000000000

```

For some values the writer gives the cardinal word and not the ordinal. These
are the Slovenian and Turkish hundreds 200 to 900 and the Croatian 1000 ([ovos-number-parser#559](https://github.com/OpenVoiceOS/ovos-number-parser/issues/559)).

## `pronounce_fraction(fraction_word, lang, scale=None)`

Speak a fraction string such as `"3/4"`. Portuguese, Asturian, Catalan,
Occitan, Aragonese, Mirandese, Galician and Romanian have their own writers.
Every other language uses the generic one.

```python
>>> from ovos_number_parser import pronounce_fraction
>>> pronounce_fraction("3/4", "pt")
'três quartos'
>>> pronounce_fraction("3/4", "en")
'three quarters'

```

## `extract_number(text, lang, short_scale=None, ordinals=False, scale=None)`

Extract the first number found in a phrase. Returns `int`, `float`, or
`False` when the text contains no number.

```python
>>> from ovos_number_parser import extract_number
>>> extract_number("set a timer for twenty one minutes", "en")
21

>>> extract_number("dos mil veintitrés", "es")
2023
>>> extract_number("einundzwanzig Katzen", "de")
21

```

Compound-written languages (German, Dutch, Danish, Swedish) split words such
as `einundzwanzig`, `eenentwintig`, `toogfyrre` or `tjugoen` automatically.

`short_scale=None` keeps the scale of the language. Spanish `billón` is
10**12 by default and 10**9 with `short_scale=True`. A `scale` value takes the
place of `short_scale`.

```python
>>> from ovos_number_parser import extract_number
>>> extract_number("un billón", "es")
1000000000000
>>> extract_number("un billón", "es", short_scale=True)
1000000000

```

## `extract_number_spans(text, lang, short_scale=None, ordinals=False, scale=None)`

Find every number in a text together with the characters it occupies. It
returns a list of `NumberSpan(start, end, surface, value)`, sorted by `start`,
and an empty list when the text holds no number.

```python
>>> from ovos_number_parser import extract_number_spans
>>> extract_number_spans("I have two cats and 3 dogs", "en")
[NumberSpan(start=7, end=10, surface='two', value=2), NumberSpan(start=20, end=21, surface='3', value=3)]
>>> extract_number_spans("nothing", "en")
[]

```

## `is_fractional(input_str, lang, short_scale=None, scale=None)`

Exact-match test for a fraction (`"half"` → `0.5`, `"two thirds"` → `0.666...`, otherwise `False`). A fraction is a count with its denominator, a half word or a fraction written in digits (`"1/2"`). A denominator word without a count (`"quarter"`) is not a fraction. Use `extract_number` to pull fractions out of longer phrases.

```python
>>> from ovos_number_parser import is_fractional
>>> is_fractional("half", "en"), is_fractional("two thirds", "en")
(0.5, 0.6666666666666666)
>>> is_fractional("the half", "en"), is_fractional("hello", "en")
(False, False)

```

## `is_ordinal(input_str, lang)`

Exact-match test for an ordinal (`"third"` → `3`, otherwise `False`). The
whole text must be one ordinal, so `"the third"` is `False`.

```python
>>> from ovos_number_parser import is_ordinal
>>> is_ordinal("third", "en"), is_ordinal("twenty-first", "en"), is_ordinal("three", "en")
(3, 21, False)

```

## `numbers_to_digits(utterance, lang, scale=None)`

Rewrite the written numbers inside a phrase as digits, keeping the rest of
the text intact.

```python
>>> from ovos_number_parser import numbers_to_digits
>>> numbers_to_digits("set a timer for five minutes", "en")
'set a timer for 5 minutes'

```

## Readers backed by numtag

`extract_number`, `extract_number_spans`, `numbers_to_digits`, `is_fractional` and `is_ordinal` read a language through [numtag](https://github.com/TigreGotico/numtag) when its language code is in `ovos_number_parser.numtag_readers.NUMTAG_LANGS`. The set holds every language numtag reads:

```text
an ar ast az bg ca cs da de el en es et eu fa fi fr fy gl he hr hu id it kab ms mwl nb nl nn oc pl pt ro ru sk sl sv tr uk
```

The ISO 639-3 codes of the Arabic varieties (`arb`, `arz`, `apc`, `ary` and the
others in `AR_DIALECT_DEFAULT_CASE`) read as `ar`, and `zsm` reads as `ms`.
numtag has no lexicon per Arabic variety, so the colloquial words of a variety
read only when `ar` has them
([numtag#266](https://github.com/TigreGotico/numtag/issues/266)).

A test row that numtag reads wrongly is a strict xfail in
`tests/numtag_xfail.json`. Its reason is the URL of the issue that tracks the
row. [Known gaps](languages.md#known-gaps) lists the limits with their issues.

### Values

numtag gives each value as an exact digit string. The readers convert it to
the `int` or `float` that the API returns.

- A value with a fraction is a `float`.

- When the `float` has no room for the digits after the point, or for the
  value at all, a decimal rounds half up to an `int`.

- A mixed number is a `float`: `5 1/2` is 5.5.

- Only when the `float` has no room for the fraction, and the whole part is
  within the range of a `float`, is the value the whole part:
  `"9007199254740993 1/2"` is 9007199254740993.

- An integer with more digits than `str` can write is no number.

Under `ordinals=True`, `extract_number` answers with the first number of the
line, ordinal or cardinal. In Danish, `"tre femte"` is 3 and `"femte tre"` is
5.

### `numbers_to_digits`

`numbers_to_digits` keeps a number written in digits as written (`"5 1/2"`,
`"007"`) and writes digits of other scripts as Western digits (`"٠٠٧"` is
`"007"`). A sign word before digits becomes the sign: `"minus 5"` is `"-5"`.
An ordinal stays as written.

`numtag_readers.numbers_to_digits` writes an ordinal as the digits of its value
when it gets `ordinals=True`. In German, a clock time written with a point
becomes a time with a colon, because speech to text writes it with a point:
`"um 13.30 Uhr"` is `"um 13:30 Uhr"`.

### `is_fractional` and `is_ordinal`

Both functions answer for a text that is exactly one fraction or one ordinal
mention of numtag. `is_ordinal("three", "en")` is `False`, because numtag
reads "three" as a cardinal. For a language outside the set, `is_ordinal`
looks the text up among the `pronounce_ordinal` forms of the language.
For a language outside the set, `numbers_to_digits` returns the text unchanged.

## Deprecated reader names

A `numbers_<code>` module exports each reader name listed below. The function calls the numtag reader and gives a `DeprecationWarning` that names the removal version. The warning fires when you call the function.

```python
>>> import warnings
>>> from ovos_number_parser.numbers_en import extract_number_en

>>> with warnings.catch_warnings(record=True) as caught:
...     warnings.simplefilter("always")
...     extract_number_en("twenty one")
21

>>> str(caught[0].message)
'extract_number_en is deprecated and is removed in 1.0.0; use ovos_number_parser.extract_number(text, "en")'

```

The deprecated names are:

- `extract_number_<code>` for az, bg, cs, en, et, fi, fy, hr, hu, it, kab, nl, pl, ru, sk and uk
- `numbers_to_digits_<code>` for az, ca, cs, da, de, en, es, nb, nl, nn, pl, pt, ru and uk
- `is_ordinal_<code>` for da, et, fi, nb and nn

Each deprecated name keeps the parameters of the reader it replaces, and it answers what
the public function answers.

The `numbers_to_digits` method of a `RomanceNumberExtractor` engine, such as
`CA` or `PT_PT`, gives the same warning with the removal version.

`pronounce_number_ca`, and `pronounce_number`, `pronounce_ordinal` and
`pronounce_fraction` with the suffix `_gl`, `_mwl` or `_pt`, also give a
`DeprecationWarning`. Its text is `migrate to use RomanceNumberExtractor and
NumberVocabulary directly instead`. That warning names no removal version.

## Enums

- `Scale`: `Scale.SHORT` / `Scale.LONG` large-number scales.
- `GrammaticalGender`: `MASCULINE` / `FEMININE` / `NEUTRAL`.
- `DigitPronunciation`: full-number vs digit-by-digit reading styles.

---
[Index](index.md) · [← Home](../README.md) · [Language notes →](languages.md)
