# Language notes

Per-language behaviour that goes beyond the support matrix in the README.

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
and the variant spellings without the etymological `-s-` (`sechtjin`,
`sechtich`) are accepted alongside the standard `sechstjin`/`sechstich`.
Danish accepts both the standard spellings (`elleve`, `halvtreds`,
`halvfjerds`) and the legacy variants kept for backward compatibility.

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

Aragonese pronounces the general forms of the current academic norm
(`cuatre`, `ueito`, `deciséis`, `vintiún`, `trenta y cinco`, `cient`) and
accepts the dialectal variants (`quatre`, `güeito`, `setse`, `vente`,
`noranta`) on extraction. Ordinals use the characteristic `-eno` series
(`cuatreno`, `cinqueno`, `onceno`). Tens ordinals above the attested range
follow the same productive `-eno` pattern.

## Spanish and Catalan

`es` and `ca` handle fused twenties (`veintiuno`, `vint-i-u`), the irregular
hundreds (`quinientos`, `setecientos`, `novecientos`), scale words including
`millón/millones` and `milió/milions`, and additive continuations such as
`dos mil veintitrés`.

## English

`extract_number` understands the `and` connector inside a number
(`one hundred and one` = 101), digit grouping (`1,000,000`) and spoken-style
comma pauses (`two thousand, twenty three`).

## Kabyle

Kabyle carries two numeral systems: the pan-Amazigh cardinals (`yiwen`,
`sin`, `kṛaḍ`, ... `mraw`) and the Algerian-Arabic borrowed numerals used
for everyday counting above ten (`ḥḍac` = 11, `ɛecrin` = 20, `mya` = 100,
`alef` = 1000). Pronunciation uses the Amazigh forms for 0-10 and the
Arabic-derived forms above ten, joining compounds with the conjunction `u`
with the unit before the ten (`waḥed u ɛecrin` = 21). Extraction accepts
both systems, feminine forms (`yiwet`, `snat`), additive Amazigh compounds
(`mraw d yiwen` = 11) and diacritic-stripped spellings (`hdac`).

Ordinals use `amezwaru` (f. `tamezwarut`) for "first" and `wis`/`tis` +
cardinal otherwise. The only attested fraction noun is `azgen` (half).

Coverage boundary: pronunciation spans 0–9999. The minus word, a
decimal-separator word, ordinal suffix forms, larger scale words and
further fraction nouns are not reliably attested and are deliberately
omitted.

## Persian

Numbers are written and parsed in Persian script (`بیست و یک` = 21). Both
extraction and pronunciation cover units through millions, including decimal
readings.

## Known gaps

These are cases where the generic parity fallback (see below) is in use and
its result is rougher than a dedicated implementation would be: the call still
returns, it is just less polished:

- `fr`, `it`, `eu`, `fa` and other languages marked `·` for `numbers_to_digits`
  in the README matrix rely on the generic span-replacement fallback.
- Polish extraction does not merge `tysiąc` groups written with the singular
  form (`jeden tysiąc jeden`). Plural forms (`dwa tysiące trzy`) work.
- Czech pronounces four-digit numbers date-style (`1234` →
  `dvanáct třicet čtyři`), which extraction does not reverse.

## Full function parity

Every supported language provides every public function. Where a language
has no hand-written implementation, a documented generic fallback fills in:

- `pronounce_fraction` reuses the language's `nice_number` fraction wording
  (which carries its plural/declension rules) and spells out any digits. The
  Slavic languages use feminine numerators (`dvě třetiny`, `две трети`) and
  Hungarian its `két` allomorph. Denominators outside the language's fraction
  vocabulary fall back to "cardinal numerator + ordinal denominator".
- `is_ordinal` falls back to a reverse lookup over `pronounce_ordinal`
  (1–100, round hundreds, 1000, 1000000), registering both `-o`/`-a`
  grammatical-gender variants.
- `numbers_to_digits` falls back to replacing maximal spoken-number spans
  found by `extract_number`, joining across connector words (`vingt et un`,
  `sto in ena`) only when the combined words read as one larger number.
  Languages whose hand-written converters stopped at twenty or mishandled
  compound and comma-grouped numbers (az, ca, cs, da, en, es, nl, pl) now
  use this path.

The parity guarantee is enforced by `tests/test_lang_parity.py`, which runs
every public function against every supported language.

---
[← API reference](api.md) · [Home](../README.md) · [Adding a language →](adding-a-language.md)
