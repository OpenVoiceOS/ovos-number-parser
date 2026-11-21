# Language notes

<!-- agent-hint
covers: which of the 40 languages read through numtag, which use the in-repo reader, and the rules of single languages
source: ovos_number_parser/numtag_readers.py:NUMTAG_LANGS, ovos_number_parser/__init__.py (dispatchers), ovos_number_parser/numbers_<code>.py
generated: no
verify: python -m pytest tests/test_numtag_routed_languages.py tests/test_lang_parity.py
see: api.md, adding-a-language.md, ../README.md
-->

This page shows how each of the 40 languages is read and spoken. It then
gives the rules of single languages and the known gaps.

## Language table

Words are read in one of two ways. Thirty-nine languages read through
[numtag](https://github.com/TigreGotico/numtag). Their codes are in
`NUMTAG_LANGS` in `ovos_number_parser/numtag_readers.py`. Malay (`ms`) reads
with the reader in `ovos_number_parser/numbers_id.py`. The functions
`extract_number`, `extract_number_spans` and `numbers_to_digits` follow this
route.

Every language speaks numbers with its own `pronounce_number_<code>` writer.
The `pronounce_*` writers are in this repository for all languages.
`is_fractional` and `is_ordinal` never use numtag. The last column shows
whether `is_ordinal` has a dedicated reader or looks the word up among the
`pronounce_ordinal` forms.

| Code | Language | Reads words with | `is_ordinal` |
|------|----------|------------------|--------------|
| `ar` | Arabic | numtag | dedicated |
| `an` | Aragonese | numtag | dedicated |
| `ast` | Asturian | numtag | dedicated |
| `az` | Azerbaijani | numtag | reverse lookup |
| `eu` | Basque | numtag | dedicated |
| `bg` | Bulgarian | numtag | reverse lookup |
| `ca` | Catalan | numtag | dedicated |
| `hr` | Croatian | numtag | reverse lookup |
| `cs` | Czech | numtag | reverse lookup |
| `da` | Danish | numtag | dedicated |
| `nl` | Dutch | numtag | reverse lookup |
| `en` | English | numtag | dedicated |
| `et` | Estonian | numtag | dedicated |
| `fi` | Finnish | numtag | dedicated |
| `fr` | French | numtag | reverse lookup |
| `gl` | Galician | numtag | dedicated |
| `de` | German | numtag | dedicated |
| `el` | Greek | numtag | dedicated |
| `he` | Hebrew | numtag | dedicated |
| `hu` | Hungarian | numtag | dedicated |
| `id` | Indonesian | numtag | reverse lookup |
| `it` | Italian | numtag | reverse lookup |
| `kab` | Kabyle | numtag | dedicated |
| `ms` | Malay | in-repo reader | reverse lookup |
| `mwl` | Mirandese | numtag | dedicated |
| `nb` | Norwegian Bokmål | numtag | dedicated |
| `nn` | Norwegian Nynorsk | numtag | dedicated |
| `oc` | Occitan | numtag | dedicated |
| `fa` | Persian | numtag | reverse lookup |
| `pl` | Polish | numtag | reverse lookup |
| `pt` | Portuguese | numtag | dedicated |
| `ro` | Romanian | numtag | dedicated |
| `ru` | Russian | numtag | reverse lookup |
| `sk` | Slovak | numtag | reverse lookup |
| `sl` | Slovenian | numtag | dedicated |
| `es` | Spanish | numtag | reverse lookup |
| `sv` | Swedish | numtag | reverse lookup |
| `tr` | Turkish | numtag | reverse lookup |
| `uk` | Ukrainian | numtag | reverse lookup |
| `fy` | West Frisian | numtag | reverse lookup |

A code with a region (`pt-BR`, `fr-BE`) uses the language of its first
subtag. `no` reads as `nb`, `azj` as `az`, `ekk` as `et` and `pes` as `fa`.

## Germanic compound numbers (de, nl, da, sv, fy)

These languages write numbers as single compound words. The extractors split
them into their component number words and evaluate the result, so both the
compound and the spaced form parse:

| Language | Example | Value |
|----------|---------|-------|
| German   | `einundzwanzig`, `zweihundertdreiundvierzig` | 21, 243 |
| Dutch    | `eenentwintig`, `tweehonderddrieëntwintig` | 21, 223 |
| Danish   | `toogfyrre`, `nihundredenioghalvfems` | 42, 999 |
| Swedish  | `tjugoen`, `etthundratjugotre`, `tvåtusen tjugotre` | 21, 123, 2023 |
| West Frisian | `ienentweintich`, `twahûnderttrijeentweintich` | 21, 223 |

Dutch diacritics (`één`, `drieëntwintig`) are normalized before parsing.
West Frisian diacritics (`sân`, `hûndert`, `tûzen`) are likewise normalized,
and the standard spellings `sechstjin` and `sechstich` read as 16 and 60.
Danish reads the standard spellings `elleve`, `halvtreds` and `halvfjerds`
as 11, 50 and 70.

## Czech declensions

Hundreds and thousands decline: `sto`, `dvě stě`, `tři sta`, `pět set`,
`dva tisíce`. Both pronouncing and extraction use the declined forms.

## Basque vigesimal counting

Basque counts in twenties. The `-ta` joiner forms are understood when
extracting: `hogeita bat` (20 + 1 = 21), `berrogeita hamar` (40 + 10 = 50),
`laurogeita hemeretzi` (80 + 19 = 99).

## Romance languages (pt, gl, mwl, ast, an)

Portuguese, Galician, Mirandese, Asturian and Aragonese share a declarative
`NumberVocabulary` + `RomanceNumberExtractor` implementation in
`ovos_number_parser.util`. Each language is described by its vocabulary
(units, tens, hundreds, scales, ordinals, fractions, gender rules and joiner
placement). The shared engine handles pronunciation and extraction for all
of them. This is the preferred path for adding new Romance languages.

Portuguese distinguishes European and Brazilian variants (`pt-PT` reads
16 as `dezasseis`, `pt-BR` as `dezesseis`) and inflects `um/uma`,
`dois/duas` and the hundreds (`duzentos/duzentas`) for grammatical gender.

Aragonese pronounces 4, 8, 16, 21, 35 and 100 as `cuatre`, `ueito`,
`deciséis`, `vintiún`, `trenta y cinco` and `cient`. It reads the variants
`quatre`, `vente` and `noranta` as 4, 20 and 90. Ordinals use the `-eno`
series (`cuatreno`, `cinqueno`).

## Spanish and Catalan

`es` and `ca` handle fused twenties (`veintiuno`, `vint-i-u`), the irregular
hundreds (`quinientos`, `setecientos`, `novecientos`), scale words including
`millón/millones` and `milió/milions`, and additive continuations such as
`dos mil veintitrés`.

## English

`extract_number` understands the `and` connector inside a number
(`one hundred and one` = 101) and digit grouping (`1,000,000`). A comma
between two number words ends the number: `two thousand, twenty three` reads
as 2000, and `two thousand twenty three` reads as 2023.

## Kabyle

Kabyle carries two numeral systems: the pan-Amazigh cardinals (`yiwen`,
`sin`, `kṛaḍ`, ... `mraw`) and the Algerian-Arabic borrowed numerals used
for everyday counting above ten (`ḥḍac` = 11, `ɛecrin` = 20, `mya` = 100,
`alef` = 1000). Pronunciation uses the Amazigh forms for 0-10 and the
Arabic-derived forms above ten, joining compounds with the conjunction `u`
with the unit before the ten (`waḥed u ɛecrin` = 21). Extraction accepts
both systems, feminine forms (`yiwet`, `snat`) and diacritic-stripped
spellings (`hdac` = 11).

Ordinals use `amezwaru` (f. `tamezwarut`) for "first" and `wis`/`tis` +
cardinal otherwise. The only attested fraction noun is `azgen` (half).

Coverage boundary: pronunciation spans 0–9999. The minus word, a
decimal-separator word, ordinal suffix forms, larger scale words and
further fraction nouns are not reliably attested and are deliberately
omitted.

## Persian

Numbers are written and parsed in Persian script (`بیست و یک` = 21). Both
extraction and pronunciation cover units through millions. Pronunciation reads
2.5 as `دو و نیم`.

## Known gaps

These are cases where the generic parity fallback (see below) is in use and
its result is rougher than a dedicated implementation would be: the call still
returns, it is just less polished:

- A comma between two number words ends the number in English:
  `extract_number("two thousand, twenty three", "en")` is 2000. The output of
  `pronounce_number(2023, "en")`, `two thousand, twenty three`, does not read
  back as 2023. Czech output such as `tisíc, dvě stě třicet čtyři` reads back
  as 1000.
- Kabyle `mraw d yiwen` and `mraw u yiwen` read as 10, not 11.
- Aragonese `güeito` and `setse` read as no number.

## Full function parity

Every supported language provides every public function. Where a language
has no hand-written implementation, a generic fallback fills in:

- `pronounce_fraction` reuses the language's `nice_number` fraction wording
  (which carries its plural/declension rules) and spells out any digits. The
  Slavic languages use feminine numerators (`dvě třetiny`, `две трети`) and
  Hungarian its `két` allomorph. Denominators outside the language's fraction
  vocabulary fall back to "cardinal numerator + ordinal denominator".
- `is_ordinal` falls back to a reverse lookup over `pronounce_ordinal`
  (1–100, round hundreds, 1000, 1000000), registering both `-o`/`-a`
  grammatical-gender variants.
- `pronounce_number` and `pronounce_ordinal` fall back to
  [unicode-rbnf](https://github.com/rhasspy/unicode-rbnf) for the values that
  a language writer does not cover.

The parity guarantee is enforced by `tests/test_lang_parity.py`, which runs
every public function against every supported language.

---
[Index](index.md) · [← API reference](api.md) · [Adding a language →](adding-a-language.md)
