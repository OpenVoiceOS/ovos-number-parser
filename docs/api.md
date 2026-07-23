# API reference

All public functions live in the top-level `ovos_number_parser` package and
take a BCP-47 language code (`lang`). Language dialects resolve by prefix, so
`"pt-BR"`, `"pt-PT"` and `"pt"` all reach the Portuguese parser (with variant
handling where it matters, e.g. Brazilian vs European Portuguese).

All 40 supported languages provide every public function. Where a language has
no hand-written implementation, a documented generic fallback fills in:
`pronounce_number` / `pronounce_ordinal` use
[unicode-rbnf](https://github.com/rhasspy/unicode-rbnf); the rest use the
parity fallbacks described in
[Full function parity](languages.md#full-function-parity). A `lang` outside the
supported set (or a value the fallback genuinely cannot handle) raises
`NotImplementedError`.

Every function returns `int`/`float`/`str`/`bool` as documented below; the
extraction and classification helpers return `False` (not `None`) when no
number is present, so test with `is not False` rather than truthiness (a valid
`0` or `0.0` is falsy).

Language-specific `*_<code>` variants (e.g. `pronounce_number_de`,
`nice_number_de`) are also importable from the top-level package if you want to
skip the dispatcher; `nice_number_<code>` (formats a `float` as a mixed
fraction with a spoken denominator, e.g. `nice_number_de(5.5)` →
`"5 und ein halb"`) has no top-level dispatcher and is only exposed
per-language.

## `pronounce_number(number, lang, places=3, short_scale=True, scientific=False, ordinals=False, digits=..., gender=...)`

Convert a numeric value to its spoken form.

```python
>>> pronounce_number(4.5, "en")
'four point five'
>>> pronounce_number(21, "cs")
'dvacet jedna'
>>> pronounce_number(2023, "gl")
'dous mil e vinte e tres'
```

- `places` — decimal places to speak.
- `short_scale` — short vs long scale for large numbers
  (https://en.wikipedia.org/wiki/Names_of_large_numbers).
- `scientific` — read `5e-6` style notation aloud.
- `ordinals` — speak `"first"` instead of `"one"`.
- `digits` — `DigitPronunciation` enum; digit-by-digit reading styles.
- `gender` — `GrammaticalGender` enum for languages whose numerals inflect
  (e.g. Portuguese `"uma hora"` vs `"um minuto"`).

## `pronounce_ordinal(number, lang, short_scale=True, gender=...)`

Spoken ordinal form (`1 -> "first"`). Languages without a handwritten
implementation use the unicode-rbnf fallback.

## `pronounce_fraction(fraction_word, lang, scale=Scale.LONG)`

Speak a fraction string such as `"3/4"`. Currently implemented for Portuguese
and Mirandese.

## `extract_number(text, lang, short_scale=True, ordinals=False)`

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

## `is_fractional(input_str, lang, short_scale=True)`

Exact-match test for a fraction word (`"half"` → `0.5`, otherwise `False`).
Use `extract_number` to pull fractions out of longer phrases.

## `is_ordinal(input_str, lang)`

Exact-match test for an ordinal word (`"third"` → `3`, otherwise `False`).
Implemented for `en`, `pt`, `mwl`, `de` and `da`.

## `numbers_to_digits(utterance, lang, scale=Scale.LONG, *, ordinals=False, fractions=True, scale_words=True)`

Rewrite the written numbers inside a phrase as digits, keeping the rest of
the text intact.

```python
>>> numbers_to_digits("set a timer for five minutes", "en")
'set a timer for 5 minutes'
```

Three keyword flags tune what counts as a number. Each defaults to the
conversion this function has always done, so existing callers see no change.

| Flag | Default | Off/on effect |
| --- | --- | --- |
| `ordinals` | `False` | `True` reads ordinal words as values: `"the twenty fifth"` → `"the 25"`. Left off, an ordinal word is kept as a word. |
| `fractions` | `True` | `False` keeps a *bare* fraction word: `"half past nine"` → `"half past 9"`. A fraction inside a quantity always converts: `"two and a half hours"` → `"2.5 hours"`. |
| `scale_words` | `True` | `False` converts only the count and keeps the scale word: `"sixty six million years ago"` → `"66 million years ago"`. |

```python
>>> numbers_to_digits("a quarter to five", "en", fractions=False)
'a quarter to 5'
>>> numbers_to_digits("sixty six million years ago", "en", scale_words=False)
'66 million years ago'
```

### Language support

All three flags are honoured for **every supported language**, and `ordinals`
works everywhere without exception. For `fractions` and `scale_words` a handful
of languages have nothing to suppress: their parser never converted that kind of
word in the first place, so the word already survives and the flag has nothing
left to do.

| Flag | Fully applied | Nothing to suppress (word already survives) |
| --- | --- | --- |
| `ordinals` | all languages | — |
| `fractions` | ar, az, bg, ca, cs, da, de, el, en, es, et, eu, fi, fr, fy, he, hr, hu, it, nb, nl, nn, pl, ru, sk, sl, sv, tr, uk | an, ast, fa, gl, id, ms, mwl, oc, pt, ro |
| `scale_words` | an, ar, ast, az, bg, ca, cs, da, el, en, es, et, eu, fa, fi, fr, fy, gl, he, hr, hu, it, mwl, nb, nl, nn, oc, pl, pt, ro, ru, sk, sl, sv, tr, uk | de, id, ms |

`kab` counts only to 9999 and has neither scale nor fraction vocabulary, so
those two flags cannot apply to it; `ordinals` does.

No language ever returns something *other* than what a flag asks for. The table
lives in `tests/test_numbers_to_digits_flags_all_langs.py`, which iterates
`SUPPORTED_LANGUAGES` and fails if a newly added language is not declared.

## Enums

- `Scale` — `Scale.SHORT` / `Scale.LONG` large-number scales.
- `GrammaticalGender` — `MASCULINE` / `FEMININE` / `NEUTRAL`.
- `DigitPronunciation` — full-number vs digit-by-digit reading styles.
