"""Differential harness: ovos-number-parser pronounce_number vs ICU RBNF spellout.

ICU's RuleBasedNumberFormat is the reference implementation for spelling
numbers out, so it is the natural yardstick. It is *not* an oracle: where the
two disagree, either side may be wrong, and each disagreement has to be
adjudicated against the language's canonical source. Nothing here is pinned to
ICU output.

Two things are deliberately normalised away before comparing, because they are
orthography conventions rather than readings:

* hyphen / underscore / space between words -- we already treat these as
  interchangeable, and ICU's choice differs per locale;
* commas and full stops used as group separators in the spelled form.

Locales ICU has no rules for are detected and excluded rather than counted as
Those are detected and reported as "no ICU rules" rather than counted as
mismatches, so the scoreboard never claims coverage ICU does not have.
"""
import re
import sys
from collections import OrderedDict

import icu

from ovos_number_parser import pronounce_number

#: values worth comparing: every small integer (where most irregularity
#: lives), the teens/tens boundaries, hundred and thousand joins, and each
#: scale boundary
VALUES = (
    list(range(0, 101))
    + [101, 110, 111, 115, 120, 121, 130, 171, 180, 181, 190, 199,
       200, 201, 300, 500, 700, 900, 999,
       1000, 1001, 1100, 1500, 2000, 2500, 10000, 21000, 100000, 123456,
       1000000, 1000001, 2000000, 10 ** 9, 10 ** 12]
    + [-1, -21, -100, -1000]
)

_PUNCT = re.compile(r"[,\.]")
_JOIN = re.compile(r"[-_\s]+")


def norm(text):
    """Collapse orthography differences that are not reading differences."""
    text = _PUNCT.sub(" ", text.lower())
    return " ".join(_JOIN.sub(" ", text).split())


def icu_formatter(lang):
    """RBNF spellout formatter for a language, or None if ICU lacks rules.

    ICU resolves a locale it has no rules for by falling back to another one,
    and the substitute is not necessarily English -- ICU hands `gl`, `eu`,
    `oc`, `ast`, `kab` and others a Portuguese formatter. Comparing against
    that would score our Galician against Portuguese spellings and report
    nonsense, so the *actual* locale ICU resolved to is what decides whether
    a comparison is meaningful.
    """
    try:
        fmt = icu.RuleBasedNumberFormat(icu.URBNFRuleSetTag.SPELLOUT,
                                        icu.Locale(lang))
        actual = fmt.getLocale(icu.ULocDataLocaleType.ACTUAL_LOCALE).getName()
    except Exception:
        return None
    # "pt" may legitimately resolve to "pt_PT"; a different base language is a
    # fallback and makes the comparison meaningless
    if actual.split("_")[0] != lang.split("_")[0]:
        return None
    return fmt


def compare(lang):
    fmt = icu_formatter(lang)
    if fmt is None:
        return None
    agree, diffs, errors = 0, [], []
    for value in VALUES:
        try:
            ours = pronounce_number(value, lang)
        except Exception as exc:
            errors.append((value, f"{type(exc).__name__}: {exc}"))
            continue
        theirs = fmt.format(value)
        if norm(ours) == norm(theirs):
            agree += 1
        else:
            diffs.append((value, ours, theirs))
    return agree, diffs, errors


def main(langs):
    results = OrderedDict()
    skipped = []
    for lang in langs:
        out = compare(lang)
        if out is None:
            skipped.append(lang)
            continue
        results[lang] = out

    total = len(VALUES)
    print(f"{'lang':6} {'agree':>12}  {'diffs':>5} {'errors':>6}")
    print("-" * 40)
    for lang, (agree, diffs, errors) in sorted(
            results.items(), key=lambda kv: kv[1][0] / total):
        pct = 100.0 * agree / total
        print(f"{lang:6} {agree:5}/{total:<4} {pct:5.1f}% "
              f"{len(diffs):5} {len(errors):6}")
    if skipped:
        print(f"\nno ICU spellout rules ({len(skipped)}): {' '.join(skipped)}")

    print("\n" + "=" * 60)
    for lang, (agree, diffs, errors) in results.items():
        if not diffs and not errors:
            continue
        print(f"\n### {lang}  ({len(diffs)} diffs, {len(errors)} errors)")
        for value, exc in errors[:5]:
            print(f"  !! {value}: {exc}")
        for value, ours, theirs in diffs[:12]:
            print(f"  {value}:\n     ours: {ours}\n      icu: {theirs}")
        if len(diffs) > 12:
            print(f"  ... {len(diffs) - 12} more")


if __name__ == "__main__":
    main(sys.argv[1:] or [
        'an', 'ar', 'ast', 'az', 'bg', 'ca', 'cs', 'da', 'de', 'el', 'en',
        'es', 'et', 'eu', 'fa', 'fi', 'fr', 'fy', 'gl', 'he', 'hr', 'hu',
        'id', 'it', 'kab', 'ms', 'mwl', 'nb', 'nl', 'nn', 'no', 'oc', 'pl',
        'pt', 'ro', 'ru', 'sk', 'sl', 'sv', 'tr', 'uk'])
