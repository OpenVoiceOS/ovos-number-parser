# API reference

<!-- agent-hint
covers: every public function of ovos_number_parser with its parameters, defaults and examples
source: ovos_number_parser/__init__.py (dispatchers), ovos_number_parser/numtag_readers.py (NUMTAG_LANGS), ovos_number_parser/util.py (enums)
generated: no
verify: python -m doctest docs/api.md
see: languages.md, adding-a-language.md, ../README.md
-->

This page lists each public function, its parameters and an example. Read it
when you need the exact call for reading a number or for speaking one.

All public functions live in the top-level `ovos_number_parser` package and
take a BCP-47 language code (`lang`). The primary language subtag selects the
parser and must match exactly, in any letter case and with `-` or `_` between
subtags, so `"pt-BR"`, `"pt_PT"` and `"pt"` all reach the Portuguese parser
(with variant handling where it matters, e.g. Brazilian vs European
Portuguese), while `"fil"` (Filipino) does not reach the Finnish parser.

All 40 supported languages provide every public function. Where a language has
no hand-written implementation, a generic fallback fills in, as
[Full function parity](languages.md#full-function-parity) describes.

A `lang` outside the supported set raises `NotImplementedError` in
`extract_number`, `extract_number_spans` and `is_fractional`. The other
functions answer through unicode-rbnf or return the text unchanged:

```python
>>> from ovos_number_parser import *
>>> from ovos_number_parser.util import Scale
>>> pronounce_number(5, "ja")
'五'
>>> pronounce_ordinal(5, "ja")
'第五'
>>> is_fractional("half", "ja")
Traceback (most recent call last):
    ...
NotImplementedError: Unsupported language: 'ja'

```

Every function returns `int`/`float`/`str`/`bool` as documented below. The
extraction and classification helpers return `False` (not `None`) when no
number is present. Test with `is not False` rather than truthiness, since a
valid `0` or `0.0` is falsy.

Language-specific `*_<code>` variants (e.g. `pronounce_number_de`,
`nice_number_de`) are also importable from the top-level package if you want to
skip the dispatcher. `nice_number_<code>` (formats a `float` as a mixed
fraction with a spoken denominator, e.g. `nice_number_de(5.5)` →
`"5 und ein halb"`) has no top-level dispatcher and is only exposed
per-language.

## `pronounce_number(number, lang, places=3, short_scale=None, scientific=False, ordinals=False, digits=None, gender=GrammaticalGender.MASCULINE, scale=None, case=None)`

Convert a numeric value to its spoken form.

```python
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

A whole number past the largest scale compound a language uses is read in
scientific form. Romanian reads `10 ** 24` as `"un milion de trilioane"` and
`10 ** 27` as `"unu ori zece la puterea douăzeci și șapte"`.
Belgian and Swiss French (`fr-BE`, `fr-CH`) read 70 and 90 as `septante` and
`nonante`, and Swiss French reads 80 as `huitante`. Their ordinals use the same
words (`septantième`, `nonantième`, `huitantième`).

## `pronounce_ordinal(number, lang, short_scale=None, gender=GrammaticalGender.MASCULINE, scale=None, case=None)`

Spoken ordinal form (`1 -> "first"`). `short_scale`, `scale` and `case` work
as in `pronounce_number`.

English ordinals come from unicode-rbnf. French 0 and French values from
10**15 also come from it. Azerbaijani from 10**24, Spanish from 10**24 (from
10**18 on the short scale) and Russian from 10**96 reach unicode-rbnf too. It
has no ordinal for them, and the call raises `NotImplementedError`.

## `pronounce_fraction(fraction_word, lang, scale=None)`

Speak a fraction string such as `"3/4"`. Portuguese, Asturian, Catalan,
Occitan, Aragonese, Mirandese, Galician and Romanian have their own writers.
Every other language uses the generic one.

```python
>>> pronounce_fraction("3/4", "pt")
'três quartos'
>>> pronounce_fraction("3/4", "en")
'three quarters'

```

## `extract_number(text, lang, short_scale=None, ordinals=False, scale=None)`

Extract the first number found in a phrase. Returns `int`, `float`, or
`False` when the text contains no number.

```python
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
>>> extract_number_spans("I have two cats and 3 dogs", "en")
[NumberSpan(start=7, end=10, surface='two', value=2), NumberSpan(start=20, end=21, surface='3', value=3)]
>>> extract_number_spans("nothing", "en")
[]

```

## `is_fractional(input_str, lang, short_scale=None, scale=None)`

Exact-match test for a fraction word (`"half"` → `0.5`, otherwise `False`).
Use `extract_number` to pull fractions out of longer phrases.

## `is_ordinal(input_str, lang)`

Exact-match test for an ordinal word (`"third"` → `3`, otherwise `False`).
The [language table](languages.md#language-table) shows which languages have a
dedicated reader. The others look the word up among their `pronounce_ordinal`
forms.

## `numbers_to_digits(utterance, lang, scale=None)`

Rewrite the written numbers inside a phrase as digits, keeping the rest of
the text intact.

```python
>>> numbers_to_digits("set a timer for five minutes", "en")
'set a timer for 5 minutes'

```

## Readers backed by numtag

`extract_number`, `extract_number_spans` and `numbers_to_digits` read a
language through [numtag](https://github.com/TigreGotico/numtag) when its
language code is in `ovos_number_parser.numtag_readers.NUMTAG_LANGS`. Every
other language keeps its `numbers_<code>.py` reader. A test that numtag reads
differently from the old reader is a strict xfail, and its reason is the URL of
the issue that tracks the difference.

numtag gives each value as an exact digit string. The readers convert it to
the `int` or `float` the API returns. A value that is no whole number is a
`float`. When the `float` drops the part after the point, the value rounds
half up to an `int`. An integer with more digits than `str` can write is no
number. `numbers_to_digits` keeps a number written in digits and an ordinal
as written. `numtag_readers.numbers_to_digits` writes an ordinal as the
digits of its value when it gets `ordinals=True`.
`is_fractional` and `is_ordinal` answer a question about one
word, which numtag does not read, so they keep the parser for every language.

The set holds every language numtag reads: an, ar, ast, az, bg, ca, cs, da,
de, el, en, es, et, eu, fa, fi, fr, fy, gl, he, hr, hu, id, it, kab, mwl, nb,
nl, nn, oc, pl, pt, ro, ru, sk, sl, sv, tr and uk.

## Enums

- `Scale`: `Scale.SHORT` / `Scale.LONG` large-number scales.
- `GrammaticalGender`: `MASCULINE` / `FEMININE` / `NEUTRAL`.
- `DigitPronunciation`: full-number vs digit-by-digit reading styles.

---
[Index](index.md) · [← Home](../README.md) · [Language notes →](languages.md)
