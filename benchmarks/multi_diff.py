"""Three-way differential: ours vs ICU RBNF vs num2words.

One reference implementation can be wrong or simply absent for a language.
Using two independent ones - ICU's RuleBasedNumberFormat and the num2words
library - turns the comparison into a vote:

* both references agree with us            -> almost certainly correct
* both agree with EACH OTHER but not us    -> strongest bug signal; investigate
* the two references disagree with each other -> the value is genuinely
  contested (dialect, scale, orthography); adjudicate against a grammar, never
  auto-trust either lib.

Nothing is pinned to a library. A disagreement is a lead, and the expected
value in any test still comes from a cited canonical source.
"""
import re
import sys

import icu
from num2words import num2words

from ovos_number_parser import pronounce_number

_JOIN = re.compile(r"[-_\s­]+")   # includes ICU's soft hyphen


def norm(text):
    text = re.sub(r"[,\.]", " ", text.lower())
    return " ".join(_JOIN.sub(" ", text).split())


def icu_fmt(lang):
    try:
        f = icu.RuleBasedNumberFormat(icu.URBNFRuleSetTag.SPELLOUT,
                                      icu.Locale(lang))
        actual = f.getLocale(icu.ULocDataLocaleType.ACTUAL_LOCALE).getName()
    except Exception:
        return None
    if actual.split("_")[0] != lang.split("_")[0]:
        return None
    return lambda n: f.format(n)


def n2w_fmt(lang):
    try:
        num2words(1, lang=lang)
    except Exception:
        return None
    return lambda n: num2words(n, lang=lang)


VALUES = list(range(0, 101)) + [
    101, 111, 121, 200, 500, 999, 1000, 1100, 1500, 2000, 2023, 5953,
    21000, 100000, 1000000]


def main(langs):
    for lang in langs:
        icu_f = icu_fmt(lang)
        n2w_f = n2w_fmt(lang)
        refs = [("icu", icu_f), ("n2w", n2w_f)]
        present = [name for name, f in refs if f]
        if not present:
            print(f"{lang}: no reference (ICU + num2words both absent)")
            continue

        both_vs_us = []      # both refs agree with each other, differ from us
        refs_disagree = 0
        for v in VALUES:
            try:
                ours = norm(pronounce_number(v, lang))
            except Exception as e:
                both_vs_us.append((v, f"<raise {type(e).__name__}>", "", ""))
                continue
            vals = {}
            for name, f in refs:
                if f:
                    try:
                        vals[name] = norm(f(v))
                    except Exception:
                        pass
            uniq = set(vals.values())
            if len(uniq) > 1:
                refs_disagree += 1
                continue
            if uniq and ours not in uniq:
                ref_str = next(iter(uniq))
                both_vs_us.append((v, ours, ref_str, "+".join(vals)))

        print(f"\n### {lang}  (refs: {'+'.join(present)}; "
              f"{len(both_vs_us)} vs-us, {refs_disagree} refs-split)")
        for v, ours, ref, who in both_vs_us[:16]:
            print(f"  {v}: ours={ours!r}  {who}={ref!r}")


if __name__ == "__main__":
    main(sys.argv[1:] or [
        "en", "pt", "es", "ca", "fr", "it", "de", "nl", "da", "sv", "no",
        "fi", "hu", "ru", "pl", "cs", "sk", "sl", "tr", "ar", "he", "uk",
        "ro", "id", "fa", "az", "bg"])
