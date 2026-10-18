# Changelog

## [0.24.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.24.0a2) (2026-10-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.24.0a1...0.24.0a2)

**Merged pull requests:**

- test\(ar\): natural-language Arabic and Saudi number cases [\#377](https://github.com/OpenVoiceOS/ovos-number-parser/pull/377) ([JarbasAl](https://github.com/JarbasAl))

## [0.24.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.24.0a1) (2026-10-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.23.2a1...0.24.0a1)

**Merged pull requests:**

- feat\(ar\): Saudi colloquial cardinals for lang="ars" and the spoken half نص [\#375](https://github.com/OpenVoiceOS/ovos-number-parser/pull/375) ([JarbasAl](https://github.com/JarbasAl))
- fix: a lone ordinal in numbers\_to\_digits is a word, not the fraction 1/n [\#372](https://github.com/OpenVoiceOS/ovos-number-parser/pull/372) ([goldyfruit](https://github.com/goldyfruit))

## [0.23.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.23.2a1) (2026-10-08)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.23.1a1...0.23.2a1)

**Merged pull requests:**

- fix: state the leftmost-ordinal fraction invariant per locale, skip the span scan for one word [\#370](https://github.com/OpenVoiceOS/ovos-number-parser/pull/370) ([openvoiceos-bot](https://github.com/openvoiceos-bot))

## [0.23.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.23.1a1) (2026-09-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.23.0a2...0.23.1a1)

**Merged pull requests:**

- fix\(nb,nn\): a bare cardinal under ordinals=True falls through instead of returning False [\#366](https://github.com/OpenVoiceOS/ovos-number-parser/pull/366) ([openvoiceos-bot](https://github.com/openvoiceos-bot))

## [0.23.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.23.0a2) (2026-09-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.23.0a1...0.23.0a2)

**Merged pull requests:**

- perf\(generic\): ask each token once, not once per walk [\#363](https://github.com/OpenVoiceOS/ovos-number-parser/pull/363) ([openvoiceos-bot](https://github.com/openvoiceos-bot))

## [0.23.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.23.0a1) (2026-09-25)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.17a1...0.23.0a1)

**Merged pull requests:**

- feat\(ordinals\): the leftmost number of a mixed line wins under ordinals=True [\#361](https://github.com/OpenVoiceOS/ovos-number-parser/pull/361) ([openvoiceos-bot](https://github.com/openvoiceos-bot))

## [0.22.17a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.17a1) (2026-09-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.16a2...0.22.17a1)

**Merged pull requests:**

- fix\(da, de\): ordinals=True keeps the cardinal reading [\#359](https://github.com/OpenVoiceOS/ovos-number-parser/pull/359) ([openvoiceos-bot](https://github.com/openvoiceos-bot))

## [0.22.16a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.16a2) (2026-09-23)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.16a1...0.22.16a2)

**Merged pull requests:**

- chore\(ci\): drop the broken Dependabot config [\#309](https://github.com/OpenVoiceOS/ovos-number-parser/pull/309) ([openvoiceos-bot](https://github.com/openvoiceos-bot))

## [0.22.16a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.16a1) (2026-09-22)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.15a1...0.22.16a1)

**Merged pull requests:**

- fix\(ar\): a construct unit after و still multiplies the next hundred [\#356](https://github.com/OpenVoiceOS/ovos-number-parser/pull/356) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.15a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.15a1) (2026-09-22)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.14a1...0.22.15a1)

**Merged pull requests:**

- fix\(ar\): a full-form unit after و closes a filled hundred [\#353](https://github.com/OpenVoiceOS/ovos-number-parser/pull/353) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.14a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.14a1) (2026-09-22)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.13a1...0.22.14a1)

**Merged pull requests:**

- fix\(ar\): read the teen spellings of the SADA transcripts [\#345](https://github.com/OpenVoiceOS/ovos-number-parser/pull/345) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.13a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.13a1) (2026-09-22)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.12a1...0.22.13a1)

**Closed issues:**

- Arabic: numbers\_to\_digits merges a repeated hundred across two numbers [\#351](https://github.com/OpenVoiceOS/ovos-number-parser/issues/351)

**Merged pull requests:**

- fix\(ar\): a unit two before a hundred builds two hundred again [\#350](https://github.com/OpenVoiceOS/ovos-number-parser/pull/350) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.12a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.12a1) (2026-09-22)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.11a1...0.22.12a1)

**Merged pull requests:**

- fix\(ar\): read ميه as the hundred مية, by the same context rules [\#346](https://github.com/OpenVoiceOS/ovos-number-parser/pull/346) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.11a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.11a1) (2026-09-22)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.10a1...0.22.11a1)

**Closed issues:**

- Arabic: hundreds composed on واحد and اثنين \(اتنين مية → 200\) [\#343](https://github.com/OpenVoiceOS/ovos-number-parser/issues/343)

**Merged pull requests:**

- fix\(ar\): only the units three to nine build a hundred [\#347](https://github.com/OpenVoiceOS/ovos-number-parser/pull/347) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.10a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.10a1) (2026-09-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.9a1...0.22.10a1)

**Merged pull requests:**

- fix\(ar\): a word that also means water, dead, Tuesday or lady is a number only in a number's context [\#335](https://github.com/OpenVoiceOS/ovos-number-parser/pull/335) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.9a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.9a1) (2026-09-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.8a1...0.22.9a1)

**Merged pull requests:**

- fix\(ar\): every attested teen spelling reads as its number [\#339](https://github.com/OpenVoiceOS/ovos-number-parser/pull/339) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.8a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.8a1) (2026-09-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.7a1...0.22.8a1)

**Closed issues:**

- Arabic numbers\_to\_digits drops the conjunction و before a number that does not continue the one before [\#336](https://github.com/OpenVoiceOS/ovos-number-parser/issues/336)

**Merged pull requests:**

- fix\(ar\): numbers\_to\_digits keeps the conjunction و before a new number [\#338](https://github.com/OpenVoiceOS/ovos-number-parser/pull/338) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.7a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.7a1) (2026-09-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.6a1...0.22.7a1)

**Merged pull requests:**

- fix\(ar\): every Arabic form stands on a source [\#334](https://github.com/OpenVoiceOS/ovos-number-parser/pull/334) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.6a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.6a1) (2026-09-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.5a1...0.22.6a1)

**Merged pull requests:**

- fix\(ar\): ماية is not a spelling of "hundred" [\#332](https://github.com/OpenVoiceOS/ovos-number-parser/pull/332) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.5a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.5a1) (2026-09-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.4a1...0.22.5a1)

**Merged pull requests:**

- fix\(ar\): او is "or"; transcript repair belongs to the caller [\#330](https://github.com/OpenVoiceOS/ovos-number-parser/pull/330) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.4a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.4a1) (2026-09-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.3a1...0.22.4a1)

**Merged pull requests:**

- fix\(ar\): او joins a hundreds word only to a count of thousands [\#328](https://github.com/OpenVoiceOS/ovos-number-parser/pull/328) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.3a1) (2026-09-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.2a1...0.22.3a1)

**Merged pull requests:**

- fix\(ar\): او joins a number only in the shape transcripts show [\#326](https://github.com/OpenVoiceOS/ovos-number-parser/pull/326) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.2a1) (2026-09-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.1a1...0.22.2a1)

**Merged pull requests:**

- fix\(ar\): read Gulf number joins [\#324](https://github.com/OpenVoiceOS/ovos-number-parser/pull/324) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.1a1) (2026-09-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.22.0a1...0.22.1a1)

**Closed issues:**

- Arabic: the hundreds spelling ماية is not recognised \(اربعماية الاف reads 1000\) [\#319](https://github.com/OpenVoiceOS/ovos-number-parser/issues/319)

**Merged pull requests:**

- fix\(ar\): accept the hundreds spelling ماية [\#321](https://github.com/OpenVoiceOS/ovos-number-parser/pull/321) ([JarbasAl](https://github.com/JarbasAl))

## [0.22.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.22.0a1) (2026-09-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.21.1a1...0.22.0a1)

**Closed issues:**

- Arabic: an unknown case or an unsupported gender returns the nominative masculine silently [\#318](https://github.com/OpenVoiceOS/ovos-number-parser/issues/318)

**Merged pull requests:**

- feat\(ar\): gender and case for Arabic cardinals and ordinals [\#320](https://github.com/OpenVoiceOS/ovos-number-parser/pull/320) ([JarbasAl](https://github.com/JarbasAl))

## [0.21.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.21.1a1) (2026-09-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.21.0a1...0.21.1a1)

**Merged pull requests:**

- fix\(ar\): decline twelve in the oblique case \(اثنا عشر -\> اثني عشر\) [\#316](https://github.com/OpenVoiceOS/ovos-number-parser/pull/316) ([JarbasAl](https://github.com/JarbasAl))

## [0.21.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.21.0a1) (2026-09-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.20.4a1...0.21.0a1)

**Merged pull requests:**

- feat\(ar\): cardinals in the words a lect uses, keyed by its ISO 639-3 code [\#311](https://github.com/OpenVoiceOS/ovos-number-parser/pull/311) ([JarbasAl](https://github.com/JarbasAl))

## [0.20.4a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.20.4a1) (2026-09-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.20.3a1...0.20.4a1)

**Merged pull requests:**

- fix\(de\): a spaced "und" between numerals separates numbers [\#304](https://github.com/OpenVoiceOS/ovos-number-parser/pull/304) ([JarbasAl](https://github.com/JarbasAl))

## [0.20.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.20.3a1) (2026-09-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.20.2a1...0.20.3a1)

**Merged pull requests:**

- fix\(oc\): native-speaker observations from \#302 [\#307](https://github.com/OpenVoiceOS/ovos-number-parser/pull/307) ([openvoiceos-bot](https://github.com/openvoiceos-bot))

## [0.20.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.20.2a1) (2026-09-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.20.1a1...0.20.2a1)

**Merged pull requests:**

- fix\(ar\): fused colloquial teens are read in the spellings transcribers use [\#310](https://github.com/OpenVoiceOS/ovos-number-parser/pull/310) ([JarbasAl](https://github.com/JarbasAl))

## [0.20.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.20.1a1) (2026-09-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.20.0a1...0.20.1a1)

**Merged pull requests:**

- fix\(mwl\): read the hundreds periphrastically [\#306](https://github.com/OpenVoiceOS/ovos-number-parser/pull/306) ([JarbasAl](https://github.com/JarbasAl))

## [0.20.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.20.0a1) (2026-09-06)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.13...0.20.0a1)

**Merged pull requests:**

- feat: extract\_number\_spans returns code-point spans for every parsed number [\#303](https://github.com/OpenVoiceOS/ovos-number-parser/pull/303) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.13](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.13) (2026-08-13)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.13a2...0.19.13)

## [0.19.13a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.13a2) (2026-08-13)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.13a1...0.19.13a2)

**Merged pull requests:**

- Improving kabyle parser [\#300](https://github.com/OpenVoiceOS/ovos-number-parser/pull/300) ([athmanemokraoui](https://github.com/athmanemokraoui))

## [0.19.13a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.13a1) (2026-08-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.12a1...0.19.13a1)

**Merged pull requests:**

- Release 0.19.13a1 [\#299](https://github.com/OpenVoiceOS/ovos-number-parser/pull/299) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix\(ar\): digit runs with an attached clitic \(و355\) join mixed number spans [\#297](https://github.com/OpenVoiceOS/ovos-number-parser/pull/297) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.12a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.12a1) (2026-08-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.11a1...0.19.12a1)

**Merged pull requests:**

- Release 0.19.12a1 [\#298](https://github.com/OpenVoiceOS/ovos-number-parser/pull/298) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: numbers\_to\_digits must not corrupt standalone digit runs \(leading zeros lost\) [\#296](https://github.com/OpenVoiceOS/ovos-number-parser/pull/296) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.11a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.11a1) (2026-08-11)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.10a1...0.19.11a1)

**Merged pull requests:**

- Release 0.19.11a1 [\#295](https://github.com/OpenVoiceOS/ovos-number-parser/pull/295) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix\(ar\): spaced unit+hundred parses additively \(خمس مية وثلاثين → 135 instead of 530\) [\#294](https://github.com/OpenVoiceOS/ovos-number-parser/pull/294) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.10a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.10a1) (2026-08-10)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.9a1...0.19.10a1)

**Merged pull requests:**

- Release 0.19.10a1 [\#293](https://github.com/OpenVoiceOS/ovos-number-parser/pull/293) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix\(en\): route numbers\_to\_digits to the English backend [\#286](https://github.com/OpenVoiceOS/ovos-number-parser/pull/286) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.9a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.9a1) (2026-08-10)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.8a2...0.19.9a1)

**Merged pull requests:**

- Release 0.19.9a1 [\#292](https://github.com/OpenVoiceOS/ovos-number-parser/pull/292) ([github-actions[bot]](https://github.com/apps/github-actions))
- feat\(ar\): register-aware pronunciation and Arabic dialect code resolution [\#291](https://github.com/OpenVoiceOS/ovos-number-parser/pull/291) ([JarbasAl](https://github.com/JarbasAl))
- fix\(ar\): extract accepts colloquial and dialectal number forms [\#290](https://github.com/OpenVoiceOS/ovos-number-parser/pull/290) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.8a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.8a2) (2026-07-31)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.8a1...0.19.8a2)

**Merged pull requests:**

- Release 0.19.8a2 [\#285](https://github.com/OpenVoiceOS/ovos-number-parser/pull/285) ([github-actions[bot]](https://github.com/apps/github-actions))
- docs: rewrite README in Simplified Technical English [\#284](https://github.com/OpenVoiceOS/ovos-number-parser/pull/284) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.8a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.8a1) (2026-07-22)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.7...0.19.8a1)

**Merged pull requests:**

- Release 0.19.8a1 [\#281](https://github.com/OpenVoiceOS/ovos-number-parser/pull/281) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: guard non-decimal Unicode digits in number word tokenization [\#280](https://github.com/OpenVoiceOS/ovos-number-parser/pull/280) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.7](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.7) (2026-07-21)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.7a3...0.19.7)

## [0.19.7a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.7a3) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.7a2...0.19.7a3)

**Merged pull requests:**

- fix: drop the plural -s on French quatre-vingt/cent before mille [\#278](https://github.com/OpenVoiceOS/ovos-number-parser/pull/278) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.7a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.7a2) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.7a1...0.19.7a2)

**Merged pull requests:**

- Release 0.19.7a2 [\#277](https://github.com/OpenVoiceOS/ovos-number-parser/pull/277) ([github-actions[bot]](https://github.com/apps/github-actions))
- refactor: route French pronunciation through the shared engine [\#276](https://github.com/OpenVoiceOS/ovos-number-parser/pull/276) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.7a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.7a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.6a2...0.19.7a1)

**Merged pull requests:**

- Release 0.19.7a1 [\#275](https://github.com/OpenVoiceOS/ovos-number-parser/pull/275) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: fuse Italian cardinals into one word below a million [\#274](https://github.com/OpenVoiceOS/ovos-number-parser/pull/274) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.6a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.6a2) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.6a1...0.19.6a2)

**Merged pull requests:**

- Release 0.19.6a2 [\#273](https://github.com/OpenVoiceOS/ovos-number-parser/pull/273) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: Hebrew abstract numbers default to the feminine counting form [\#272](https://github.com/OpenVoiceOS/ovos-number-parser/pull/272) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.6a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.6a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.5a1...0.19.6a1)

**Merged pull requests:**

- Release 0.19.6a1 [\#271](https://github.com/OpenVoiceOS/ovos-number-parser/pull/271) ([github-actions[bot]](https://github.com/apps/github-actions))
- fix: Persian teens 15-18 use standard forms, not Tehrani colloquial [\#270](https://github.com/OpenVoiceOS/ovos-number-parser/pull/270) ([JarbasAl](https://github.com/JarbasAl))

## [0.19.5a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.5a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.4a1...0.19.5a1)

**Merged pull requests:**

- Release 0.19.5a1 [\#269](https://github.com/OpenVoiceOS/ovos-number-parser/pull/269) ([github-actions[bot]](https://github.com/apps/github-actions))

## [0.19.4a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.4a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.3a3...0.19.4a1)

## [0.19.3a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.3a3) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.3a2...0.19.3a3)

## [0.19.3a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.3a2) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.3a1...0.19.3a2)

## [0.19.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.3a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.2a1...0.19.3a1)

## [0.19.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.2a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.1a1...0.19.2a1)

## [0.19.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.1a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.19.0a1...0.19.1a1)

## [0.19.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.19.0a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.20a1...0.19.0a1)

## [0.18.20a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.20a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.19a1...0.18.20a1)

## [0.18.19a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.19a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.18a1...0.18.19a1)

## [0.18.18a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.18a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.17a1...0.18.18a1)

## [0.18.17a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.17a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.16a1...0.18.17a1)

## [0.18.16a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.16a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.15a1...0.18.16a1)

## [0.18.15a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.15a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.14a1...0.18.15a1)

## [0.18.14a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.14a1) (2026-07-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.13a1...0.18.14a1)

## [0.18.13a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.13a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.12a1...0.18.13a1)

## [0.18.12a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.12a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.11a1...0.18.12a1)

## [0.18.11a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.11a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.10a1...0.18.11a1)

## [0.18.10a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.10a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a35...0.18.10a1)

## [0.18.9a35](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a35) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a34...0.18.9a35)

## [0.18.9a34](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a34) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a33...0.18.9a34)

## [0.18.9a33](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a33) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a32...0.18.9a33)

## [0.18.9a32](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a32) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a31...0.18.9a32)

## [0.18.9a31](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a31) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a30...0.18.9a31)

## [0.18.9a30](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a30) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a29...0.18.9a30)

## [0.18.9a29](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a29) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a27...0.18.9a29)

## [0.18.9a27](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a27) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a26...0.18.9a27)

## [0.18.9a26](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a26) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a21...0.18.9a26)

## [0.18.9a21](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a21) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a17...0.18.9a21)

## [0.18.9a17](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a17) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a18...0.18.9a17)

## [0.18.9a18](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a18) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a19...0.18.9a18)

## [0.18.9a19](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a19) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a20...0.18.9a19)

## [0.18.9a20](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a20) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a16...0.18.9a20)

## [0.18.9a16](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a16) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a22...0.18.9a16)

## [0.18.9a22](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a22) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a23...0.18.9a22)

## [0.18.9a23](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a23) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a24...0.18.9a23)

## [0.18.9a24](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a24) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a25...0.18.9a24)

## [0.18.9a25](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a25) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a15...0.18.9a25)

## [0.18.9a15](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a15) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a14...0.18.9a15)

## [0.18.9a14](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a14) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a28...0.18.9a14)

## [0.18.9a28](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a28) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a13...0.18.9a28)

## [0.18.9a13](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a13) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a12...0.18.9a13)

## [0.18.9a12](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a12) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a11...0.18.9a12)

## [0.18.9a11](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a11) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a10...0.18.9a11)

## [0.18.9a10](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a10) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a9...0.18.9a10)

## [0.18.9a9](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a9) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a8...0.18.9a9)

## [0.18.9a8](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a8) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a7...0.18.9a8)

## [0.18.9a7](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a7) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a6...0.18.9a7)

## [0.18.9a6](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a6) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.8a1...0.18.9a6)

## [0.18.8a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.8a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a4...0.18.8a1)

## [0.18.9a4](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a4) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a3...0.18.9a4)

## [0.18.9a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a3) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a2...0.18.9a3)

## [0.18.9a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a2) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a1...0.18.9a2)

## [0.18.9a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.9a5...0.18.9a1)

## [0.18.9a5](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.9a5) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.7a1...0.18.9a5)

## [0.18.7a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.7a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.6a1...0.18.7a1)

## [0.18.6a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.6a1) (2026-07-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.4a1...0.18.6a1)

## [0.18.4a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.4a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.5a1...0.18.4a1)

## [0.18.5a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.5a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.3a1...0.18.5a1)

## [0.18.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.3a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.2a2...0.18.3a1)

## [0.18.2a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.2a2) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.2a1...0.18.2a2)

## [0.18.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.2a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.1a2...0.18.2a1)

## [0.18.1a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.1a2) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.1a1...0.18.1a2)

## [0.18.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.1a1) (2026-07-17)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.18.0a1...0.18.1a1)

## [0.18.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.18.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.17.0a1...0.18.0a1)

## [0.17.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.17.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.16.0a2...0.17.0a1)

## [0.16.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.16.0a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.16.0a1...0.16.0a2)

## [0.16.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.16.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.15.0a1...0.16.0a1)

## [0.15.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.15.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.14.0a1...0.15.0a1)

## [0.14.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.14.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.13.0a2...0.14.0a1)

## [0.13.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.13.0a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.13.0a1...0.13.0a2)

## [0.13.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.13.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.12.0a1...0.13.0a1)

## [0.12.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.12.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.11.0a2...0.12.0a1)

## [0.11.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.11.0a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.11.0a1...0.11.0a2)

## [0.11.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.11.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.10.0a4...0.11.0a1)

## [0.10.0a4](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.10.0a4) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.10.0a3...0.10.0a4)

## [0.10.0a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.10.0a3) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.10.0a2...0.10.0a3)

## [0.10.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.10.0a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.10.0a1...0.10.0a2)

## [0.10.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.10.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.9.0a1...0.10.0a1)

## [0.9.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.9.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.8.0a1...0.9.0a1)

## [0.8.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.8.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.7.0a1...0.8.0a1)

## [0.7.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.7.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.6.3a1...0.7.0a1)

## [0.6.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.6.3a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.6.2a1...0.6.3a1)

## [0.6.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.6.2a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.6.1a3...0.6.2a1)

## [0.6.1a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.6.1a3) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.6.1a2...0.6.1a3)

## [0.6.1a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.6.1a2) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.6.1a1...0.6.1a2)

## [0.6.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.6.1a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.6.0a1...0.6.1a1)

## [0.6.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.6.0a1) (2026-07-16)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.3a1...0.6.0a1)

## [0.5.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.3a1) (2026-06-20)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.2a4...0.5.3a1)

## [0.5.2a4](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.2a4) (2025-12-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.2a3...0.5.2a4)

## [0.5.2a3](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.2a3) (2025-12-19)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.2a2...0.5.2a3)

## [0.5.2a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.2a2) (2025-12-18)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.2a1...0.5.2a2)

## [0.5.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.2a1) (2025-10-12)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.1...0.5.2a1)

## [0.5.1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.1) (2025-10-12)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.1a1...0.5.1)

## [0.5.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.1a1) (2025-10-12)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.5.0a1...0.5.1a1)

## [0.5.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.5.0a1) (2025-10-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.4.2...0.5.0a1)

## [0.4.2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.4.2) (2025-08-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.4.1...0.4.2)

## [0.4.1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.4.1) (2025-08-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.4.1a1...0.4.1)

## [0.4.1a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.4.1a1) (2025-08-04)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.4.0...0.4.1a1)

## [0.4.0](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.4.0) (2025-08-03)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.4.0a1...0.4.0)

## [0.4.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.4.0a1) (2025-08-03)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.3.3a1...0.4.0a1)

## [0.3.3a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.3.3a1) (2025-08-03)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.3.2...0.3.3a1)

## [0.3.2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.3.2) (2025-03-25)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.3.1...0.3.2)

## [0.3.1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.3.1) (2025-02-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.3.0...0.3.1)

## [0.3.0](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.3.0) (2025-02-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.2.0a1...0.3.0)

## [0.2.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.2.0a1) (2025-02-27)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.1.0...0.2.0a1)

## [0.1.0](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.1.0) (2025-02-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.1.0a2...0.1.0)

## [0.1.0a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.1.0a2) (2025-02-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.1.0a1...0.1.0a2)

## [0.1.0a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.1.0a1) (2025-02-26)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.0.2...0.1.0a1)

## [0.0.2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.0.2) (2024-11-13)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.0.2a1...0.0.2)

## [0.0.2a1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.0.2a1) (2024-11-13)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.0.1...0.0.2a1)

## [0.0.1](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.0.1) (2024-11-07)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/0.0.1a2...0.0.1)

## [0.0.1a2](https://github.com/OpenVoiceOS/ovos-number-parser/tree/0.0.1a2) (2024-11-07)

[Full Changelog](https://github.com/OpenVoiceOS/ovos-number-parser/compare/bc086aef8c1f18b03f6481e222a6c460f5b94962...0.0.1a2)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
